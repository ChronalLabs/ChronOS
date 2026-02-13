"""
Helper module to generate synthetic resume PDFs for regression testing.
Uses reportlab to create deterministic test files.
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_test_pdfs(output_dir: str):
    """Generate a suite of test PDFs."""
    os.makedirs(output_dir, exist_ok=True)
    
    _create_standard_resume(os.path.join(output_dir, "standard.pdf"))
    _create_two_column_resume(os.path.join(output_dir, "two_column.pdf"))
    _create_messy_resume(os.path.join(output_dir, "messy.pdf"))

def _create_standard_resume(path: str):
    """Create a standard one-column resume."""
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "John Doe")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 65, "john@example.com | (555) 123-4567")
    
    # Skills
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "SKILLS")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 115, "Python, JavaScript, React, Docker, SQL")
    
    # Experience
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 150, "EXPERIENCE")
    
    c.setFont("Helvetica-Bold", 10)
    # Parser expects "Company | Title" format (split by pipe)
    c.drawString(50, height - 170, "TechCorp | Software Engineer")
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, height - 182, "Jan 2020 - Present")
    
    c.setFont("Helvetica", 10)
    c.drawString(60, height - 200, "• Developed REST APIs using FastAPI")
    c.drawString(60, height - 215, "• Managed team of 5 developers")
    c.drawString(60, height - 230, "• Optimized database queries relating to SQL")
    
    # Education
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 270, "EDUCATION")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 290, "B.S. Computer Science | University of Tech")
    
    c.save()

def _create_two_column_resume(path: str):
    """Create a two-column designer resume."""
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    
    # Left sidebar (gray background)
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.rect(0, 0, 200, height, fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0)
    
    # Sidebar content
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20, height - 50, "Alice Design")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20, height - 100, "CONTACT")
    c.setFont("Helvetica", 10)
    c.drawString(20, height - 120, "alice@test.com")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20, height - 160, "SKILLS")
    c.setFont("Helvetica", 10)
    c.drawString(20, height - 180, "Figma")
    c.drawString(20, height - 195, "Photoshop")
    c.drawString(20, height - 210, "HTML/CSS")
    c.drawString(20, height - 225, "React")
    
    # Main content (Right column)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(220, height - 50, "WORK HISTORY")
    
    c.setFont("Helvetica-Bold", 12)
    # Parser extracts company from first part of split
    c.drawString(220, height - 80, "Creative Studio - Senior Designer")
    c.drawString(220, height - 95, "2018 - 2022")
    
    c.setFont("Helvetica", 10)
    c.drawString(230, height - 115, "• Led UI design for mobile apps")
    c.drawString(230, height - 130, "• Collaborated with developers on React implementation")
    
    c.save()

def _create_messy_resume(path: str):
    """Create a resume with inconsistent formatting."""
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    
    # Weird spacing and capitalization
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 50, "bob smith") # lowercase name
    
    c.drawString(50, height - 100, "work_history:") # snake_case header
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 120, "devops engr @ cloud sys")
    c.drawString(50, height - 135, "2019-2021")
    c.drawString(50, height - 150, "built ci/cd pipelines using jenkins")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 200, "Tech Skills") # Mixed case
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 220, "linux, aws, python, kubernetes")
    
    c.save()
