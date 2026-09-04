from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes.health import router as health_router
from app.api.routes.documents import router as documents_router
from app.api.routes.interviews import router as interviews_router
from app.core.config import settings


# ============================================================
# BASE DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

AUDIO_DIR = BASE_DIR / "audio"
UPLOAD_DIR = BASE_DIR / "uploads"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title=settings.app_name,
    description="Voice-based AI Interview Coach",
    version="0.1.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# SERVE GENERATED AUDIO
# ============================================================

app.mount(
    "/audio",
    StaticFiles(directory=str(AUDIO_DIR)),
    name="audio",
)


# ============================================================
# API ROUTES
# ============================================================

app.include_router(
    health_router
)

# IMPORTANT:
# No "/documents" prefix here.
#
# This makes the endpoints:
#
# POST /upload/resume
# POST /upload/job_description
# POST /job-description

app.include_router(
    documents_router,
    tags=["Documents"],
)

app.include_router(
    interviews_router,
    tags=["Interviews"],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI Interview Coach API",
        "status": "running",
        "version": "0.1.0",
    }