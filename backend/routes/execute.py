from fastapi import APIRouter, Request
from pydantic import BaseModel
from urllib.parse import urlparse
import ast
import logging
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/execute", tags=["execute"])

# Pre-installed libraries that are acceptable for Orion's local learning sandbox.
# Keep this list narrow: the executor is for lessons, not general scripting.
ALLOWED_DATA_SCIENCE_IMPORTS = {
    "datetime",
    "json",
    "math",
    "matplotlib",
    "numpy",
    "pandas",
    "random",
    "re",
    "scipy",
    "seaborn",
    "sklearn",
    "statistics",
}

BLOCKED_IMPORT_ROOTS = {
    "builtins",
    "ctypes",
    "http",
    "importlib",
    "io",
    "marshal",
    "os",
    "pathlib",
    "pickle",
    "requests",
    "shutil",
    "socket",
    "subprocess",
    "sys",
    "tempfile",
    "urllib",
}

BLOCKED_IMPORT_PARTS = BLOCKED_IMPORT_ROOTS | {"popen2"}

BLOCKED_CALL_NAMES = {
    "__import__",
    "breakpoint",
    "compile",
    "delattr",
    "dir",
    "eval",
    "exec",
    "getattr",
    "globals",
    "help",
    "input",
    "locals",
    "memoryview",
    "open",
    "setattr",
    "vars",
}

BLOCKED_ATTRIBUTE_NAMES = {
    "connect",
    "exec",
    "execfile",
    "load",
    "loadtxt",
    "open",
    "popen",
    "read",
    "read_clipboard",
    "read_csv",
    "read_excel",
    "read_feather",
    "read_fwf",
    "read_html",
    "read_json",
    "read_orc",
    "read_parquet",
    "read_pickle",
    "read_sas",
    "read_spss",
    "read_sql",
    "read_stata",
    "read_table",
    "read_xml",
    "recv",
    "run",
    "save",
    "savefig",
    "savetxt",
    "savez",
    "savez_compressed",
    "send",
    "spawn",
    "system",
    "to_clipboard",
    "to_csv",
    "to_excel",
    "to_feather",
    "to_json",
    "to_orc",
    "to_parquet",
    "to_pickle",
    "to_sql",
    "to_stata",
}

LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost", "testclient"}

# Only .py filenames with no path components are acceptable in /execute/multi.
_SAFE_FILENAME_RE = re.compile(r"^[A-Za-z0-9_\-.]+\.(py|txt)$")


class ExecutePythonRequest(BaseModel):
    code: str


class ExecuteMultiFileRequest(BaseModel):
    files: list[dict[str, str]]  # [{"name": "main.py", "content": "..."}]


class ExecuteSQLRequest(BaseModel):
    query: str


def _normalize_host(raw: str) -> str:
    value = raw.strip()
    if not value:
        return ""
    if "://" in value:
        value = urlparse(value).hostname or ""
    elif value.startswith("[") and "]" in value:
        value = value[1:value.index("]")]
    elif ":" in value:
        value = value.split(":", 1)[0]
    return value.lower()


def _is_loopback_host(raw: str) -> bool:
    return _normalize_host(raw) in LOOPBACK_HOSTS


def _remote_execution_allowed(request: Request) -> bool:
    if os.getenv("ORION_ALLOW_REMOTE_EXECUTION") == "1":
        return True

    host_values = [request.client.host if request.client else ""]
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        host_values.append(forwarded_for.split(",", 1)[0])
    host_values.append(request.headers.get("x-real-ip", ""))

    for value in host_values:
        if value and not _is_loopback_host(value):
            return False

    for header in ("origin", "referer", "x-forwarded-host"):
        value = request.headers.get(header, "")
        if value and not _is_loopback_host(value):
            return False

    non_empty_hosts = [value for value in host_values if value]
    return bool(non_empty_hosts) and all(_is_loopback_host(value) for value in non_empty_hosts)


def _remote_execution_error() -> dict:
    return {
        "output": "",
        "error": (
            "Code execution is limited to local requests. "
            "Set ORION_ALLOW_REMOTE_EXECUTION=1 only on a trusted network."
        ),
        "duration_ms": 0,
    }


def _safe_filename(name: str) -> str | None:
    if not name:
        return None
    base = os.path.basename(name)
    if base != name:
        return None
    if not _SAFE_FILENAME_RE.match(base):
        return None
    return base


def _import_is_allowed(module_name: str) -> bool:
    parts = [part for part in module_name.split(".") if part]
    if not parts:
        return False
    return parts[0] in ALLOWED_DATA_SCIENCE_IMPORTS and not any(
        part in BLOCKED_IMPORT_PARTS for part in parts
    )


