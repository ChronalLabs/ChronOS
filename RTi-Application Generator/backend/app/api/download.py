"""
Document Download API Router
Exports documents in PDF, DOCX, XLSX formats.

DESIGN PRINCIPLE:
- Documents generated on-demand
- Streamed directly to user
- NO server-side storage (privacy by design)
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
from loguru import logger

from app.services.document_generator import get_document_generator
from app.config import get_settings

router = APIRouter()
settings = get_settings()


# =============================================================================
# REQUEST SCHEMAS
# =============================================================================

class ApplicantInfo(BaseModel):
    """Applicant information for document"""
    name: str = Field(..., min_length=2)
    address: str = Field(..., min_length=10)
    state: str
    district: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class AuthorityInfo(BaseModel):
    """Authority information for document"""
    department_name: str
    department_address: str
    designation: Optional[str] = None


class DownloadRequest(BaseModel):
    """Request body for document download"""
    draft_text: str = Field(
        ...,
        min_length=100,
        description="Complete draft text to convert to document"
    )
    document_type: str = Field(
        ...,
        description="Type of document (information_request, grievance, etc.)"
    )
    format: str = Field(
        ...,
        description="Output format: pdf, docx, xlsx"
    )
    applicant: ApplicantInfo
    authority: Optional[AuthorityInfo] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "draft_text": "To,\nThe Public Information Officer...",
                "document_type": "information_request",
                "format": "pdf",
                "applicant": {
                    "name": "Rahul Sharma",
                    "address": "123, Gandhi Nagar",
                    "state": "Rajasthan"
                }
            }
        }


# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.post(
    "/download",
    summary="Download document in specified format",
    description="""
    Generate and download document in specified format.
    
    **Supported Formats:**
    - `pdf` - Official submission format
    - `docx` - Editable Word document
    - `xlsx` - Tracking spreadsheet with draft content
    
    **Privacy:**
    - Document is generated in memory
    - Streamed directly to client
    - NOT stored on server
    """,
    responses={
        200: {
            "description": "Document file stream",
            "content": {
                "application/pdf": {},
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {},
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
            }
        },
        400: {"description": "Invalid format or input"},
        500: {"description": "Document generation failed"}
    }
)
async def download_document(request: DownloadRequest):
    """Generate and stream document file"""
    logger.info(f"Download request: format={request.format}, type={request.document_type}")
    
    try:
        # Validate format
        valid_formats = ["pdf", "docx", "xlsx"]
        format_lower = request.format.lower().strip()
        
        if format_lower not in valid_formats:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid format. Supported: {valid_formats}"
            )
        
        # Check XLSX feature flag
        if format_lower == "xlsx" and not settings.FEATURE_XLSX_EXPORT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="XLSX export is currently disabled"
            )
        
        # Prepare applicant details for XLSX
        applicant_details = {
            "name": request.applicant.name,
            "address": request.applicant.address,
            "state": request.applicant.state,
            "district": request.applicant.district,
            "phone": request.applicant.phone,
            "email": request.applicant.email
        }
        
        # Prepare authority details for XLSX
        authority_details = None
        if request.authority:
            authority_details = {
                "department": request.authority.department_name,
                "address": request.authority.department_address,
                "designation": request.authority.designation
            }
        
        # Metadata
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "document_type": request.document_type
        }
        
        # Generate document
        generator = get_document_generator()
        buffer, filename, content_type = generator.generate(
            format=format_lower,
            draft_text=request.draft_text,
            document_type=request.document_type,
            applicant_name=request.applicant.name,
            applicant_details=applicant_details,
            authority_details=authority_details,
            metadata=metadata
        )
        
        logger.info(f"Document generated: {filename}")
        
        # Stream response
        return StreamingResponse(
            buffer,
            media_type=content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Document-Type": request.document_type,
                "X-Generated-At": datetime.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Invalid request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Document generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document generation failed: {str(e)}"
        )


@router.post(
    "/download/pdf",
    summary="Download as PDF",
    description="Shortcut endpoint for PDF download"
)
async def download_pdf(request: DownloadRequest):
    """Generate and download PDF document"""
    request.format = "pdf"
    return await download_document(request)


@router.post(
    "/download/docx",
    summary="Download as DOCX",
    description="Shortcut endpoint for DOCX download"
)
async def download_docx(request: DownloadRequest):
    """Generate and download DOCX document"""
    request.format = "docx"
    return await download_document(request)


@router.post(
    "/download/xlsx",
    summary="Download as XLSX",
    description="Shortcut endpoint for XLSX tracking sheet download"
)
async def download_xlsx(request: DownloadRequest):
    """Generate and download XLSX tracking sheet"""
    request.format = "xlsx"
    return await download_document(request)


@router.get(
    "/download/formats",
    summary="List supported formats",
    description="Get list of supported download formats"
)
async def list_formats() -> Dict[str, Any]:
    """List supported download formats"""
    return {
        "formats": [
            {
                "id": "pdf",
                "name": "PDF Document",
                "extension": ".pdf",
                "mime_type": "application/pdf",
                "description": "Official submission format - non-editable",
                "recommended_for": "Official submission to government offices"
            },
            {
                "id": "docx",
                "name": "Word Document",
                "extension": ".docx",
                "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "description": "Editable document format",
                "recommended_for": "Making edits before printing"
            },
            {
                "id": "xlsx",
                "name": "Excel Spreadsheet",
                "extension": ".xlsx",
                "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "description": "Tracking sheet with draft content",
                "recommended_for": "Record keeping and tracking submissions",
                "enabled": settings.FEATURE_XLSX_EXPORT
            }
        ],
        "default": "pdf"
    }

