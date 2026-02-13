"""
Pytest fixtures for Smart Resume Analyzer tests.
"""
import pytest
from fastapi.testclient import TestClient
import tempfile
import os

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing."""
    return """
    John Doe
    Software Engineer
    john.doe@email.com | (555) 123-4567
    
    EXPERIENCE
    
    Senior Software Engineer - TechCorp Inc.
    January 2021 - Present
    - Developed microservices using Python and FastAPI
    - Built data pipelines with Docker and Kubernetes
    - Led a team of 5 engineers on AWS infrastructure
    
    EDUCATION
    
    Master of Science in Computer Science
    Stanford University, 2018
    
    SKILLS
    Python, JavaScript, React, Node.js, PostgreSQL, MongoDB, AWS, Docker, Kubernetes
    """


@pytest.fixture
def sample_jd_text():
    """Sample job description for testing."""
    return """
    Senior Software Engineer
    
    Requirements:
    - 5+ years of experience with Python
    - Strong experience with React and Node.js
    - Experience with AWS and Docker
    - Knowledge of PostgreSQL or MongoDB
    
    Nice to have:
    - Experience with Kubernetes
    - Machine learning background
    """


@pytest.fixture
def temp_docx_file(sample_resume_text):
    """Create a temporary DOCX file for testing."""
    from docx import Document
    
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as f:
        doc = Document()
        for line in sample_resume_text.strip().split('\n'):
            doc.add_paragraph(line.strip())
        doc.save(f.name)
        yield f.name
    
    # Cleanup
    if os.path.exists(f.name):
        os.remove(f.name)


@pytest.fixture
def temp_pdf_file(sample_resume_text):
    """Create a temporary PDF file for testing."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        pytest.skip("reportlab not installed")
    
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        c = canvas.Canvas(f.name, pagesize=letter)
        y = 750
        for line in sample_resume_text.strip().split('\n'):
            if line.strip():
                c.drawString(72, y, line.strip())
                y -= 15
        c.save()
        yield f.name
    
    # Cleanup
    if os.path.exists(f.name):
        os.remove(f.name)
