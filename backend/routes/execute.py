from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import sqlite3
import time
import os
import re
import sys

router = APIRouter(prefix="/execute", tags=["execute"])

# Data science libraries that are allowed in the sandbox
ALLOWED_DATA_SCIENCE_IMPORTS = {"pandas", "numpy", "scipy", "sklearn", "matplotlib", "seaborn", "statistics", "math", "json", "random", "datetime", "re"}

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
    r"\bimport\s+pandas\s+as\b",
    r"\bimport\s+numpy\s+as\b",
    r"\bimport\s+scipy\s+as\b",
    r"\bimport\s+sklearn\s+as\b",
    r"\bimport\s+matplotlib\s+as\b",
    r"\bimport\s+seaborn\s+as\b",
]

_COMPILED_PATTERNS = [re.compile(p) for p in BLOCKED_PATTERNS]


def _is_unsafe(code: str) -> tuple[bool, str]:
    for pattern_re, pattern_src in zip(_COMPILED_PATTERNS, BLOCKED_PATTERNS):
        if pattern_re.search(code):
            return True, pattern_src
    return False, ""


def _check_data_science_imports(code: str) -> list[str]:
    """Check for data science library imports and verify they're available."""
    import_pattern = re.compile(r'^\s*import\s+([a-zA-Z_][a-zA-Z0-9_]*)', re.MULTILINE)
    found_imports = import_pattern.findall(code)
    needed = []
    for imp in found_imports:
        if imp in ALLOWED_DATA_SCIENCE_IMPORTS:
            try:
                __import__(imp)
            except ImportError:
                needed.append(imp)
    return needed


class ExecutePythonRequest(BaseModel):
    code: str
    files: list[dict[str, str]] | None = None  # For multi-file execution


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
    
    # Check for needed data science libraries
    needed_libs = _check_data_science_imports(code)
    
    # Build command with pip install if needed
    cmd = ["python", "-c", code]
    if needed_libs:
        # Prepend pip install to the command
        install_cmd = f"pip install --quiet {' '.join(needed_libs)} && python -c {repr(code)}"
        cmd = ["python", "-c", install_cmd]
    
    start = time.monotonic()
    try:
        result = subprocess.run(
            cmd,
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


@router.post("/multi")
def execute_multi(req: ExecuteMultiFileRequest) -> dict:
    """Execute multiple Python files concurrently."""
    files = req.files
    if not files:
        return {"error": "No files provided", "outputs": {}}
    
    # Create a temporary directory for the files
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    outputs = {}
    errors = {}
    
    try:
        # Write all files to the temp directory
        for file in files:
            file_path = os.path.join(temp_dir, file["name"])
            with open(file_path, "w") as f:
                f.write(file["content"])
        
        # Find the main file (first .py file or the first file)
        main_file = next((f for f in files if f["name"].endswith(".py")), files[0])
        
        # Check all files for unsafe patterns
        for file in files:
            unsafe, matched = _is_unsafe(file["content"])
            if unsafe:
                return {
                    "error": f"Unsafe pattern in {file['name']}: {matched}",
                    "outputs": {},
                }
        
        # Check for data science imports across all files
        all_code = "\n".join(f["content"] for f in files)
        needed_libs = _check_data_science_imports(all_code)
        
        # Build command
        main_path = os.path.join(temp_dir, main_file["name"])
        cmd = ["python", main_path]
        
        if needed_libs:
            install_cmd = f"pip install --quiet {' '.join(needed_libs)} && python {main_path}"
            cmd = ["python", "-c", install_cmd]
        
        start = time.monotonic()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=20,
            cwd=temp_dir,
        )
        duration_ms = int((time.monotonic() - start) * 1000)
        
        outputs = {
            "main": result.stdout[:5000],
            "all_files": [f["name"] for f in files],
        }
        
        if result.returncode != 0:
            errors = {"main": result.stderr[:2000]}
        
        return {
            "outputs": outputs,
            "errors": errors if errors else None,
            "duration_ms": duration_ms,
        }
        
    except subprocess.TimeoutExpired:
        return {
            "error": "Execution timed out (20 s limit)",
            "outputs": {},
            "duration_ms": 20000,
        }
    except Exception as exc:
        return {
            "error": str(exc),
            "outputs": {},
            "duration_ms": 0,
        }
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