def _blocked_identifier(name: str) -> bool:
    return name in BLOCKED_CALL_NAMES or name.startswith("__") or name.endswith("__")


def _validate_python_code(code: str) -> tuple[bool, str]:
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return False, f"Syntax error: {exc.msg}"

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _import_is_allowed(alias.name):
                    return False, f"Import not allowed: {alias.name}"

        elif isinstance(node, ast.ImportFrom):
            module_name = "." * node.level + (node.module or "")
            if node.level or not _import_is_allowed(node.module or ""):
                return False, f"Import not allowed: {module_name}"

        elif isinstance(node, ast.Name) and _blocked_identifier(node.id):
            return False, f"Name not allowed: {node.id}"

        elif isinstance(node, ast.Attribute):
            attr = node.attr
            if attr in BLOCKED_ATTRIBUTE_NAMES or attr.startswith("__") or attr.endswith("__"):
                return False, f"Attribute not allowed: {attr}"

        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and _blocked_identifier(func.id):
                return False, f"Call not allowed: {func.id}"
            if isinstance(func, ast.Attribute):
                attr = func.attr
                if attr in BLOCKED_ATTRIBUTE_NAMES or attr.startswith("__") or attr.endswith("__"):
                    return False, f"Call not allowed: {attr}"

    return True, ""


@router.post("/python")
def execute_python(req: ExecutePythonRequest, request: Request) -> dict:
    if not _remote_execution_allowed(request):
        return _remote_execution_error()

    code = req.code
    is_valid, reason = _validate_python_code(code)
    if not is_valid:
        return {"output": "", "error": f"Blocked: {reason}", "duration_ms": 0}

    start = time.monotonic()
    try:
        result = subprocess.run(
            [sys.executable, "-I", "-c", code],
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
        return {"output": "", "error": "Execution timed out (15 s limit)", "duration_ms": 15000}
    except Exception as exc:
        logger.error("Python execution error: %s", exc, exc_info=True)
        return {"output": "", "error": str(exc), "duration_ms": 0}


@router.post("/sql")
def execute_sql(req: ExecuteSQLRequest, request: Request) -> dict:
    if not _remote_execution_allowed(request):
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "duration_ms": 0,
            "error": _remote_execution_error()["error"],
        }

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
            "error": "Semicolons are not allowed - only single SELECT queries permitted",
        }
    forbidden = re.search(
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC|PRAGMA|ATTACH|DETACH)\b",
        query,
        re.IGNORECASE,
    )
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
        return {"columns": [], "rows": [], "row_count": 0, "duration_ms": 0, "error": str(exc)}
    except Exception as exc:
        logger.error("SQL execution error: %s", exc, exc_info=True)
        return {"columns": [], "rows": [], "row_count": 0, "duration_ms": 0, "error": str(exc)}


@router.post("/multi")
def execute_multi(req: ExecuteMultiFileRequest, request: Request) -> dict:
    if not _remote_execution_allowed(request):
        return {"error": _remote_execution_error()["error"], "outputs": {}, "duration_ms": 0}

    if not req.files:
        return {"error": "No files provided", "outputs": {}}

    sanitized: list[tuple[str, str]] = []
    for file in req.files:
        raw_name = file.get("name", "")
        safe = _safe_filename(raw_name)
        if safe is None:
            return {
                "error": f"Invalid filename: {raw_name!r}. "
                "Names must be simple basenames ending in .py or .txt.",
                "outputs": {},
            }
        sanitized.append((safe, file.get("content", "")))

    for name, content in sanitized:
        is_valid, reason = _validate_python_code(content)
        if not is_valid:
            return {"error": f"Blocked in {name}: {reason}", "outputs": {}}

    temp_dir = tempfile.mkdtemp(prefix="orion_exec_")
    try:
        sandbox_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sandbox.db")
        if os.path.exists(sandbox_path):
            shutil.copy2(sandbox_path, os.path.join(temp_dir, "sandbox.db"))

        for name, content in sanitized:
            file_path = os.path.join(temp_dir, name)
            if os.path.commonpath(
                [os.path.realpath(file_path), os.path.realpath(temp_dir)]
            ) != os.path.realpath(temp_dir):
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

        return {
            "outputs": {
                "main": result.stdout[:5000],
                "all_files": [n for n, _ in sanitized],
            },
            "errors": {"main": result.stderr[:2000]} if result.returncode != 0 else None,
            "duration_ms": duration_ms,
        }

    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out (20 s limit)", "outputs": {}, "duration_ms": 20000}
    except Exception as exc:
        logger.error("Multi-file execution error: %s", exc, exc_info=True)
        return {"error": str(exc), "outputs": {}, "duration_ms": 0}
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
