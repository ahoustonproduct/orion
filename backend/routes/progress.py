from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import date, datetime, timedelta, timezone
from typing import Optional
from lesson_sources import get_ready_notebooks
from models import get_db, UserProgress, LearningProfile, Note, BookmarkedPosition, ConfidenceRating
from curriculum_data import ALL_MODULES

router = APIRouter(prefix="/progress", tags=["progress"])


class ProgressUpdate(BaseModel):
    lesson_id: str = Field(..., min_length=1, max_length=120)
    stars: int = Field(..., ge=0, le=3)
    attempts: int = Field(..., ge=0, le=1000)
    hints_used: int = Field(..., ge=0, le=1000)
    completed: bool
    time_spent_minutes: Optional[float] = Field(0.0, ge=0, le=1440)


class FlagUpdate(BaseModel):
    lesson_id: str = Field(..., min_length=1, max_length=120)
    flagged: bool


class NoteUpdate(BaseModel):
    content: str = Field("", max_length=100000)


class BookmarkUpdate(BaseModel):
    lesson_id: str = Field(..., min_length=1, max_length=120)
    step_index: int = Field(..., ge=0, le=1000)
    sub_step: int = Field(0, ge=0, le=1000)
    saved_code: str = Field("", max_length=200000)


class ConfidenceUpdate(BaseModel):
    lesson_id: str = Field(..., min_length=1, max_length=120)
    rating: int = Field(..., ge=1, le=5)


class AnalogyUpdate(BaseModel):
    lesson_id: str = Field(..., min_length=1, max_length=120)
    analogy: str = Field(..., min_length=1, max_length=5000)


def get_or_create_profile(user_key: str, db: Session, *, commit: bool = True) -> LearningProfile:
    profile = db.query(LearningProfile).filter(LearningProfile.user_key == user_key).first()
    if not profile:
        profile = LearningProfile(user_key=user_key)
        db.add(profile)
        if commit:
            db.commit()
            db.refresh(profile)
        else:
            db.flush()
    return profile


@router.get("/{user_key}")
def get_progress(user_key: str, db: Session = Depends(get_db)):
    """Get all progress and profile for a user."""
    progress_rows = db.query(UserProgress).filter(UserProgress.user_key == user_key).all()
    progress = _coalesce_progress_rows(progress_rows)
    profile = get_or_create_profile(user_key, db)

    completed_lessons = {p["lesson_id"] for p in progress if p["completed"]}
    module_status = {}
    for i, module in enumerate(ALL_MODULES):
        lesson_ids = {l["id"] for l in module["lessons"]}
        completed_in_module = lesson_ids & completed_lessons
        # Mastery: % with 3 stars
        starred = sum(1 for p in progress if p["lesson_id"] in lesson_ids and p["stars"] == 3)
        module_status[module["id"]] = {
            "completed_count": len(completed_in_module),
            "total": len(lesson_ids),
            "mastery_pct": round((starred / len(lesson_ids)) * 100) if lesson_ids else 0,
            "unlocked": True,
        }

    for notebook in get_ready_notebooks(db, user_key):
        lessons = (notebook.module_data or {}).get("lessons") or []
        lesson_ids = {l.get("id") for l in lessons if l.get("id")}
        completed_in_module = lesson_ids & completed_lessons
        starred = sum(1 for p in progress if p["lesson_id"] in lesson_ids and p["stars"] == 3)
        module_status[notebook.id] = {
            "completed_count": len(completed_in_module),
            "total": len(lesson_ids),
            "mastery_pct": round((starred / len(lesson_ids)) * 100) if lesson_ids else 0,
            "unlocked": True,
        }

    # Confidence ratings
    confidence = db.query(ConfidenceRating).filter(
        ConfidenceRating.user_key == user_key
    ).order_by(ConfidenceRating.rated_at.desc(), ConfidenceRating.id.desc()).all()
    confidence_map = {}
    for c in confidence:
        confidence_map.setdefault(c.lesson_id, c.rating)

    return {
        "lessons": [
            {
                "lesson_id": p["lesson_id"],
                "stars": p["stars"],
                "attempts": p["attempts"],
                "completed": p["completed"],
                "flagged": p["flagged"],
                "last_accessed": _isoformat(p["last_accessed"]),
            }
            for p in progress
        ],
        "module_status": module_status,
        "study_log": profile.study_log or {},
        "weak_topics": profile.weak_topics or [],
        "mastered_concepts": profile.mastered_concepts or [],
        "preferred_analogies": profile.preferred_analogies or {},
        "topic_confidence": confidence_map,
        "study_plan": profile.study_plan or {},
    }




