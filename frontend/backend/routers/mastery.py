"""
routers/mastery.py — Concept mastery tracking endpoints.

GET  /mastery/{user_key}          → mastery scores per concept tag
POST /mastery/{user_key}/record   → record a correct/incorrect attempt
"""

from fastapi import APIRouter
from db import get_db
from models import RecordMasteryRequest
from datetime import datetime

router = APIRouter(tags=["mastery"])


# ---------------------------------------------------------------------------
# GET /mastery/{user_key}
# ---------------------------------------------------------------------------

@router.get("/{user_key}")
def get_mastery(user_key: str) -> dict:
    """
    Return per-concept mastery scores with recency-weighted decay (γ = 0.9).

    Most recent attempt counts most; older attempts decay exponentially.
    """
    with get_db() as conn:
        events = conn.execute(
            """SELECT concept_tag, correct, recorded_at
               FROM mastery_events
               WHERE user_key = ?
               ORDER BY recorded_at DESC""",
            (user_key,),
        ).fetchall()

    # Group events by concept_tag (already sorted newest-first)
    tag_events: dict[str, list[int]] = {}
    for e in events:
        tag = e["concept_tag"]
        if tag not in tag_events:
            tag_events[tag] = []
        tag_events[tag].append(int(e["correct"]))

    DECAY = 0.9

    # Compute weighted mastery per tag
    tag_mastery: dict[str, float] = {}
    for tag, corrects in tag_events.items():
        weighted_correct = sum(c * (DECAY ** i) for i, c in enumerate(corrects))
        weighted_total   = sum(DECAY ** i for i in range(len(corrects)))
        mastery = (weighted_correct / weighted_total * 100) if weighted_total > 0 else 0.0
        tag_mastery[tag] = round(mastery, 1)

    # Focus areas: up to 3 weakest concepts (mastery < 70 %)
    focus_areas = sorted(
        [(tag, score) for tag, score in tag_mastery.items() if score < 70],
        key=lambda x: x[1],
    )[:3]

    # Heatmap data sorted weakest-first
    heatmap_data = sorted(
        [
            {
                "tag":      tag,
                "mastery":  score,
                "attempts": len(tag_events[tag]),
            }
            for tag, score in tag_mastery.items()
        ],
        key=lambda x: x["mastery"],
    )

    return {
        "tags":        tag_mastery,
        "focus_areas": [{"tag": t, "mastery": s} for t, s in focus_areas],
        "heatmap_data": heatmap_data,
    }


# ---------------------------------------------------------------------------
# POST /mastery/{user_key}/record
# ---------------------------------------------------------------------------

@router.post("/{user_key}/record")
def record_mastery(user_key: str, req: RecordMasteryRequest) -> dict:
    """Record a single correct/incorrect mastery event for a concept tag."""
    now = datetime.utcnow().isoformat()
    with get_db() as conn:
        conn.execute(
            """INSERT INTO mastery_events (user_key, concept_tag, correct, recorded_at)
               VALUES (?, ?, ?, ?)""",
            (user_key, req.concept_tag, 1 if req.correct else 0, now),
        )
        conn.commit()
    return {"ok": True}
