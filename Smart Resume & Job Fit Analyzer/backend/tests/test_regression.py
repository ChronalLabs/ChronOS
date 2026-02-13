
import pytest
import os
import json
from rules.engine import evaluate
from api.schemas import ParsedResume, ParsedJobDescription
from parsers import parse_resume
from tests.pdf_generator import generate_test_pdfs

# Constants
TEST_RESUMES_DIR = os.path.join(os.path.dirname(__file__), "resumes")
GOLDEN_CASES_DIR = os.path.join(os.path.dirname(__file__), "golden_cases")

@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    """Generate test PDFs before running tests."""
    generate_test_pdfs(TEST_RESUMES_DIR)
    yield

class TestLayer1And2Parsing:
    """
    Layers 1 & 2: Parsing stability and Section Detection.
    Regression tests for different layouts.
    """
    
    def test_standard_resume_parsing(self):
        """Test parsing of a standard one-column resume."""
        path = os.path.join(TEST_RESUMES_DIR, "standard.pdf")
        resume = parse_resume(path, "pdf")
        
        assert "John Doe" in resume.raw_text
        assert len(resume.skills) >= 5
        assert resume.experience[0].company == "TechCorp"
        assert "Python" in [s.canonical_name for s in resume.skills]

    def test_two_column_parsing(self):
        """Test parsing of a two-column layout."""
        path = os.path.join(TEST_RESUMES_DIR, "two_column.pdf")
        resume = parse_resume(path, "pdf")
        
        # Should detect skills from sidebar
        skill_names = [s.canonical_name for s in resume.skills]
        assert "React" in skill_names
        assert "Figma" in skill_names
        
        # Should detect experience from main column
        assert len(resume.experience) > 0
        assert "Creative Studio" in resume.experience[0].company

    def test_messy_parsing_fallback(self):
        """Test parsing of inconsistent formatting."""
        path = os.path.join(TEST_RESUMES_DIR, "messy.pdf")
        resume = parse_resume(path, "pdf")
        
        # Should still find skills despite case issues
        skill_names = [s.canonical_name for s in resume.skills]
        assert "Linux" in skill_names
        assert "AWS" in skill_names
        
        # Should extract email if present (none in messy pdf, but check robustness)
        assert resume.parsing_warnings == []  # Should accept it without crashing

class TestLayer3ScoringDeterminism:
    """
    Layer 3: Scoring Consistency.
    Ensures same input always yields exact same score.
    """
    
    def test_scoring_stability(self):
        """Verify deterministic scoring for standard resume."""
        path = os.path.join(TEST_RESUMES_DIR, "standard.pdf")
        resume = parse_resume(path, "pdf")
        
        jd_text = """
        Looking for a Software Engineer with Python, SQL, and Docker skills.
        Experience with REST APIs and team management is a plus.
        """
        from parsers import parse_job_description
        jd = parse_job_description(jd_text)
        
        # Run evaluation 3 times
        score1 = evaluate(resume, jd).job_fit_score
        score2 = evaluate(resume, jd).job_fit_score
        score3 = evaluate(resume, jd).job_fit_score
        
        # Must be exactly equal
        assert score1 == score2 == score3
        assert score1 > 50  # Should be a decent match

class TestLayer4ExplanationStability:
    """
    Layer 4: Explanation Text Quality.
    Ensures explanations are generated consistently.
    """
    
    def test_explanation_wording(self):
        path = os.path.join(TEST_RESUMES_DIR, "standard.pdf")
        resume = parse_resume(path, "pdf")
        
        jd_text = "Looking for Python and SQL developer."
        from parsers import parse_job_description
        jd = parse_job_description(jd_text)
        
        result = evaluate(resume, jd)
        
        explanation = result.explanation.lower()
        
        # Check for key phrases in the template
        assert "job-fit score is" in explanation
        assert "matched" in explanation
        assert "experience depth" in explanation

class TestGoldenCases:
    """
    Regression Testing: Snapshot comparison.
    """
    
    def test_golden_output_match(self, tmp_path):
        """
        Compare current output against a saved 'golden' JSON.
        If this fails, either the logic broke or the rules changed intentionally.
        """
        path = os.path.join(TEST_RESUMES_DIR, "standard.pdf")
        resume = parse_resume(path, "pdf")
        
        jd_text = "Golden JD: Python, React, SQL required."
        from parsers import parse_job_description
        jd = parse_job_description(jd_text)
        
        result = evaluate(resume, jd)
        
        # Create a simplified snapshot dict
        snapshot = {
            "score": result.job_fit_score,
            "matched_skills": sorted([m.skill_name for m in result.skill_matches]),
            "missing_count": result.missing_count
        }
        
        golden_file = os.path.join(GOLDEN_CASES_DIR, "standard_golden.json")
        
        # If golden file doesn't exist, create it (first run)
        if not os.path.exists(golden_file):
            with open(golden_file, 'w') as f:
                json.dump(snapshot, f, indent=2)
            # Fail first run to notify user to verify the snapshot
            pytest.skip("Created new golden snapshot. Verify tests/golden_cases/standard_golden.json matches expectations.")
        
        # Load golden
        with open(golden_file, 'r') as f:
            expected = json.load(f)
            
        assert snapshot == expected
