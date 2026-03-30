"""
routers/spaced_repetition.py — Spaced-repetition review queue.

Uses a simplified SM-2-style algorithm with fixed intervals: [1, 3, 7, 14] days.
- Correct answer → advance to next interval (graduate when past 14 days)
- Wrong answer   → reset to 1-day interval, increment wrong_count

Endpoints:
  GET  /review/{user_key}/queue  → questions due today
  POST /review/{user_key}/record → record answer and update interval
  POST /review/{user_key}/add    → add a question to the queue
"""

from fastapi import APIRouter
from db import get_db
from models import RecordReviewRequest, AddToReviewRequest
import json
from datetime import date, timedelta

router = APIRouter(tags=["spaced_repetition"])

INTERVALS: list[int] = [1, 3, 7, 14]


# ---------------------------------------------------------------------------
# GET /review/{user_key}/queue
# ---------------------------------------------------------------------------

@router.get("/{user_key}/queue")
def get_review_queue(user_key: str) -> dict:
    """Return all questions due today (next_review_date ≤ today), max 20."""
    today = date.today().isoformat()

    with get_db() as conn:
        due = conn.execute(
            """SELECT id, question_id, lesson_id, question_json, wrong_count,
                      next_review_date, interval_days
               FROM review_queue
               WHERE user_key = ? AND next_review_date <= ?
               ORDER BY next_review_date
               LIMIT 20""",
            (user_key, today),
        ).fetchall()

        total_due = conn.execute(
            """SELECT COUNT(*) AS c FROM review_queue
               WHERE user_key = ? AND next_review_date <= ?""",
            (user_key, today),
        ).fetchone()["c"]

    questions = []
    for row in due:
        try:
            question_data = json.loads(row["question_json"])
        except (json.JSONDecodeError, TypeError):
            question_data = {}
        questions.append({
            "id":          row["id"],
            "question_id": row["question_id"],
            "lesson_id":   row["lesson_id"],
            "wrong_count": row["wrong_count"],
            "question":    question_data,
        })

    return {"questions": questions, "total_due": total_due}


# ---------------------------------------------------------------------------
# POST /review/{user_key}/record
# ---------------------------------------------------------------------------

@router.post("/{user_key}/record")
def record_review(user_key: str, req: RecordReviewRequest) -> dict:
    """
    Record a review attempt and advance (or reset) the interval.

    Correct → move to the next interval bracket; graduate (delete) if past 14 days.
    Wrong   → reset to 1-day interval, increment wrong_count.
    """
    today = date.today()

    with get_db() as conn:
        row = conn.execute(
            """SELECT interval_days FROM review_queue
               WHERE user_key = ? AND question_id = ?""",
            (user_key, req.question_id),
        ).fetchone()

        if not row:
            return {"ok": True, "note": "question not found in queue"}

        current_interval = row["interval_days"]

        if req.correct:
            try:
                idx = INTERVALS.index(current_interval)
            except ValueError:
                idx = 0  # treat unknown interval as the first bucket

            next_idx = idx + 1
            if next_idx >= len(INTERVALS):
                # Graduated — remove from queue
                conn.execute(
                    "DELETE FROM review_queue WHERE user_key = ? AND question_id = ?",
                    (user_key, req.question_id),
                )
            else:
                next_interval = INTERVALS[next_idx]
                next_date = (today + timedelta(days=next_interval)).isoformat()
                conn.execute(
                    """UPDATE review_queue
                       SET interval_days = ?, next_review_date = ?
                       WHERE user_key = ? AND question_id = ?""",
                    (next_interval, next_date, user_key, req.question_id),
                )
        else:
            # Wrong: reset to 1-day
            next_date = (today + timedelta(days=1)).isoformat()
            conn.execute(
                """UPDATE review_queue
                   SET interval_days = 1, next_review_date = ?, wrong_count = wrong_count + 1
                   WHERE user_key = ? AND question_id = ?""",
                (next_date, user_key, req.question_id),
            )

        conn.commit()

    return {"ok": True}


# ---------------------------------------------------------------------------
# POST /review/{user_key}/add
# ---------------------------------------------------------------------------

@router.post("/{user_key}/add")
def add_to_review(user_key: str, req: AddToReviewRequest) -> dict:
    """
    Add a question to the spaced-repetition queue.

    If the question already exists, increment wrong_count and reset the
    interval to 1 day so it resurfaces tomorrow.
    """
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    with get_db() as conn:
        conn.execute(
            """INSERT INTO review_queue
                 (user_key, question_id, lesson_id, question_json, wrong_count, next_review_date, interval_days)
               VALUES (?, ?, ?, ?, 1, ?, 1)
               ON CONFLICT(user_key, question_id) DO UPDATE SET
                 wrong_count      = wrong_count + 1,
                 next_review_date = ?,
                 interval_days    = 1""",
            (
                user_key,
                req.question_id,
                req.lesson_id,
                req.question_json,
                tomorrow,
                tomorrow,          # for the ON CONFLICT SET clause
            ),
        )
        conn.commit()

    return {"ok": True}
