from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from models import get_db, UserProgress, LearningProfile
from curriculum_data import ALL_MODULES
import json
import random

router = APIRouter(prefix="/review", tags=["review"])


class AddReviewRequest(BaseModel):
    question_id: str
    lesson_id: str
    question_json: str


class RecordReviewRequest(BaseModel):
    question_id: str
    correct: bool


@router.get("/{user_key}/queue")
def get_review_queue(user_key: str, db: Session = Depends(get_db)):
    """
    Return questions the user got wrong, using spaced repetition.
    Pulls from flagged lessons and low-star lessons.
    """
    progress = db.query(UserProgress).filter(UserProgress.user_key == user_key).all()
    profile = db.query(LearningProfile).filter(LearningProfile.user_key == user_key).first()

    lesson_map = {}
    for module in ALL_MODULES:
        for lesson in module["lessons"]:
            lesson_map[lesson["id"]] = lesson

    wrong_questions: list[dict] = []
    question_id_counter = 0

    for p in progress:
        if p.flagged or p.stars < 3:
            lesson = lesson_map.get(p.lesson_id)
            if not lesson or not lesson.get("questions"):
                continue
            for q in lesson["questions"]:
                question_id_counter += 1
                wrong_questions.append({
                    "id": question_id_counter,
                    "question_id": f"{lesson['id']}_q_{q.get('question', '')[:20].replace(' ', '_')}",
                    "lesson_id": lesson["id"],
                    "wrong_count": 1 if p.stars < 3 else 0,
                    "question": {
                        "type": q.get("type", "multiple_choice"),
                        "question": q.get("question", ""),
                        "options": q.get("options", []),
                        "correct_index": q.get("answer") if q.get("type") == "multiple_choice" else None,
                        "explanation": q.get("explanation", ""),
                        "concept_tags": [lesson.get("title", "").lower().replace(" ", "_")],
                    },
                })

    random.shuffle(wrong_questions)
    queue = wrong_questions[:10]

    return {
        "questions": queue,
        "total_due": len(wrong_questions),
    }


@router.post("/{user_key}/record")
def record_review(user_key: str, req: RecordReviewRequest, db: Session = Depends(get_db)):
    """Record a review attempt."""
    profile = db.query(LearningProfile).filter(LearningProfile.user_key == user_key).first()
    if not profile:
        profile = LearningProfile(user_key=user_key)
        db.add(profile)
        db.commit()

    review_log = dict(profile.study_log or {})
    today = datetime.now().date().isoformat()
    key = f"review_{today}"
    review_log[key] = review_log.get(key, 0) + 1
    profile.study_log = review_log
    db.commit()

    return {"ok": True}


@router.post("/{user_key}/add")
def add_to_review_queue(user_key: str, req: AddReviewRequest, db: Session = Depends(get_db)):
    """Add a question to the review queue (stored in profile)."""
    profile = db.query(LearningProfile).filter(LearningProfile.user_key == user_key).first()
    if not profile:
        profile = LearningProfile(user_key=user_key)
        db.add(profile)
        db.commit()

    review_data = dict(profile.preferred_analogies or {})
    review_data[f"review_{req.question_id}"] = req.question_json
    profile.preferred_analogies = review_data
    db.commit()

    return {"ok": True}
