from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone
from lesson_sources import lesson_map_for_user
from models import get_db, UserProgress, LearningProfile, ReviewItem
import json

router = APIRouter(prefix="/review", tags=["review"])


class AddReviewRequest(BaseModel):
    question_id: str = Field(..., min_length=1, max_length=240)
    lesson_id: str = Field(..., min_length=1, max_length=120)
    question_json: str = Field(..., min_length=1, max_length=200000)


class RecordReviewRequest(BaseModel):
    question_id: str = Field(..., min_length=1, max_length=240)
    correct: bool


@router.get("/{user_key}/queue")
def get_review_queue(user_key: str, db: Session = Depends(get_db)):
    """
    Return questions due for review.

    Sources are explicit missed questions first, then flagged or low-star
    lessons. Legacy profile-stored review items are still surfaced so older
    saved queues are not lost.
    """
    now = datetime.now(timezone.utc)
    progress = db.query(UserProgress).filter(UserProgress.user_key == user_key).all()
    profile = db.query(LearningProfile).filter(LearningProfile.user_key == user_key).first()
    lesson_map = lesson_map_for_user(db, user_key)

    review_items = (
        db.query(ReviewItem)
        .filter(ReviewItem.user_key == user_key, ReviewItem.resolved == False)
        .order_by(ReviewItem.next_due_at.asc(), ReviewItem.last_missed_at.desc(), ReviewItem.id.asc())
        .all()
    )
    due_items = [item for item in review_items if _is_due(item, now)]

    queue: list[dict] = []
    seen_question_ids: set[str] = set()
    for item in due_items:
        queue.append(_review_item_to_queue_question(item, lesson_map))
        seen_question_ids.add(item.question_id)

    queue.extend(_legacy_review_questions(profile, lesson_map, seen_question_ids, len(queue) + 1))
    queue.extend(_progress_review_questions(progress, lesson_map, seen_question_ids, len(queue) + 1))

    recent_misses = [
        _review_item_summary(item, lesson_map)
        for item in sorted(
            review_items,
            key=lambda item: _datetime_sort_value(item.last_missed_at),
            reverse=True,
        )
        if item.last_missed_at
    ][:10]

    return {
        "questions": queue[:10],
        "total_due": len(queue),
        "due_review_count": len(queue),
        "recent_misses": recent_misses,
    }


@router.post("/{user_key}/record")
def record_review(user_key: str, req: RecordReviewRequest, db: Session = Depends(get_db)):
    """Record a review attempt and move explicit review items along a due schedule."""
    try:
        profile = db.query(LearningProfile).filter(LearningProfile.user_key == user_key).first()
        if not profile:
            profile = LearningProfile(user_key=user_key)
            db.add(profile)
            db.flush()

        now = datetime.now(timezone.utc)
        review_log = dict(profile.study_log or {})
        today = now.date().isoformat()
        key = f"review_{today}"
        review_log[key] = review_log.get(key, 0) + 1
        profile.study_log = review_log

        item = (
            db.query(ReviewItem)
            .filter(ReviewItem.user_key == user_key, ReviewItem.question_id == req.question_id)
            .first()
        )
        if item:
            item.last_reviewed_at = now
            item.updated_at = now
            if req.correct:
                item.correct_count = (item.correct_count or 0) + 1
                item.next_due_at = now + timedelta(days=_review_delay_days(item.correct_count))
            else:
                item.wrong_count = (item.wrong_count or 0) + 1
                item.last_missed_at = now
                item.next_due_at = now
                item.resolved = False

        db.commit()
    except Exception:
        db.rollback()
        raise

    return {"ok": True}


@router.post("/{user_key}/add")
def add_to_review_queue(user_key: str, req: AddReviewRequest, db: Session = Depends(get_db)):
    """Add or refresh a missed question in the explicit review queue."""
    try:
        now = datetime.now(timezone.utc)
        question_payload = _parse_question_json(req.question_json)
        item = (
            db.query(ReviewItem)
            .filter(ReviewItem.user_key == user_key, ReviewItem.question_id == req.question_id)
            .first()
        )

        if item:
            item.lesson_id = req.lesson_id
            item.question_json = question_payload
            item.wrong_count = (item.wrong_count or 0) + 1
            item.last_missed_at = now
            item.next_due_at = now
            item.resolved = False
            item.updated_at = now
        else:
            db.add(ReviewItem(
                user_key=user_key,
                question_id=req.question_id,
                lesson_id=req.lesson_id,
                question_json=question_payload,
                wrong_count=1,
                last_missed_at=now,
                next_due_at=now,
                resolved=False,
                created_at=now,
                updated_at=now,
            ))

        db.commit()
    except Exception:
        db.rollback()
        raise

    return {"ok": True}


