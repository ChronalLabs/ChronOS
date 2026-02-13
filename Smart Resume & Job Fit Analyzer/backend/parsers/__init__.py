"""
Parsers package for Smart Resume & Job Fit Analyzer.
Provides unified interface for parsing resumes and job descriptions.
"""
from .pdf_parser import parse_pdf
from .docx_parser import parse_docx
from .section_detector import detect_sections
from .jd_parser import parse_job_description


def parse_resume(file_path: str, file_type: str):
    """
    Unified resume parsing interface.
    
    Args:
        file_path: Path to the resume file
        file_type: File extension ('pdf' or 'docx')
    
    Returns:
        ParsedResume object with all sections identified
    """
    from api.schemas import ParsedResume, ExtractedSkill, SkillCategory, ConfidenceLevel
    
    # Extract raw text based on file type
    if file_type == "pdf":
        raw_text, text_blocks = parse_pdf(file_path)
    elif file_type == "docx":
        raw_text, text_blocks = parse_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    # Detect sections
    sections = detect_sections(raw_text, text_blocks)
    
    # Debug logging
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"[PARSE DEBUG] File: {file_path}")
    logger.info(f"[PARSE DEBUG] Text blocks count: {len(text_blocks)}")
    logger.info(f"[PARSE DEBUG] Skills: {len(sections.get('skills', []))}")
    logger.info(f"[PARSE DEBUG] Experience: {len(sections.get('experience', []))}")
    logger.info(f"[PARSE DEBUG] Education: {len(sections.get('education', []))}")
    
    # Log sample blocks for debugging
    for i, block in enumerate(text_blocks[:10]):
        left = block.get('left', 0)
        text = block.get('text', '')[:40]
        logger.info(f"[BLOCK {i}] left={left:.0f} | {text}")
    
    # Build parsed resume
    parsed = ParsedResume(
        raw_text=raw_text,
        education=sections.get("education", []),
        experience=sections.get("experience", []),
        projects=sections.get("projects", []),
        skills=sections.get("skills", []),
        contact_info=sections.get("contact_info", {}),
        parsing_warnings=sections.get("warnings", []),
    )
    
    return parsed


__all__ = [
    "parse_resume",
    "parse_pdf",
    "parse_docx",
    "detect_sections",
    "parse_job_description",
]
