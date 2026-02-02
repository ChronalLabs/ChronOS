"""
Pydantic Schemas - Issue
"""

from pydantic import BaseModel
from typing import Optional, List


class IssueBase(BaseModel):
    """Base issue information"""
    description: str
    category: Optional[str] = None
    urgency: Optional[str] = "normal"  # normal, urgent, critical


class IssueAnalysis(BaseModel):
    """Analysis results for an issue"""
    category: str
    subcategory: Optional[str] = None
    departments: List[str]
    keywords: List[str]
    sentiment: str
    confidence: float


class IssueCreate(IssueBase):
    """Issue data for creating documents"""
    specific_request: Optional[str] = None
    time_period: Optional[str] = None
    previous_attempts: Optional[str] = None
