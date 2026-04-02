import os
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
from models import get_db, LearningProfile
from prompts import (
    explain_concept_prompt, code_feedback_prompt,
    give_hint_prompt, lesson_recap_prompt,
    generate_challenge_prompt, explain_your_answer_prompt,
    study_plan_prompt, week_review_prompt, what_next_prompt
)
from curriculum_data import ALL_MODULES

router = APIRouter(prefix="/orion", tags=["orion"])

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:7b")
client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


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


def stream_response(prompt: str, max_tokens: int = 1500):
    """Stream Ollama's response token by token."""
    def generate():
        stream = client.chat.completions.create(
            model=MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    return StreamingResponse(generate(), media_type="text/plain")


class ExplainRequest(BaseModel):
    user_key: str
    lesson: dict


class FeedbackRequest(BaseModel):
    user_key: str
    lesson: dict
    student_code: str
    actual_output: str
    expected_output: str
    attempts: int


class HintRequest(BaseModel):
    lesson: dict
    student_code: str
    hint_number: int


class RecapRequest(BaseModel):
    user_key: str
    lesson: dict
    stars: int
    attempts: int
    student_code: str


class ChallengeRequest(BaseModel):
    user_key: str
    lesson: dict
    variation_index: Optional[int] = 0


class ExplainAnswerRequest(BaseModel):
    lesson: dict
    question: dict
    chosen_option: str
    student_reasoning: str


class StudyPlanRequest(BaseModel):
    user_key: str
    progress_data: dict
    days_until_start: int


class WeekReviewRequest(BaseModel):
    user_key: str
    week_data: dict


class WhatNextRequest(BaseModel):
    user_key: str
    progress_data: dict


@router.post("/explain")
def explain_concept(req: ExplainRequest, db: Session = Depends(get_db)):
    """Stream Orion's thorough lesson explanation."""
    profile = get_profile(req.user_key, db)
    prompt = explain_concept_prompt(req.lesson, profile)
    return stream_response(prompt, max_tokens=1800)


@router.post("/feedback")
def code_feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    """Stream Orion's code review and feedback."""
    profile = get_profile(req.user_key, db)
    prompt = code_feedback_prompt(
        req.lesson, req.student_code, req.actual_output,
        req.expected_output, req.attempts, profile
    )
    return stream_response(prompt, max_tokens=600)


@router.post("/hint")
def give_hint(req: HintRequest):
    """Stream a progressive hint from Orion."""
    prompt = give_hint_prompt(req.lesson, req.student_code, req.hint_number)
    return stream_response(prompt, max_tokens=300)


@router.post("/recap")
def lesson_recap(req: RecapRequest, db: Session = Depends(get_db)):
    """Stream Orion's personalized lesson recap."""
    profile = get_profile(req.user_key, db)
    prompt = lesson_recap_prompt(req.lesson, req.stars, req.attempts, req.student_code, profile)
    return stream_response(prompt, max_tokens=400)


@router.post("/generate-challenge")
def generate_challenge(req: ChallengeRequest, db: Session = Depends(get_db)):
    """Stream a new AI-generated practice challenge."""
    profile = get_profile(req.user_key, db)
    prompt = generate_challenge_prompt(req.lesson, profile, req.variation_index or 0)
    return stream_response(prompt, max_tokens=800)


@router.post("/explain-your-answer")
def explain_your_answer(req: ExplainAnswerRequest):
    """Orion evaluates the student's reasoning behind their quiz answer."""
    prompt = explain_your_answer_prompt(
        req.lesson, req.question, req.chosen_option, req.student_reasoning
    )
    return stream_response(prompt, max_tokens=300)


@router.post("/study-plan")
def generate_study_plan(req: StudyPlanRequest, db: Session = Depends(get_db)):
    """Generate a personalized weekly study plan."""
    profile = get_profile(req.user_key, db)
    prompt = study_plan_prompt(profile, req.progress_data, req.days_until_start)
    db_profile = db.query(LearningProfile).filter(LearningProfile.user_key == req.user_key).first()
    if db_profile:
        db_profile.study_plan = req.progress_data
        db.commit()
    return stream_response(prompt, max_tokens=800)


@router.post("/week-review")
def generate_week_review(req: WeekReviewRequest):
    """Generate the Sunday Week in Review summary."""
    wd = req.week_data
    prompt = week_review_prompt(
        study_log=wd.get("study_log", {}),
        lessons_completed_this_week=wd.get("lessons_completed", []),
        stars_earned=wd.get("stars_earned", {}),
        streak=wd.get("streak", 0),
    )
    return stream_response(prompt, max_tokens=600)


@router.post("/what-next")
def what_next(req: WhatNextRequest, db: Session = Depends(get_db)):
    """Generate Orion's 'What's Next' dashboard recommendation."""
    profile = get_profile(req.user_key, db)
    prompt = what_next_prompt(req.progress_data, ALL_MODULES, profile)
    if prompt is None:
        def done():
            yield "You've completed all available lessons — Orion is proud of you!"
        return StreamingResponse(done(), media_type="text/plain")
    return stream_response(prompt, max_tokens=200)


class ChatRequest(BaseModel):
    user_message: str
    lesson_id: str
    lesson_title: str
    current_code: str
    chat_history: list[dict[str, str]]


@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    """Stream a chat response for the AI Sidebar."""
    profile = db.query(LearningProfile).filter(LearningProfile.user_key == "default").first()
    weak_topics = profile.weak_topics if profile else []
    
    system_prompt = f"""You are Orion, an AI tutor for a business analytics student. You are helpful, patient, and explain concepts clearly.

Context:
- Student is working on lesson: {req.lesson_title} (ID: {req.lesson_id})
- Weak areas to keep in mind: {', '.join(weak_topics) if weak_topics else 'None identified yet'}
- Current code in editor:
```python
{req.current_code or '(No code yet)'}
```

Guidelines:
1. Be conversational but educational
2. If the user asks about code, reference their current code
3. If they're stuck, give hints rather than solutions
4. Use simple analogies for business concepts
5. Keep responses concise but helpful

Previous conversation:
{chr(10).join([f"{m['role'].capitalize()}: {m['content'][:200]}" for m in req.chat_history[-5:]])}

User: {req.user_message}

Orion:"""

    def generate():
        stream = client.chat.completions.create(
            model=MODEL,
            max_tokens=800,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.user_message}
            ],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    return StreamingResponse(generate(), media_type="text/plain")
