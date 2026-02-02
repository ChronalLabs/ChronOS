"""
LLM Enhancement API Router
============================

Provides controlled LLM-powered text improvement endpoints.

DESIGN PRINCIPLE:
    "Rules decide what is allowed. LLMs improve how it is expressed."

These endpoints ENHANCE existing content - they don't generate new legal content.
All enhancements are transparent and reversible.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from loguru import logger

from app.config import get_settings

router = APIRouter()
settings = get_settings()


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class EnhanceTextRequest(BaseModel):
    """Request for text enhancement"""
    text: str = Field(
        ...,
        min_length=10,
        max_length=10000,
        description="Text to enhance"
    )
    mode: str = Field(
        default="polish",
        description="Enhancement mode: polish, clarify, translate, tone_adjust"
    )
    target_language: Optional[str] = Field(
        default=None,
        description="Target language for translation (hindi)"
    )
    target_tone: Optional[str] = Field(
        default=None,
        description="Target tone: formal, assertive, neutral"
    )
    preserve_placeholders: bool = Field(
        default=True,
        description="Preserve [PLACEHOLDER] markers"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "I want information about road construction expenses in my area",
                "mode": "clarify"
            }
        }


class EnhanceTextResponse(BaseModel):
    """Response from text enhancement"""
    original_text: str
    enhanced_text: str
    was_enhanced: bool
    enhancement_mode: str
    changes_summary: str
    tokens_used: int
    model_used: str
    timestamp: datetime


class ClarifyIssueRequest(BaseModel):
    """Request to clarify an issue description"""
    description: str = Field(
        ...,
        min_length=20,
        max_length=5000,
        description="User's issue description"
    )
    category: Optional[str] = Field(
        None,
        description="Issue category for context (electricity, water, etc.)"
    )


class ClarifyIssueResponse(BaseModel):
    """Response with clarified issue"""
    original: str
    clarified: str
    was_clarified: bool
    suggestions: List[str]


class LLMStatusResponse(BaseModel):
    """LLM service status"""
    available: bool
    enabled: bool
    model: str
    features: List[str]


# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.get(
    "/llm/status",
    response_model=LLMStatusResponse,
    summary="Check LLM service status",
    description="Check if LLM enhancement features are available and enabled"
)
async def get_llm_status() -> LLMStatusResponse:
    """Check if LLM service is available"""
    try:
        from app.services.llm import is_llm_available
        available = is_llm_available()
    except Exception:
        available = False
    
    features = []
    if available:
        features = ["polish", "clarify", "translate", "tone_adjust"]
    
    return LLMStatusResponse(
        available=available,
        enabled=settings.FEATURE_LLM_ASSIST,
        model=settings.OPENAI_MODEL if available else "none",
        features=features
    )


@router.post(
    "/llm/enhance",
    response_model=EnhanceTextResponse,
    summary="Enhance text using LLM",
    description="""
    Enhance text using AI while preserving meaning and legal accuracy.
    
    **Modes:**
    - `polish`: Improve clarity and readability
    - `clarify`: Organize and clarify issue description
    - `translate`: Translate to Hindi (formal government language)
    - `tone_adjust`: Adjust formality level
    
    **Important:**
    - Original text is always preserved
    - LLM does not add new facts or legal claims
    - All changes are transparent
    """
)
async def enhance_text(request: EnhanceTextRequest) -> EnhanceTextResponse:
    """Enhance text using LLM"""
    
    if not settings.FEATURE_LLM_ASSIST:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM enhancement is disabled"
        )
    
    try:
        from app.services.llm import (
            enhance_draft_text, 
            clarify_issue_description,
            improve_formal_tone,
            translate_to_hindi_llm,
            is_llm_available
        )
        
        if not is_llm_available():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="LLM service not available. Check OPENAI_API_KEY."
            )
        
        # Route to appropriate enhancement function
        if request.mode == "clarify":
            result = await clarify_issue_description(request.text)
        elif request.mode == "translate":
            result = await translate_to_hindi_llm(request.text)
        elif request.mode == "tone_adjust":
            target_tone = request.target_tone or "formal"
            result = await improve_formal_tone(request.text, target_tone)
        else:  # default: polish
            result = await enhance_draft_text(
                draft_text=request.text,
                preserve_placeholders=request.preserve_placeholders
            )
        
        return EnhanceTextResponse(
            original_text=result.original_text,
            enhanced_text=result.enhanced_text,
            was_enhanced=result.was_enhanced,
            enhancement_mode=result.enhancement_mode,
            changes_summary=result.changes_summary,
            tokens_used=result.tokens_used,
            model_used=result.model_used,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"LLM enhancement failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Enhancement failed: {str(e)}"
        )


@router.post(
    "/llm/clarify-issue",
    response_model=ClarifyIssueResponse,
    summary="Clarify issue description",
    description="""
    Help clarify a user's issue description without changing facts.
    
    The LLM will:
    - Organize the text logically
    - Remove redundancy
    - Improve sentence structure
    
    The LLM will NOT:
    - Add facts or claims not present
    - Change the meaning
    - Add legal language
    """
)
async def clarify_issue(request: ClarifyIssueRequest) -> ClarifyIssueResponse:
    """Clarify an issue description"""
    
    if not settings.FEATURE_LLM_ASSIST:
        return ClarifyIssueResponse(
            original=request.description,
            clarified=request.description,
            was_clarified=False,
            suggestions=["LLM enhancement is disabled"]
        )
    
    try:
        from app.services.llm import clarify_issue_description, is_llm_available
        
        if not is_llm_available():
            return ClarifyIssueResponse(
                original=request.description,
                clarified=request.description,
                was_clarified=False,
                suggestions=["LLM service not available"]
            )
        
        result = await clarify_issue_description(
            user_description=request.description,
            category=request.category
        )
        
        suggestions = []
        if result.was_enhanced:
            suggestions.append("Your description has been organized for clarity")
            suggestions.append("Please verify all facts are accurate")
        else:
            suggestions.append(result.changes_summary)
        
        return ClarifyIssueResponse(
            original=result.original_text,
            clarified=result.enhanced_text,
            was_clarified=result.was_enhanced,
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"Issue clarification failed: {e}")
        return ClarifyIssueResponse(
            original=request.description,
            clarified=request.description,
            was_clarified=False,
            suggestions=["Clarification failed, using original text"]
        )
