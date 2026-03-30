"""
routers/quiz.py — Quiz / review question endpoints.

Returns lessons that are flagged or have low stars so the frontend
can surface targeted review questions.
"""

from fastapi import APIRouter
from db import get_db

router = APIRouter(tags=["quiz"])


@router.get("/{user_key}")
def get_quiz(user_key: str) -> dict:
    """
    Return up to 10 lesson IDs that need review (flagged or stars < 3).
    The actual question objects are constructed by the frontend from lesson JSON;
    the backend simply surfaces which lessons warrant review.
    """
    with get_db() as conn:
        flagged = conn.execute(
            """SELECT lesson_id FROM lesson_progress
               WHERE user_key = ? AND flagged = 1
               LIMIT 5""",
            (user_key,),
        ).fetchall()

        low_score = conn.execute(
            """SELECT lesson_id FROM lesson_progress
               WHERE user_key = ? AND stars < 3 AND completed = 1
               ORDER BY stars ASC
               LIMIT 5""",
            (user_key,),
        ).fetchall()

    # Deduplicate while preserving order: flagged first
    seen: set[str] = set()
    lesson_ids: list[str] = []
    for row in flagged + low_score:
        lid = row["lesson_id"]
        if lid not in seen:
            seen.add(lid)
            lesson_ids.append(lid)

    return {
        "questions":  [],        # populated by frontend from lesson JSONs
        "lesson_ids": lesson_ids,
        "total":      len(lesson_ids),
    }
