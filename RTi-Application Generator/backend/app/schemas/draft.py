"""
Pydantic Schemas - Draft
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class DraftRequest(BaseModel):
    """Request for draft generation"""
    applicant_name: str
    applicant_address: str
    applicant_state: str
    applicant_phone: Optional[str] = None
    applicant_email: Optional[str] = None
    
    issue_description: str
    specific_request: Optional[str] = None
    
    document_type: str
    language: str = "english"
    tone: str = "neutral"  # neutral, formal, assertive


class DraftResponse(BaseModel):
    """Generated draft response"""
    draft_text: str
    document_type: str
    language: str
    
    # Metadata
    generated_at: datetime
    template_used: str
    word_count: int
    
    # For user review
    editable_sections: Dict[str, str]
    placeholders_filled: Dict[str, str]


class DraftEdit(BaseModel):
    """User edits to draft"""
    draft_text: str
    edited_sections: Dict[str, str]
    user_approved: bool = False
