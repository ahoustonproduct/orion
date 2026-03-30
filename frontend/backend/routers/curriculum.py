"""
routers/curriculum.py — Curriculum data endpoints.

Serves modules and lessons from JSON files located at:
  <repo-root>/curriculum_data/modules.json
  <repo-root>/curriculum_data/lessons/<module_id>_<lesson_id>.json
  <repo-root>/curriculum_data/glossary.json
"""

from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter(tags=["curriculum"])

# Path to the curriculum_data directory (one level up from this file's parent)
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "curriculum_data")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_modules() -> list:
    path = os.path.join(BASE, "modules.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _load_lesson_file(fpath: str) -> dict:
    with open(fpath, encoding="utf-8") as f:
        return json.load(f)


def _lesson_summary(lesson: dict) -> dict:
    """Return a lightweight summary dict for module lesson lists."""
    return {
        "id":             lesson.get("id"),
        "title":          lesson.get("title"),
        "order":          lesson.get("order", 0),
        "duration_min":   lesson.get("duration_min", 20),
        "difficulty":     lesson.get("difficulty", "intermediate"),
        "concept_tags":   lesson.get("concept_tags", []),
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/modules")
def get_modules() -> list:
    """Return the full list of module objects (without expanded lesson bodies)."""
    return _load_modules()


@router.get("/modules/{module_id}")
def get_module(module_id: str) -> dict:
    """Return a single module with its lesson summaries attached."""
    modules = _load_modules()
    if not modules:
        raise HTTPException(status_code=404, detail="modules.json not found")

    match = next((m for m in modules if m["id"] == module_id), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Module '{module_id}' not found")

    # Attach lesson summaries
    lessons_dir = os.path.join(BASE, "lessons")
    lessons: list[dict] = []
    if os.path.exists(lessons_dir):
        for fname in sorted(os.listdir(lessons_dir)):
            if fname.startswith(module_id + "_") and fname.endswith(".json"):
                fpath = os.path.join(lessons_dir, fname)
                try:
                    lesson = _load_lesson_file(fpath)
                    lessons.append(_lesson_summary(lesson))
                except (json.JSONDecodeError, OSError):
                    pass  # Skip malformed files silently

    lessons.sort(key=lambda l: l["order"])
    match = dict(match)  # avoid mutating the source list
    match["lessons"] = lessons
    return match


@router.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: str) -> dict:
    """Return the full lesson JSON by lesson ID (e.g. 'm01_l01')."""
    lessons_dir = os.path.join(BASE, "lessons")
    if not os.path.exists(lessons_dir):
        raise HTTPException(status_code=404, detail="Lessons directory not found")

    for fname in os.listdir(lessons_dir):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(lessons_dir, fname)
        try:
            lesson = _load_lesson_file(fpath)
        except (json.JSONDecodeError, OSError):
            continue
        if lesson.get("id") == lesson_id:
            return lesson

    raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")


@router.get("/glossary")
def get_glossary() -> list:
    """Return the glossary term list."""
    path = os.path.join(BASE, "glossary.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)
