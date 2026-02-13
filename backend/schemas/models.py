"""
Pydantic models for API request/response schemas
"""

from typing import Optional
from pydantic import BaseModel


class PolicyInput(BaseModel):
    """Input schema for simulation endpoint"""
    night_shifts: bool
    safety_level: str  # "low", "standard", "high"
    urgency: str       # "standard", "high"
    labor: str         # "standard", "increased"
    traffic: str       # "basic", "advanced"


class PolicyTextInput(BaseModel):
    """Input schema for ML analysis endpoints"""
    text: str
    policy_name: Optional[str] = "Uploaded Policy"
