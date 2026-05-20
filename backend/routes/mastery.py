from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from lesson_sources import lesson_map_for_user
from models import get_db, UserProgress, LearningProfile, ConceptMastery

router = APIRouter(prefix="/mastery", tags=["mastery"])


class MasteryRecordRequest(BaseModel):
    concept_tag: str = Field(..., min_length=1, max_length=160)
    correct: bool


@router.get("/{user_key}")
def get_mastery(user_key: str, db: Session = Depends(get_db)):
    """
    Compute concept mastery from progress plus explicit concept attempts.

    Lesson confidence ratings remain owned by progress. Concept mastery writes
    are stored separately so quiz misses/reviews do not overwrite confidence.
    """
    progress = db.query(UserProgress).filter(UserProgress.user_key == user_key).all()
    profile = db.query(LearningProfile).filter(LearningProfile.user_key == user_key).first()
    concept_rows = db.query(ConceptMastery).filter(ConceptMastery.user_key == user_key).all()

    lesson_map = lesson_map_for_user(db, user_key)

    tags: dict[str, dict[str, int]] = {}
    for row in progress:
        lesson = lesson_map.get(row.lesson_id)
        if not lesson:
            continue
        score = _progress_mastery_score(row)
        for tag in _lesson_tags(lesson):
            _merge_tag(tags, tag, score, row.attempts or 0)

    for row in concept_rows:
        _merge_tag(tags, row.concept_tag, row.score or 0, row.attempts or 0)

    # Backward compatibility: older builds wrote concept scores into
    # topic_confidence. Values 1-5 are lesson confidence ratings and are skipped.
    legacy_confidence = (profile.topic_confidence or {}) if profile else {}
    for tag, value in legacy_confidence.items():
        if isinstance(value, (int, float)) and value > 5:
            _merge_tag(tags, tag, int(value), 0)

    mastery_pct = {tag: data["mastery"] for tag, data in tags.items()}
    focus_areas = [
        {"tag": tag, "mastery": data["mastery"]}
        for tag, data in tags.items()
        if data["mastery"] < 70
    ]
    focus_areas.sort(key=lambda item: (item["mastery"], item["tag"]))

    heatmap_data = [
        {"tag": tag, "mastery": data["mastery"], "attempts": data["attempts"]}
        for tag, data in tags.items()
    ]
    heatmap_data.sort(key=lambda item: item["tag"])

    return {
        "tags": mastery_pct,
        "focus_areas": focus_areas,
        "heatmap_data": heatmap_data,
    }


@router.post("/{user_key}/record")
def record_mastery(
    user_key: str, req: MasteryRecordRequest, db: Session = Depends(get_db)
):
    """Record a concept attempt (correct/incorrect) for mastery tracking."""
    try:
        now = datetime.now(timezone.utc)
        row = (
            db.query(ConceptMastery)
            .filter(
                ConceptMastery.user_key == user_key,
                ConceptMastery.concept_tag == req.concept_tag,
            )
            .first()
        )

        if not row:
            row = ConceptMastery(
                user_key=user_key,
                concept_tag=req.concept_tag,
                score=50,
                attempts=0,
                correct_count=0,
                last_attempted_at=now,
            )
            db.add(row)
            db.flush()

        delta = 5 if req.correct else -3
        base_score = row.score if row.score is not None else 50
        row.score = max(0, min(100, base_score + delta))
        row.attempts = (row.attempts or 0) + 1
        if req.correct:
            row.correct_count = (row.correct_count or 0) + 1
        row.last_attempted_at = now
        db.commit()
    except Exception:
        db.rollback()
        raise

    return {"ok": True}


def _progress_mastery_score(row: UserProgress) -> int:
    score = 0
    if row.completed:
        score += 40
    score += ((row.stars or 0) / 3) * 40
    score += min(row.attempts or 0, 5) * 4
    return min(round(score), 100)


def _lesson_tags(lesson: dict) -> list[str]:
    tags = lesson.get("concept_tags") or lesson.get("tags")
    if isinstance(tags, list) and tags:
        return [str(tag) for tag in tags if str(tag).strip()]
    return [lesson.get("title", "Untitled Lesson")]


def _merge_tag(tags: dict[str, dict[str, int]], tag: str, mastery: int, attempts: int) -> None:
    current = tags.setdefault(tag, {"mastery": 0, "attempts": 0})
    current["mastery"] = max(current["mastery"], max(0, min(100, mastery)))
    current["attempts"] += max(0, attempts)
