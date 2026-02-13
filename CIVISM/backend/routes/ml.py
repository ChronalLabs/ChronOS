"""
ML Analysis API Routes
"""

import io
from fastapi import APIRouter, HTTPException, UploadFile, File

from schemas import PolicyTextInput
from services import MLService

router = APIRouter(prefix="/ml", tags=["ML Analysis"])

# Initialize ML service (singleton)
ml_service = MLService()


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file"""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_content))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse DOCX: {str(e)}")


def extract_text_from_doc(file_content: bytes) -> str:
    """Extract text from DOC file (legacy Word format)"""
    # DOC format is complex - try using docx library as fallback
    # For true .doc support, you'd need additional tools like antiword
    raise HTTPException(
        status_code=400, 
        detail="Legacy .doc format is not supported. Please convert to .docx or use a PDF/TXT file."
    )


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and extract text from PDF, DOCX, or TXT files.
    Returns the extracted text content.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    filename = file.filename.lower()
    content = await file.read()
    
    try:
        if filename.endswith('.txt'):
            text = content.decode('utf-8')
        elif filename.endswith('.pdf'):
            text = extract_text_from_pdf(content)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(content)
        elif filename.endswith('.doc'):
            text = extract_text_from_doc(content)
        else:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file type. Please upload TXT, PDF, or DOCX files."
            )
        
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Could not extract text from file. The file may be empty or corrupted.")
        
        return {
            "success": True,
            "filename": file.filename,
            "text": text,
            "character_count": len(text)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/status")
async def get_status():
    """Check ML models status"""
    return ml_service.get_status()


@router.post("/analyze")
async def analyze_policy_text(input_data: PolicyTextInput):
    """
    Full ML pipeline analysis on policy text.
    Returns comprehensive analysis from all ML tasks.
    """
    try:
        return ml_service.full_analysis(
            text=input_data.text,
            policy_name=input_data.policy_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-intent")
async def extract_intent(input_data: PolicyTextInput):
    """Extract policy intent and key concepts"""
    try:
        results = ml_service.extract_intent(input_data.text)
        return {"success": True, **results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-entities")
async def extract_entities(input_data: PolicyTextInput):
    """Extract named entities from policy"""
    try:
        results = ml_service.extract_entities(input_data.text)
        return {"success": True, "entities": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-ambiguity")
async def analyze_ambiguity(input_data: PolicyTextInput):
    """Analyze ambiguity in policy text"""
    try:
        results = ml_service.analyze_ambiguity(input_data.text)
        return {
            "success": True,
            "score": results["score"],
            "trust_level": results["trust_level"],
            "by_severity": results["by_severity"],
            "findings": [
                {"phrase": f["phrase"], "severity": f["severity"], "context": f["context"]}
                for f in results["findings"][:10]
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/classify")
async def classify_policy(input_data: PolicyTextInput):
    """Classify policy focus (speed vs safety)"""
    try:
        results = ml_service.classify_policy(input_data.text)
        return {
            "success": True,
            "primary_classification": results["primary_classification"],
            "confidence": results["confidence"],
            "recommendation": results["recommendation"],
            "all_scores": results["all_scores"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
