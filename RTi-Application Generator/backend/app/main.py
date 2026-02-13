"""
FastAPI Application Entry Point
AI-Powered Public Complaint & RTI Generator

Production-grade backend with:
- Rule-based intent classification (PRIMARY)
- Bounded NLP assistance (SECONDARY)
- Human-in-the-loop confirmation
- Privacy-first design (no database)
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from datetime import datetime
from loguru import logger
import sys

from app.config import get_settings
from app.middleware import (
    ErrorHandlingMiddleware,
    RequestLoggingMiddleware,
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    APIKeyMiddleware
)

# Import routers
from app.api.infer import router as infer_router
from app.api.draft import router as draft_router
from app.api.authority import router as authority_router
from app.api.download import router as download_router
from app.api.validate import router as validate_router
from app.api.enhance import router as enhance_router


# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

def configure_logging():
    """Configure loguru logging"""
    settings = get_settings()
    
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stdout,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # Add file handler if enabled
    if settings.LOG_TO_FILE:
        logger.add(
            settings.LOG_FILE_PATH,
            format=settings.LOG_FORMAT,
            level=settings.LOG_LEVEL,
            rotation="10 MB",
            retention="7 days",
            compression="gz"
        )
    
    logger.info(f"Logging configured: level={settings.LOG_LEVEL}")


# =============================================================================
# APPLICATION LIFESPAN
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    settings = get_settings()
    
    # Startup
    configure_logging()
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Pre-load NLP models in production
    if settings.ENVIRONMENT == "production":
        logger.info("Pre-loading NLP models...")
        try:
            from app.services.nlp.spacy_engine import get_nlp
            get_nlp()
            logger.info("spaCy model loaded")
            
            if settings.ENABLE_DISTILBERT:
                from app.services.nlp.distilbert_semantic import get_model
                get_model()
                logger.info("DistilBERT model loaded")
        except Exception as e:
            logger.warning(f"Model pre-loading failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# =============================================================================
# CREATE APPLICATION
# =============================================================================

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="""
    ## AI-Powered Public Complaint & RTI Generator API
    
    Helps Indian citizens generate legally correct:
    - **RTI Applications** (Right to Information Act, 2005)
    - **Public Complaints** to government departments
    
    ### Design Principles
    
    1. **Rules decide, AI assists** - Rule engine is primary, NLP only assists
    2. **Human confirmation mandatory** - Low confidence requires user verification
    3. **Privacy-first** - No database, stateless, nothing stored
    4. **No AI-generated legal text** - Templates are pre-written, AI only fills placeholders
    
    ### Control Flow
    
    ```
    User Input → Rule Engine → spaCy NLP → Confidence Gate → DistilBERT (if needed) → User Confirmation → Draft
    ```
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",  # Always enable in development
    redoc_url="/redoc",  # Always enable in development
    lifespan=lifespan
)


# =============================================================================
# MIDDLEWARE (Order matters - last added runs first)
# =============================================================================

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# API key authentication (optional)
app.add_middleware(APIKeyMiddleware)

# Rate limiting
app.add_middleware(
    RateLimitMiddleware,
    requests_per_window=settings.RATE_LIMIT_REQUESTS,
    window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS
)

# Request logging
app.add_middleware(RequestLoggingMiddleware)

# Error handling
app.add_middleware(ErrorHandlingMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# =============================================================================
# EXCEPTION HANDLERS
# =============================================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom handler for validation errors"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " → ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "message": "Request validation failed",
            "details": errors,
            "timestamp": datetime.now().isoformat()
        }
    )


# =============================================================================
# ROUTES
# =============================================================================

# Health check (not under /api prefix)
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for load balancers and monitoring.
    Returns application status and version.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now().isoformat()
    }


# API info
@app.get("/", tags=["Info"])
async def root():
    """API information and available endpoints"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "AI-Powered Public Complaint & RTI Generator",
        "documentation": "/docs" if settings.DEBUG else "Documentation disabled in production",
        "endpoints": {
            "inference": "/api/infer",
            "draft": "/api/draft",
            "authority": "/api/authority",
            "download": "/api/download",
            "validate": "/api/validate",
            "health": "/health"
        },
        "design_principles": [
            "Rules decide, AI assists",
            "Human confirmation mandatory for ambiguity",
            "Privacy-first (no database)",
            "No AI-generated legal text"
        ]
    }


# Include API routers
app.include_router(infer_router, prefix="/api", tags=["Inference"])
app.include_router(draft_router, prefix="/api", tags=["Draft"])
app.include_router(authority_router, prefix="/api", tags=["Authority"])
app.include_router(download_router, prefix="/api", tags=["Download"])
app.include_router(validate_router, prefix="/api", tags=["Validation"])
app.include_router(enhance_router, prefix="/api", tags=["LLM Enhancement"])


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
