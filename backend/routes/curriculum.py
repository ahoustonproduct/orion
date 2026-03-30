from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from curriculum_data import ALL_MODULES

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


@router.get("/modules")
def get_modules():
    """Return all modules with basic info (no full lesson content)."""
    return [
        {
            "id": m["id"],
            "title": m["title"],
            "description": m["description"],
            "course": m["course"],
            "order": m["order"],
            "locked": m["locked"],
            "lesson_count": len(m["lessons"]),
        }
        for m in ALL_MODULES
    ]


@router.get("/modules/{module_id}")
def get_module(module_id: str):
    """Return a module with all lesson summaries (no full content)."""
    module = next((m for m in ALL_MODULES if m["id"] == module_id), None)
    if not module:
        return {"error": "Module not found"}
    return {
        **module,
        "lessons": [
            {
                "id": l["id"],
                "title": l["title"],
                "order": l["order"],
                "duration_min": l["duration_min"],
            }
            for l in module["lessons"]
        ],
    }


@router.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: str):
    """Return full lesson content by ID."""
    for module in ALL_MODULES:
        for lesson in module["lessons"]:
            if lesson["id"] == lesson_id:
                return {**lesson, "module_title": module["title"]}
    return {"error": "Lesson not found"}


@router.get("/glossary")
def get_glossary():
    """Return all glossary terms."""
    try:
        from glossary_data import GLOSSARY
        return GLOSSARY
    except ImportError:
        return []


@router.get("/modules/{module_id}/export", response_class=PlainTextResponse)
def export_module_study_packet(module_id: str):
    """Generate a formatted markdown study packet for NotebookLM upload."""
    module = next((m for m in ALL_MODULES if m["id"] == module_id), None)
    if not module:
        return PlainTextResponse("Module not found", status_code=404)

    # Collect glossary terms that match this module's topic area
    try:
        from glossary_data import GLOSSARY
        # Map module ids to glossary module names
        module_glossary_map = {
            "module1": "Python",
            "module2": "Data Analytics",
            "module3": "SQL",
            "module4": "Machine Learning",
            "module5": "AI",
            "module6": "AI",
            "module7": "AI",
        }
        glossary_label = module_glossary_map.get(module_id, "")
        relevant_terms = [t for t in GLOSSARY if glossary_label and t.get("module", "") == glossary_label]
    except ImportError:
        relevant_terms = []

    lines = []

    # ── Header ──────────────────────────────────────────────────────
    lines.append(f"# {module['title']} — Study Packet")
    lines.append(f"**Course:** {module['course']}")
    lines.append(f"**Description:** {module['description']}")
    lines.append(f"**Total Lessons:** {len(module['lessons'])}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## How to Use This Packet")
    lines.append("Upload this file to [NotebookLM](https://notebooklm.google.com) to generate audio overviews,")
    lines.append("ask questions about the material, and create study guides.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Lessons ─────────────────────────────────────────────────────
    lines.append("## Lessons")
    lines.append("")

    for lesson in module["lessons"]:
        lines.append(f"### Lesson {lesson['order']}: {lesson['title']}")
        lines.append(f"*Estimated time: {lesson['duration_min']} minutes*")
        lines.append("")

        # Concept
        lines.append("#### Concept")
        lines.append(lesson.get("concept", ""))
        lines.append("")

        # Reference sheet
        ref = lesson.get("reference", {})
        if ref:
            lines.append("#### Quick Reference")
            key_syntax = ref.get("key_syntax", [])
            if key_syntax:
                lines.append("**Key Syntax:**")
                for s in key_syntax:
                    lines.append(f"- `{s}`")
            notes = ref.get("notes", "")
            if notes:
                lines.append(f"\n**Notes:** {notes}")
            lines.append("")

        # Challenge
        challenge = lesson.get("challenge", {})
        if challenge:
            lines.append("#### Coding Challenge")
            lines.append(challenge.get("instructions", ""))
            starter = challenge.get("starter_code", "").strip()
            if starter:
                lines.append("")
                lines.append("**Starter Code:**")
                lines.append("```python")
                lines.append(starter)
                lines.append("```")
            solution = challenge.get("solution", "").strip()
            if solution:
                lines.append("")
                lines.append("**Solution:**")
                lines.append("```python")
                lines.append(solution)
                lines.append("```")
            lines.append("")

        # Practice questions (written out for self-testing)
        questions = lesson.get("questions", [])
        if questions:
            lines.append("#### Self-Test Questions")
            for i, q in enumerate(questions, 1):
                qtype = q.get("type", "")
                lines.append(f"{i}. {q.get('question', '')}")
                if qtype == "multiple_choice":
                    for j, opt in enumerate(q.get("options", [])):
                        marker = "**→**" if j == q.get("answer") else "   "
                        lines.append(f"   {marker} {chr(65+j)}) {opt}")
                elif qtype == "true_false":
                    answer_str = "True" if q.get("answer") else "False"
                    lines.append(f"   *Answer: {answer_str}*")
                elif qtype == "fill_blank":
                    lines.append(f"   Template: `{q.get('template', '')}`")
                    lines.append(f"   *Answer: `{q.get('answer', '')}`*")
                explanation = q.get("explanation", "")
                if explanation:
                    lines.append(f"   *Explanation: {explanation}*")
                lines.append("")

        lines.append("---")
        lines.append("")

    # ── Glossary ─────────────────────────────────────────────────────
    if relevant_terms:
        lines.append("## Key Terms & Definitions")
        lines.append("")
        for term in relevant_terms:
            lines.append(f"**{term['term']}**")
            lines.append(f": {term['definition']}")
            lines.append("")

    content = "\n".join(lines)
    filename = f"orion-study-packet-{module_id}.md"
    return PlainTextResponse(
        content,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
