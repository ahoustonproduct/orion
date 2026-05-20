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
    "sqlite3",
    "statistics",
    "sqlalchemy",
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

ALLOWED_DUNDER_NAMES = {
    "__tablename__",
}

BLOCKED_ATTRIBUTE_NAMES = {
    "exec",
    "enable_load_extension",
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

PYTHON_TIMEOUT_SECONDS = 15
PYTHON_MULTI_TIMEOUT_SECONDS = 20
PYTHON_CODE_MAX_CHARS = 25_000
PYTHON_AST_NODE_LIMIT = 8_000
PYTHON_STDOUT_MAX_CHARS = 5_000
PYTHON_STDERR_MAX_CHARS = 2_000
PYTHON_MEMORY_LIMIT_BYTES = 512 * 1024 * 1024
PYTHON_FILE_SIZE_LIMIT_BYTES = 1 * 1024 * 1024

SQL_QUERY_MAX_CHARS = 10_000
SQL_ROW_LIMIT = 500
SQL_CELL_MAX_CHARS = 1_000
SQL_TIMEOUT_SECONDS = 2.0
SQL_PROGRESS_STEP = 1_000
SQL_PROGRESS_MAX_OPS = 1_000_000

SAFE_SQLITE_PRAGMAS = {
    "foreign_key_list",
    "foreign_keys",
    "index_info",
    "index_list",
    "read_uncommitted",
    "table_info",
}

READONLY_SQLITE_DENIED_ACTIONS = {
    action
    for action in (
        getattr(sqlite3, name, None)
        for name in (
            "SQLITE_ALTER_TABLE",
            "SQLITE_ATTACH",
            "SQLITE_CREATE_INDEX",
            "SQLITE_CREATE_TABLE",
            "SQLITE_CREATE_TEMP_INDEX",
            "SQLITE_CREATE_TEMP_TABLE",
            "SQLITE_CREATE_TEMP_TRIGGER",
            "SQLITE_CREATE_TEMP_VIEW",
            "SQLITE_CREATE_TRIGGER",
            "SQLITE_CREATE_VIEW",
            "SQLITE_DELETE",
            "SQLITE_DETACH",
            "SQLITE_DROP_INDEX",
            "SQLITE_DROP_TABLE",
            "SQLITE_DROP_TEMP_INDEX",
            "SQLITE_DROP_TEMP_TABLE",
            "SQLITE_DROP_TEMP_TRIGGER",
            "SQLITE_DROP_TEMP_VIEW",
            "SQLITE_DROP_TRIGGER",
            "SQLITE_DROP_VIEW",
            "SQLITE_INSERT",
            "SQLITE_TRANSACTION",
            "SQLITE_UPDATE",
        )
    )
    if action is not None
}
SQLITE_BLOCKED_FUNCTIONS = {"load_extension", "randomblob", "readfile", "writefile", "zeroblob"}

SQLITE_BLOCKED_SQL_RE = re.compile(
    r"\b(?:ATTACH|DETACH)\b|VACUUM\s+INTO|\b(?:load_extension|readfile|writefile|randomblob|zeroblob)\s*\(",
    re.IGNORECASE,
)

PYTHON_SANDBOX_PREAMBLE = f"""
def __orion_install_sqlite_guard():
    import sqlite3 as __sqlite3
    import time as __time

    __original_connect = __sqlite3.connect
    __blocked_functions = {{"load_extension", "readfile", "writefile", "randomblob", "zeroblob"}}
    __allowed_pragmas = {sorted(SAFE_SQLITE_PRAGMAS)!r}
    __max_ops = {SQL_PROGRESS_MAX_OPS * 5}
    __step = {SQL_PROGRESS_STEP}
    __timeout_seconds = {max(1, PYTHON_TIMEOUT_SECONDS - 1)}

    def __set_limit(__conn, __name, __value):
        __category = getattr(__sqlite3, __name, None)
        if __category is not None and hasattr(__conn, "setlimit"):
            try:
                __conn.setlimit(__category, __value)
            except Exception:
                pass

    def __authorizer(__action, __arg1, __arg2, __db_name, __source):
        if __action in (
            getattr(__sqlite3, "SQLITE_ATTACH", -1),
            getattr(__sqlite3, "SQLITE_DETACH", -1),
        ):
            return __sqlite3.SQLITE_DENY
        if __action == getattr(__sqlite3, "SQLITE_FUNCTION", -1):
            __function_name = str(__arg2 or __arg1 or "").lower()
            if __function_name in __blocked_functions:
                return __sqlite3.SQLITE_DENY
        if __action == getattr(__sqlite3, "SQLITE_PRAGMA", -1):
            __pragma = str(__arg1 or "").lower()
            if __pragma not in __allowed_pragmas:
                return __sqlite3.SQLITE_DENY
        return __sqlite3.SQLITE_OK

    def __safe_connect(__database=":memory:", *args, **kwargs):
        if str(__database) != ":memory:":
            raise ValueError("Only in-memory SQLite databases are allowed in the lesson sandbox")
        if kwargs.get("uri"):
            raise ValueError("SQLite URI connections are not allowed in the lesson sandbox")

        __conn = __original_connect(":memory:", *args, **kwargs)
        __deadline = __time.monotonic() + __timeout_seconds
        __ops = 0

        def __progress():
            nonlocal __ops
            __ops += __step
            if __ops > __max_ops or __time.monotonic() > __deadline:
                return 1
            return 0

        __conn.set_authorizer(__authorizer)
        __conn.set_progress_handler(__progress, __step)
        __set_limit(__conn, "SQLITE_LIMIT_ATTACHED", 0)
        __set_limit(__conn, "SQLITE_LIMIT_LENGTH", {SQL_CELL_MAX_CHARS * SQL_ROW_LIMIT})
        __set_limit(__conn, "SQLITE_LIMIT_SQL_LENGTH", {SQL_QUERY_MAX_CHARS * 2})
        __set_limit(__conn, "SQLITE_LIMIT_COLUMN", 200)
        return __conn

    __sqlite3.connect = __safe_connect
    try:
        __sqlite3.dbapi2.connect = __safe_connect
    except AttributeError:
        pass

__orion_install_sqlite_guard()
del __orion_install_sqlite_guard
"""

MAX_CODE_CHARS = PYTHON_CODE_MAX_CHARS
MAX_MULTI_FILES = 8
MAX_MULTI_FILE_CHARS = 12000
MAX_SQL_QUERY_CHARS = SQL_QUERY_MAX_CHARS
MAX_OUTPUT_CHARS = PYTHON_STDOUT_MAX_CHARS
MAX_ERROR_CHARS = PYTHON_STDERR_MAX_CHARS
MAX_SQL_ROWS = SQL_ROW_LIMIT


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


def _execution_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "MPLBACKEND": "Agg",
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "NUMEXPR_NUM_THREADS": "1",
            "PYTHONNOUSERSITE": "1",
        }
    )
    return env


