from fastapi import APIRouter

router = APIRouter(tags=["Report"])

@router.get("/report")
def get_report():
    return {
        "reportId": "rep_123456",
        "downloadUrl": "/api/report/download/pdf",
        "summary": "Data cleaning improved consistency by 15%."
    }
