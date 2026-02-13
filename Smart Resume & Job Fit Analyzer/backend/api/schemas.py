"""
Pydantic models for API request/response types.
All schemas match the system design document exactly.
"""
from pydantic import BaseModel, Field

from typing import Optional, Literal
from enum import Enum
from datetime import datetime


# ============================================================================
# Enums
# ============================================================================

class MatchType(str, Enum):
    """Skill match classification."""
    MATCHED = "matched"
    PARTIAL = "partial"
    MISSING = "missing"


class ConfidenceLevel(str, Enum):
    """Confidence level for matches."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SkillCategory(str, Enum):
    """Skill category types."""
    PROGRAMMING_LANGUAGES = "programming_languages"
    FRAMEWORKS = "frameworks"
    DATABASES = "databases"
    TOOLS = "tools"
    CLOUD = "cloud"
    SOFT_SKILLS = "soft_skills"
    CERTIFICATIONS = "certifications"
    HEALTHCARE = "healthcare"
    OTHER = "other"


class SkillPriority(str, Enum):
    """Skill priority from job description."""
    REQUIRED = "required"
    OPTIONAL = "optional"


# ============================================================================
# Resume Parsing Schemas
# ============================================================================

class EducationEntry(BaseModel):
    """Education section entry."""
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    source_text: str = Field(..., description="Original text from resume")


class ExperienceEntry(BaseModel):
    """Work experience section entry."""
    company: str
    title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: str
    responsibilities: list[str] = []
    source_text: str = Field(..., description="Original text from resume")


class ProjectEntry(BaseModel):
    """Project section entry."""
    name: str
    description: str
    technologies: list[str] = []
    url: Optional[str] = None
    source_text: str = Field(..., description="Original text from resume")


class CertificationEntry(BaseModel):
    """Certification/credential entry."""
    name: str
    issuer: str = ""
    date: Optional[str] = None
    credential_id: Optional[str] = None
    url: Optional[str] = None
    source_text: str = Field(..., description="Original text from resume")


class ExtractedSkill(BaseModel):
    """Skill extracted from resume."""
    name: str
    canonical_name: str
    category: SkillCategory
    confidence: ConfidenceLevel
    source_text: str = Field(..., description="Text where skill was found")
    line_number: Optional[int] = None


class ParsedResume(BaseModel):
    """Complete parsed resume structure."""
    raw_text: str
    education: list[EducationEntry] = []
    experience: list[ExperienceEntry] = []
    projects: list[ProjectEntry] = []
    certifications: list[CertificationEntry] = []
    skills: list[ExtractedSkill] = []
    contact_info: dict = {}
    parsing_warnings: list[str] = []


class ResumeUploadResponse(BaseModel):
    """Response after resume upload and parsing."""
    session_id: str
    filename: str
    parsed_resume: ParsedResume
    message: str = "Resume parsed successfully"


# ============================================================================
# Job Description Schemas
# ============================================================================

class JDRequirement(BaseModel):
    """Single requirement from job description."""
    text: str
    skills: list[str] = []
    priority: SkillPriority = SkillPriority.REQUIRED


class ParsedJobDescription(BaseModel):
    """Parsed job description structure."""
    raw_text: str
    title: Optional[str] = None
    company: Optional[str] = None
    requirements: list[JDRequirement] = []
    required_skills: list[str] = []
    optional_skills: list[str] = []
    experience_requirements: Optional[str] = None
    education_requirements: Optional[str] = None


class JobDescriptionRequest(BaseModel):
    """Request to analyze a job description."""
    job_description: str = Field(..., min_length=50, description="Job description text")


class JobDescriptionResponse(BaseModel):
    """Response after JD parsing."""
    session_id: str
    parsed_jd: ParsedJobDescription
    message: str = "Job description parsed successfully"


# ============================================================================
# Evaluation Schemas
# ============================================================================

class SkillMatch(BaseModel):
    """Individual skill match result with evidence."""
    skill_name: str
    canonical_name: str
    match_type: MatchType
    confidence: ConfidenceLevel
    jd_priority: SkillPriority
    evidence: Optional[str] = Field(None, description="Resume snippet showing skill")
    line_number: Optional[int] = None
    match_score: float = Field(..., ge=0.0, le=1.0)


class ScoreBreakdown(BaseModel):
    """Breakdown of how score was calculated."""
    required_skills_score: float = Field(..., ge=0.0, le=100.0)
    optional_skills_score: float = Field(..., ge=0.0, le=100.0)
    experience_depth_score: float = Field(..., ge=0.0, le=100.0)
    education_match_score: float = Field(..., ge=0.0, le=100.0)
    weights_applied: dict = {}
    penalties_applied: list[str] = []


class ImprovementSuggestion(BaseModel):
    """Single improvement suggestion."""
    category: str
    priority: int = Field(..., ge=1, le=5, description="1=highest priority")
    suggestion: str
    evidence_gap: Optional[str] = None
    affected_skills: list[str] = []


class ExperienceSignals(BaseModel):
    """Signals extracted from experience section."""
    relevant_years: float = 0.0
    ownership_strength: str = "Medium"  # High, Medium, Low
    leadership_signals: list[str] = []
    responsibility_alignment: str = ""

class EvaluationResult(BaseModel):
    """Complete evaluation result."""
    job_fit_score: int = Field(..., ge=0, le=100)
    confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM
    score_breakdown: ScoreBreakdown
    skill_matches: list[SkillMatch] = []
    matched_count: int = 0
    partial_count: int = 0
    missing_count: int = 0
    explanation: str
    experience_signals: Optional[ExperienceSignals] = None
    improvement_suggestions: list[ImprovementSuggestion] = []
    advisory_notice: str = Field(
        default="This analysis is advisory only and should not be used as the sole basis for hiring decisions.",
        description="Required disclaimer"
    )


class EvaluationRequest(BaseModel):
    """Request to evaluate resume against JD."""
    session_id: str
    resume_session_id: Optional[str] = None
    jd_session_id: Optional[str] = None


class EvaluationResponse(BaseModel):
    """Response containing evaluation results."""
    session_id: str
    result: EvaluationResult
    evaluated_at: datetime
    message: str = "Evaluation completed successfully"


# ============================================================================
# Session Management
# ============================================================================

class SessionData(BaseModel):
    """Session data for tracking analysis."""
    session_id: str
    resume: Optional[ParsedResume] = None
    job_description: Optional[ParsedJobDescription] = None
    evaluation: Optional[EvaluationResult] = None
    created_at: datetime
    updated_at: datetime


# ============================================================================
# Export Schemas
# ============================================================================

class ExportRequest(BaseModel):
    """Request to export results."""
    session_id: str
    format: Literal["pdf", "json"] = "pdf"


class ExportResponse(BaseModel):
    """Response with export file information."""
    session_id: str
    download_url: str
    format: str
    expires_at: datetime
