"""
routers/progress.py — All user progress endpoints.

Endpoints:
  GET  /progress/{user_key}                     → ProgressData
  POST /progress/{user_key}/lesson              → save lesson result
  POST /progress/{user_key}/flag                → flag / unflag a lesson
  GET  /progress/{user_key}/note                → fetch personal notes
  POST /progress/{user_key}/note                → save personal notes
  POST /progress/{user_key}/bookmark            → save bookmark
  GET  /progress/{user_key}/bookmark/{lesson_id}→ get bookmark for lesson
  POST /progress/{user_key}/confidence          → save self-confidence rating
  POST /progress/{user_key}/analogy             → save preferred analogy
  GET  /progress/{user_key}/week-review         → last-7-day activity data
"""

from fastapi import APIRouter, HTTPException
from db import get_db
from models import (
    SaveLessonRequest,
    FlagRequest,
    NoteRequest,
    BookmarkRequest,
    ConfidenceRequest,
    AnalogyRequest,
)
import json
import os
from datetime import datetime, date, timedelta

router = APIRouter(tags=["progress"])

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_user_meta(conn, user_key: str) -> None:
    """Insert a default user_meta row if one does not exist."""
    conn.execute(
        "INSERT OR IGNORE INTO user_meta (user_key) VALUES (?)",
        (user_key,),
    )


