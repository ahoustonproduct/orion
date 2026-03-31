from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from models import get_db, UserProgress, LearningProfile
from curriculum_data import ALL_MODULES
import json

router = APIRouter(prefix="/mastery", tags=["mastery"])


class MasteryRecordRequest(BaseModel):
    concept_tag: str
    correct: bool


@router.get("/{user_key}")
def get_mastery(user_key: str, db: Session = Depends(get_db)):
    """
    Compute concept mastery from progress data.
    Tags concepts based on lesson completion and star ratings.
    """
    progress = db.query(UserProgress).filter(UserProgress.user_key == user_key).all()
    profile = db.query(LearningProfile).filter(LearningProfile.user_key == user_key).first()

    lesson_map = {}
    for module in ALL_MODULES:
        for lesson in module["lessons"]:
            lesson_map[lesson["id"]] = lesson

    tags: dict[str, dict[str, int]] = {}
    for p in progress:
        lesson = lesson_map.get(p.lesson_id)
        if not lesson:
            continue
        title = lesson.get("title", p.lesson_id)
        tags[title] = {
            "stars": max(tags.get(title, {}).get("stars", 0), p.stars),
            "attempts": tags.get(title, {}).get("attempts", 0) + p.attempts,
            "completed": 1 if p.completed else 0,
        }

    total_tags = len(tags)
    mastery_pct = {}
    for tag, data in tags.items():
        score = 0
        if data["completed"]:
            score += 40
        score += (data["stars"] / 3) * 40
        score += min(data["attempts"], 5) * 4
        mastery_pct[tag] = min(round(score), 100)

    focus_areas = [
        {"tag": tag, "mastery": score}
        for tag, score in mastery_pct.items()
        if score < 70
    ]
    focus_areas.sort(key=lambda x: x["mastery"])

    heatmap_data = [
        {"tag": tag, "mastery": score, "attempts": tags[tag]["attempts"]}
        for tag, score in mastery_pct.items()
    ]
    heatmap_data.sort(key=lambda x: x["tag"])

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
    profile = db.query(LearningProfile).filter(LearningProfile.user_key == user_key).first()
    if not profile:
        profile = LearningProfile(user_key=user_key)
        db.add(profile)
        db.commit()

    tags = dict(profile.topic_confidence or {})
    current = tags.get(req.concept_tag, 50)
    delta = 5 if req.correct else -3
    tags[req.concept_tag] = max(0, min(100, current + delta))
    profile.topic_confidence = tags
    db.commit()

    return {"ok": True}
