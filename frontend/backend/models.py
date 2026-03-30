"""
models.py — Pydantic request/response models for Orion Code API.
"""

from pydantic import BaseModel
from typing import Optional, Any


# ---------------------------------------------------------------------------
# Progress / lesson models
# ---------------------------------------------------------------------------

class SaveLessonRequest(BaseModel):
    lesson_id: str
    stars: int
    completed: bool
    time_spent_minutes: float
    hints_used: int = 0


class FlagRequest(BaseModel):
    lesson_id: str
    flagged: bool


class NoteRequest(BaseModel):
    content: str


class BookmarkRequest(BaseModel):
    lesson_id: str
    step_index: int
    sub_step: str = ""
    saved_code: str = ""


class ConfidenceRequest(BaseModel):
    lesson_id: str
    rating: int


class AnalogyRequest(BaseModel):
    lesson_id: str
    analogy: str


# ---------------------------------------------------------------------------
# Code execution models
# ---------------------------------------------------------------------------

class ExecutePythonRequest(BaseModel):
    code: str


class ExecuteSQLRequest(BaseModel):
    query: str


# ---------------------------------------------------------------------------
# Decision / mastery / review models
# ---------------------------------------------------------------------------

class DecisionEvaluateRequest(BaseModel):
    lesson_id: str
    block_id: str
    decision_type: str
    user_value: Any


class RecordMasteryRequest(BaseModel):
    concept_tag: str
    correct: bool


class RecordReviewRequest(BaseModel):
    question_id: str
    correct: bool


class AddToReviewRequest(BaseModel):
    question_id: str
    lesson_id: str
    question_json: str


# ---------------------------------------------------------------------------
# Orion AI streaming request models
# ---------------------------------------------------------------------------

class OrionExplainRequest(BaseModel):
    lesson_id: str
    concept: str
    context: str = ""


class OrionFeedbackRequest(BaseModel):
    lesson_id: str
    code: str
    expected: str = ""


class OrionHintRequest(BaseModel):
    lesson_id: str
    hint_number: int
    context: str = ""


class OrionRecapRequest(BaseModel):
    lesson_id: str
    completed_steps: list = []


class OrionChallengeRequest(BaseModel):
    lesson_id: str
    concept: str
    difficulty: str = "medium"


class OrionDecisionRequest(BaseModel):
    lesson_id: str
    decision_value: Any
    decision_type: str
    scenario: str = ""


class OrionWhatNextRequest(BaseModel):
    user_key: str
    progress: dict = {}


class OrionStudyPlanRequest(BaseModel):
    user_key: str
    weak_topics: list = []
    goals: str = ""


class OrionWeekReviewRequest(BaseModel):
    user_key: str
    week_data: dict = {}


class OrionExplainAnswerRequest(BaseModel):
    lesson_id: str
    question: str = ""
    user_answer: str = ""
    correct_answer: str = ""


class OrionEvaluateDecisionRequest(BaseModel):
    lesson_id: str
    justification: str
    decision_value: Any = None
    scenario: str = ""
