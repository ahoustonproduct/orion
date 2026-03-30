"""
main.py — Orion Code FastAPI application entry point.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load .env before any module that reads environment variables
load_dotenv()

from db import init_db
from routers import curriculum, progress, quiz, orion, execute, decision, mastery, spaced_repetition

app = FastAPI(
    title="Orion Code API",
    description="Backend for the Orion Code FinTech analytics learning platform",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS — allow the Next.js dev server and any local previews
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

@app.on_event("startup")
def startup() -> None:
    """Initialise the SQLite database schema on first run."""
    init_db()


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(curriculum.router,        prefix="/curriculum")
app.include_router(progress.router,          prefix="/progress")
app.include_router(quiz.router,              prefix="/quiz")
app.include_router(orion.router,             prefix="/orion")
app.include_router(execute.router,           prefix="/execute")
app.include_router(decision.router,          prefix="/decision")
app.include_router(mastery.router,           prefix="/mastery")
app.include_router(spaced_repetition.router, prefix="/review")


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok"}
