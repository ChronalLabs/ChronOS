from fastapi import APIRouter
from app.schemas.schemas import AnalysisResponse

router = APIRouter(tags=["Analysis"])

@router.get("/analyze", response_model=AnalysisResponse)
def get_analysis():
    # Dummy analysis data
    return {
        "stats": {
            "totalRecords": 1500,
            "missingValues": 120,
            "duplicateRows": 15
        },
        "charts": {
            "pieChart": [{"name": "Active", "value": 800}, {"name": "Inactive", "value": 700}],
            "barChart": [{"name": "Jan", "value": 400}, {"name": "Feb", "value": 300}, {"name": "Mar", "value": 500}],
            "lineChart": [{"name": "2024-01-01", "value": 10}, {"name": "2024-02-01", "value": 20}]
        },
        "insights": [
            "Age correlates strongly with income.",
            "10% of rows contain missing data in 'score'."
        ]
    }
