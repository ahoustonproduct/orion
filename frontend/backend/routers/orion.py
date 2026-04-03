"""
routers/orion.py — All Orion AI streaming endpoints.

Every endpoint returns a StreamingResponse (text/plain, chunked) so the
frontend can display tokens as they arrive from Claude.
"""

import os
import anthropic
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from models import (
    OrionExplainRequest,
    OrionFeedbackRequest,
    OrionHintRequest,
    OrionRecapRequest,
    OrionChallengeRequest,
    OrionDecisionRequest,
    OrionWhatNextRequest,
    OrionStudyPlanRequest,
    OrionWeekReviewRequest,
    OrionExplainAnswerRequest,
    OrionEvaluateDecisionRequest,
    OrionChatRequest,
)

router = APIRouter(tags=["orion"])

# ---------------------------------------------------------------------------
# Anthropic client (lazy init so missing key doesn't crash at import time)
# ---------------------------------------------------------------------------

def _get_client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")
    return anthropic.Anthropic(api_key=api_key)


# Base persona injected into every request
_BASE_SYSTEM = (
    "You are Orion, an expert FinTech analytics tutor. "
    "You help students prepare for the WashU MS Business Analytics & AI program. "
    "Be direct, specific, and always connect technical concepts to real FinTech business decisions. "
    "Reference real companies where relevant (Stripe, Affirm, JPMorgan, Chime, Square, Plaid, etc.). "
    "Use plain language — your student has zero prior coding experience but strong business intuition. "
    "Keep responses focused and actionable."
)

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024


# ---------------------------------------------------------------------------
# Core streaming helper
# ---------------------------------------------------------------------------