@router.post("/{user_key}/lesson")
def update_lesson_progress(user_key: str, update: ProgressUpdate, db: Session = Depends(get_db)):
    """Save lesson progress and profile updates in one transaction."""
    try:
        existing = db.query(UserProgress).filter(
            UserProgress.user_key == user_key,
            UserProgress.lesson_id == update.lesson_id
        ).first()

        if existing:
            existing.stars = max(existing.stars or 0, update.stars)
            existing.attempts = max(existing.attempts or 0, update.attempts)
            existing.hints_used = max(existing.hints_used or 0, update.hints_used)
            existing.completed = bool(existing.completed or update.completed)
            existing.last_accessed = datetime.now(timezone.utc)
        else:
            existing = UserProgress(
                user_key=user_key,
                lesson_id=update.lesson_id,
                stars=update.stars,
                attempts=update.attempts,
                hints_used=update.hints_used,
                completed=update.completed,
            )
            db.add(existing)

        profile = get_or_create_profile(user_key, db, commit=False)
        _update_study_log(profile, update.time_spent_minutes or 0)
        _update_weak_topics(profile, update.lesson_id, existing.stars or 0)
        _update_mastered(profile, update.lesson_id, existing.stars or 0)

        db.commit()
        db.refresh(existing)
    except Exception:
        db.rollback()
        raise

    return {"success": True, "stars": existing.stars}


@router.post("/{user_key}/flag")
def toggle_flag(user_key: str, update: FlagUpdate, db: Session = Depends(get_db)):
    """Flag or unflag a lesson for review."""
    existing = db.query(UserProgress).filter(
        UserProgress.user_key == user_key,
        UserProgress.lesson_id == update.lesson_id
    ).first()

    if existing:
        existing.flagged = update.flagged
        db.commit()
    else:
        db.add(UserProgress(user_key=user_key, lesson_id=update.lesson_id, flagged=update.flagged))
        db.commit()

    return {"success": True}


@router.get("/{user_key}/note")
def get_note(user_key: str, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.user_key == user_key).first()
    return {"content": note.content if note else ""}


@router.post("/{user_key}/note")
def save_note(user_key: str, update: NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.user_key == user_key).first()
    if note:
        note.content = update.content
        note.updated_at = datetime.now(timezone.utc)
    else:
        note = Note(user_key=user_key, content=update.content)
        db.add(note)
    db.commit()
    return {"success": True}


@router.post("/{user_key}/bookmark")
def save_bookmark(user_key: str, update: BookmarkUpdate, db: Session = Depends(get_db)):
    """Save the user's position within a lesson so they can resume."""
    try:
        existing = _get_bookmark_row(db, user_key, update.lesson_id)

        if existing:
            existing.step_index = update.step_index
            existing.sub_step = update.sub_step
            if _field_was_provided(update, "saved_code"):
                existing.saved_code = update.saved_code
            existing.updated_at = datetime.now(timezone.utc)
        else:
            db.add(BookmarkedPosition(
                user_key=user_key,
                lesson_id=update.lesson_id,
                step_index=update.step_index,
                sub_step=update.sub_step,
                saved_code=update.saved_code,
            ))
        db.commit()
    except Exception:
        db.rollback()
        raise
    return {"success": True}


@router.get("/{user_key}/bookmark/{lesson_id}")
def get_bookmark(user_key: str, lesson_id: str, db: Session = Depends(get_db)):
    """Get the saved position for a lesson."""
    bookmark = _get_bookmark_row(db, user_key, lesson_id)

    if not bookmark:
        return {"found": False, "step_index": 0, "sub_step": 0, "saved_code": ""}

    return {
        "found": True,
        "step_index": bookmark.step_index,
        "sub_step": bookmark.sub_step,
        "saved_code": bookmark.saved_code,
    }


@router.post("/{user_key}/confidence")
def save_confidence(user_key: str, update: ConfidenceUpdate, db: Session = Depends(get_db)):
    """Save a self-reported confidence rating (1-5) after completing a lesson."""
    try:
        existing = db.query(ConfidenceRating).filter(
            ConfidenceRating.user_key == user_key,
            ConfidenceRating.lesson_id == update.lesson_id
        ).order_by(ConfidenceRating.rated_at.desc(), ConfidenceRating.id.desc()).first()

        if existing:
            existing.rating = update.rating
            existing.rated_at = datetime.now(timezone.utc)
        else:
            db.add(ConfidenceRating(
                user_key=user_key,
                lesson_id=update.lesson_id,
                rating=update.rating,
            ))

        # Keep the rating row and profile map in one transaction.
        profile = get_or_create_profile(user_key, db, commit=False)
        tc = dict(profile.topic_confidence or {})
        tc[update.lesson_id] = update.rating
        profile.topic_confidence = tc
        db.commit()
    except Exception:
        db.rollback()
        raise

    return {"success": True}


@router.post("/{user_key}/analogy")
def save_analogy(user_key: str, update: AnalogyUpdate, db: Session = Depends(get_db)):
    """Record an analogy that worked for this student (Orion remembers it)."""
    profile = get_or_create_profile(user_key, db)
    analogies = dict(profile.preferred_analogies or {})
    analogies[update.lesson_id] = update.analogy
    profile.preferred_analogies = analogies
    db.commit()
    return {"success": True}


