"""
Notebook routes — NotebookLM-style feature.

A user pastes a YouTube URL; Orion pulls the transcript, asks the local
`orion-tutor` Ollama model to produce a module + lessons in the same JSON
shape as the built-in curriculum, and stores it so it can be rendered with
the existing /curriculum and /learn UI.
"""
import json
import os
import re
import uuid
import threading
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from openai import OpenAI

from models import get_db, Notebook, SessionLocal


router = APIRouter(prefix="/notebooks", tags=["notebooks"])


# ── Ollama client (mirrors routes/ai.py so we stay on `orion-tutor`) ──
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
MODEL = os.environ.get("OLLAMA_MODEL", "orion-tutor")
_client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


# ─────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────
YOUTUBE_ID_RE = re.compile(
    r"(?:youtube\.com/(?:watch\?v=|embed/|v/|shorts/)|youtu\.be/)([A-Za-z0-9_-]{11})"
)


def extract_video_id(url: str) -> Optional[str]:
    """Pull the 11-char YouTube ID out of any common URL form."""
    if not url:
        return None
    url = url.strip()
    m = YOUTUBE_ID_RE.search(url)
    if m:
        return m.group(1)
    # raw ID
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url
    return None


def _entries_to_text(entries) -> str:
    """Flatten either list-of-dicts (legacy) or FetchedTranscript (v1.x) to text."""
    out = []
    # v1.x FetchedTranscript is iterable yielding FetchedTranscriptSnippet
    # with a `.text` attribute. Legacy returns list of {"text": ..., "start": ...}.
    iterable = entries
    # v1.x also exposes a `.snippets` attribute
    snippets = getattr(entries, "snippets", None)
    if snippets is not None:
        iterable = snippets
    for e in iterable:
        text = None
        if isinstance(e, dict):
            text = e.get("text")
        else:
            text = getattr(e, "text", None)
        if text:
            out.append(text.strip())
    return " ".join(out)


def fetch_transcript(video_id: str) -> str:
    """Fetch plain-text transcript from a YouTube video.

    Supports both youtube-transcript-api v1.x (instance methods) and the
    pre-1.0 classmethod API. Raises RuntimeError with a human-readable
    message if no transcript is available.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            "youtube-transcript-api is not installed on the server. "
            "Run: pip install youtube-transcript-api"
        ) from e

    langs = ["en", "en-US", "en-GB"]
    entries = None
    errors = []

    # Try v1.x instance API first
    try:
        api = YouTubeTranscriptApi()
        if hasattr(api, "fetch"):
            try:
                entries = api.fetch(video_id, languages=langs)
            except Exception as e:
                errors.append(f"v1.fetch(en): {e}")
                # Fall back to any available language
                try:
                    listing = api.list(video_id)
                    # Prefer a manually-created English transcript, then any English,
                    # then translate to English from anything available.
                    chosen = None
                    try:
                        chosen = listing.find_manually_created_transcript(langs)
                    except Exception:
                        pass
                    if chosen is None:
                        try:
                            chosen = listing.find_transcript(langs)
                        except Exception:
                            pass
                    if chosen is None:
                        for t in listing:
                            chosen = t
                            break
                    if chosen is None:
                        raise RuntimeError("No transcript available for this video.")
                    entries = chosen.fetch()
                except Exception as e2:
                    errors.append(f"v1.list: {e2}")
    except Exception as e:
        errors.append(f"v1.init: {e}")

    # Legacy classmethod API fallback (<1.0)
    if entries is None:
        try:
            entries = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)  # type: ignore[attr-defined]
        except AttributeError:
            pass  # new version, already tried
        except Exception as e:
            errors.append(f"legacy.get_transcript: {e}")
            try:
                listing = YouTubeTranscriptApi.list_transcripts(video_id)  # type: ignore[attr-defined]
                chosen = None
                for t in listing:
                    chosen = t
                    break
                if chosen is None:
                    raise RuntimeError("No transcript available for this video.")
                entries = chosen.fetch()
            except AttributeError:
                pass
            except Exception as e2:
                errors.append(f"legacy.list_transcripts: {e2}")

    if entries is None:
        raise RuntimeError(
            "Could not fetch transcript for this video. "
            + ("Details: " + " | ".join(errors) if errors else "")
        )

    text = _entries_to_text(entries)
    if not text.strip():
        raise RuntimeError("Transcript fetched but empty.")
    return text


def _try_parse_json(text: str) -> Optional[dict]:
    """Try very hard to pull a JSON object out of model output."""
    if not text:
        return None
    text = text.strip()
    # Strip markdown fencing
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        if text.endswith("```"):
            text = text[:-3].strip()
    # Direct parse
    try:
        return json.loads(text)
    except Exception:
        pass
    # Greedy object match
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return None
    return None


def build_generation_prompt(title_hint: str, transcript: str) -> str:
    """Craft the prompt that asks orion-tutor to turn a transcript into
    a module + lessons JSON matching the existing curriculum schema.
    """
    # Keep the prompt size sane — transcripts can be huge
    max_chars = 12000
    snippet = transcript[:max_chars]
    if len(transcript) > max_chars:
        snippet += "\n[... transcript truncated for length ...]"

    return f"""<role>
