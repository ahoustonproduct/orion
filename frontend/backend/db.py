"""
db.py — SQLite connection helper and schema initialisation for Orion Code.
The database file (orion.db) lives in the same directory as this module.
"""

from contextlib import contextmanager
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orion.db")

# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------

@contextmanager
def get_db():
    """Yield an open sqlite3.Connection with Row row_factory, then close it."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrent read performance
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_DDL = """
-- Progress tables (all keyed by user_key TEXT)
CREATE TABLE IF NOT EXISTS lesson_progress (
    user_key              TEXT,
    lesson_id             TEXT,
    stars                 INTEGER DEFAULT 0,
    attempts              INTEGER DEFAULT 0,
    completed             INTEGER DEFAULT 0,
    flagged               INTEGER DEFAULT 0,
    last_accessed         TEXT,
    time_spent_minutes    REAL    DEFAULT 0,
    hints_used            INTEGER DEFAULT 0,
    PRIMARY KEY (user_key, lesson_id)
);

CREATE TABLE IF NOT EXISTS user_meta (
    user_key                  TEXT PRIMARY KEY,
    streak                    INTEGER DEFAULT 0,
    last_studied_date         TEXT,
    study_log_json            TEXT    DEFAULT '{}',
    weak_topics_json          TEXT    DEFAULT '[]',
    mastered_concepts_json    TEXT    DEFAULT '[]',
    preferred_analogies_json  TEXT    DEFAULT '{}',
    topic_confidence_json     TEXT    DEFAULT '{}',
    study_plan_json           TEXT    DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS notes (
    user_key   TEXT PRIMARY KEY,
    content    TEXT DEFAULT '',
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS bookmarks (
    user_key    TEXT,
    lesson_id   TEXT,
    step_index  INTEGER,
    sub_step    TEXT,
    saved_code  TEXT,
    PRIMARY KEY (user_key, lesson_id)
);

CREATE TABLE IF NOT EXISTS confidence (
    user_key    TEXT,
    lesson_id   TEXT,
    rating      INTEGER,
    recorded_at TEXT,
    PRIMARY KEY (user_key, lesson_id)
);

-- FinTech feature tables
CREATE TABLE IF NOT EXISTS mastery_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_key    TEXT,
    concept_tag TEXT,
    correct     INTEGER,
    recorded_at TEXT
);

CREATE TABLE IF NOT EXISTS decision_history (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    user_key         TEXT,
    lesson_id        TEXT,
    block_id         TEXT,
    decision_type    TEXT,
    user_value_json  TEXT,
    user_outcome     REAL,
    optimal_outcome  REAL,
    worst_outcome    REAL,
    score            REAL,
    recorded_at      TEXT
);

CREATE TABLE IF NOT EXISTS review_queue (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    user_key         TEXT,
    question_id      TEXT,
    lesson_id        TEXT,
    question_json    TEXT,
    wrong_count      INTEGER DEFAULT 1,
    next_review_date TEXT,
    interval_days    INTEGER DEFAULT 1,
    UNIQUE(user_key, question_id)
);
"""


def init_db() -> None:
    """Create all tables if they do not already exist. Called at app startup."""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(_DDL)
        conn.commit()
    finally:
        conn.close()
