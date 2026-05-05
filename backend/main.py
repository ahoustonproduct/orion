import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import create_tables
from init_sandbox import init_sandbox
from routes.curriculum import router as curriculum_router
from routes.progress import router as progress_router
from routes.quiz import router as quiz_router
from routes.execute import router as execute_router
from routes.mastery import router as mastery_router
from routes.review import router as review_router
from routes.notebooks import router as notebooks_router
from routes.decision import router as decision_router

import logging
from fastapi.responses import JSONResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Orion Code API", version="1.0.0")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error. Please try again later."},
    )

# CORS: restrict origins to an explicit allowlist.
# Set ALLOWED_ORIGINS env var (comma-separated) to add origins in staging/prod.
# Wildcards are intentionally NOT supported because wildcard plus credentials is a silent no-op
# in browsers and a footgun the moment we add cookie auth.
_default_origins = "http://localhost:3000,http://127.0.0.1:3000"
_allowed_origins = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", _default_origins).split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(curriculum_router)
app.include_router(progress_router)
app.include_router(quiz_router)
app.include_router(execute_router)
app.include_router(mastery_router)
app.include_router(review_router)
app.include_router(notebooks_router)
app.include_router(decision_router)


@app.on_event("startup")
def startup():
    create_tables()
    init_sandbox()


@app.get("/")
def root():
    return {"message": "Orion Code API", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}
