import random
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import get_db, UserProgress
from curriculum_data import ALL_MODULES

router = APIRouter(prefix="/quiz", tags=["quiz"])

def get_lesson_by_id(lesson_id: str) -> dict | None:
    for module in ALL_MODULES:
        for lesson in module["lessons"]:
            if lesson["id"] == lesson_id:
                return {**lesson, "module_title": module["title"]}
    return None


@router.get("/{user_key}")
def get_daily_quiz(user_key: str, db: Session = Depends(get_db)):
    """
    Return 5 review questions focused on:
    1. Flagged lessons
    2. Lessons with < 3 stars
    """
    progress = db.query(UserProgress).filter(UserProgress.user_key == user_key).all()

    # Priority pool: flagged first, then low-starred
    flagged = [p.lesson_id for p in progress if p.flagged]
    low_star = [p.lesson_id for p in progress if p.stars < 3 and not p.flagged]

    pool = flagged + low_star

    if not pool:
        return {"questions": [], "message": "No flagged or low-scored lessons yet. Complete some lessons first!"}

    # Pick up to 5, cycling through pool
    selected = []
    while len(selected) < 5:
        if not pool:
            break
        selected.append(pool[len(selected) % len(pool)])

    # Get built-in questions from selected lessons
    quiz_questions = []
    for lesson_id in selected[:5]:
        lesson = get_lesson_by_id(lesson_id)
        if lesson and lesson.get("questions"):
            q = random.choice(lesson["questions"])
            quiz_questions.append({**q, "lesson_id": lesson_id, "lesson_title": lesson["title"]})

    return {"questions": quiz_questions, "lesson_ids": selected[:5]}


class GenerateQuizRequest(BaseModel):
    user_key: str
    lesson_ids: list[str]


def _fallback_question(lesson: dict, lesson_id: str) -> dict | None:
    """Return a built-in question for deterministic quiz generation."""
    lesson_questions = lesson.get("questions") or []
    if not lesson_questions:
        return None
    q = random.choice(lesson_questions)
    return {**q, "lesson_id": lesson_id, "lesson_title": lesson["title"]}


@router.post("/generate")
def generate_quiz(req: GenerateQuizRequest):
    """Return fresh built-in quiz questions for given lesson IDs."""
    questions = []
    for lesson_id in req.lesson_ids[:5]:
        lesson = get_lesson_by_id(lesson_id)
        if not lesson:
            continue
        fallback = _fallback_question(lesson, lesson_id)
        if fallback:
            questions.append(fallback)

    return {"questions": questions}
