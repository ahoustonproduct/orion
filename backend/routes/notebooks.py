"""
Notebook routes for saved study modules.

Core Orion does not create notebooks in-app. Notebooks are persisted modules
that were imported or created outside the running application, then rendered
through the same lesson experience as built-in curriculum modules.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import get_db, Notebook
from routes.curriculum import normalize_lesson


router = APIRouter(prefix="/notebooks", tags=["notebooks"])


def notebook_summary(row: Notebook) -> dict:
    module_data = row.module_data or {}
    lessons = module_data.get("lessons") or []
    is_ready = row.status == "ready" and bool(lessons)
    return {
        "id": row.id,
        "title": row.title or module_data.get("title") or "Untitled Notebook",
        "status": "ready" if is_ready else "failed",
        "error": "" if is_ready else row.error or "Saved module has no lessons.",
        "source_type": row.source_type or "",
        "source_url": row.source_url or "",
        "lesson_count": len(lessons),
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }


@router.get("/{user_key}")
def list_notebooks(user_key: str, db: Session = Depends(get_db)):
    """List all saved notebook modules for a user."""
    rows = (
        db.query(Notebook)
        .filter(Notebook.user_key == user_key)
        .order_by(Notebook.created_at.desc())
        .all()
    )
    return [notebook_summary(row) for row in rows]


@router.get("/{user_key}/{notebook_id}")
def get_notebook(user_key: str, notebook_id: str, db: Session = Depends(get_db)):
    """Return a saved notebook module, including its lessons."""
    notebook = (
        db.query(Notebook)
        .filter(Notebook.id == notebook_id, Notebook.user_key == user_key)
        .first()
    )
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    return {
        **notebook_summary(notebook),
        "module_data": notebook.module_data or {},
    }


@router.get("/{user_key}/{notebook_id}/lesson/{lesson_id}")
def get_notebook_lesson(
    user_key: str,
    notebook_id: str,
    lesson_id: str,
    db: Session = Depends(get_db),
):
    """Return one lesson from a saved notebook module."""
    notebook = (
        db.query(Notebook)
        .filter(Notebook.id == notebook_id, Notebook.user_key == user_key)
        .first()
    )
    if not notebook or not notebook.module_data:
        raise HTTPException(status_code=404, detail="Notebook not found")

    module = {"title": notebook.module_data.get("title", notebook.title)}
    for index, lesson in enumerate(notebook.module_data.get("lessons") or [], 1):
        if lesson.get("id") == lesson_id:
            return normalize_lesson(module, lesson, index)

    raise HTTPException(status_code=404, detail="Lesson not found in notebook")


@router.delete("/{user_key}/{notebook_id}")
def delete_notebook(user_key: str, notebook_id: str, db: Session = Depends(get_db)):
    notebook = (
        db.query(Notebook)
        .filter(Notebook.id == notebook_id, Notebook.user_key == user_key)
        .first()
    )
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    db.delete(notebook)
    db.commit()
    return {"ok": True}
