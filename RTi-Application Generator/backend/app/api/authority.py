"""
Authority Resolution API Router
Suggests appropriate government authorities.

DESIGN PRINCIPLE:
- Uses DETERMINISTIC rules for authority mapping
- AI is NOT used for guessing authorities
- spaCy entity hints may assist but don't decide
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from loguru import logger

from app.services.authority_resolver import (
    resolve_authority,
    get_all_categories,
    get_all_states,
    AuthorityLevel
)
from app.config import get_settings

router = APIRouter()
settings = get_settings()


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class AuthorityRequest(BaseModel):
    """Request for authority resolution"""
    issue_category: str = Field(
        ...,
        description="Category of issue: electricity, water, roads, education, health, police, land, transport, ration, pension, municipal, general"
    )
    state: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="State name"
    )
    district: Optional[str] = Field(
        None,
        max_length=50,
        description="District name for more specific resolution"
    )
    area: Optional[str] = Field(
        None,
        max_length=100,
        description="Local area/locality"
    )
    is_rti: bool = Field(
        default=True,
        description="True for RTI application, False for complaint"
    )
    extracted_entities: Optional[Dict[str, List[str]]] = Field(
        None,
        description="Entities extracted from text (optional hints)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "issue_category": "electricity",
                "state": "Rajasthan",
                "district": "Jaipur",
                "is_rti": True
            }
        }


class AuthorityInfo(BaseModel):
    """Information about a resolved authority"""
    name: str
    designation: str
    department: str
    level: str = Field(..., description="local, district, state, central")
    address: str
    rti_fee: int = 10
    notes: Optional[str] = None


class AuthorityMatch(BaseModel):
    """Authority match with confidence"""
    authority: AuthorityInfo
    confidence: float = Field(..., ge=0.0, le=1.0)
    match_reason: str
    is_primary: bool = False


class AuthorityResponse(BaseModel):
    """Response from authority resolution"""
    # Primary recommendation
    primary: Optional[AuthorityMatch] = Field(
        None,
        description="Primary recommended authority"
    )
    
    # All matches
    matches: List[AuthorityMatch] = Field(
        ...,
        description="All matched authorities in order of relevance"
    )
    
    # Category info
    category: str
    department: str
    
    # Suggestions
    suggestions: List[str] = Field(default_factory=list)
    
    # Flags
    requires_state_selection: bool = Field(
        default=False,
        description="True if state needs verification"
    )
    
    # Metadata
    timestamp: datetime


class CategoryInfo(BaseModel):
    """Information about an issue category"""
    id: str
    name: str
    description: str
    common_issues: List[str]


class StateInfo(BaseModel):
    """Information about a state"""
    name: str
    code: str


# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.post(
    "/authority",
    response_model=AuthorityResponse,
    summary="Resolve appropriate authority",
    description="""
    Resolves the appropriate government authority based on:
    - Issue category (electricity, water, roads, etc.)
    - State and district
    - Document type (RTI or Complaint)
    
    **Important:**
    - Uses deterministic rules, not AI guessing
    - For RTI: Always recommends PIO first
    - For Complaints: Recommends appropriate level based on issue
    """,
    responses={
        200: {"description": "Authority resolved successfully"},
        400: {"description": "Invalid category or state"},
        500: {"description": "Resolution failed"}
    }
)
async def suggest_authority(request: AuthorityRequest) -> AuthorityResponse:
    """
    Suggest appropriate authorities based on issue category and location.
    Uses deterministic mapping first, then semantic matching if needed.
    """
    logger.info(f"Authority request: category={request.issue_category}, state={request.state}, is_rti={request.is_rti}")
    
    try:
        # Validate category
        valid_categories = get_all_categories()
        category = request.issue_category.lower().strip()
        
        if category not in valid_categories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid issue_category. Valid options: {valid_categories}"
            )
        
        # Resolve authority
        result = resolve_authority(
            category=category,
            state=request.state,
            district=request.district,
            area=request.area,
            is_rti=request.is_rti,
            extracted_entities=request.extracted_entities
        )
        
        # Convert to response format
        matches = []
        for match in result.matches:
            auth_info = AuthorityInfo(
                name=match.authority.name,
                designation=match.authority.designation,
                department=match.authority.department,
                level=match.authority.level.value,
                address=match.authority.address_template,
                rti_fee=match.authority.rti_fee,
                notes=match.authority.notes
            )
            matches.append(AuthorityMatch(
                authority=auth_info,
                confidence=match.confidence,
                match_reason=match.match_reason,
                is_primary=match.is_primary
            ))
        
        # Build primary
        primary = None
        if result.primary:
            auth_info = AuthorityInfo(
                name=result.primary.authority.name,
                designation=result.primary.authority.designation,
                department=result.primary.authority.department,
                level=result.primary.authority.level.value,
                address=result.primary.authority.address_template,
                rti_fee=result.primary.authority.rti_fee,
                notes=result.primary.authority.notes
            )
            primary = AuthorityMatch(
                authority=auth_info,
                confidence=result.primary.confidence,
                match_reason=result.primary.match_reason,
                is_primary=True
            )
        
        response = AuthorityResponse(
            primary=primary,
            matches=matches,
            category=result.category,
            department=result.department,
            suggestions=result.suggestions,
            requires_state_selection=result.requires_state_selection,
            timestamp=datetime.now()
        )
        
        logger.info(f"Authority resolved: {len(matches)} matches, primary={primary.authority.designation if primary else 'None'}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authority resolution failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authority resolution failed: {str(e)}"
        )


@router.get(
    "/authority/categories",
    response_model=List[CategoryInfo],
    summary="List all issue categories",
    description="Get list of all supported issue categories with descriptions"
)
async def list_categories() -> List[CategoryInfo]:
    """List all supported issue categories"""
    categories = [
        CategoryInfo(
            id="electricity",
            name="Electricity",
            description="Power supply, billing, meters, transformers",
            common_issues=["Power outage", "High bills", "Meter issues", "New connection"]
        ),
        CategoryInfo(
            id="water",
            name="Water Supply",
            description="Water supply, pipelines, sewage, drainage",
            common_issues=["No water supply", "Contaminated water", "Pipeline leakage", "Drainage issues"]
        ),
        CategoryInfo(
            id="roads",
            name="Roads & Infrastructure",
            description="Roads, potholes, highways, footpaths",
            common_issues=["Potholes", "Road damage", "Street lights", "Footpath encroachment"]
        ),
        CategoryInfo(
            id="education",
            name="Education",
            description="Schools, colleges, admissions, certificates",
            common_issues=["Admission issues", "Fee problems", "Certificate delay", "Teacher absence"]
        ),
        CategoryInfo(
            id="health",
            name="Health",
            description="Hospitals, medical services, medicines",
            common_issues=["Poor treatment", "Medicine unavailability", "Staff behavior", "Facility issues"]
        ),
        CategoryInfo(
            id="police",
            name="Police",
            description="Law enforcement, FIR, safety",
            common_issues=["FIR not registered", "Harassment", "Delayed investigation", "Safety concerns"]
        ),
        CategoryInfo(
            id="land",
            name="Land & Revenue",
            description="Land records, property, mutations",
            common_issues=["Mutation delay", "Land disputes", "Registry issues", "Encroachment"]
        ),
        CategoryInfo(
            id="transport",
            name="Transport & RTO",
            description="Licenses, registration, traffic",
            common_issues=["License delay", "Registration issues", "Permit problems", "Traffic violations"]
        ),
        CategoryInfo(
            id="ration",
            name="Ration & PDS",
            description="Ration cards, fair price shops",
            common_issues=["Ration card issues", "Shop not giving ration", "Quality problems", "Aadhaar linking"]
        ),
        CategoryInfo(
            id="pension",
            name="Pension",
            description="Pension disbursement, retirement benefits",
            common_issues=["Pension not received", "Amount incorrect", "Delay in processing", "Documentation"]
        ),
        CategoryInfo(
            id="municipal",
            name="Municipal/Civic",
            description="Civic amenities, sanitation, property tax",
            common_issues=["Garbage collection", "Sanitation", "Property tax", "Building permission"]
        ),
        CategoryInfo(
            id="general",
            name="General/Other",
            description="Other government services",
            common_issues=["Service delay", "Staff behavior", "Documentation", "General grievance"]
        ),
    ]
    
    return categories


@router.get(
    "/authority/states",
    response_model=List[StateInfo],
    summary="List all states",
    description="Get list of all supported Indian states and union territories"
)
async def list_states() -> List[StateInfo]:
    """List all supported states"""
    states = get_all_states()
    return [StateInfo(name=s["name"], code=s["code"]) for s in states]