def _progress_review_questions(
    progress: list[UserProgress],
    lesson_map: dict[str, dict],
    seen_question_ids: set[str],
    start_id: int,
) -> list[dict]:
    questions: list[dict] = []
    next_id = start_id

    for row in progress:
        if not row.flagged and (row.stars or 0) >= 3:
            continue

        lesson = lesson_map.get(row.lesson_id)
        if not lesson or not lesson.get("questions"):
            continue

        for index, question in enumerate(lesson["questions"], 1):
            question_id = f"{row.lesson_id}:q{index}"
            if question_id in seen_question_ids:
                continue
            seen_question_ids.add(question_id)
            questions.append({
                "id": next_id,
                "question_id": question_id,
                "lesson_id": row.lesson_id,
                "wrong_count": max(1 if (row.stars or 0) < 3 else 0, 0),
                "question": _normalize_question(question, lesson),
            })
            next_id += 1

    return questions


def _legacy_review_questions(
    profile: LearningProfile | None,
    lesson_map: dict[str, dict],
    seen_question_ids: set[str],
    start_id: int,
) -> list[dict]:
    if not profile:
        return []

    questions: list[dict] = []
    next_id = start_id
    for key, raw_payload in (profile.preferred_analogies or {}).items():
        if not isinstance(key, str) or not key.startswith("review_"):
            continue

        question_id = key.removeprefix("review_")
        if question_id in seen_question_ids:
            continue

        payload = _parse_question_json(raw_payload)
        lesson_id = payload.get("lesson_id", "")
        lesson = lesson_map.get(lesson_id, {})
        questions.append({
            "id": next_id,
            "question_id": question_id,
            "lesson_id": lesson_id,
            "wrong_count": 1,
            "question": _normalize_question(payload, lesson),
        })
        seen_question_ids.add(question_id)
        next_id += 1

    return questions


def _review_item_to_queue_question(item: ReviewItem, lesson_map: dict[str, dict]) -> dict:
    lesson = lesson_map.get(item.lesson_id, {})
    return {
        "id": item.id,
        "question_id": item.question_id,
        "lesson_id": item.lesson_id,
        "wrong_count": item.wrong_count or 0,
        "question": _normalize_question(item.question_json or {}, lesson),
    }


def _review_item_summary(item: ReviewItem, lesson_map: dict[str, dict]) -> dict:
    lesson = lesson_map.get(item.lesson_id, {})
    question = _normalize_question(item.question_json or {}, lesson)
    return {
        "question_id": item.question_id,
        "lesson_id": item.lesson_id,
        "lesson_title": lesson.get("title", item.lesson_id),
        "question": question.get("question", ""),
        "wrong_count": item.wrong_count or 0,
        "last_missed_at": _isoformat(item.last_missed_at),
        "next_due_at": _isoformat(item.next_due_at),
    }


def _normalize_question(raw_question, lesson: dict | None = None) -> dict:
    question = _parse_question_json(raw_question)
    lesson = lesson or {}
    question_type = question.get("type", "multiple_choice")
    answer = question.get("answer")
    correct_index = question.get("correct_index")

    if correct_index is None:
        if question_type == "multiple_choice" and isinstance(answer, int):
            correct_index = answer
        elif question_type == "true_false" and isinstance(answer, bool):
            correct_index = 0 if answer else 1

    if answer is None and question_type == "true_false" and correct_index is not None:
        answer = correct_index == 0

    accepted_answers = question.get("accepted_answers")
    if not accepted_answers and answer is not None:
        accepted_answers = [str(answer)]

    sample_answer = question.get("sample_answer")
    if not sample_answer and answer is not None:
        sample_answer = str(answer)

    concept_tags = question.get("concept_tags") or question.get("key_concepts")
    if not concept_tags:
        concept_tags = [_slug(lesson.get("title", "review"))]

    return {
        "type": question_type,
        "question": question.get("question", ""),
        "options": question.get("options", []),
        "correct_index": correct_index,
        "answer": answer,
        "template": question.get("template"),
        "lines": question.get("lines", []),
        "broken_code": question.get("broken_code"),
        "accepted_answers": accepted_answers or [],
        "sample_answer": sample_answer or "",
        "explanation": question.get("explanation", ""),
        "concept_tags": concept_tags,
    }


def _parse_question_json(raw_payload) -> dict:
    if isinstance(raw_payload, dict):
        return raw_payload
    if isinstance(raw_payload, str):
        try:
            parsed = json.loads(raw_payload)
            return parsed if isinstance(parsed, dict) else {"question": raw_payload}
        except json.JSONDecodeError:
            return {"type": "short_answer", "question": raw_payload, "explanation": ""}
    return {}


def _is_due(item: ReviewItem, now: datetime) -> bool:
    due_at = _as_aware(item.next_due_at)
    return due_at is None or due_at <= now


def _review_delay_days(correct_count: int) -> int:
    if correct_count <= 1:
        return 1
    if correct_count == 2:
        return 3
    return 7


def _as_aware(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def _datetime_sort_value(value: datetime | None) -> float:
    value = _as_aware(value)
    return value.timestamp() if value else 0.0


def _isoformat(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def _slug(value: str) -> str:
    return "_".join(value.lower().split()) or "review"
