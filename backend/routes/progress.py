from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date, datetime, timedelta
from typing import Optional
from models import get_db, UserProgress, LearningProfile, Note, BookmarkedPosition, ConfidenceRating
from curriculum_data import ALL_MODULES

router = APIRouter(prefix="/progress", tags=["progress"])


class ProgressUpdate(BaseModel):
    lesson_id: str
    stars: int
    attempts: int
    hints_used: int
    completed: bool
    time_spent_minutes: Optional[float] = 0.0


class FlagUpdate(BaseModel):
    lesson_id: str
    flagged: bool


class NoteUpdate(BaseModel):
    content: str


class BookmarkUpdate(BaseModel):
    lesson_id: str
    step_index: int
    sub_step: int = 0
    saved_code: str = ""


class ConfidenceUpdate(BaseModel):
    lesson_id: str
    rating: int  # 1-5


class AnalogyUpdate(BaseModel):
    lesson_id: str
    analogy: str


def get_or_create_profile(user_key: str, db: Session) -> LearningProfile:
    profile = db.query(LearningProfile).filter(LearningProfile.user_key == user_key).first()
    if not profile:
        profile = LearningProfile(user_key=user_key)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.get("/{user_key}")
def get_progress(user_key: str, db: Session = Depends(get_db)):
    """Get all progress and profile for a user."""
    progress = db.query(UserProgress).filter(UserProgress.user_key == user_key).all()
    profile = get_or_create_profile(user_key, db)

    completed_lessons = {p.lesson_id for p in progress if p.completed}
    module_status = {}
    for i, module in enumerate(ALL_MODULES):
        lesson_ids = {l["id"] for l in module["lessons"]}
        completed_in_module = lesson_ids & completed_lessons
        # Mastery: % with 3 stars
        starred = db.query(UserProgress).filter(
            UserProgress.user_key == user_key,
            UserProgress.lesson_id.in_(lesson_ids),
            UserProgress.stars == 3
        ).count()
        module_status[module["id"]] = {
            "completed_count": len(completed_in_module),
            "total": len(lesson_ids),
            "mastery_pct": round((starred / len(lesson_ids)) * 100) if lesson_ids else 0,
            "unlocked": True,
        }

    # Confidence ratings
    confidence = db.query(ConfidenceRating).filter(
        ConfidenceRating.user_key == user_key
    ).all()
    confidence_map = {c.lesson_id: c.rating for c in confidence}

    return {
        "lessons": [
            {
                "lesson_id": p.lesson_id,
                "stars": p.stars,
                "attempts": p.attempts,
                "completed": p.completed,
                "flagged": p.flagged,
                "last_accessed": p.last_accessed.isoformat() if p.last_accessed else None,
            }
            for p in progress
        ],
        "module_status": module_status,
        "streak": profile.streak_count,
        "study_log": profile.study_log or {},
        "weak_topics": profile.weak_topics or [],
        "mastered_concepts": profile.mastered_concepts or [],
        "preferred_analogies": profile.preferred_analogies or {},
        "topic_confidence": confidence_map,
        "study_plan": profile.study_plan or {},
    }




@router.post("/{user_key}/lesson")
def update_lesson_progress(user_key: str, update: ProgressUpdate, db: Session = Depends(get_db)):
    """Save or update lesson progress."""
    existing = db.query(UserProgress).filter(
        UserProgress.user_key == user_key,
        UserProgress.lesson_id == update.lesson_id
    ).first()

    if existing:
        existing.stars = max(existing.stars, update.stars)
        existing.attempts = update.attempts
        existing.hints_used = update.hints_used
        existing.completed = update.completed
        existing.last_accessed = datetime.utcnow()
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

    db.commit()

    profile = get_or_create_profile(user_key, db)
    _update_streak(profile, update.time_spent_minutes or 0, db)
    _update_weak_topics(profile, update.lesson_id, update.stars, db)
    _update_mastered(profile, update.lesson_id, update.stars, db)

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
        note.updated_at = datetime.utcnow()
    else:
        note = Note(user_key=user_key, content=update.content)
        db.add(note)
    db.commit()
    return {"success": True}