@router.get("/{user_key}/week-review")
def get_week_data(user_key: str, db: Session = Depends(get_db)):
    """Get this week's study data for the Week in Review feature."""
    profile = get_or_create_profile(user_key, db)
    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # Monday

    study_log = profile.study_log or {}
    week_log = {
        k: v for k, v in study_log.items()
        if k >= week_start.isoformat()
    }

    # Lessons completed this week
    week_progress_rows = db.query(UserProgress).filter(
        UserProgress.user_key == user_key,
        UserProgress.completed == True,
        UserProgress.last_accessed >= datetime.combine(
            week_start, datetime.min.time()
        ).replace(tzinfo=timezone.utc)
    ).all()
    week_progress = _coalesce_progress_rows(week_progress_rows)

    # Stars earned this week per lesson
    stars_this_week = {p["lesson_id"]: p["stars"] for p in week_progress}

    # Resolve lesson titles
    lesson_map = {}
    for module in ALL_MODULES:
        for lesson in module["lessons"]:
            lesson_map[lesson["id"]] = lesson["title"]

    completed_titles = [lesson_map.get(p["lesson_id"], p["lesson_id"]) for p in week_progress]

    return {
        "study_log": week_log,
        "lessons_completed": completed_titles,
        "stars_earned": stars_this_week,
        "days_studied": len([v for v in week_log.values() if v > 0]),
        "total_minutes": sum(week_log.values()),
    }


def _update_study_log(profile: LearningProfile, minutes: int) -> None:
    """Mutate study_log on the profile in-place. Does NOT commit."""
    today = date.today()
    study_log = dict(profile.study_log or {})
    today_str = today.isoformat()

    study_log[today_str] = study_log.get(today_str, 0) + minutes
    profile.study_log = study_log


def _coalesce_progress_rows(rows: list[UserProgress]) -> list[dict]:
    by_lesson: dict[str, dict] = {}
    for row in rows:
        current = by_lesson.get(row.lesson_id)
        if current is None:
            by_lesson[row.lesson_id] = {
                "lesson_id": row.lesson_id,
                "stars": row.stars or 0,
                "attempts": row.attempts or 0,
                "hints_used": row.hints_used or 0,
                "completed": bool(row.completed),
                "flagged": bool(row.flagged),
                "last_accessed": row.last_accessed,
            }
            continue

        current["stars"] = max(current["stars"], row.stars or 0)
        current["attempts"] = max(current["attempts"], row.attempts or 0)
        current["hints_used"] = max(current["hints_used"], row.hints_used or 0)
        current["completed"] = bool(current["completed"] or row.completed)
        current["flagged"] = bool(current["flagged"] or row.flagged)
        if _later(row.last_accessed, current["last_accessed"]) is row.last_accessed:
            current["last_accessed"] = row.last_accessed

    return sorted(
        by_lesson.values(),
        key=lambda item: _datetime_sort_value(item["last_accessed"]),
    )


def _later(left: datetime | None, right: datetime | None) -> datetime | None:
    if left is None:
        return right
    if right is None:
        return left
    return left if _datetime_sort_value(left) >= _datetime_sort_value(right) else right


def _datetime_sort_value(value: datetime | None) -> float:
    if value is None:
        return 0.0
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.timestamp()


def _isoformat(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def _field_was_provided(update: BaseModel, field_name: str) -> bool:
    fields_set = getattr(update, "model_fields_set", None)
    if fields_set is None:
        fields_set = getattr(update, "__fields_set__", set())
    return field_name in fields_set


def _get_bookmark_row(db: Session, user_key: str, lesson_id: str) -> BookmarkedPosition | None:
    return db.query(BookmarkedPosition).filter(
        BookmarkedPosition.user_key == user_key,
        BookmarkedPosition.lesson_id == lesson_id
    ).order_by(BookmarkedPosition.updated_at.desc(), BookmarkedPosition.id.desc()).first()

def _update_weak_topics(profile: LearningProfile, lesson_id: str, stars: int) -> None:
    """Mutate weak_topics on the profile in-place. Does NOT commit."""
    weak = list(profile.weak_topics or [])
    if stars < 3 and lesson_id not in weak:
        weak.append(lesson_id)
    elif stars == 3 and lesson_id in weak:
        weak.remove(lesson_id)
    profile.weak_topics = weak


def _update_mastered(profile: LearningProfile, lesson_id: str, stars: int) -> None:
    """Mutate mastered_concepts on the profile in-place. Does NOT commit."""
    mastered = list(profile.mastered_concepts or [])
    if stars == 3 and lesson_id not in mastered:
        mastered.append(lesson_id)
    profile.mastered_concepts = mastered
