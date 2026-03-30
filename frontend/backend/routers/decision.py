"""
routers/decision.py — Business decision evaluation endpoints.

Loads lesson JSON to find a decision_block, computes outcomes using a
registry of named outcome functions, and returns a scored evaluation.
"""

from fastapi import APIRouter, HTTPException
from models import DecisionEvaluateRequest
import json
import math
import os

router = APIRouter(tags=["decision"])

LESSONS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "curriculum_data", "lessons"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_lesson(lesson_id: str) -> dict:
    """Find and load a lesson JSON by ID. Raises HTTPException if not found."""
    if not os.path.exists(LESSONS_DIR):
        raise HTTPException(status_code=404, detail="Lessons directory not found")

    for fname in os.listdir(LESSONS_DIR):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(LESSONS_DIR, fname)
        try:
            with open(fpath, encoding="utf-8") as f:
                lesson = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        if lesson.get("id") == lesson_id:
            return lesson

    raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")


def _find_decision_block(lesson: dict, block_id: str | None = None) -> dict:
    """Return the first decision_block in a lesson, or the one matching block_id."""
    for block in lesson.get("blocks", []):
        if block.get("type") == "decision_block":
            if block_id is None or block.get("id") == block_id:
                return block
    raise HTTPException(status_code=404, detail="No matching decision_block in this lesson")


# ---------------------------------------------------------------------------
# Outcome function registry
# ---------------------------------------------------------------------------

def _credit_threshold_pl(value) -> float:
    """
    Simulate monthly P&L for a credit approval threshold (FICO-style score).

    Higher threshold → fewer approvals but lower default rate.
    Returns expected monthly profit in USD assuming 1 000 applications/month.
    """
    score = float(value) if value is not None else 640.0
    approval_rate  = 1 / (1 + math.exp(0.015 * (score - 650)))
    default_rate   = 1 / (1 + math.exp(0.02  * (score - 500)))
    monthly_interest = 1000 * 0.22 / 12          # $1 000 loan at 22 % APR
    profit_per_approval = (1 - default_rate) * monthly_interest - default_rate * 1000
    monthly_profit = approval_rate * 1000 * profit_per_approval
    return round(monthly_profit, 2)


def _fraud_threshold_pl(value) -> float:
    """
    Simulate monthly net revenue for a fraud detection threshold (0–1).

    Higher threshold → stricter fraud blocking, lower fraud loss but also
    lower conversion (more false positives block legitimate transactions).
    """
    threshold        = float(value) if value is not None else 0.5
    base_conversion  = 0.85
    fraud_rate_base  = 0.003
    conversion       = base_conversion * (1 - 0.3 * threshold)
    fraud_rate       = fraud_rate_base * (1 - 0.8 * threshold)
    monthly_txns     = 50_000
    avg_txn          = 100
    revenue          = conversion * monthly_txns * avg_txn * 0.015  # 1.5 % take rate
    fraud_loss       = fraud_rate * monthly_txns * avg_txn
    return round(revenue - fraud_loss, 2)


def _compute_outcome(function_name: str, value, lesson: dict) -> float:
    """Dispatch to the named outcome function, with a sensible default."""
    if function_name == "credit_threshold_pl":
        return _credit_threshold_pl(value)
    if function_name == "fraud_threshold_pl":
        return _fraud_threshold_pl(value)

    # Generic fallback: penalise distance from the optimal value
    blocks = lesson.get("blocks", [])
    optimal = None
    for block in blocks:
        if block.get("type") == "decision_block":
            optimal = block.get("optimal_value")
            break

    try:
        return -abs(float(value) - float(optimal)) if optimal is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


# ---------------------------------------------------------------------------
# POST /decision/evaluate
# ---------------------------------------------------------------------------

@router.post("/evaluate")
def evaluate_decision(req: DecisionEvaluateRequest) -> dict:
    lesson = _load_lesson(req.lesson_id)
    block  = _find_decision_block(lesson, req.block_id or None)

    optimal = block.get("optimal_value")
    worst   = block.get("worst_value")
    fn_name = block.get("outcome_function", "")

    user_outcome    = _compute_outcome(fn_name, req.user_value, lesson)
    optimal_outcome = _compute_outcome(fn_name, optimal,       lesson)
    worst_outcome   = _compute_outcome(fn_name, worst,         lesson)

    outcome_range = abs(optimal_outcome - worst_outcome)
    if outcome_range == 0:
        score = 1.0
    else:
        score = max(0.0, min(1.0,
            1.0 - abs(user_outcome - optimal_outcome) / outcome_range
        ))

    pl_delta = round(user_outcome - optimal_outcome, 2)

    return {
        "user_outcome":    user_outcome,
        "optimal_outcome": optimal_outcome,
        "worst_outcome":   worst_outcome,
        "score":           round(score, 3),
        "pl_delta":        pl_delta,
        "explanation":     block.get(
            "outcome_explanation",
            f"Optimal choice: {optimal}. Your choice: {req.user_value}."
        ),
    }
