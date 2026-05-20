from typing import Iterator

from sqlalchemy.orm import Session

from curriculum_data import ALL_MODULES
from models import Notebook


def iter_builtin_lessons() -> Iterator[tuple[dict, dict, int]]:
    for module in ALL_MODULES:
        for index, lesson in enumerate(module.get("lessons", []), 1):
            yield module, lesson, index


def notebook_id_from_lesson_id(lesson_id: str) -> str:
    if "-l" in lesson_id:
        return lesson_id.rsplit("-l", 1)[0]
    return lesson_id


def get_ready_notebooks(db: Session, user_key: str) -> list[Notebook]:
    return (
        db.query(Notebook)
        .filter(Notebook.user_key == user_key, Notebook.status == "ready")
        .all()
    )


def iter_notebook_lessons(db: Session, user_key: str) -> Iterator[tuple[dict, dict, int]]:
    for notebook in get_ready_notebooks(db, user_key):
        module_data = notebook.module_data or {}
        module = {
            "id": notebook.id,
            "title": module_data.get("title", notebook.title or "Untitled Notebook"),
            "course": module_data.get("course", "Saved Module"),
            "order": module_data.get("order", 99),
            "locked": False,
        }
        for index, lesson in enumerate(module_data.get("lessons") or [], 1):
            yield module, lesson, index


def lesson_map_for_user(db: Session, user_key: str) -> dict[str, dict]:
    lessons: dict[str, dict] = {}
    for module, lesson, _ in iter_builtin_lessons():
        lessons[lesson["id"]] = {**lesson, "module_title": module["title"], "module_id": module["id"]}
    for module, lesson, _ in iter_notebook_lessons(db, user_key):
        lesson_id = lesson.get("id")
        if lesson_id:
            lessons[lesson_id] = {**lesson, "module_title": module["title"], "module_id": module["id"]}
    return lessons


def resolve_lesson(
    lesson_id: str,
    db: Session | None = None,
    user_key: str | None = None,
) -> tuple[dict, dict, int] | None:
    for module, lesson, index in iter_builtin_lessons():
        if lesson["id"] == lesson_id:
            return module, lesson, index

    if db is None or not lesson_id.startswith("notebook_") or not user_key:
        return None

    notebook_id = notebook_id_from_lesson_id(lesson_id)
    query = db.query(Notebook).filter(
        Notebook.id == notebook_id,
        Notebook.user_key == user_key,
        Notebook.status == "ready",
    )
    notebook = query.first()
    if not notebook or not notebook.module_data:
        return None

    module = {
        "id": notebook.id,
        "title": notebook.module_data.get("title", notebook.title or "Untitled Notebook"),
        "course": notebook.module_data.get("course", "Saved Module"),
        "order": notebook.module_data.get("order", 99),
        "locked": False,
    }
    for index, lesson in enumerate(notebook.module_data.get("lessons") or [], 1):
        if lesson.get("id") == lesson_id:
            return module, lesson, index

    return None