@router.post("/{user_key}/bookmark")
def save_bookmark(user_key: str, update: BookmarkUpdate, db: Session = Depends(get_db)):
    """Save the user's position within a lesson so they can resume."""
    existing = db.query(BookmarkedPosition).filter(
        BookmarkedPosition.user_key == user_key,
        BookmarkedPosition.lesson_id == update.lesson_id
    ).first()

    if existing:
        existing.step_index = update.step_index
        existing.sub_step = update.sub_step
        existing.saved_code = update.saved_code
        existing.updated_at = datetime.utcnow()
    else:
        db.add(BookmarkedPosition(
            user_key=user_key,
            lesson_id=update.lesson_id,
            step_index=update.step_index,
            sub_step=update.sub_step,
            saved_code=update.saved_code,
        ))
    db.commit()
    return {"success": True}


@router.get("/{user_key}/bookmark/{lesson_id}")
def get_bookmark(user_key: str, lesson_id: str, db: Session = Depends(get_db)):
    """Get the saved position for a lesson."""
    bookmark = db.query(BookmarkedPosition).filter(
        BookmarkedPosition.user_key == user_key,
        BookmarkedPosition.lesson_id == lesson_id
    ).first()

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
    existing = db.query(ConfidenceRating).filter(
        ConfidenceRating.user_key == user_key,
        ConfidenceRating.lesson_id == update.lesson_id
    ).first()

    if existing:
        existing.rating = update.rating
        existing.rated_at = datetime.utcnow()
    else:
        db.add(ConfidenceRating(
            user_key=user_key,
            lesson_id=update.lesson_id,
            rating=update.rating,
        ))
    db.commit()

    # Update profile's topic_confidence map
    profile = get_or_create_profile(user_key, db)
    tc = dict(profile.topic_confidence or {})
    tc[update.lesson_id] = update.rating
    profile.topic_confidence = tc
    db.commit()

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
    week_progress = db.query(UserProgress).filter(
        UserProgress.user_key == user_key,
        UserProgress.completed == True,
        UserProgress.last_accessed >= datetime.combine(week_start, datetime.min.time())
    ).all()

    # Stars earned this week per lesson
    stars_this_week = {p.lesson_id: p.stars for p in week_progress}

    # Resolve lesson titles
    lesson_map = {}
    for module in ALL_MODULES:
        for lesson in module["lessons"]:
            lesson_map[lesson["id"]] = lesson["title"]

    completed_titles = [lesson_map.get(p.lesson_id, p.lesson_id) for p in week_progress]

    return {
        "study_log": week_log,
        "lessons_completed": completed_titles,
        "stars_earned": stars_this_week,
        "streak": profile.streak_count,
        "days_studied": len([v for v in week_log.values() if v > 0]),
        "total_minutes": sum(week_log.values()),
    }


def _update_streak(profile: LearningProfile, minutes: int, db: Session):
    today = date.today()
    study_log = dict(profile.study_log or {})
    today_str = today.isoformat()

    study_log[today_str] = study_log.get(today_str, 0) + minutes
    profile.study_log = study_log

    if profile.last_active and profile.last_active == today:
        pass
    else:
        yesterday = today - timedelta(days=1)
        if profile.last_active == yesterday:
            profile.streak_count += 1
        else:
            profile.streak_count = 1
        profile.last_active = today

    db.commit()


def _update_weak_topics(profile: LearningProfile, lesson_id: str, stars: int, db: Session):
    weak = list(profile.weak_topics or [])
    if stars < 3 and lesson_id not in weak:
        weak.append(lesson_id)
    elif stars == 3 and lesson_id in weak:
        weak.remove(lesson_id)
    profile.weak_topics = weak
    db.commit()


def _update_mastered(profile: LearningProfile, lesson_id: str, stars: int, db: Session):
    mastered = list(profile.mastered_concepts or [])
    if stars == 3 and lesson_id not in mastered:
        mastered.append(lesson_id)
    profile.mastered_concepts = mastered
    db.commit()
