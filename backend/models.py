import os
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, JSON, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date

# Anchor the SQLite DB to the backend directory so that progress persists
# regardless of the working directory the server is launched from.
_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
_DB_PATH = os.environ.get("ORION_DB_PATH", os.path.join(_BACKEND_DIR, "orion_code.db"))
DATABASE_URL = f"sqlite:///{_DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_key = Column(String, index=True)
    lesson_id = Column(String)
    stars = Column(Integer, default=0)  # 0-3
    attempts = Column(Integer, default=0)
    hints_used = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    flagged = Column(Boolean, default=False)
    last_accessed = Column(DateTime, default=datetime.utcnow)


class LearningProfile(Base):
    __tablename__ = "learning_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_key = Column(String, unique=True, index=True)
    weak_topics = Column(JSON, default=list)           # lesson_ids with low stars
    common_mistakes = Column(JSON, default=list)       # tracked error patterns
    preferred_analogies = Column(JSON, default=dict)   # lesson_id -> analogy that worked
    topic_confidence = Column(JSON, default=dict)      # lesson_id -> confidence rating (1-5)
    mastered_concepts = Column(JSON, default=list)     # lesson_ids with 3 stars (for comparisons)
    study_plan = Column(JSON, default=dict)            # generated weekly study plan
    streak_count = Column(Integer, default=0)
    last_active = Column(Date, default=date.today)
    study_log = Column(JSON, default=dict)             # "YYYY-MM-DD" -> minutes


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_key = Column(String, index=True)
    content = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class BookmarkedPosition(Base):
    __tablename__ = "bookmarked_positions"

    id = Column(Integer, primary_key=True, index=True)
    user_key = Column(String, index=True)
    lesson_id = Column(String)
    step_index = Column(Integer, default=0)    # which step of the lesson (0=concept, 1=questions, 2=challenge)
    sub_step = Column(Integer, default=0)      # e.g. which question within questions
    saved_code = Column(String, default="")    # preserve in-progress code
    updated_at = Column(DateTime, default=datetime.utcnow)


class ConfidenceRating(Base):
    __tablename__ = "confidence_ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_key = Column(String, index=True)
    lesson_id = Column(String)
    rating = Column(Integer)   # 1-5 (1=lost, 3=okay, 5=totally got it)
    rated_at = Column(DateTime, default=datetime.utcnow)


class Notebook(Base):
    """A user-generated module, built from a YouTube transcript by the tutor LLM.

    `module_data` stores the generated module JSON — same shape as the built-in
    curriculum modules in curriculum_data/, so it can be rendered with the
    existing /curriculum and /learn UI.
    """
    __tablename__ = "notebooks"

    id = Column(String, primary_key=True, index=True)   # notebook_<uuid>
    user_key = Column(String, index=True)
    title = Column(String)
    source_type = Column(String, default="youtube")     # youtube | text | ...
    source_url = Column(String, default="")
    status = Column(String, default="pending")          # pending | generating | ready | failed
    error = Column(String, default="")
    module_data = Column(JSON, default=dict)            # module dict with nested lessons
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
