from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import sqlite3
import time
import os
import re
import sys
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/execute", tags=["execute"])

# Data science libraries that users may import in the sandbox.
# These are PRE-INSTALLED via backend/requirements.txt. There is deliberately
# no install-on-demand path — that would (a) add 10–30 s of per-request latency,
# (b) create an attack surface through pip, and (c) silently drift the sandbox.
ALLOWED_DATA_SCIENCE_IMPORTS = {
    "pandas", "numpy", "scipy", "sklearn", "matplotlib", "seaborn",
    "statistics", "math", "json", "random", "datetime", "re",
}

# Security patterns that are never allowed
BLOCKED_PATTERNS: list[str] = [
    r"\bimport\s+os\b",
    r"\bimport\s+sys\b",
    r"\bimport\s+subprocess\b",
    r"\bimport\s+socket\b",
    r"\bimport\s+shutil\b",
    r"\bimport\s+pathlib\b",
    r"\bimport\s+importlib\b",
    r"\bimport\s+ctypes\b",
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


# Only .py filenames with no path components are acceptable in /execute/multi.
_SAFE_FILENAME_RE = re.compile(r"^[A-Za-z0-9_\-.]+\.(py|txt)$")


def _safe_filename(name: str) -> str | None:
    """Return a safe basename, or None if the name is unacceptable."""
    if not name:
        return None
    base = os.path.basename(name)
    if base != name:
        # Caller supplied a path component — reject.
        return None
    if not _SAFE_FILENAME_RE.match(base):
        return None
    return base


class ExecutePythonRequest(BaseModel):
    code: str


class ExecuteMultiFileRequest(BaseModel):
    files: list[dict[str, str]]  # [{"name": "main.py", "content": "..."}]


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

    # Run user code directly. Allowed libs are pre-installed via requirements.txt;
    # if a user imports something not installed, they'll get a clean ImportError
    # in stderr, which is the correct pedagogical signal.
    start = time.monotonic()
    try:
        result = subprocess.run(
            [sys.executable, "-I", "-c", code],  # -I: isolate from user site-packages/env
            capture_output=True,
            text=True,
            timeout=15,
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
            "error": "Execution timed out (15 s limit)",
            "duration_ms": 15000,
        }
    except Exception as exc:
        logger.error(f"Python execution error: {exc}", exc_info=True)
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
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sandbox.db")
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
    except sqlite3.Error as exc:
        logger.info("SQL query failed in sandbox: %s", exc)
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "duration_ms": 0,
            "error": str(exc),
        }
    except Exception as exc:
        logger.error(f"SQL execution error: {exc}", exc_info=True)
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "duration_ms": 0,
            "error": str(exc),
        }


@router.post("/multi")
def execute_multi(req: ExecuteMultiFileRequest) -> dict:
    """Execute a multi-file Python program. Runs the first .py file found."""
    files = req.files
    if not files:
        return {"error": "No files provided", "outputs": {}}

    import tempfile
    import shutil

    # Validate every filename BEFORE touching the filesystem. Reject path-traversal,
    # absolute paths, and non-.py/.txt files.
    sanitized: list[tuple[str, str]] = []
    for file in files:
        raw_name = file.get("name", "")
        safe = _safe_filename(raw_name)
        if safe is None:
            return {
                "error": f"Invalid filename: {raw_name!r}. "
                         "Names must be simple basenames ending in .py or .txt.",
                "outputs": {},
            }
        sanitized.append((safe, file.get("content", "")))

    # Scan every file for unsafe patterns BEFORE writing anything.
    for name, content in sanitized:
        unsafe, matched = _is_unsafe(content)
        if unsafe:
            return {
                "error": f"Unsafe pattern in {name}: {matched}",
                "outputs": {},
            }

    temp_dir = tempfile.mkdtemp(prefix="orion_exec_")
    try:
        sandbox_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sandbox.db")
        if os.path.exists(sandbox_path):
            shutil.copy2(sandbox_path, os.path.join(temp_dir, "sandbox.db"))

        for name, content in sanitized:
            file_path = os.path.join(temp_dir, name)
            # Belt-and-suspenders: make sure the resolved path is still inside temp_dir.
            if os.path.commonpath([os.path.realpath(file_path), os.path.realpath(temp_dir)]) != os.path.realpath(temp_dir):
                return {"error": f"Refusing to write outside sandbox: {name}", "outputs": {}}
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

        main_name = next((n for n, _ in sanitized if n.endswith(".py")), sanitized[0][0])
        main_path = os.path.join(temp_dir, main_name)

        start = time.monotonic()
        result = subprocess.run(
            [sys.executable, "-I", main_path],
            capture_output=True,
            text=True,
            timeout=20,
            cwd=temp_dir,
        )
        duration_ms = int((time.monotonic() - start) * 1000)

        outputs = {
            "main": result.stdout[:5000],
            "all_files": [n for n, _ in sanitized],
        }
        errors = {"main": result.stderr[:2000]} if result.returncode != 0 else None

        return {
            "outputs": outputs,
            "errors": errors,
            "duration_ms": duration_ms,
        }

    except subprocess.TimeoutExpired:
        return {
            "error": "Execution timed out (20 s limit)",
            "outputs": {},
            "duration_ms": 20000,
        }
    except Exception as exc:
        logger.error(f"Multi-file execution error: {exc}", exc_info=True)
        return {
            "error": str(exc),
            "outputs": {},
            "duration_ms": 0,
        }
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