You are Orion, an expert AI tutor for a Masters of Business Analytics student (WashU,
Financial Technical Analysis). You turn raw learning material into structured,
beginner-friendly lessons that match the student's existing curriculum format.
</role>

<task>
Given the transcript of a YouTube video below, generate a **complete module JSON**
with 3–5 lessons covering the key concepts. Output MUST be valid JSON — nothing
else. No prose, no markdown fencing, just the JSON object.
</task>

<schema>
{{
  "id": "notebook_<slug>",
  "title": "<short, specific module title>",
  "description": "<2-3 sentences describing what the student will learn and why it matters for business analytics>",
  "course": "My Notebook",
  "order": 99,
  "locked": false,
  "lessons": [
    {{
      "id": "<module_id>-l1",
      "title": "<lesson title>",
      "order": 1,
      "duration_min": 20,
      "real_world_context": "<how this concept applies in business/finance analytics>",
      "concept": "<markdown-formatted explanation with code blocks using triple backticks + python where appropriate. At least 4-6 paragraphs. Use **bold**, bullet points, and concrete examples.>",
      "worked_example": {{
        "description": "<what this example demonstrates>",
        "code": "<a short python/sql/etc snippet demonstrating the concept>",
        "explanation": "<step-by-step walkthrough of what each line does>"
      }},
      "reference": {{
        "key_syntax": ["<snippet1>", "<snippet2>"],
        "notes": "<short reminders / gotchas>"
      }},
      "questions": [
        {{"type": "true_false", "question": "<statement>", "answer": true, "explanation": "<why>"}},
        {{"type": "multiple_choice", "question": "<q>", "options": ["a","b","c","d"], "answer": 1, "explanation": "<why>"}},
        {{"type": "fill_blank", "question": "<prompt>", "template": "<code with ___ for blank>", "answer": "<expected answer>", "explanation": "<why>"}}
      ],
      "challenge": {{
        "instructions": "<what the student should code>",
        "starter_code": "# Write your code below\\n",
        "tests": [{{"type": "output_contains", "value": "<expected output substring>"}}],
        "solution": "<full working solution>"
      }}
    }}
    // ... 2-4 more lessons
  ]
}}
</schema>

<rules>
- Every lesson MUST include: id, title, order, duration_min, real_world_context, concept, worked_example, reference, questions (3+), challenge.
- Lesson IDs follow pattern "<module_id>-l1", "<module_id>-l2", etc.
- multiple_choice `answer` is the index (0-based) of the correct option.
- true_false `answer` is a JSON boolean (true/false, lowercase).
- fill_blank MUST include a `template` field with `___` where the blank goes.
- Keep code examples relevant to business analytics / finance when possible.
- Concept text is markdown with literal newlines inside the string (use \\n).
- OUTPUT VALID JSON ONLY. No commentary before or after.
</rules>

<suggested_title>
{title_hint or '(infer from transcript)'}
</suggested_title>

<transcript>
{snippet}
</transcript>

