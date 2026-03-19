"""
CivicFix Pydantic Schemas
Request/response models for API endpoints
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# --- Enums ---
class IssueType(str, Enum):
    POTHOLE = "Pothole"
    GARBAGE = "Garbage"
    BROKEN_STREETLIGHT = "Broken streetlight"
    WATER_LEAKAGE = "Water leakage"
    OTHER = "Other"


class ReportStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    RESOLVED = "resolved"
    REJECTED = "rejected"


# --- Auth Schemas ---
class UserCreate(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=6, max_length=128)
    display_name: Optional[str] = Field(None, max_length=100)


class UserLogin(BaseModel):
    email: str
    password: str


class OTPRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)


class OTPVerify(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    code: str = Field(..., min_length=6, max_length=6)
    password: str = Field(..., min_length=6, max_length=128)
    display_name: Optional[str] = Field(None, max_length=100)


class FirebaseLoginRequest(BaseModel):
    firebase_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    display_name: Optional[str] = None
    role: str = "user"


class UserResponse(BaseModel):
    id: str
    email: str
    display_name: Optional[str] = None
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Report Schemas ---
class ReportCreate(BaseModel):
    """Validated from form data, not JSON body."""
    issue_type: str
    description: str = Field(..., min_length=1, max_length=500)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timestamp: Optional[str] = None
    device_id: Optional[str] = None

    @field_validator("issue_type")
    @classmethod
    def validate_issue_type(cls, v):
        allowed = [e.value for e in IssueType]
        if v not in allowed:
            raise ValueError(f"issue_type must be one of: {', '.join(allowed)}")
        return v


class ReportResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    issue_type: str
    description: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    incident_date: Optional[datetime] = None
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    status: str
    complaint_text: Optional[str] = None
    admin_note: Optional[str] = None
    posted_to_x: bool
    x_post_id: Optional[str] = None
    resolved_image_url: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    resolved_note: Optional[str] = None
    declined_at: Optional[datetime] = None
    declined_by: Optional[str] = None
    decline_reason: Optional[str] = None
    is_fake: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReportCreateResponse(BaseModel):
    report_id: str
    complaint_text: str
    image_url: Optional[str] = None
    address: Optional[str] = None
    status: str = "pending"


class ReportListResponse(BaseModel):
    reports: List[ReportResponse]
    total: int
    page: int
    page_size: int


class PostToXResponse(BaseModel):
    posted_status: str
    tweet_id: Optional[str] = None
    mock_id: Optional[str] = None
    message: str


# --- Admin Schemas ---
class AdminUpdateReport(BaseModel):
    status: Optional[ReportStatus] = None
    admin_note: Optional[str] = Field(None, max_length=1000)


# --- Health ---
class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
    mock_mode: bool = True
    database: str = "connected"
