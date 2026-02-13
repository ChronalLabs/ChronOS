"""
Pydantic Schemas - Inference
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum


class IntentType(str, Enum):
    RTI = "rti"
    COMPLAINT = "complaint"
    APPEAL = "appeal"
    UNKNOWN = "unknown"


class DocumentType(str, Enum):
    INFORMATION_REQUEST = "information_request"
    RECORDS_REQUEST = "records_request"
    INSPECTION_REQUEST = "inspection_request"
    GRIEVANCE = "grievance"
    ESCALATION = "escalation"
    FOLLOW_UP = "follow_up"


class InferenceRequest(BaseModel):
    """Request for intent inference"""
    text: str
    language: str = "english"
    context: Optional[Dict[str, Any]] = None


class InferenceResult(BaseModel):
    """Result of intent inference"""
    intent: IntentType
    document_type: DocumentType
    confidence: float
    requires_confirmation: bool
    extracted_entities: Dict[str, List[str]]
    suggestions: List[str]
    legal_triggers: Dict[str, Any]
    explanation: str


class ConfidenceInfo(BaseModel):
    """Confidence information for UI display"""
    level: str  # high, medium, low, very_low
    score: float
    message: str
    show_alternatives: bool