def _stream(messages: list[dict], system: str = _BASE_SYSTEM, max_tokens: int = MAX_TOKENS) -> StreamingResponse:
    """Return a StreamingResponse that yields raw text tokens from Claude."""

    def _generate():
        client = _get_client()
        try:
            with client.messages.stream(
                model=MODEL,
                max_tokens=max_tokens,
                system=system,
                messages=messages,
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except anthropic.APIError as exc:
            yield f"\n\n[Orion error: {exc}]"
        except RuntimeError as exc:
            yield f"\n\n[Configuration error: {exc}]"

    return StreamingResponse(_generate(), media_type="text/plain")


# ---------------------------------------------------------------------------
# /explain
# ---------------------------------------------------------------------------

@router.post("/explain")
def explain(req: OrionExplainRequest) -> StreamingResponse:
    """Explain a lesson concept in plain English with FinTech context."""
    user_msg = (
        f"Lesson: {req.lesson_id}\n"
        f"Concept to explain: {req.concept}\n"
    )
    if req.context:
        user_msg += f"Additional context: {req.context}\n"
    user_msg += (
        "\nPlease explain this concept clearly, using a real-world FinTech analogy. "
        "Start with the intuition, then give a concrete example, then explain why it matters "
        "for data analysts at companies like Stripe or Chime."
    )
    return _stream([{"role": "user", "content": user_msg}])


# ---------------------------------------------------------------------------
# /feedback
# ---------------------------------------------------------------------------

@router.post("/feedback")
def feedback(req: OrionFeedbackRequest) -> StreamingResponse:
    """Give structured feedback on the student's code."""
    user_msg = (
        f"Lesson: {req.lesson_id}\n"
        f"Student's code:\n```python\n{req.code}\n```\n"
    )
    if req.expected:
        user_msg += f"Expected outcome / goal: {req.expected}\n"
    user_msg += (
        "\nProvide feedback in this order:\n"
        "1. What they got right\n"
        "2. Any bugs or issues (be specific about the line)\n"
        "3. A business-context note — how does this code relate to a real FinTech decision?\n"
        "4. One concrete improvement suggestion\n"
        "Be encouraging but honest."
    )
    return _stream([{"role": "user", "content": user_msg}])


# ---------------------------------------------------------------------------
# /hint
# ---------------------------------------------------------------------------

@router.post("/hint")
def hint(req: OrionHintRequest) -> StreamingResponse:
    """Provide a progressive hint (1 = vague, 2 = moderate, 3 = near-answer)."""
    verbosity = {1: "very vague — just a nudge in the right direction, no code",
                 2: "moderate — explain the approach without giving the exact solution",
                 3: "detailed — show the structure or a near-complete example"}
    level_desc = verbosity.get(req.hint_number, verbosity[2])

    user_msg = (
        f"Lesson: {req.lesson_id}\n"
        f"Hint level requested: {req.hint_number}/3 ({level_desc})\n"
    )
    if req.context:
        user_msg += f"What the student is stuck on: {req.context}\n"
    user_msg += f"\nProvide a hint that is {level_desc}. Tie it to the FinTech use case."

    return _stream([{"role": "user", "content": user_msg}])


# ---------------------------------------------------------------------------
# /recap
# ---------------------------------------------------------------------------

@router.post("/recap")
def recap(req: OrionRecapRequest) -> StreamingResponse:
    """Summarise what was learned in a lesson."""
    steps_text = ""
    if req.completed_steps:
        steps_text = "Completed steps:\n" + "\n".join(f"- {s}" for s in req.completed_steps) + "\n"

    user_msg = (
        f"Lesson: {req.lesson_id}\n"
        f"{steps_text}"
        "\nWrite a brief recap (3–5 bullet points) of what the student learned. "
        "For each point, include the Python/data concept AND its FinTech application. "
        "End with one 'key takeaway' sentence they can share in an interview."
    )
    return _stream([{"role": "user", "content": user_msg}])


# ---------------------------------------------------------------------------
# /generate-challenge
# ---------------------------------------------------------------------------

@router.post("/generate-challenge")
def generate_challenge(req: OrionChallengeRequest) -> StreamingResponse:
    """Generate a harder, novel exercise variant."""
    difficulty_map = {
        "easy":   "slightly simpler than the original, good for reinforcement",
        "medium": "comparable difficulty but a different business scenario",
        "hard":   "significantly harder — multi-step problem, realistic messy data",
    }
    diff_desc = difficulty_map.get(req.difficulty, difficulty_map["medium"])

    user_msg = (
        f"Lesson: {req.lesson_id}\n"
        f"Concept: {req.concept}\n"
        f"Difficulty: {req.difficulty} ({diff_desc})\n"
        "\nGenerate a new coding challenge. Format your response as:\n"
        "**Scenario:** (2–3 sentence FinTech business context)\n"
        "**Task:** (what the student must do)\n"
        "**Starter code:**\n```python\n# starter code here\n```\n"
        "**Expected output:** (describe or show)\n"
        "**Hint:** (one subtle pointer)\n"
    )
    return _stream([{"role": "user", "content": user_msg}], max_tokens=1500)


# ---------------------------------------------------------------------------
# /explain-your-answer
# ---------------------------------------------------------------------------

@router.post("/explain-your-answer")
def explain_your_answer(req: OrionExplainAnswerRequest) -> StreamingResponse:
    """Help the student understand the reasoning behind a correct answer."""
    user_msg = (
        f"Lesson: {req.lesson_id}\n"
        f"Question: {req.question}\n"
        f"Student's answer: {req.user_answer}\n"
        f"Correct answer: {req.correct_answer}\n"
        "\nExplain WHY the correct answer is right. "
        "If the student was wrong, be empathetic and explain the common misconception. "
        "Connect the reasoning to a real FinTech scenario to make it memorable."
    )
    return _stream([{"role": "user", "content": user_msg}])


# ---------------------------------------------------------------------------
# /study-plan
# ---------------------------------------------------------------------------

@router.post("/study-plan")
def study_plan(req: OrionStudyPlanRequest) -> StreamingResponse:
    """Create a personalised study plan based on weak topics and goals."""
    weak_text = ", ".join(req.weak_topics) if req.weak_topics else "not specified"
    user_msg = (
        f"Student: {req.user_key}\n"
        f"Weak topics: {weak_text}\n"
        f"Goals: {req.goals or 'Prepare for MS Business Analytics & AI at WashU (starting June 2026)'}\n"
        "\nCreate a structured 2-week study plan. Format it as:\n"
        "**Week 1** — focus area + specific lessons/topics + daily time estimate\n"
        "**Week 2** — continuation + stretch topics\n"
        "**Key milestones** — measurable checkpoints\n"
        "Be realistic — the student has business experience but no coding background."
    )
    return _stream([{"role": "user", "content": user_msg}], max_tokens=1500)


# ---------------------------------------------------------------------------
# /week-review
# ---------------------------------------------------------------------------

@router.post("/week-review")
def week_review(req: OrionWeekReviewRequest) -> StreamingResponse:
    """Generate a weekly AI summary of the student's learning activity."""
    data_text = ""
    if req.week_data:
        data_text = f"Week data:\n{req.week_data}\n"

    user_msg = (
        f"Student: {req.user_key}\n"
        f"{data_text}"
        "\nWrite an encouraging weekly learning review. Include:\n"
        "1. **What you accomplished** — highlight lessons completed and concepts mastered\n"
        "2. **Patterns noticed** — any gaps or topics that need more practice\n"
        "3. **This week's FinTech insight** — one real-world connection to what they studied\n"
        "4. **Next week's focus** — 2–3 specific recommendations\n"
        "Tone: coach-like, honest, motivating."
    )
    return _stream([{"role": "user", "content": user_msg}], max_tokens=1200)


# ---------------------------------------------------------------------------
# /what-next
# ---------------------------------------------------------------------------

@router.post("/what-next")
def what_next(req: OrionWhatNextRequest) -> StreamingResponse:
    """Recommend the next best lesson or topic to study."""
    progress_text = ""
    if req.progress:
        completed = [k for k, v in req.progress.items() if v.get("completed")]
        progress_text = f"Completed lessons: {', '.join(completed) or 'none yet'}\n"

    user_msg = (
        f"Student: {req.user_key}\n"
        f"{progress_text}"
        "\nBased on the student's progress, recommend the single best next step. "
        "Format: **Recommended:** [lesson/topic name]\n**Why:** (2–3 sentences on why this is the right next step)\n"
        "**What you'll be able to do after:** (concrete skill outcome)\n"
        "Keep it brief and motivating."
    )
    return _stream([{"role": "user", "content": user_msg}])


# ---------------------------------------------------------------------------
# /evaluate-decision
# ---------------------------------------------------------------------------

@router.post("/evaluate-decision")
def evaluate_decision(req: OrionEvaluateDecisionRequest) -> StreamingResponse:
    """Evaluate a written justification for a business decision exercise."""
    user_msg = (
        f"Lesson: {req.lesson_id}\n"
        f"Scenario: {req.scenario or '(see lesson context)'}\n"
        f"Student's decision value: {req.decision_value}\n"
        f"Student's written justification:\n{req.justification}\n"
        "\nEvaluate the quality of this justification. Score it on:\n"
        "1. **Business reasoning** (1–5): Does it reference risk, revenue, or customer impact?\n"
        "2. **Data intuition** (1–5): Does it show understanding of the underlying data/model?\n"
        "3. **Clarity** (1–5): Is it well-articulated?\n"
        "Then provide 2–3 sentences of specific, constructive feedback. "
        "Reference what a real FinTech analyst at a company like Affirm or Chime would consider."
    )
    return _stream([{"role": "user", "content": user_msg}])


# ---------------------------------------------------------------------------
# /chat — Interactive mid-lesson Q&A
# ---------------------------------------------------------------------------

@router.post("/chat")
def chat(req: OrionChatRequest) -> StreamingResponse:
    """Interactive AI chat for mid-lesson questions."""
    messages: list[dict] = []

    # Reconstruct conversation history
    for msg in req.chat_history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    # Build the new user message with context
    context_parts = [f"The student is working on lesson: {req.lesson_title or req.lesson_id}."]
    if req.current_code:
        context_parts.append(f"Their current code:\n```python\n{req.current_code}\n```")
    context_parts.append(f"\nStudent question: {req.user_message}")

    messages.append({"role": "user", "content": "\n".join(context_parts)})

    return _stream(messages, max_tokens=800)
