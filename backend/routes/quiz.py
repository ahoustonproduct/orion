import os
import random
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from openai import OpenAI
from models import get_db, UserProgress, LearningProfile
from curriculum_data import ALL_MODULES
from prompts import quiz_question_prompt

router = APIRouter(prefix="/quiz", tags=["quiz"])
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:7b")
client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

QUESTION_TYPES = ["multiple_choice", "true_false", "fill_blank"]


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


def get_profile(user_key: str, db: Session) -> dict:
    profile = db.query(LearningProfile).filter(LearningProfile.user_key == user_key).first()
    if not profile:
        return {
            "weak_topics": [],
            "common_mistakes": [],
            "mastered_concepts": [],
            "preferred_analogies": {},
            "topic_confidence": {},
        }
    return {
        "weak_topics": profile.weak_topics or [],
        "common_mistakes": profile.common_mistakes or [],
        "mastered_concepts": profile.mastered_concepts or [],
        "preferred_analogies": profile.preferred_analogies or {},
        "topic_confidence": profile.topic_confidence or {},
    }


@router.post("/generate")
def generate_ai_quiz(req: GenerateQuizRequest, db: Session = Depends(get_db)):
    """Generate fresh AI quiz questions for given lesson IDs."""
    profile = get_profile(req.user_key, db)
    questions = []
    for lesson_id in req.lesson_ids[:5]:
        lesson = get_lesson_by_id(lesson_id)
        if not lesson:
            continue
        q_type = random.choice(QUESTION_TYPES)
        prompt = quiz_question_prompt(lesson, q_type, profile)
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            text = response.choices[0].message.content
            # Extract JSON from response
            start = text.find("{")
            end = text.rfind("}") + 1
            q = json.loads(text[start:end])
            q["lesson_id"] = lesson_id
            q["lesson_title"] = lesson["title"]
            questions.append(q)
        except Exception:
            pass  # Skip malformed responses

    return {"questions": questions}
