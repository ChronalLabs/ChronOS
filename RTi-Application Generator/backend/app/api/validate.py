"""
Quality Scoring API
Endpoint for validating and scoring RTI/Complaint drafts.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from loguru import logger

from ..services.validation_engine import get_validator, ValidationResult, ValidationIssue

router = APIRouter(prefix="/validate", tags=["Validation"])


class ValidationRequest(BaseModel):
    """Request for validation"""
    information_sought: str
    time_period: Optional[str] = None
    department: Optional[str] = None
    record_type: Optional[str] = None
    applicant_name: Optional[str] = None
    applicant_address: Optional[str] = None
    applicant_state: Optional[str] = None
    document_type: str = "information_request"
    language: str = "english"


class ValidationIssueResponse(BaseModel):
    """Single validation issue"""
    code: str
    message: str
    severity: str  # error, warning, info
    category: str
    field: Optional[str] = None
    suggestion: Optional[str] = None


class ValidationResponse(BaseModel):
    """Validation response"""
    is_valid: bool
    can_generate: bool
    score: int  # 0-100
    grade: str  # A, B, C, D, F
    scores_breakdown: Dict[str, int]
    issues: List[ValidationIssueResponse]
    summary: str
    summary_hi: str


class EditValidationRequest(BaseModel):
    """Request to validate user edits"""
    original_text: str
    edited_text: str
    document_type: str = "information_request"


class EditValidationResponse(BaseModel):
    """Response for edit validation"""
    is_safe: bool
    issues: List[ValidationIssueResponse]
    warnings: List[str]


def score_to_grade(score: int) -> str:
    """Convert numeric score to letter grade"""
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "F"


def generate_summary(result: ValidationResult, language: str = "english") -> tuple:
    """Generate human-readable summary"""
    error_count = sum(1 for i in result.issues if i.severity.value == "error")
    warning_count = sum(1 for i in result.issues if i.severity.value == "warning")
    
    if language == "hindi":
        if result.score >= 90:
            summary = "उत्कृष्ट! आपका RTI अनुरोध अच्छी तरह से संरचित और पूर्ण है।"
        elif result.score >= 75:
            summary = f"अच्छा। कुछ सुधारों के साथ ({warning_count} चेतावनी), आपका अनुरोध तैयार है।"
        elif result.score >= 60:
            summary = f"औसत। {warning_count} मुद्दे हैं जिन्हें ठीक करने से सफलता की संभावना बढ़ेगी।"
        elif result.score >= 40:
            summary = f"कमजोर। {error_count} त्रुटियां और {warning_count} चेतावनियां हैं। कृपया सुधार करें।"
        else:
            summary = f"अपूर्ण। {error_count} गंभीर त्रुटियां हैं। आगे बढ़ने से पहले इन्हें ठीक करें।"
        summary_hi = summary
    else:
        if result.score >= 90:
            summary = "Excellent! Your RTI request is well-structured and complete."
            summary_hi = "उत्कृष्ट! आपका RTI अनुरोध अच्छी तरह से संरचित और पूर्ण है।"
        elif result.score >= 75:
            summary = f"Good. With minor improvements ({warning_count} warnings), your request is ready."
            summary_hi = f"अच्छा। कुछ सुधारों के साथ ({warning_count} चेतावनी), आपका अनुरोध तैयार है।"
        elif result.score >= 60:
            summary = f"Fair. {warning_count} issues found that could improve success rate."
            summary_hi = f"औसत। {warning_count} मुद्दे हैं जिन्हें ठीक करने से सफलता की संभावना बढ़ेगी।"
        elif result.score >= 40:
            summary = f"Weak. {error_count} errors and {warning_count} warnings found. Please review."
            summary_hi = f"कमजोर। {error_count} त्रुटियां और {warning_count} चेतावनियां हैं। कृपया सुधार करें।"
        else:
            summary = f"Incomplete. {error_count} critical errors found. Fix these before proceeding."
            summary_hi = f"अपूर्ण। {error_count} गंभीर त्रुटियां हैं। आगे बढ़ने से पहले इन्हें ठीक करें।"
    
    return summary, summary_hi


@router.post("/rti", response_model=ValidationResponse)
async def validate_rti_request(request: ValidationRequest):
    """
    Validate an RTI request before draft generation.
    
    Returns:
    - is_valid: True if no blocking errors
    - can_generate: True if safe to generate
    - score: Quality score 0-100
    - grade: Letter grade (A-F)
    - issues: List of validation issues
    - summary: Human-readable summary
    """
    try:
        validator = get_validator()
        
        result = validator.validate(
            information_sought=request.information_sought,
            time_period=request.time_period or "",
            department=request.department or "",
            record_type=request.record_type or "",
            applicant_name=request.applicant_name or "",
            applicant_address=request.applicant_address or "",
            applicant_state=request.applicant_state or "",
        )
        
        # Convert issues to response format
        issues_response = [
            ValidationIssueResponse(
                code=issue.code,
                message=issue.message if request.language == "english" else issue.message_hi,
                severity=issue.severity.value,
                category=issue.category.value,
                field=issue.field,
                suggestion=issue.suggestion if request.language == "english" else issue.suggestion_hi
            )
            for issue in result.issues
        ]
        
        summary, summary_hi = generate_summary(result, request.language)
        
        return ValidationResponse(
            is_valid=result.is_valid,
            can_generate=result.can_generate,
            score=result.score,
            grade=score_to_grade(result.score),
            scores_breakdown=result.scores_breakdown,
            issues=issues_response,
            summary=summary,
            summary_hi=summary_hi
        )
        
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@router.post("/edit", response_model=EditValidationResponse)
async def validate_edit(request: EditValidationRequest):
    """
    Validate user edits to a draft.
    
    Checks if critical legal elements have been removed
    and warns about potentially unsafe changes.
    """
    try:
        validator = get_validator()
        
        is_safe, issues = validator.validate_edit(
            original_text=request.original_text,
            edited_text=request.edited_text,
            document_type=request.document_type
        )
        
        issues_response = [
            ValidationIssueResponse(
                code=issue.code,
                message=issue.message,
                severity=issue.severity.value,
                category=issue.category.value,
                field=issue.field,
                suggestion=issue.suggestion
            )
            for issue in issues
        ]
        
        warnings = [issue.message for issue in issues if issue.severity.value in ["error", "warning"]]
        
        return EditValidationResponse(
            is_safe=is_safe,
            issues=issues_response,
            warnings=warnings
        )
        
    except Exception as e:
        logger.error(f"Edit validation error: {e}")
        raise HTTPException(status_code=500, detail=f"Edit validation failed: {str(e)}")


@router.get("/health")
async def validation_health():
    """Health check for validation service"""
    return {"status": "ok", "service": "validation_engine"}
