from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import dataset, analysis, report

app = FastAPI(
    title="AI Data Intelligence Platform API",
    description="Backend API for Dataset Cleaning and Analysis System",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API is running"}

app.include_router(dataset.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(report.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