def _posix_resource_limiter(timeout: int = PYTHON_TIMEOUT_SECONDS):
    if os.name != "posix":
        return None

    def _limit_resources() -> None:
        try:
            import resource

            resource.setrlimit(
                resource.RLIMIT_AS,
                (PYTHON_MEMORY_LIMIT_BYTES, PYTHON_MEMORY_LIMIT_BYTES),
            )
            resource.setrlimit(
                resource.RLIMIT_FSIZE,
                (PYTHON_FILE_SIZE_LIMIT_BYTES, PYTHON_FILE_SIZE_LIMIT_BYTES),
            )
            resource.setrlimit(
                resource.RLIMIT_CPU,
                (timeout, timeout + 1),
            )
        except Exception:
            pass

    return _limit_resources


def _python_run_kwargs(cwd: str, timeout: int) -> dict:
    kwargs = {
        "capture_output": True,
        "cwd": cwd,
        "env": _execution_env(),
        "text": True,
        "timeout": timeout,
    }
    limiter = _posix_resource_limiter(timeout)
    if limiter is not None:
        kwargs["preexec_fn"] = limiter
    return kwargs


def _literal_string(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _call_name(func: ast.AST) -> str | None:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _is_module_attribute(func: ast.AST, module_name: str, attr_name: str) -> bool:
    return (
        isinstance(func, ast.Attribute)
        and func.attr == attr_name
        and isinstance(func.value, ast.Name)
        and func.value.id == module_name
    )


def _validate_sqlite_connect_call(node: ast.Call) -> tuple[bool, str]:
    if _is_module_attribute(node.func, "sqlite3", "connect") or (
        isinstance(node.func, ast.Name) and node.func.id == "connect"
    ):
        database = _literal_string(node.args[0]) if node.args else ":memory:"
        if database != ":memory:":
            return False, "SQLite connections must use ':memory:' in the lesson sandbox"
        for keyword in node.keywords:
            if keyword.arg == "uri" and not (
                isinstance(keyword.value, ast.Constant) and keyword.value.value is False
            ):
                return False, "SQLite URI connections are not allowed"
    return True, ""


def _validate_sqlalchemy_engine_call(node: ast.Call) -> tuple[bool, str]:
    if _is_module_attribute(node.func, "sqlalchemy", "create_engine") or (
        isinstance(node.func, ast.Name) and node.func.id == "create_engine"
    ):
        url = _literal_string(node.args[0]) if node.args else None
        if url not in {"sqlite:///:memory:", "sqlite+pysqlite:///:memory:"}:
            return False, "SQLAlchemy engines must use an in-memory SQLite URL"
    return True, ""


def _validate_sql_literal(value: str) -> tuple[bool, str]:
    if len(value) > SQL_QUERY_MAX_CHARS * 2:
        return False, "SQL string literal is too long"
    forbidden = SQLITE_BLOCKED_SQL_RE.search(value)
    if forbidden:
        return False, f"SQLite operation not allowed: {forbidden.group(0)}"
    return True, ""


def _validate_embedded_sql_call(node: ast.Call) -> tuple[bool, str]:
    call_name = _call_name(node.func)
    if call_name not in {"execute", "executemany", "executescript", "read_sql_query"}:
        return True, ""
    if not node.args:
        return True, ""
    sql = _literal_string(node.args[0])
    if sql is None:
        return True, ""
    return _validate_sql_literal(sql)


def _sqlite_set_limit(conn: sqlite3.Connection, limit_name: str, value: int) -> None:
    category = getattr(sqlite3, limit_name, None)
    if category is not None and hasattr(conn, "setlimit"):
        try:
            conn.setlimit(category, value)
        except sqlite3.Error:
            pass


def _sqlite_readonly_authorizer(action, arg1, arg2, db_name, source) -> int:
    if action in READONLY_SQLITE_DENIED_ACTIONS:
        return sqlite3.SQLITE_DENY

    if action == getattr(sqlite3, "SQLITE_PRAGMA", -1):
        pragma = str(arg1 or "").lower()
        return sqlite3.SQLITE_OK if pragma in SAFE_SQLITE_PRAGMAS else sqlite3.SQLITE_DENY

    if action == getattr(sqlite3, "SQLITE_FUNCTION", -1):
        function_name = str(arg2 or arg1 or "").lower()
        if function_name in SQLITE_BLOCKED_FUNCTIONS:
            return sqlite3.SQLITE_DENY

    return sqlite3.SQLITE_OK


def _sql_progress_handler(deadline: float, max_ops: int):
    ops = 0

    def _progress() -> int:
        nonlocal ops
        ops += SQL_PROGRESS_STEP
        if ops > max_ops or time.monotonic() > deadline:
            return 1
        return 0

    return _progress


def _format_sql_cell(value):
    if isinstance(value, (bytes, bytearray, memoryview)):
        return f"<{len(value)} bytes>"
    if isinstance(value, str) and len(value) > SQL_CELL_MAX_CHARS:
        return value[:SQL_CELL_MAX_CHARS] + "...[truncated]"
    return value


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
    if name in ALLOWED_DUNDER_NAMES:
        return False
    return name in BLOCKED_CALL_NAMES or name.startswith("__") or name.endswith("__")


def _is_memory_literal(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value == ":memory:"


def _memory_database_names(tree: ast.AST) -> set[str]:
    assignments: dict[str, list[bool]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignments.setdefault(target.id, []).append(_is_memory_literal(node.value))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assignments.setdefault(node.target.id, []).append(
                _is_memory_literal(node.value) if node.value is not None else False
            )
    return {name for name, values in assignments.items() if values and all(values)}


def _is_sqlite_memory_connect(node: ast.Call, memory_database_names: set[str]) -> bool:
    func = node.func
    if not isinstance(func, ast.Attribute) or func.attr != "connect":
        return False
    if not isinstance(func.value, ast.Name) or func.value.id != "sqlite3":
        return False
    for keyword in node.keywords:
        if keyword.arg == "uri" and not (
            isinstance(keyword.value, ast.Constant) and keyword.value.value is False
        ):
            return False
    if len(node.args) != 1:
        return False
    database_arg = node.args[0]
    if _is_memory_literal(database_arg):
        return True
    return isinstance(database_arg, ast.Name) and database_arg.id in memory_database_names


def _validate_python_code(code: str) -> tuple[bool, str]:
    if len(code) > PYTHON_CODE_MAX_CHARS:
        return False, f"Code is too long ({PYTHON_CODE_MAX_CHARS} character limit)"

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return False, f"Syntax error: {exc.msg}"

    nodes = list(ast.walk(tree))
    if len(nodes) > PYTHON_AST_NODE_LIMIT:
        return False, f"Code is too complex ({PYTHON_AST_NODE_LIMIT} AST node limit)"

    memory_database_names = _memory_database_names(tree)

    for node in nodes:
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
                if attr == "connect":
                    if _is_sqlite_memory_connect(node, memory_database_names):
                        continue
                    if _is_module_attribute(func, "sqlite3", "connect"):
                        return False, "SQLite connections must use ':memory:' in the lesson sandbox"
                    return False, "Call not allowed: connect"
                if attr in BLOCKED_ATTRIBUTE_NAMES or attr.startswith("__") or attr.endswith("__"):
                    return False, f"Call not allowed: {attr}"

            for validator in (
                _validate_sqlite_connect_call,
                _validate_sqlalchemy_engine_call,
                _validate_embedded_sql_call,
            ):
                ok, reason = validator(node)
                if not ok:
                    return False, reason

    return True, ""


@router.post("/python")
def execute_python(req: ExecutePythonRequest, request: Request) -> dict:
    if not _remote_execution_allowed(request):
        return _remote_execution_error()

    code = req.code
    if len(code) > MAX_CODE_CHARS:
        return {
            "output": "",
            "error": f"Code is too long ({len(code)} characters). Limit is {MAX_CODE_CHARS}.",
            "duration_ms": 0,
        }
    is_valid, reason = _validate_python_code(code)
    if not is_valid:
        return {"output": "", "error": f"Blocked: {reason}", "duration_ms": 0}

    start = time.monotonic()
    try:
        with tempfile.TemporaryDirectory(prefix="orion_py_exec_") as temp_dir:
            result = subprocess.run(
                [sys.executable, "-I", "-c", PYTHON_SANDBOX_PREAMBLE + "\n" + code],
                **_python_run_kwargs(temp_dir, PYTHON_TIMEOUT_SECONDS),
            )
        duration_ms = int((time.monotonic() - start) * 1000)
        return {
            "output": result.stdout[:MAX_OUTPUT_CHARS],
            "error": result.stderr[:MAX_ERROR_CHARS] if result.returncode != 0 else None,
            "duration_ms": duration_ms,
        }
    except subprocess.TimeoutExpired:
        return {
            "output": "",
            "error": f"Execution timed out ({PYTHON_TIMEOUT_SECONDS} s limit)",
            "duration_ms": PYTHON_TIMEOUT_SECONDS * 1000,
        }
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
    if len(query) > MAX_SQL_QUERY_CHARS:
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "duration_ms": 0,
            "error": f"Query is too long ({len(query)} characters). Limit is {MAX_SQL_QUERY_CHARS}.",
        }
    if not re.match(r"^\s*(SELECT|WITH)\b", query, re.IGNORECASE):
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "duration_ms": 0,
            "error": "Only read-only SELECT queries are allowed",
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
    ok, reason = _validate_sql_literal(query)
    if not ok:
        return {"columns": [], "rows": [], "row_count": 0, "duration_ms": 0, "error": reason}

    start = time.monotonic()
    conn = None
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sandbox.db")
        conn = sqlite3.connect(os.path.abspath(db_path), timeout=1)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA query_only = ON")
        conn.set_authorizer(_sqlite_readonly_authorizer)
        conn.set_progress_handler(
            _sql_progress_handler(time.monotonic() + SQL_TIMEOUT_SECONDS, SQL_PROGRESS_MAX_OPS),
            SQL_PROGRESS_STEP,
        )
        _sqlite_set_limit(conn, "SQLITE_LIMIT_ATTACHED", 0)
        _sqlite_set_limit(conn, "SQLITE_LIMIT_COLUMN", 200)
        _sqlite_set_limit(conn, "SQLITE_LIMIT_LENGTH", SQL_CELL_MAX_CHARS * MAX_SQL_ROWS)
        _sqlite_set_limit(conn, "SQLITE_LIMIT_SQL_LENGTH", MAX_SQL_QUERY_CHARS)
        cursor = conn.execute(query)
        rows = cursor.fetchmany(MAX_SQL_ROWS)
        columns = [d[0] for d in cursor.description] if cursor.description else []
        duration_ms = int((time.monotonic() - start) * 1000)
        return {
            "columns": columns,
            "rows": [[_format_sql_cell(value) for value in row] for row in rows],
            "row_count": len(rows),
            "duration_ms": duration_ms,
            "error": None,
        }
    except sqlite3.Error as exc:
        logger.info("SQL query failed in sandbox: %s", exc)
        duration_ms = int((time.monotonic() - start) * 1000)
        error = (
            f"SQL execution timed out or exceeded resource limits ({SQL_TIMEOUT_SECONDS:g} s limit)"
            if str(exc).lower() == "interrupted"
            else str(exc)
        )
        return {"columns": [], "rows": [], "row_count": 0, "duration_ms": duration_ms, "error": error}
    except Exception as exc:
        logger.error("SQL execution error: %s", exc, exc_info=True)
        return {"columns": [], "rows": [], "row_count": 0, "duration_ms": 0, "error": str(exc)}
    finally:
        if conn is not None:
            conn.close()


@router.post("/multi")
def execute_multi(req: ExecuteMultiFileRequest, request: Request) -> dict:
    if not _remote_execution_allowed(request):
        return {"error": _remote_execution_error()["error"], "outputs": {}, "duration_ms": 0}

    if not req.files:
        return {"error": "No files provided", "outputs": {}}
    if len(req.files) > MAX_MULTI_FILES:
        return {"error": f"Too many files. Limit is {MAX_MULTI_FILES}.", "outputs": {}}

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
        content = file.get("content", "")
        if len(content) > MAX_MULTI_FILE_CHARS:
            return {
                "error": f"{safe} is too long ({len(content)} characters). Limit is {MAX_MULTI_FILE_CHARS}.",
                "outputs": {},
            }
        sanitized.append((safe, content))

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
        runner_path = os.path.join(temp_dir, "__orion_runner.py")
        with open(runner_path, "w", encoding="utf-8") as f:
            f.write(
                PYTHON_SANDBOX_PREAMBLE
                + "\nimport runpy as __orion_runpy\n"
                + f"__orion_runpy.run_path({main_path!r}, run_name='__main__')\n"
            )

        start = time.monotonic()
        result = subprocess.run(
            [sys.executable, "-I", runner_path],
            **_python_run_kwargs(temp_dir, PYTHON_MULTI_TIMEOUT_SECONDS),
        )
        duration_ms = int((time.monotonic() - start) * 1000)

        return {
            "outputs": {
                "main": result.stdout[:MAX_OUTPUT_CHARS],
                "all_files": [n for n, _ in sanitized],
            },
            "errors": {"main": result.stderr[:MAX_ERROR_CHARS]} if result.returncode != 0 else None,
            "duration_ms": duration_ms,
        }

    except subprocess.TimeoutExpired:
        return {
            "error": f"Execution timed out ({PYTHON_MULTI_TIMEOUT_SECONDS} s limit)",
            "outputs": {},
            "duration_ms": PYTHON_MULTI_TIMEOUT_SECONDS * 1000,
        }
    except Exception as exc:
        logger.error("Multi-file execution error: %s", exc, exc_info=True)
        return {"error": str(exc), "outputs": {}, "duration_ms": 0}
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
