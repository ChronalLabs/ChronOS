"""
Middleware for the application.
Includes error handling, logging, and rate limiting.
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
from datetime import datetime
from collections import defaultdict
import asyncio
from loguru import logger

from app.config import get_settings


# =============================================================================
# ERROR HANDLING MIDDLEWARE
# =============================================================================

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Global error handling middleware.
    Catches all unhandled exceptions and returns consistent error responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            # Re-raise HTTP exceptions (they have their own handlers)
            raise exc
        except Exception as exc:
            # Log the error
            logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
            
            # Return generic error response
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "internal_server_error",
                    "message": "An unexpected error occurred. Please try again later.",
                    "timestamp": datetime.now().isoformat(),
                    "path": str(request.url.path)
                }
            )


# =============================================================================
# LOGGING MIDDLEWARE
# =============================================================================

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs all incoming requests and outgoing responses.
    Sanitizes sensitive data before logging.
    """
    
    SENSITIVE_HEADERS = {"authorization", "x-api-key", "cookie"}
    SENSITIVE_PATHS = {"/health"}  # Don't log health checks
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Skip logging for certain paths
        if request.url.path in self.SENSITIVE_PATHS:
            return await call_next(request)
        
        # Start timer
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"client={request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = (time.time() - start_time) * 1000
        
        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"status={response.status_code} duration={duration:.2f}ms"
        )
        
        # Add timing header
        response.headers["X-Process-Time-Ms"] = f"{duration:.2f}"
        
        return response


# =============================================================================
# RATE LIMITING MIDDLEWARE
# =============================================================================

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiting.
    For production, use Redis-based rate limiting.
    """
    
    def __init__(self, app, requests_per_window: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.request_counts = defaultdict(list)
        self._lock = asyncio.Lock()
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier (IP address)"""
        # Check for forwarded header (behind proxy)
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        if request.client:
            return request.client.host
        
        return "unknown"
    
    async def dispatch(self, request: Request, call_next: Callable):
        settings = get_settings()
        
        # Skip if rate limiting is disabled
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
        
        # Skip rate limiting for health checks
        if request.url.path == "/health":
            return await call_next(request)
        
        client_id = self._get_client_id(request)
        current_time = time.time()
        
        async with self._lock:
            # Clean old entries
            window_start = current_time - self.window_seconds
            self.request_counts[client_id] = [
                t for t in self.request_counts[client_id] if t > window_start
            ]
            
            # Check rate limit
            if len(self.request_counts[client_id]) >= self.requests_per_window:
                logger.warning(f"Rate limit exceeded for client: {client_id}")
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": "rate_limit_exceeded",
                        "message": f"Too many requests. Limit: {self.requests_per_window} requests per {self.window_seconds} seconds.",
                        "retry_after_seconds": self.window_seconds
                    },
                    headers={
                        "Retry-After": str(self.window_seconds),
                        "X-RateLimit-Limit": str(self.requests_per_window),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(window_start + self.window_seconds))
                    }
                )
            
            # Record this request
            self.request_counts[client_id].append(current_time)
            remaining = self.requests_per_window - len(self.request_counts[client_id])
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_window)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response


# =============================================================================
# SECURITY HEADERS MIDDLEWARE
# =============================================================================

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds security headers to all responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Don't cache API responses
        if request.url.path.startswith("/api"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
            response.headers["Pragma"] = "no-cache"
        
        return response


# =============================================================================
# API KEY AUTHENTICATION MIDDLEWARE (Optional)
# =============================================================================

class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Optional API key authentication.
    Enable via API_KEY_ENABLED config.
    """
    
    # Paths that don't require API key
    PUBLIC_PATHS = {"/health", "/docs", "/redoc", "/openapi.json"}
    
    async def dispatch(self, request: Request, call_next: Callable):
        settings = get_settings()
        
        # Skip if API key auth is disabled
        if not settings.API_KEY_ENABLED:
            return await call_next(request)
        
        # Skip for public paths
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)
        
        # Check for API key
        api_key = request.headers.get(settings.API_KEY_HEADER)
        
        if not api_key:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": "missing_api_key",
                    "message": f"API key required. Provide via {settings.API_KEY_HEADER} header."
                }
            )
        
        if api_key not in settings.API_KEYS:
            logger.warning(f"Invalid API key attempt from {request.client.host if request.client else 'unknown'}")
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "error": "invalid_api_key",
                    "message": "Invalid API key."
                }
            )
        
        return await call_next(request)
