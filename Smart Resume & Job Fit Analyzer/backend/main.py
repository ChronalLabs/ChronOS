"""
Smart Resume & Job Fit Analyzer - Backend API
FastAPI application entry point with CORS, health checks, and router mounting.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import spacy

from api.routes import router as api_router

# Global spaCy model instance
nlp = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ML models on startup, cleanup on shutdown."""
    global nlp
    # Load spaCy model on startup
    nlp = spacy.load("en_core_web_sm")
    yield
    # Cleanup on shutdown
    nlp = None


app = FastAPI(
    title="Smart Resume & Job Fit Analyzer",
    description="AI-assisted, rule-based resume analysis with explainable scoring",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

# Add production origins from environment
import os
prod_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
for origin in prod_origins:
    origin = origin.strip().rstrip("/")
    if origin:
        origins.append(origin)

print(f"Allowed Origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "smart-resume-analyzer",
        "spacy_loaded": nlp is not None,
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Smart Resume & Job Fit Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Mount API router
app.include_router(api_router, prefix="/api")


def get_nlp():
    """Get the loaded spaCy model."""
    return nlp
