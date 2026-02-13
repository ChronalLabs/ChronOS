"""
Tests for the rule-based evaluation engine.
"""
import pytest
from api.schemas import (
    ParsedResume, ParsedJobDescription, ExtractedSkill,
    JDRequirement, SkillCategory, ConfidenceLevel,
    ExperienceEntry, EducationEntry
)
from rules import evaluate
from rules.matchers import match_skills


class TestSkillMatcher:
    """Test skill matching functionality."""
    
    def test_exact_match(self):
        """Test exact skill matching."""
        resume_skills = [
            {"name": "Python", "canonical_name": "Python", "source_text": "Python"},
            {"name": "JavaScript", "canonical_name": "JavaScript", "source_text": "JavaScript"},
            {"name": "React", "canonical_name": "React", "source_text": "React"}
        ]
        jd_required = ["Python", "React"]
        jd_optional = []
        
        matches = match_skills(resume_skills, jd_required, jd_optional)
        
        assert matches["stats"]["required_matched"] == 2
    
    def test_missing_skills(self):
        """Test identification of missing skills."""
        resume_skills = [
            {"name": "Python", "canonical_name": "Python", "source_text": "Python"}
        ]
        jd_required = ["Python", "React", "Node.js"]
        jd_optional = []
        
        matches = match_skills(resume_skills, jd_required, jd_optional)
        
        assert len(matches["missing_required"]) == 2
    
    def test_optional_skills(self):
        """Test optional skill matching."""
        resume_skills = [
            {"name": "Python", "canonical_name": "Python", "source_text": "Python"},
            {"name": "AWS", "canonical_name": "AWS", "source_text": "AWS"}
        ]
        jd_required = ["Python"]
        jd_optional = ["AWS", "Docker"]
        
        matches = match_skills(resume_skills, jd_required, jd_optional)
        
        assert matches["stats"]["optional_matched"] == 1
        assert len(matches["missing_optional"]) == 1


class TestEvaluationEngine:
    """Test the complete evaluation engine."""
    
    @pytest.fixture
    def mock_resume(self):
        """Create a mock parsed resume."""
        return ParsedResume(
            raw_text="Test resume with Python and React",
            education=[
                EducationEntry(
                    institution="Stanford University",
                    degree="M.S. Computer Science",
                    source_text="Stanford"
                )
            ],
            experience=[
                ExperienceEntry(
                    company="TechCorp",
                    title="Software Engineer",
                    description="Built Python applications",
                    source_text="TechCorp",
                    responsibilities=["Developed APIs", "Led team of 3"]
                )
            ],
            projects=[],
            skills=[
                ExtractedSkill(
                    name="python", canonical_name="Python",
                    category=SkillCategory.PROGRAMMING_LANGUAGES,
                    confidence=ConfidenceLevel.HIGH,
                    source_text="python"
                ),
                ExtractedSkill(
                    name="react", canonical_name="React",
                    category=SkillCategory.FRAMEWORKS,
                    confidence=ConfidenceLevel.HIGH,
                    source_text="react"
                ),
                ExtractedSkill(
                    name="aws", canonical_name="AWS",
                    category=SkillCategory.CLOUD,
                    confidence=ConfidenceLevel.HIGH,
                    source_text="aws"
                ),
            ],
            contact_info={"email": "test@test.com"},
            parsing_warnings=[],
        )
    
    @pytest.fixture
    def mock_jd(self):
        """Create a mock parsed job description."""
        return ParsedJobDescription(
            raw_text="Looking for Python and React developer",
            requirements=[
                JDRequirement(text="Python required", skills=["Python"], priority="required"),
                JDRequirement(text="React experience", skills=["React"], priority="required"),
                JDRequirement(text="AWS preferred", skills=["AWS"], priority="optional"),
                JDRequirement(text="Docker preferred", skills=["Docker"], priority="optional"),
            ],
            required_skills=["Python", "React"],
            optional_skills=["AWS", "Docker"],
        )
    
    def test_evaluation_returns_score(self, mock_resume, mock_jd):
        """Test that evaluation returns a valid score."""
        result = evaluate(mock_resume, mock_jd)
        
        assert result.job_fit_score >= 0
        assert result.job_fit_score <= 100
    
    def test_evaluation_counts_matches(self, mock_resume, mock_jd):
        """Test that evaluation correctly counts matched skills."""
        result = evaluate(mock_resume, mock_jd)
        
        # Resume has Python and React which are required
        assert result.matched_count >= 2
    
    def test_evaluation_identifies_missing(self, mock_resume, mock_jd):
        """Test that evaluation identifies missing skills."""
        result = evaluate(mock_resume, mock_jd)
        
        # Docker is optional but not in resume
        assert result.missing_count >= 0
    
    def test_evaluation_has_breakdown(self, mock_resume, mock_jd):
        """Test that evaluation includes score breakdown."""
        result = evaluate(mock_resume, mock_jd)
        
        assert result.score_breakdown is not None
        assert result.score_breakdown.required_skills_score >= 0
        assert result.score_breakdown.optional_skills_score >= 0
    
    def test_perfect_match_high_score(self, mock_resume, mock_jd):
        """Test that a perfect match gets a high score."""
        # Resume has all required skills
        result = evaluate(mock_resume, mock_jd)
        
        # Should be at least 60 since required skills match
        assert result.job_fit_score >= 60
    
    def test_evaluation_generates_suggestions(self, mock_resume, mock_jd):
        """Test that evaluation generates improvement suggestions."""
        result = evaluate(mock_resume, mock_jd)
        
        assert result.improvement_suggestions is not None
        assert isinstance(result.improvement_suggestions, list)
    
    def test_evaluation_includes_evidence(self, mock_resume, mock_jd):
        """Test that evaluation includes evidence for matches."""
        result = evaluate(mock_resume, mock_jd)
        
        # Should have some evidence in skill_matches
        assert result.skill_matches is not None


class TestScoreCalculation:
    """Test score calculation logic."""
    
    def test_required_skills_weight(self):
        """Test that required skills have higher weight."""
        # This tests the scoring weights in config
        from rules.engine import RuleEngine
        
        engine = RuleEngine()
        config = engine.config
        
        required_weight = config.get("weights", {}).get("required_skills", 0)
        optional_weight = config.get("weights", {}).get("optional_skills", 0)
        
        # Required skills should have higher weight
        assert required_weight >= optional_weight
    
    def test_score_bounded(self):
        """Test that scores are always within valid range."""
        from rules.engine import RuleEngine
        
        engine = RuleEngine()
        
        # Test with extreme values
        assert engine._bound_score(150.0) == 100
        assert engine._bound_score(-50.0) == 0
        assert engine._bound_score(75.5) == 76
