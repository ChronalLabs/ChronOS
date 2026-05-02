from fastapi import APIRouter, UploadFile, File
from app.schemas.schemas import UploadResponse, DatasetPreviewResponse
import random

router = APIRouter(tags=["Dataset"])

@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    # Mock upload logic
    return {
        "success": True,
        "fileName": file.filename,
        "rows": random.randint(1000, 5000)
    }

@router.get("/preview", response_model=DatasetPreviewResponse)
def get_dataset_preview():
    # Mock data preview
    columns = ["id", "age", "income", "score", "status"]
    rows = [
        {"id": 1, "age": 25, "income": 50000, "score": 85, "status": "active"},
        {"id": 2, "age": 34, "income": 75000, "score": 92, "status": "active"},
        {"id": 3, "age": 28, "income": 40000, "score": 75, "status": "inactive"},
        {"id": 4, "age": 45, "income": 120000, "score": 88, "status": "active"},
        {"id": 5, "age": 22, "income": 30000, "score": 60, "status": "inactive"}
    ]
    return {
        "columns": columns,
        "rows": rows,
        "totalRows": 1500
    }
