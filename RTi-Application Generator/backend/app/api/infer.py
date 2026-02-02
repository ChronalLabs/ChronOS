"""
Inference API Router
Handles intent detection and NLP analysis.

CONTROL FLOW:
User Input → Rule Engine → spaCy NLP → Confidence Gate → DistilBERT (if required) → Response

This endpoint NEVER makes final decisions - it provides suggestions with confidence scores.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from loguru import logger

from app.services.inference_orchestrator import run_inference, IntentType, DocumentType
from app.services.nlp.confidence_gate import ConfidenceLevel
from app.utils.text_sanitizer import warn_about_pii, clean_input
from app.config import get_settings

router = APIRouter()
settings = get_settings()


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class InferenceRequest(BaseModel):
    """Request body for inference endpoint"""
    text: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="User's issue description or query"
    )
    language: str = Field(
        default="english",
        description="Language of input (english, hindi)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "I want to know the expenditure details of road construction in my area from January 2024 to December 2024",
                "language": "english"
            }
        }


class ExtractedEntities(BaseModel):
    """Entities extracted from user text"""
    organizations: List[str] = Field(default_factory=list, alias="ORG")
    locations: List[str] = Field(default_factory=list, alias="GPE")
    dates: List[str] = Field(default_factory=list, alias="DATE")
    persons: List[str] = Field(default_factory=list, alias="PERSON")
    money: List[str] = Field(default_factory=list, alias="MONEY")
    
    class Config:
        populate_by_name = True


class LegalTriggers(BaseModel):
    """Legal triggers detected in text"""
    rti_sections: List[Dict[str, str]] = Field(default_factory=list)
    grievance_markers: List[Dict[str, str]] = Field(default_factory=list)
    suggested_citations: List[str] = Field(default_factory=list)


class DepartmentMatch(BaseModel):
    """Department mapping result"""
    category: str
    departments: List[str]
    confidence: float


class ConfidenceInfo(BaseModel):
    """Confidence information for UI display"""
    score: float = Field(..., ge=0.0, le=1.0)
    level: str = Field(..., description="high, medium, low, very_low")
    requires_confirmation: bool
    message: str


class PIIWarning(BaseModel):
    """PII detection warnings"""
    has_pii: bool
    warnings: List[str] = Field(default_factory=list)
    types_found: List[str] = Field(default_factory=list)


class InferenceResponse(BaseModel):
    """Response from inference endpoint"""
    # Primary results
    intent: str = Field(..., description="Detected intent: rti, complaint, appeal, unknown")
    document_type: str = Field(..., description="Suggested document type")
    
    # Confidence information
    confidence: ConfidenceInfo
    
    # Extracted data
    extracted_entities: Dict[str, List[str]]
    key_phrases: List[str]
    
    # Legal analysis
    legal_triggers: LegalTriggers
    
    # Department mapping
    department_mapping: DepartmentMatch | None
    
    # Sentiment
    sentiment: str = Field(..., description="urgent, frustrated, neutral")
    
    # Suggestions for user
    suggestions: List[str]
    
    # Transparency
    explanation: str
    decision_path: List[str]
    
    # PII warnings
    pii_warnings: PIIWarning
    
    # Metadata
    timestamp: datetime
    processing_time_ms: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "intent": "rti",
                "document_type": "information_request",
                "confidence": {
                    "score": 0.85,
                    "level": "medium",
                    "requires_confirmation": False,
                    "message": "Medium confidence (85%) - please verify"
                },
                "extracted_entities": {
                    "DATE": ["January 2024", "December 2024"],
                    "GPE": ["my area"]
                },
                "key_phrases": ["expenditure details", "road construction"],
                "suggestions": ["Consider specifying the exact location"],
                "explanation": "Decision made with medium confidence (85%). Path: Rule Engine → RTI keywords matched",
                "decision_path": ["Rule Engine", "RTI keywords (3 matches)"]
            }
        }


# =============================================================================
# API ENDPOINT
# =============================================================================

@router.post(
    "/infer",
    response_model=InferenceResponse,
    summary="Analyze user input and infer document type",
    description="""
    Analyzes user input text to determine:
    - Intent (RTI application, Complaint, Appeal)
    - Document type
    - Relevant entities (names, dates, organizations)
    - Department suggestions
    
    **Control Flow:**
    1. Rule Engine (keyword matching) - PRIMARY
    2. spaCy NLP (entity extraction)
    3. Confidence Gate (threshold checking)
    4. DistilBERT (only if confidence is low)
    
    **Important:** This endpoint provides SUGGESTIONS. The user must confirm the intent.
    """,
    responses={
        200: {"description": "Successful inference"},
        400: {"description": "Invalid input"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def infer_intent(request: InferenceRequest) -> InferenceResponse:
    """
    Analyze user input and infer document type and intent.
    Uses rule engine first, then NLP if needed.
    """
    import time
    start_time = time.time()
    
    logger.info(f"Inference request received, text length: {len(request.text)}")
    
    try:
        # Clean input
        cleaned_text = clean_input(request.text)
        
        if len(cleaned_text) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input text too short after cleaning. Please provide more details."
            )
        
        # Check for PII
        pii_result = warn_about_pii(cleaned_text)
        
        # Run inference
        result = run_inference(cleaned_text, request.language)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Map confidence level to string
        confidence_level_map = {
            ConfidenceLevel.HIGH: "high",
            ConfidenceLevel.MEDIUM: "medium",
            ConfidenceLevel.LOW: "low",
            ConfidenceLevel.VERY_LOW: "very_low"
        }
        
        # Build confidence message
        confidence_messages = {
            "high": f"High confidence ({result.confidence:.0%}) - auto-applied",
            "medium": f"Medium confidence ({result.confidence:.0%}) - please verify",
            "low": f"Low confidence ({result.confidence:.0%}) - please select from options",
            "very_low": f"Very low confidence ({result.confidence:.0%}) - manual input recommended"
        }
        
        confidence_level = confidence_level_map.get(result.confidence_level, "medium")
        
        # Build department mapping
        dept_mapping = None
        if result.department_mapping and result.department_mapping.get("primary_category"):
            dept_mapping = DepartmentMatch(
                category=result.department_mapping["primary_category"],
                departments=result.department_mapping.get("primary_departments", []),
                confidence=result.department_mapping["matches"][0]["confidence"] if result.department_mapping.get("matches") else 0.5
            )
        
        # Build response
        response = InferenceResponse(
            intent=result.intent.value,
            document_type=result.document_type.value,
            confidence=ConfidenceInfo(
                score=result.confidence,
                level=confidence_level,
                requires_confirmation=result.requires_confirmation,
                message=confidence_messages[confidence_level]
            ),
            extracted_entities=result.extracted_entities,
            key_phrases=result.key_phrases,
            legal_triggers=LegalTriggers(
                rti_sections=result.legal_triggers.get("rti_sections", []),
                grievance_markers=result.legal_triggers.get("grievance_markers", []),
                suggested_citations=result.legal_triggers.get("suggested_citations", [])
            ),
            department_mapping=dept_mapping,
            sentiment=result.sentiment,
            suggestions=result.suggestions,
            explanation=result.explanation,
            decision_path=result.decision_path,
            pii_warnings=PIIWarning(
                has_pii=pii_result["has_pii"],
                warnings=pii_result.get("warnings", []),
                types_found=pii_result.get("types_found", [])
            ),
            timestamp=datetime.now(),
            processing_time_ms=processing_time
        )
        
        logger.info(f"Inference completed: intent={result.intent.value}, confidence={result.confidence:.2f}, time={processing_time:.2f}ms")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Inference failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference processing failed: {str(e)}"
        )

