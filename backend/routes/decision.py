from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from curriculum_data import ALL_MODULES


router = APIRouter(prefix="/decision", tags=["decision"])


class DecisionEvaluateRequest(BaseModel):
    lesson_id: str
    block_id: str | None = None
    decision_type: str
    user_value: Any


def _find_decision_block(lesson_id: str, block_id: str | None, decision_type: str) -> dict:
    for module in ALL_MODULES:
        for lesson in module.get("lessons", []):
            if lesson.get("id") != lesson_id:
                continue
            for index, block in enumerate(lesson.get("blocks", []) or []):
                if block.get("type") != "decision_block":
                    continue
                block_key = block.get("id") or f"decision_block_{index}"
                if block_id and block_id not in {block_key, "decision_block"}:
                    continue
                if block.get("decision_type") == decision_type:
                    return block
    return {}


def _score_by_distance(value: float, optimal: float, worst: float) -> float:
    worst_distance = abs(worst - optimal) or 1.0
    distance = abs(value - optimal)
    return max(0.0, min(1.0, 1.0 - (distance / worst_distance)))


def _numeric_outcome(block: dict, user_value: Any) -> tuple[float, float, float, float]:
    value = float(user_value)
    optimal = float(block.get("optimal_value", block.get("default_value", value)))
    worst = float(block.get("worst_value", block.get("slider_min", optimal - 1)))
    score = _score_by_distance(value, optimal, worst)
    optimal_outcome = float(block.get("optimal_outcome", 1000))
    worst_outcome = float(block.get("worst_outcome", 0))
    user_outcome = worst_outcome + (optimal_outcome - worst_outcome) * score
    return user_outcome, optimal_outcome, worst_outcome, score


def _choice_outcome(block: dict, user_value: Any) -> tuple[float, float, float, float]:
    optimal = block.get("optimal_option")
    worst = block.get("worst_option")
    if optimal and user_value == optimal:
        score = 1.0
    elif worst and user_value == worst:
        score = 0.0
    elif optimal:
        score = 0.6
    else:
        score = 0.75 if user_value else 0.0
    optimal_outcome = 1000.0
    worst_outcome = 0.0
    user_outcome = worst_outcome + (optimal_outcome - worst_outcome) * score
    return user_outcome, optimal_outcome, worst_outcome, score


def _mapping_outcome(block: dict, user_value: Any, optimal_key: str) -> tuple[float, float, float, float]:
    if not isinstance(user_value, dict):
        return 0.0, 1000.0, 0.0, 0.0

    optimal = block.get(optimal_key)
    if not isinstance(optimal, dict) or not optimal:
        score = 0.75
    elif all(isinstance(v, (int, float)) for v in optimal.values()):
        total = sum(abs(float(v)) for v in optimal.values()) or 1.0
        diff = sum(abs(float(user_value.get(k, 0)) - float(v)) for k, v in optimal.items())
        score = max(0.0, min(1.0, 1.0 - (diff / total)))
    else:
        matches = sum(1 for key, expected in optimal.items() if user_value.get(key) == expected)
        score = matches / len(optimal)

    optimal_outcome = 1000.0
    worst_outcome = 0.0
    user_outcome = worst_outcome + (optimal_outcome - worst_outcome) * score
    return user_outcome, optimal_outcome, worst_outcome, score


def _written_outcome(block: dict, user_value: Any) -> tuple[float, float, float, float]:
    text = str(user_value or "").lower()
    required = block.get("key_concepts_required") or []
    if required:
        hits = sum(1 for concept in required if str(concept).lower() in text)
        concept_score = hits / len(required)
    else:
        concept_score = 0.7 if len(text.strip()) >= 20 else 0.0
    length_score = min(1.0, len(text.strip()) / 120)
    score = max(0.0, min(1.0, (concept_score * 0.7) + (length_score * 0.3)))
    optimal_outcome = 1000.0
    worst_outcome = 0.0
    user_outcome = worst_outcome + (optimal_outcome - worst_outcome) * score
    return user_outcome, optimal_outcome, worst_outcome, score


@router.post("/evaluate")
def evaluate_decision(req: DecisionEvaluateRequest) -> dict:
    block = _find_decision_block(req.lesson_id, req.block_id, req.decision_type)

    try:
        if req.decision_type == "numeric_threshold":
            user_outcome, optimal_outcome, worst_outcome, score = _numeric_outcome(block, req.user_value)
        elif req.decision_type == "budget_allocation":
            user_outcome, optimal_outcome, worst_outcome, score = _mapping_outcome(
                block, req.user_value, "optimal_allocation"
            )
        elif req.decision_type == "approval_matrix":
            user_outcome, optimal_outcome, worst_outcome, score = _mapping_outcome(
                block, req.user_value, "optimal_matrix"
            )
        elif req.decision_type == "written_justification":
            user_outcome, optimal_outcome, worst_outcome, score = _written_outcome(block, req.user_value)
        else:
            user_outcome, optimal_outcome, worst_outcome, score = _choice_outcome(block, req.user_value)
    except (TypeError, ValueError):
        user_outcome, optimal_outcome, worst_outcome, score = 0.0, 1000.0, 0.0, 0.0

    return {
        "user_outcome": round(user_outcome, 2),
        "optimal_outcome": round(optimal_outcome, 2),
        "worst_outcome": round(worst_outcome, 2),
        "score": round(score, 4),
        "pl_delta": round(user_outcome - optimal_outcome, 2),
        "explanation": "Decision evaluated against the lesson's available optimal policy.",
    }
