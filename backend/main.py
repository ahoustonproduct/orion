import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import create_tables
from routes.curriculum import router as curriculum_router
from routes.progress import router as progress_router
from routes.ai import router as ai_router
from routes.quiz import router as quiz_router
from routes.execute import router as execute_router
from routes.mastery import router as mastery_router
from routes.review import router as review_router

app = FastAPI(title="Orion Code API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(curriculum_router)
app.include_router(progress_router)
app.include_router(ai_router)
app.include_router(quiz_router)
app.include_router(execute_router)
app.include_router(mastery_router)
app.include_router(review_router)


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def root():
    return {"message": "Orion Code API", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}
