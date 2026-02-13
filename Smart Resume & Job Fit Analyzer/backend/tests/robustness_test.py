
import pytest
from parsers.section_detector import detect_sections

# Test cases for Section Detection
TEST_CASES = [
    {
        "name": "Standard Headers",
        "text": """
        EDUCATION
        B.Tech in Computer Science
        
        EXPERIENCE
        Software Engineer at Google
        
        SKILLS
        Python, React
        """,
        "expected": ["education", "experience", "skills"]
    },
    {
        "name": "Numbered Headers (1. Experience)",
        "text": """
        1. EDUCATION
        B.S. Mathematics
        
        2. PROFESSIONAL EXPERIENCE
        Data Analyst
        
        3. TECHNICAL SKILLS
        SQL, Tableau
        """,
        "expected": ["education", "experience", "skills"]
    },
    {
        "name": "Decorated Headers (--- Experience ---)",
        "text": """
        --- Educational Background ---
        PhD Physics
        
        *** Work History ***
        Researcher at CERN
        
        === Core Competencies ===
        Data Analysis
        """,
        "expected": ["education", "experience", "skills"]
    },
    {
        "name": "Alternative Phrasing (Academic Profile, Positions Held)",
        "text": """
        Academic Profile
        Master's in Arts
        
        Positions Held
        Art Director
        
        Technological Proficiency
        Photoshop
        """,
        "expected": ["education", "experience", "skills"]
    },
    {
        "name": "Messy Spacing / Newlines",
        "text": """
        
        
        EDUCATION
        High School
             EXPERIENCE
        
        Cashier
        
           SKILLS
        Teamwork
        """,
        "expected": ["education", "experience", "skills"]
    },
    {
        "name": "Colon Separators (Experience:)",
        "text": """
        Education:
        B.Arch
        
        Experience:
        Architect
        
        Skills:
        AutoCAD
        """,
        "expected": ["education", "experience", "skills"]
    }
]

def test_section_detection_robustness():
    """
    Run section detection on various resume text formats.
    """
    results = []
    print(f"{'TEST CASE':<40} | {'STATUS':<10} | {'MISSING'}")
    print("-" * 70)
    
    for case in TEST_CASES:
        # Mock text_blocks (since detector uses them for boundaries)
        # We'll create simple blocks for each line
        lines = case["text"].strip().split("\n")
        blocks = []
        for i, line in enumerate(lines):
            line = line.strip()
            if line:
                blocks.append({
                    "text": line,
                    "line": i + 1,
                    "is_bold": line.isupper(), # Assume uppercase lines might be bold/headers
                    "is_heading": False
                })
        
        # Run detection
        extracted = detect_sections(case["text"], blocks)
        
        # Check if expected sections are non-empty
        missing = []
        for section in case["expected"]:
            mapping = {
                "education": extracted.get("education", []),
                "experience": extracted.get("experience", []),
                "skills": extracted.get("skills", [])
            }
            if not mapping[section]:
                missing.append(section)
        
        status = "PASS" if not missing else "FAIL"
        print(f"{case['name']:<40} | {status:<10} | {', '.join(missing)}")
        results.append((case["name"], status))

    return results

if __name__ == "__main__":
    test_section_detection_robustness()
