"""
Draft Generation API Router
Creates document drafts from user input.

DESIGN PRINCIPLE:
- Templates are pre-written by legal experts
- AI ONLY fills placeholders with user-provided/extracted data
- NO generative AI for legal content
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
from loguru import logger

from app.services.draft_assembler import get_draft_assembler, DocumentType
from app.services.inference_orchestrator import IntentType
from app.services.nlp import translate_to_hindi
from app.utils.text_sanitizer import clean_input, warn_about_pii
from app.utils.tone import suggest_tone
from app.config import get_settings

router = APIRouter()
settings = get_settings()


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class ApplicantDetails(BaseModel):
    """Applicant information for document generation"""
    name: str = Field(..., min_length=2, max_length=100, description="Full name of applicant")
    address: str = Field(..., min_length=10, max_length=500, description="Complete address")
    state: str = Field(..., min_length=2, max_length=50, description="State name")
    district: Optional[str] = Field(None, max_length=50, description="District name")
    phone: Optional[str] = Field(None, pattern=r'^[6-9]\d{9}$', description="10-digit mobile number")
    email: Optional[EmailStr] = Field(None, description="Email address")


class IssueDetails(BaseModel):
    """Issue/grievance details"""
    description: str = Field(
        ...,
        min_length=20,
        max_length=5000,
        description="Detailed description of issue"
    )
    specific_request: Optional[str] = Field(
        None,
        max_length=2000,
        description="Specific information/action requested"
    )
    time_period: Optional[str] = Field(
        None,
        max_length=200,
        description="Time period for information sought"
    )
    category: Optional[str] = Field(
        None,
        description="Issue category (electricity, water, roads, etc.)"
    )


class AuthorityDetails(BaseModel):
    """Target authority details"""
    department_name: str = Field(
        default="The Concerned Department",
        description="Name of department"
    )
    department_address: str = Field(
        default="[Department Address]",
        description="Department address"
    )
    designation: Optional[str] = Field(
        None,
        description="Designation of authority (PIO, Commissioner, etc.)"
    )


class DraftRequest(BaseModel):
    """Request body for draft generation"""
    # Document type (required)
    document_type: str = Field(
        ...,
        description="Type: information_request, records_request, inspection_request, grievance, escalation, follow_up"
    )
    
    # Applicant info
    applicant: ApplicantDetails
    
    # Issue details
    issue: IssueDetails
    
    # Authority (optional - can be auto-resolved)
    authority: Optional[AuthorityDetails] = None
    
    # Preferences
    language: str = Field(default="english", description="Document language")
    tone: str = Field(
        default="neutral",
        description="Document tone: neutral, formal, assertive"
    )
    
    # Additional context
    additional_context: Optional[Dict[str, str]] = Field(
        None,
        description="Additional fields: location, impact, start_date, previous_attempts, reference_number"
    )
    
    # LLM Enhancement Options (NEW)
    enable_llm_enhancement: bool = Field(
        default=True,
        description="Enable AI-powered text enhancement (polish, clarify)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_type": "information_request",
                "applicant": {
                    "name": "Rahul Sharma",
                    "address": "123, Gandhi Nagar, Near Bus Stand",
                    "state": "Rajasthan",
                    "district": "Jaipur",
                    "phone": "9876543210",
                    "email": "rahul@example.com"
                },
                "issue": {
                    "description": "I want to know the expenditure details of road construction work in my locality",
                    "specific_request": "Please provide itemized expenditure, contractor details, and completion timeline",
                    "time_period": "January 2024 to December 2024",
                    "category": "roads"
                },
                "authority": {
                    "department_name": "Public Works Department",
                    "department_address": "PWD Office, Jaipur",
                    "designation": "Public Information Officer"
                },
                "tone": "formal"
            }
        }


class PlaceholderInfo(BaseModel):
    """Information about filled/missing placeholders"""
    filled: Dict[str, str]
    missing: List[str]


class DraftResponse(BaseModel):
    """Response containing generated draft"""
    # Draft content
    draft_text: str = Field(..., description="Complete draft document text")
    
    # Document info
    document_type: str
    template_used: str
    language: str
    
    # Metadata
    word_count: int
    generated_at: datetime
    
    # Placeholder info
    placeholders: PlaceholderInfo
    
    # Editable sections (for frontend highlighting)
    editable_sections: Dict[str, str]
    
    # Warnings
    warnings: List[str] = Field(default_factory=list)
    
    # Suggestions
    suggestions: List[str] = Field(default_factory=list)
    
    # LLM Enhancement Info (NEW)
    llm_enhanced: bool = Field(default=False, description="Whether LLM enhancement was applied")
    original_draft: Optional[str] = Field(None, description="Original rule-based draft before LLM enhancement")
    enhancement_summary: Optional[str] = Field(None, description="Summary of LLM changes")


# =============================================================================
# API ENDPOINT
# =============================================================================

@router.post(
    "/draft",
    response_model=DraftResponse,
    summary="Generate document draft",
    description="""
    Generates a document draft by filling pre-approved legal templates with user data.
    
    **Supported Document Types:**
    - `information_request` - Standard RTI application
    - `records_request` - Request for certified copies
    - `inspection_request` - Request to inspect records/works
    - `grievance` - Public complaint/grievance
    - `escalation` - Escalation of unresolved complaint
    - `follow_up` - Follow-up on pending complaint
    
    **Important:**
    - Templates are legally vetted and fixed
    - AI does NOT generate legal text
    - User must review draft before download
    """,
    responses={
        200: {"description": "Draft generated successfully"},
        400: {"description": "Invalid document type or input"},
        422: {"description": "Validation error"},
        500: {"description": "Draft generation failed"}
    }
)
async def generate_draft(request: DraftRequest) -> DraftResponse:
    """
    Generate a document draft based on user input and document type.
    Uses templates and fills in extracted/provided data.
    """
    logger.info(f"Draft request: type={request.document_type}, applicant={request.applicant.name}")
    
    try:
        # Validate document type
        try:
            doc_type = DocumentType(request.document_type)
        except ValueError:
            valid_types = [dt.value for dt in DocumentType]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid document_type. Valid options: {valid_types}"
            )
        
        # Clean inputs
        cleaned_description = clean_input(request.issue.description)
        cleaned_specific = clean_input(request.issue.specific_request) if request.issue.specific_request else None
        
        # Check for PII warnings
        pii_check = warn_about_pii(cleaned_description)
        warnings = pii_check.get("warnings", [])
        
        # Prepare authority details
        authority = request.authority or AuthorityDetails()
        
        # Prepare additional context
        additional = request.additional_context or {}
        
        # Suggest tone if not specified
        suggested_tone = request.tone
        if request.tone == "neutral" and request.issue.category:
            # Check if assertive tone might be more appropriate
            urgency = additional.get("urgency", "normal")
            suggested = suggest_tone(request.issue.category, urgency)
            if suggested != "neutral":
                warnings.append(f"Suggested tone: '{suggested}' based on issue type")
        
        # Get assembler
        assembler = get_draft_assembler()
        
        # Normalize language
        language = request.language.lower() if request.language else "english"
        if language not in ["english", "hindi"]:
            language = "english"
        
        # Translation logic
        final_description = cleaned_description
        final_specific = cleaned_specific
        
        if language == "hindi":
             try:
                 from app.utils.language_normalizer import detect_language
                 # Try to detect if input is English and wants Hindi output
                 if detect_language(cleaned_description) != "hi":
                     logger.info("Translating description to Hindi")
                     trans_desc = translate_to_hindi(cleaned_description)
                     if trans_desc:
                         final_description = trans_desc
                         
                 if cleaned_specific and detect_language(cleaned_specific) != "hi":
                     logger.info("Translating specific request to Hindi")
                     trans_spec = translate_to_hindi(cleaned_specific)
                     if trans_spec:
                         final_specific = trans_spec
             except Exception as e:
                 logger.error(f"Translation preprocessing failed: {e}")
                 # Fallback to original text matches behavior if translation service fails
        
        # Generate draft
        result = assembler.assemble_draft(
            document_type=doc_type,
            applicant_name=request.applicant.name,
            applicant_address=request.applicant.address,
            applicant_state=request.applicant.state,
            issue_description=final_description,
            applicant_phone=request.applicant.phone,
            applicant_email=request.applicant.email,
            department_name=authority.department_name,
            department_address=authority.department_address,
            authority_designation=authority.designation,
            specific_request=final_specific,
            time_period=request.issue.time_period,
            issue_category=request.issue.category,
            additional_context=additional,
            tone=request.tone,
            language=language
        )
        
        # Build suggestions
        suggestions = []
        
        if result["placeholders_missing"]:
            suggestions.append(f"Some fields need your attention: {', '.join(result['placeholders_missing'][:3])}")
        
        if doc_type in [DocumentType.INFORMATION_REQUEST, DocumentType.RECORDS_REQUEST, DocumentType.INSPECTION_REQUEST]:
            if language == "hindi":
                suggestions.append("आरटीआई शुल्क रु. 10/- आईपीओ/डीडी/ऑनलाइन के माध्यम से संलग्न करें")
                suggestions.append("अपने रिकॉर्ड के लिए इस आवेदन की एक प्रति रखें")
            else:
                suggestions.append("Remember to attach RTI fee of Rs. 10/- via IPO/DD/Online")
                suggestions.append("Keep a copy of this application for your records")
        else:
            if language == "hindi":
                suggestions.append("अनुवर्ती कार्रवाई के लिए पावती/संदर्भ संख्या रखें")
            else:
                suggestions.append("Keep the acknowledgment/reference number for follow-up")
        
        # =====================================================================
        # LLM ENHANCEMENT (Optional - Rules first, then LLM polishes)
        # =====================================================================
        llm_enhanced = False
        original_draft = None
        enhancement_summary = None
        final_draft_text = result["draft_text"]
        
        if request.enable_llm_enhancement and settings.FEATURE_LLM_ASSIST:
            try:
                from app.services.llm import enhance_draft_text, is_llm_available
                
                if is_llm_available():
                    logger.info("Applying LLM enhancement to rule-based draft...")
                    
                    # Preserve original for transparency
                    original_draft = result["draft_text"]
                    
                    # Enhance the draft
                    enhancement = await enhance_draft_text(
                        draft_text=result["draft_text"],
                        language=language,
                        tone=request.tone,
                        preserve_placeholders=True
                    )
                    
                    if enhancement.was_enhanced:
                        final_draft_text = enhancement.enhanced_text
                        llm_enhanced = True
                        enhancement_summary = enhancement.changes_summary
                        suggestions.append("✨ AI-enhanced for better clarity (original preserved)")
                        logger.info(f"LLM enhancement applied: {enhancement.tokens_used} tokens")
                    else:
                        logger.info(f"LLM enhancement skipped: {enhancement.changes_summary}")
                        
            except Exception as e:
                logger.warning(f"LLM enhancement failed (using rule-based): {e}")
                # Continue with rule-based draft - LLM failure is non-critical
        
        # Build response
        response = DraftResponse(
            draft_text=final_draft_text,
            document_type=result["document_type"],
            template_used=result["template_used"],
            language=request.language,
            word_count=len(final_draft_text.split()),
            generated_at=datetime.fromisoformat(result["generated_at"]),
            placeholders=PlaceholderInfo(
                filled=result["placeholders_filled"],
                missing=result["placeholders_missing"]
            ),
            editable_sections=result["editable_sections"],
            warnings=warnings,
            suggestions=suggestions,
            llm_enhanced=llm_enhanced,
            original_draft=original_draft if llm_enhanced else None,
            enhancement_summary=enhancement_summary
        )
        
        logger.info(f"Draft generated successfully: {result['word_count']} words")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Draft generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Draft generation failed: {str(e)}"
        )


@router.get(
    "/draft/templates",
    summary="List available templates",
    description="Get list of all available document templates"
)
async def list_templates() -> Dict[str, Any]:
    """List all available document templates"""
    assembler = get_draft_assembler()
    
    templates = {
        "rti": [
            {"type": "information_request", "name": "RTI - Information Request", "description": "Standard RTI application under Section 6(1)"},
            {"type": "records_request", "name": "RTI - Records/Copies Request", "description": "Request for certified copies of documents"},
            {"type": "inspection_request", "name": "RTI - Inspection Request", "description": "Request to inspect records or works"}
        ],
        "complaint": [
            {"type": "grievance", "name": "Public Grievance", "description": "New complaint/grievance"},
            {"type": "escalation", "name": "Escalation", "description": "Escalate unresolved complaint"},
            {"type": "follow_up", "name": "Follow-up", "description": "Follow-up on pending complaint"}
        ]
    }
    
    return {
        "templates": templates,
        "available": assembler.list_available_templates()
    }

