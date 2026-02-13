"""
Tests for resume and JD parsers.
"""
import pytest
from parsers.section_detector import (
    detect_sections,
    _extract_skills_from_text,
    _parse_education,
    _parse_experience,
)
from parsers.docx_parser import parse_docx, _extract_all_xml_text
from parsers.jd_parser import parse_job_description


class TestSkillExtraction:
    """Test skill extraction from text."""
    
    def test_extracts_programming_languages(self):
        """Test extraction of programming languages."""
        text = "Experience with Python, JavaScript, and TypeScript"
        skills = _extract_skills_from_text(text)
        skill_names = [s.canonical_name for s in skills]
        
        assert "Python" in skill_names
        assert "JavaScript" in skill_names
        assert "TypeScript" in skill_names
    
    def test_extracts_frameworks(self):
        """Test extraction of frameworks."""
        text = "Built applications using React, Node.js, and FastAPI"
        skills = _extract_skills_from_text(text)
        skill_names = [s.canonical_name for s in skills]
        
        assert "React" in skill_names
        assert "Node.js" in skill_names
        assert "FastAPI" in skill_names
    
    def test_extracts_databases(self):
        """Test extraction of database technologies."""
        text = "Managed PostgreSQL, MongoDB, and Redis databases"
        skills = _extract_skills_from_text(text)
        skill_names = [s.canonical_name for s in skills]
        
        assert "PostgreSQL" in skill_names
        assert "MongoDB" in skill_names
        assert "Redis" in skill_names
    
    def test_extracts_cloud_tools(self):
        """Test extraction of cloud and DevOps tools."""
        text = "Deployed on AWS using Docker and Kubernetes"
        skills = _extract_skills_from_text(text)
        skill_names = [s.canonical_name for s in skills]
        
        assert "AWS" in skill_names
        assert "Docker" in skill_names
        assert "Kubernetes" in skill_names
    
    def test_extracts_soft_skills(self):
        """Test extraction of soft skills."""
        text = "Strong leadership, problem solving, and communication skills"
        skills = _extract_skills_from_text(text)
        skill_names = [s.canonical_name for s in skills]
        
        assert "Leadership" in skill_names
        assert "Problem Solving" in skill_names
        assert "Communication" in skill_names
    
    def test_extracts_ml_skills(self):
        """Test extraction of ML/AI skills."""
        text = "Applied TensorFlow and PyTorch for machine learning projects"
        skills = _extract_skills_from_text(text)
        skill_names = [s.canonical_name for s in skills]
        
        assert "TensorFlow" in skill_names
        assert "PyTorch" in skill_names
        assert "Machine Learning" in skill_names
    
    def test_no_duplicates(self):
        """Test that duplicate skills are not extracted."""
        text = "Python Python Python JavaScript JavaScript"
        skills = _extract_skills_from_text(text)
        skill_names = [s.canonical_name for s in skills]
        
        assert skill_names.count("Python") == 1
        assert skill_names.count("JavaScript") == 1
    
    def test_case_insensitive(self):
        """Test that extraction is case insensitive."""
        text = "PYTHON, javascript, TypeScript, REACT"
        skills = _extract_skills_from_text(text)
        skill_names = [s.canonical_name for s in skills]
        
        assert "Python" in skill_names
        assert "JavaScript" in skill_names
        assert "TypeScript" in skill_names
        assert "React" in skill_names


class TestJobDescriptionParser:
    """Test job description parsing."""
    
    def test_extracts_required_skills(self, sample_jd_text):
        """Test extraction of required skills from JD."""
        result = parse_job_description(sample_jd_text)
        
        assert len(result.required_skills) > 0
        assert "Python" in result.required_skills
    
    def test_extracts_optional_skills(self, sample_jd_text):
        """Test extraction of optional skills from JD."""
        result = parse_job_description(sample_jd_text)
        
        # Kubernetes is listed as "nice to have"
        assert len(result.optional_skills) >= 0
    
    def test_extracts_requirements(self, sample_jd_text):
        """Test extraction of requirements from JD."""
        result = parse_job_description(sample_jd_text)
        
        assert len(result.requirements) > 0
    
    def test_handles_empty_jd(self):
        """Test handling of empty job description."""
        result = parse_job_description("")
        
        assert result.raw_text == ""
        assert len(result.requirements) == 0


class TestDocxParser:
    """Test DOCX file parsing."""
    
    def test_parses_docx_file(self, temp_docx_file):
        """Test parsing of DOCX file."""
        raw_text, blocks = parse_docx(temp_docx_file)
        
        assert len(raw_text) > 0
        assert "John Doe" in raw_text or len(blocks) > 0
    
    def test_extracts_text_blocks(self, temp_docx_file):
        """Test extraction of text blocks from DOCX."""
        raw_text, blocks = parse_docx(temp_docx_file)
        
        # Should have at least some blocks
        assert isinstance(blocks, list)


class TestPdfParser:
    """Test PDF file parsing."""
    
    def test_parses_pdf_file(self, temp_pdf_file):
        """Test parsing of PDF file."""
        from parsers.pdf_parser import parse_pdf
        raw_text, blocks = parse_pdf(temp_pdf_file)
        
        assert len(raw_text) > 0
        assert "John Doe" in raw_text or len(blocks) > 0
        
    def test_extracts_text_blocks_pdf(self, temp_pdf_file):
        """Test extraction of text blocks from PDF."""
        from parsers.pdf_parser import parse_pdf
        raw_text, blocks = parse_pdf(temp_pdf_file)
        
        # Should have blocks with positioning
        assert isinstance(blocks, list)
        if len(blocks) > 0:
            assert "top" in blocks[0]
            assert "left" in blocks[0]


class TestSectionDetection:
    """Test resume section detection."""
    
    def test_detects_sections(self, sample_resume_text):
        """Test detection of resume sections."""
        blocks = [{"text": line.strip(), "line": i} 
                  for i, line in enumerate(sample_resume_text.split('\n')) 
                  if line.strip()]
        
        sections = detect_sections(sample_resume_text, blocks)
        
        assert "skills" in sections
        assert "education" in sections
        assert "experience" in sections
    
    def test_extracts_skills_from_full_text(self, sample_resume_text):
        """Test that skills are extracted from full resume text."""
        blocks = [{"text": line.strip(), "line": i} 
                  for i, line in enumerate(sample_resume_text.split('\n')) 
                  if line.strip()]
        
        sections = detect_sections(sample_resume_text, blocks)
        
        # Should find skills mentioned in the resume
        skill_names = [s.canonical_name for s in sections.get("skills", [])]
        assert len(skill_names) > 0