Now output the module JSON:"""


def call_ollama_generate(prompt: str) -> str:
    """Blocking (non-streaming) call — we need the full JSON text."""
    resp = _client.chat.completions.create(
        model=MODEL,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        stream=False,
    )
    return resp.choices[0].message.content or ""


def normalize_module_data(data: dict, notebook_id: str) -> dict:
    """Force the generated JSON into the shape the frontend expects."""
    data.setdefault("id", notebook_id)
    data["id"] = notebook_id  # keep consistent with the DB row id
    data.setdefault("title", "Untitled Notebook")
    data.setdefault("description", "")
    data.setdefault("course", "My Notebook")
    data.setdefault("order", 99)
    data.setdefault("locked", False)
    data.setdefault("supplementary_courses", [])

    lessons = data.get("lessons", []) or []
    cleaned_lessons = []
    for idx, lesson in enumerate(lessons, 1):
        lid = lesson.get("id") or f"{notebook_id}-l{idx}"
        lesson["id"] = lid
        lesson.setdefault("order", idx)
        lesson.setdefault("duration_min", 20)
        lesson.setdefault("real_world_context", "")
        lesson.setdefault("concept", "")
        lesson.setdefault("worked_example", {
            "description": "", "code": "", "explanation": ""
        })
        lesson.setdefault("reference", {"key_syntax": [], "notes": ""})
        lesson.setdefault("questions", [])
        lesson.setdefault("challenge", {
            "instructions": "",
            "starter_code": "# Write your code below\n",
            "tests": [],
            "solution": "",
        })
        cleaned_lessons.append(lesson)
    data["lessons"] = cleaned_lessons
    return data


# ─────────────────────────────────────────────────────────────────
# Background worker
# ─────────────────────────────────────────────────────────────────
def _generate_notebook_background(notebook_id: str, source_url: str, title_hint: str):
    """Runs in a background thread: fetch transcript, call Ollama, save."""
    db = SessionLocal()
    try:
        nb = db.query(Notebook).filter(Notebook.id == notebook_id).first()
        if not nb:
            return
        nb.status = "generating"
        nb.updated_at = datetime.utcnow()
        db.commit()

        # 1. Transcript
        video_id = extract_video_id(source_url)
        if not video_id:
            raise RuntimeError("Could not extract a YouTube video ID from that URL.")
        transcript = fetch_transcript(video_id)
        if not transcript or len(transcript) < 50:
            raise RuntimeError("Transcript too short or empty.")

        # 2. Generate
        prompt = build_generation_prompt(title_hint, transcript)
        raw = call_ollama_generate(prompt)
        parsed = _try_parse_json(raw)
        if not parsed:
            # Save the raw output for debugging
            nb.status = "failed"
            nb.error = f"Could not parse model output as JSON. First 500 chars:\n{raw[:500]}"
            nb.updated_at = datetime.utcnow()
            db.commit()
            return

        # 3. Pick the best available title BEFORE normalization, because
        # normalize_module_data injects "Untitled Notebook" as a default which
        # would otherwise trump a user-supplied title. Also: never let the
        # "Generating…" placeholder leak through as the final title.
        generated_title = (parsed.get("title") or "").strip()
        user_title = (title_hint or "").strip()
        current_title = (nb.title or "").strip()
        PLACEHOLDER = "Generating…"

        if generated_title:
            final_title = generated_title
        elif user_title:
            final_title = user_title
        elif current_title and current_title != PLACEHOLDER:
            final_title = current_title
        else:
            final_title = "Untitled Notebook"

        parsed = normalize_module_data(parsed, notebook_id)
        # Force the chosen title into both the DB row and the embedded JSON so
        # list view and detail view always agree.
        parsed["title"] = final_title
        nb.title = final_title

        nb.module_data = parsed
        nb.status = "ready"
        nb.error = ""
        nb.updated_at = datetime.utcnow()
        db.commit()

    except Exception as e:
        try:
            nb = db.query(Notebook).filter(Notebook.id == notebook_id).first()
            if nb:
                nb.status = "failed"
                nb.error = str(e)[:2000]
                nb.updated_at = datetime.utcnow()
                db.commit()
        except Exception:
            pass
    finally:
        db.close()


# ─────────────────────────────────────────────────────────────────
# Request models
# ─────────────────────────────────────────────────────────────────
class GenerateRequest(BaseModel):
    user_key: str
    source_url: str
    title: Optional[str] = ""


# ─────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────
@router.post("/generate")
def generate_notebook(req: GenerateRequest, db: Session = Depends(get_db)):
    """Kick off an async notebook generation. Returns immediately with a row id."""
    if not req.source_url.strip():
        raise HTTPException(status_code=400, detail="source_url is required")

    video_id = extract_video_id(req.source_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Not a valid YouTube URL or video ID.")

    notebook_id = f"notebook_{uuid.uuid4().hex[:12]}"
    nb = Notebook(
        id=notebook_id,
        user_key=req.user_key,
        title=(req.title or "Generating…").strip(),
        source_type="youtube",
        source_url=req.source_url.strip(),
        status="pending",
        error="",
        module_data={},
    )
    db.add(nb)
    db.commit()

    # Fire-and-forget background thread
    t = threading.Thread(
        target=_generate_notebook_background,
        args=(notebook_id, req.source_url.strip(), req.title or ""),
        daemon=True,
    )
    t.start()

    return {"id": notebook_id, "status": "pending"}


@router.get("/{user_key}")
def list_notebooks(user_key: str, db: Session = Depends(get_db)):
    """List all notebooks for a user (summary only, no module_data)."""
    rows = (
        db.query(Notebook)
        .filter(Notebook.user_key == user_key)
        .order_by(Notebook.created_at.desc())
        .all()
    )
    return [
        {
            "id": r.id,
            "title": r.title,
            "status": r.status,
            "error": r.error or "",
            "source_type": r.source_type,
            "source_url": r.source_url,
            "lesson_count": len((r.module_data or {}).get("lessons", [])) if r.module_data else 0,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }
        for r in rows
    ]


@router.get("/{user_key}/{notebook_id}")
def get_notebook(user_key: str, notebook_id: str, db: Session = Depends(get_db)):
    """Return the full notebook (module_data included) for rendering."""
    nb = (
        db.query(Notebook)
        .filter(Notebook.id == notebook_id, Notebook.user_key == user_key)
        .first()
    )
    if not nb:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return {
        "id": nb.id,
        "title": nb.title,
        "status": nb.status,
        "error": nb.error or "",
        "source_type": nb.source_type,
        "source_url": nb.source_url,
        "module_data": nb.module_data or {},
        "created_at": nb.created_at.isoformat() if nb.created_at else None,
        "updated_at": nb.updated_at.isoformat() if nb.updated_at else None,
    }


@router.get("/{user_key}/{notebook_id}/lesson/{lesson_id}")
def get_notebook_lesson(user_key: str, notebook_id: str, lesson_id: str, db: Session = Depends(get_db)):
    """Return a single lesson from within a notebook, shaped like /curriculum/lessons/{id}."""
    nb = (
        db.query(Notebook)
        .filter(Notebook.id == notebook_id, Notebook.user_key == user_key)
        .first()
    )
    if not nb or not nb.module_data:
        raise HTTPException(status_code=404, detail="Notebook not found")
    for lesson in (nb.module_data.get("lessons") or []):
        if lesson.get("id") == lesson_id:
            return {**lesson, "module_title": nb.module_data.get("title", nb.title)}
    raise HTTPException(status_code=404, detail="Lesson not found in notebook")


@router.delete("/{user_key}/{notebook_id}")
def delete_notebook(user_key: str, notebook_id: str, db: Session = Depends(get_db)):
    nb = (
        db.query(Notebook)
        .filter(Notebook.id == notebook_id, Notebook.user_key == user_key)
        .first()
    )
    if not nb:
        raise HTTPException(status_code=404, detail="Notebook not found")
    db.delete(nb)
    db.commit()
    return {"ok": True}


@router.post("/{user_key}/{notebook_id}/retry")
def retry_notebook(user_key: str, notebook_id: str, db: Session = Depends(get_db)):
    """Re-run generation on a failed notebook."""
    nb = (
        db.query(Notebook)
        .filter(Notebook.id == notebook_id, Notebook.user_key == user_key)
        .first()
    )
    if not nb:
        raise HTTPException(status_code=404, detail="Notebook not found")
    nb.status = "pending"
    nb.error = ""
    nb.updated_at = datetime.utcnow()
    db.commit()

    t = threading.Thread(
        target=_generate_notebook_background,
        args=(notebook_id, nb.source_url, nb.title or ""),
        daemon=True,
    )
    t.start()
    return {"id": notebook_id, "status": "pending"}
