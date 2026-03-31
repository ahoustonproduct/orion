from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import sqlite3
import time
import os
import re

router = APIRouter(prefix="/execute", tags=["execute"])

BLOCKED_PATTERNS: list[str] = [
    r"\bimport\s+os\b",
    r"\bimport\s+sys\b",
    r"\bimport\s+subprocess\b",
    r"\bimport\s+socket\b",
    r"\bimport\s+shutil\b",
    r"\bimport\s+pathlib\b",
    r"\bimport\s+importlib\b",
    r"\b__import__\s*\(",
    r"\bopen\s*\(",
    r"\bexec\s*\(",
    r"\beval\s*\(",
    r"\bcompile\s*\(",
    r"\bgetattr\s*\(",
    r"\bsetattr\s*\(",
    r"\bdelattr\s*\(",
    r"\bglobals\s*\(",
    r"\blocals\s*\(",
    r"\bvars\s*\(",
    r"\b__builtins__\b",
    r"\b__class__\b",
    r"\b__subclasses__\b",
]

_COMPILED_PATTERNS = [re.compile(p) for p in BLOCKED_PATTERNS]


def _is_unsafe(code: str) -> tuple[bool, str]:
    for pattern_re, pattern_src in zip(_COMPILED_PATTERNS, BLOCKED_PATTERNS):
        if pattern_re.search(code):
            return True, pattern_src
    return False, ""


class ExecutePythonRequest(BaseModel):
    code: str


class ExecuteSQLRequest(BaseModel):
    query: str


@router.post("/python")
def execute_python(req: ExecutePythonRequest) -> dict:
    code = req.code
    unsafe, matched = _is_unsafe(code)
    if unsafe:
        return {
            "output": "",
            "error": f"Blocked: unsafe pattern detected — {matched}",
            "duration_ms": 0,
        }
    start = time.monotonic()
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=5,
        )
        duration_ms = int((time.monotonic() - start) * 1000)
        return {
            "output": result.stdout[:5000],
            "error": result.stderr[:2000] if result.returncode != 0 else None,
            "duration_ms": duration_ms,
        }
    except subprocess.TimeoutExpired:
        return {
            "output": "",
            "error": "Execution timed out (5 s limit)",
            "duration_ms": 5000,
        }
    except Exception as exc:
        return {
            "output": "",
            "error": str(exc),
            "duration_ms": 0,
        }


@router.post("/sql")
def execute_sql(req: ExecuteSQLRequest) -> dict:
    query = req.query.strip()
    if not re.match(r"^\s*SELECT\b", query, re.IGNORECASE):
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "duration_ms": 0,
            "error": "Only SELECT queries are allowed",
        }
    if ";" in query:
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "duration_ms": 0,
            "error": "Semicolons are not allowed — only single SELECT queries permitted",
        }
    forbidden = re.search(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC|PRAGMA|ATTACH|DETACH)\b", query, re.IGNORECASE)
    if forbidden:
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "duration_ms": 0,
            "error": f"Keyword '{forbidden.group(1)}' is not allowed",
        }
    start = time.monotonic()
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "orion.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(query)
        rows = cursor.fetchmany(500)
        columns = [d[0] for d in cursor.description] if cursor.description else []
        duration_ms = int((time.monotonic() - start) * 1000)
        conn.close()
        return {
            "columns": columns,
            "rows": [list(r) for r in rows],
            "row_count": len(rows),
            "duration_ms": duration_ms,
            "error": None,
        }
    except Exception as exc:
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "duration_ms": 0,
            "error": str(exc),
        }
