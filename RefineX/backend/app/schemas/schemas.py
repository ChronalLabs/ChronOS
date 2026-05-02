from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class UploadResponse(BaseModel):
    success: bool
    fileName: str
    rows: int

class DatasetPreviewResponse(BaseModel):
    columns: List[str]
    rows: List[Dict[str, Any]]
    totalRows: int

class Stats(BaseModel):
    totalRecords: int
    missingValues: int
    duplicateRows: int

class Charts(BaseModel):
    pieChart: List[Dict[str, Any]]
    barChart: List[Dict[str, Any]]
    lineChart: List[Dict[str, Any]]

class AnalysisResponse(BaseModel):
    stats: Stats
    charts: Charts
    insights: List[str]
