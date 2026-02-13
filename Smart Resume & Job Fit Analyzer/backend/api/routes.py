"""
API endpoints for Smart Resume & Job Fit Analyzer.
All endpoints follow the system design document.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
import uuid
import os
from typing import Optional

from .schemas import (
    ResumeUploadResponse,
    ParsedResume,
    JobDescriptionRequest,
    JobDescriptionResponse,
    ParsedJobDescription,
    EvaluationRequest,
    EvaluationResponse,
    EvaluationResult,
    ExportResponse,
    SessionData,
)
from services.session_manager import session_manager

router = APIRouter(tags=["analysis"])

# Upload directory
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())


@router.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse a resume file (PDF or DOCX).
    
    - Accepts PDF or DOCX files only
    - Returns parsed resume data with sections identified
    - Creates a session for subsequent operations
    """
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    file_ext = file.filename.lower().split(".")[-1]
    if file_ext not in ["pdf", "docx"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF and DOCX files are accepted."
        )
    
    # Save uploaded file
    session_id = generate_session_id()
    file_path = os.path.join(UPLOAD_DIR, f"{session_id}.{file_ext}")
    
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        logger.info(f"Saved file to: {file_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Parse the resume
    try:
        from parsers import parse_resume
        parsed_resume = parse_resume(file_path, file_ext)
        logger.info(f"Parsed resume - Skills count: {len(parsed_resume.skills)}")
        logger.info(f"Raw text length: {len(parsed_resume.raw_text)}")
    except Exception as e:
        # Cleanup on failure
        if os.path.exists(file_path):
            os.remove(file_path)
        logger.error(f"Parse error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")
    
    # Store session data
    now = datetime.now()
    session = SessionData(
        session_id=session_id,
        resume=parsed_resume,
        created_at=now,
        updated_at=now,
    )
    session_manager.save_session(session)
    
    # Cleanup old sessions in background
    session_manager.cleanup_old_sessions()
    
    return ResumeUploadResponse(
        session_id=session_id,
        filename=file.filename,
        parsed_resume=parsed_resume,
    )


@router.post("/analyze-jd", response_model=JobDescriptionResponse)
async def analyze_job_description(request: JobDescriptionRequest, session_id: Optional[str] = None):
    """
    Parse and analyze a job description.
    """
    # Use existing session or create new
    current_session_id = session_id if session_id else generate_session_id()
    
    session = None
    if session_id:
        session = session_manager.get_session(session_id)
        if not session and session_id:
             # If provided session ID invalid, create new one
             current_session_id = generate_session_id()
             session = None

    # Parse the job description
    try:
        from parsers import parse_job_description
        parsed_jd = parse_job_description(request.job_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse job description: {str(e)}")
    
    # Update or create session
    now = datetime.now()
    if session:
        session.job_description = parsed_jd
        session.updated_at = now
    else:
        session = SessionData(
            session_id=current_session_id,
            job_description=parsed_jd,
            created_at=now,
            updated_at=now,
        )
    
    session_manager.save_session(session)
    
    return JobDescriptionResponse(
        session_id=current_session_id,
        parsed_jd=parsed_jd,
    )


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_resume(request: EvaluationRequest):
    """
    Run rule-based evaluation of resume against job description.
    """
    session_id = request.session_id
    
    # Get session data
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Validate required data exists
    if session.resume is None:
        raise HTTPException(status_code=400, detail="Resume not yet uploaded for this session")
    if session.job_description is None:
        raise HTTPException(status_code=400, detail="Job description not yet analyzed for this session")
    
    # Run evaluation
    try:
        from rules import evaluate
        result = evaluate(session.resume, session.job_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
    
    # Update session
    now = datetime.now()
    session.evaluation = result
    session.updated_at = now
    session_manager.save_session(session)
    
    return EvaluationResponse(
        session_id=session_id,
        result=result,
        evaluated_at=now,
    )


@router.get("/results/{session_id}", response_model=EvaluationResponse)
async def get_results(session_id: str):
    """
    Retrieve evaluation results for a session.
    """
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.evaluation is None:
        raise HTTPException(status_code=404, detail="No evaluation results available for this session")
    
    return EvaluationResponse(
        session_id=session_id,
        result=session.evaluation,
        evaluated_at=session.updated_at,
    )


@router.get("/export/{session_id}")
async def export_results(session_id: str, format: str = "pdf"):
    """
    Export evaluation results as PDF or JSON.
    """
    from fastapi.responses import FileResponse
    
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.evaluation is None:
        raise HTTPException(status_code=404, detail="No evaluation results available to export")
    
    if format == "pdf":
        # Generate PDF report
        # Note: We need to implement pdf_export module
        try:
            # Check if implemented
            from exports.pdf_export import generate_pdf_report
        except ImportError:
             raise HTTPException(status_code=501, detail="PDF export not yet implemented")

        export_dir = os.path.join(UPLOAD_DIR, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        pdf_path = os.path.join(export_dir, f"{session_id}_report.pdf")
        generate_pdf_report(session, pdf_path)
        
        return FileResponse(
            path=pdf_path,
            filename=f"resume_analysis_report.pdf",
            media_type="application/pdf",
        )
    else:
        # Return JSON format
        return {
            "session_id": session_id,
            "evaluation": session.evaluation,
            "resume_skills_count": len(session.resume.skills) if session.resume else 0,
            "exported_at": datetime.now().isoformat(),
        }


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Get full session data including resume, JD, and evaluation.
    """
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session and associated data.
    """
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Delete uploaded file if exists
    for ext in ["pdf", "docx"]:
        file_path = os.path.join(UPLOAD_DIR, f"{session_id}.{ext}")
        if os.path.exists(file_path):
            os.remove(file_path)
    
    session_manager.delete_session(session_id)
    
    return {"message": "Session deleted successfully"}


@router.put("/session/{session_id}/resume", response_model=SessionData)
async def update_resume(session_id: str, resume: ParsedResume):
    """
    Update parsed resume data in an active session.
    Allows user corrections (Human-in-the-Loop).
    """
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Update resume data
    session.resume = resume
    session.updated_at = datetime.now()
    session_manager.save_session(session)
    
    return session
