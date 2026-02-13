"""
CIVISIM Backend - Main Application Entry Point
Clean architecture with modular routes and services
"""

import os
import socket

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import simulation_router, ml_router


def create_app() -> FastAPI:
    """Application factory pattern for creating FastAPI app"""
    app = FastAPI(
        title="CIVISIM Backend",
        description="Construction Policy Simulation & ML Analysis Platform",
        version="1.0.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register routes
    app.include_router(simulation_router)
    app.include_router(ml_router)
    
    return app


# Create app instance
app = create_app()


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {
        "status": "CIVISIM Online",
        "version": "1.0.0",
        "ml_enabled": True
    }


# ===== Server Utilities =====

def _is_port_available(port: int) -> bool:
    """Check if a port is available for binding"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("0.0.0.0", port))
            return True
        except OSError:
            return False


def _pick_port(preferred: int, attempts: int = 10) -> int:
    """Find an available port, starting from preferred"""
    for offset in range(attempts):
        port = preferred + offset
        if _is_port_available(port):
            return port
    raise RuntimeError("Could not find a free port for CIVISIM backend")


if __name__ == "__main__":
    import uvicorn
    
    preferred_port = int(os.getenv("CIVISIM_PORT") or os.getenv("PORT") or 8000)
    port = _pick_port(preferred_port)
    
    if port != preferred_port:
        print(f"[civisim-backend] Port {preferred_port} busy, using {port}")
    
    print(f"🚀 Starting CIVISIM Backend on port {port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=port)