def _get_all_module_ids() -> list[str]:
    """Read module IDs from modules.json if it exists."""
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "curriculum_data")
    path = os.path.join(base, "modules.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            modules = json.load(f)
        return [m["id"] for m in modules if "id" in m]
    except (json.JSONDecodeError, OSError):
        return []


def _compute_module_status(lessons: list[dict], module_ids: list[str]) -> dict:
    """
    Return module_status dict.
    Module 'm01' (or the first module) is always unlocked.
    Each subsequent module unlocks when the previous module is ≥ 60 % complete.
    """
    # Group lesson rows by module prefix (e.g. 'm01_l01' → 'm01')
    module_lessons: dict[str, list[dict]] = {mid: [] for mid in module_ids}
    for lesson in lessons:
        lid = lesson["lesson_id"]
        prefix = lid.split("_")[0]
        if prefix in module_lessons:
            module_lessons[prefix].append(lesson)

    status: dict[str, dict] = {}
    prev_pct = 100.0  # first module always unlocked

    for i, mid in enumerate(module_ids):
        m_lessons = module_lessons.get(mid, [])
        total = len(m_lessons)
        completed = sum(1 for l in m_lessons if l.get("completed"))
        mastery_pct = round((completed / total * 100) if total > 0 else 0.0, 1)
        unlocked = (i == 0) or (prev_pct >= 60.0)
        status[mid] = {
            "unlocked":        unlocked,
            "completed_count": completed,
            "total_count":     total,
            "mastery_pct":     mastery_pct,
        }
        prev_pct = mastery_pct

    return status


# ---------------------------------------------------------------------------
# GET /progress/{user_key}
# ---------------------------------------------------------------------------

@router.get("/{user_key}")
def get_progress(user_key: str) -> dict:
    with get_db() as conn:
        _ensure_user_meta(conn, user_key)
        conn.commit()

        lesson_rows = conn.execute(
            """SELECT lesson_id, stars, completed, attempts, flagged, hints_used,
                      time_spent_minutes
               FROM lesson_progress WHERE user_key = ?""",
            (user_key,),
        ).fetchall()

        meta_row = conn.execute(
            "SELECT * FROM user_meta WHERE user_key = ?",
            (user_key,),
        ).fetchone()

        confidence_rows = conn.execute(
            "SELECT lesson_id, rating FROM confidence WHERE user_key = ?",
            (user_key,),
        ).fetchall()

    lessons = [
        {
            "lesson_id":          r["lesson_id"],
            "stars":              r["stars"],
            "completed":          bool(r["completed"]),
            "attempts":           r["attempts"],
            "flagged":            bool(r["flagged"]),
            "hints_used":         r["hints_used"],
            "time_spent_minutes": r["time_spent_minutes"],
        }
        for r in lesson_rows
    ]

    module_ids = _get_all_module_ids()
    module_status = _compute_module_status(lessons, module_ids)

    topic_confidence = {r["lesson_id"]: r["rating"] for r in confidence_rows}

    def _json_load(val: str | None, default):
        try:
            return json.loads(val) if val else default
        except (json.JSONDecodeError, TypeError):
            return default

    return {
        "lessons":           lessons,
        "module_status":     module_status,
        "streak":            meta_row["streak"] if meta_row else 0,
        "study_log":         _json_load(meta_row["study_log_json"] if meta_row else None, {}),
        "weak_topics":       _json_load(meta_row["weak_topics_json"] if meta_row else None, []),
        "mastered_concepts": _json_load(meta_row["mastered_concepts_json"] if meta_row else None, []),
        "topic_confidence":  topic_confidence,
        "study_plan":        _json_load(meta_row["study_plan_json"] if meta_row else None, {}),
    }


# ---------------------------------------------------------------------------
# POST /progress/{user_key}/lesson
# ---------------------------------------------------------------------------

@router.post("/{user_key}/lesson")
def save_lesson(user_key: str, req: SaveLessonRequest) -> dict:
    today = date.today().isoformat()
    now = datetime.utcnow().isoformat()

    with get_db() as conn:
        _ensure_user_meta(conn, user_key)

        # Upsert lesson_progress
        conn.execute(
            """INSERT INTO lesson_progress
                 (user_key, lesson_id, stars, completed, attempts, time_spent_minutes, hints_used, last_accessed)
               VALUES (?, ?, ?, ?, 1, ?, ?, ?)
               ON CONFLICT(user_key, lesson_id) DO UPDATE SET
                 stars              = MAX(stars, excluded.stars),
                 completed          = MAX(completed, excluded.completed),
                 attempts           = attempts + 1,
                 time_spent_minutes = time_spent_minutes + excluded.time_spent_minutes,
                 hints_used         = hints_used + excluded.hints_used,
                 last_accessed      = excluded.last_accessed""",
            (
                user_key,
                req.lesson_id,
                req.stars,
                1 if req.completed else 0,
                req.time_spent_minutes,
                req.hints_used,
                now,
            ),
        )

        # Update study_log and streak in user_meta
        meta = conn.execute(
            "SELECT study_log_json, last_studied_date, streak FROM user_meta WHERE user_key = ?",
            (user_key,),
        ).fetchone()

        study_log: dict = {}
        streak = 0
        last_date = None
        if meta:
            try:
                study_log = json.loads(meta["study_log_json"] or "{}")
            except json.JSONDecodeError:
                study_log = {}
            streak = meta["streak"] or 0
            last_date = meta["last_studied_date"]

        # Accumulate minutes studied today
        study_log[today] = round(study_log.get(today, 0) + req.time_spent_minutes, 2)

        # Update streak
        if last_date == today:
            pass  # already counted today
        elif last_date == (date.today() - timedelta(days=1)).isoformat():
            streak += 1
        else:
            streak = 1  # reset

        conn.execute(
            """UPDATE user_meta SET
                 study_log_json    = ?,
                 last_studied_date = ?,
                 streak            = ?
               WHERE user_key = ?""",
            (json.dumps(study_log), today, streak, user_key),
        )
        conn.commit()

    return {"ok": True, "streak": streak}


# ---------------------------------------------------------------------------
# POST /progress/{user_key}/flag
# ---------------------------------------------------------------------------

@router.post("/{user_key}/flag")
def flag_lesson(user_key: str, req: FlagRequest) -> dict:
    now = datetime.utcnow().isoformat()
    with get_db() as conn:
        conn.execute(
            """INSERT INTO lesson_progress (user_key, lesson_id, flagged, last_accessed)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(user_key, lesson_id) DO UPDATE SET
                 flagged       = excluded.flagged,
                 last_accessed = excluded.last_accessed""",
            (user_key, req.lesson_id, 1 if req.flagged else 0, now),
        )
        conn.commit()
    return {"ok": True, "flagged": req.flagged}


# ---------------------------------------------------------------------------
# GET /progress/{user_key}/note
# ---------------------------------------------------------------------------

@router.get("/{user_key}/note")
def get_note(user_key: str) -> dict:
    with get_db() as conn:
        row = conn.execute(
            "SELECT content, updated_at FROM notes WHERE user_key = ?",
            (user_key,),
        ).fetchone()
    if row:
        return {"content": row["content"], "updated_at": row["updated_at"]}
    return {"content": "", "updated_at": None}


# ---------------------------------------------------------------------------
# POST /progress/{user_key}/note
# ---------------------------------------------------------------------------

@router.post("/{user_key}/note")
def save_note(user_key: str, req: NoteRequest) -> dict:
    now = datetime.utcnow().isoformat()
    with get_db() as conn:
        conn.execute(
            """INSERT INTO notes (user_key, content, updated_at) VALUES (?, ?, ?)
               ON CONFLICT(user_key) DO UPDATE SET content = excluded.content, updated_at = excluded.updated_at""",
            (user_key, req.content, now),
        )
        conn.commit()
    return {"ok": True, "updated_at": now}


# ---------------------------------------------------------------------------
# POST /progress/{user_key}/bookmark
# ---------------------------------------------------------------------------

@router.post("/{user_key}/bookmark")
def save_bookmark(user_key: str, req: BookmarkRequest) -> dict:
    with get_db() as conn:
        conn.execute(
            """INSERT INTO bookmarks (user_key, lesson_id, step_index, sub_step, saved_code)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(user_key, lesson_id) DO UPDATE SET
                 step_index = excluded.step_index,
                 sub_step   = excluded.sub_step,
                 saved_code = excluded.saved_code""",
            (user_key, req.lesson_id, req.step_index, req.sub_step, req.saved_code),
        )
        conn.commit()
    return {"ok": True}


# ---------------------------------------------------------------------------
# GET /progress/{user_key}/bookmark/{lesson_id}
# ---------------------------------------------------------------------------

@router.get("/{user_key}/bookmark/{lesson_id}")
def get_bookmark(user_key: str, lesson_id: str) -> dict:
    with get_db() as conn:
        row = conn.execute(
            "SELECT step_index, sub_step, saved_code FROM bookmarks WHERE user_key = ? AND lesson_id = ?",
            (user_key, lesson_id),
        ).fetchone()
    if not row:
        return {"lesson_id": lesson_id, "step_index": 0, "sub_step": "", "saved_code": ""}
    return {
        "lesson_id":  lesson_id,
        "step_index": row["step_index"],
        "sub_step":   row["sub_step"],
        "saved_code": row["saved_code"],
    }


# ---------------------------------------------------------------------------
# POST /progress/{user_key}/confidence
# ---------------------------------------------------------------------------

@router.post("/{user_key}/confidence")
def save_confidence(user_key: str, req: ConfidenceRequest) -> dict:
    now = datetime.utcnow().isoformat()
    with get_db() as conn:
        conn.execute(
            """INSERT INTO confidence (user_key, lesson_id, rating, recorded_at)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(user_key, lesson_id) DO UPDATE SET
                 rating      = excluded.rating,
                 recorded_at = excluded.recorded_at""",
            (user_key, req.lesson_id, req.rating, now),
        )
        conn.commit()
    return {"ok": True}


# ---------------------------------------------------------------------------
# POST /progress/{user_key}/analogy
# ---------------------------------------------------------------------------

@router.post("/{user_key}/analogy")
def save_analogy(user_key: str, req: AnalogyRequest) -> dict:
    with get_db() as conn:
        _ensure_user_meta(conn, user_key)
        meta = conn.execute(
            "SELECT preferred_analogies_json FROM user_meta WHERE user_key = ?",
            (user_key,),
        ).fetchone()
        analogies: dict = {}
        if meta:
            try:
                analogies = json.loads(meta["preferred_analogies_json"] or "{}")
            except json.JSONDecodeError:
                analogies = {}
        analogies[req.lesson_id] = req.analogy
        conn.execute(
            "UPDATE user_meta SET preferred_analogies_json = ? WHERE user_key = ?",
            (json.dumps(analogies), user_key),
        )
        conn.commit()
    return {"ok": True}


# ---------------------------------------------------------------------------
# GET /progress/{user_key}/week-review
# ---------------------------------------------------------------------------

@router.get("/{user_key}/week-review")
def week_review(user_key: str) -> dict:
    cutoff = (date.today() - timedelta(days=6)).isoformat()  # last 7 days inclusive

    with get_db() as conn:
        rows = conn.execute(
            """SELECT lesson_id, stars, completed, time_spent_minutes, last_accessed
               FROM lesson_progress
               WHERE user_key = ? AND last_accessed >= ?""",
            (user_key, cutoff),
        ).fetchall()
        meta = conn.execute(
            "SELECT streak, study_log_json FROM user_meta WHERE user_key = ?",
            (user_key,),
        ).fetchone()

    lessons_this_week = [
        {
            "lesson_id":          r["lesson_id"],
            "stars":              r["stars"],
            "completed":          bool(r["completed"]),
            "time_spent_minutes": r["time_spent_minutes"],
            "last_accessed":      r["last_accessed"],
        }
        for r in rows
    ]
    total_time = round(sum(l["time_spent_minutes"] for l in lessons_this_week), 2)
    completed_count = sum(1 for l in lessons_this_week if l["completed"])

    study_log: dict = {}
    if meta:
        try:
            study_log = json.loads(meta["study_log_json"] or "{}")
        except json.JSONDecodeError:
            study_log = {}
    # Filter to last 7 days only
    week_study_log = {k: v for k, v in study_log.items() if k >= cutoff}

    return {
        "lessons_this_week": lessons_this_week,
        "total_time_minutes": total_time,
        "completed_count":   completed_count,
        "streak":            meta["streak"] if meta else 0,
        "study_log":         week_study_log,
    }
