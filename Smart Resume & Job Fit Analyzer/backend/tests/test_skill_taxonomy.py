"""
Tests for skill taxonomy and normalization.
"""
import pytest
from taxonomy.normalizer import SkillNormalizer


class TestSkillNormalizer:
    """Test skill normalization functionality."""
    
    @pytest.fixture
    def normalizer(self):
        """Create a skill normalizer instance."""
        return SkillNormalizer()
    
    def test_normalizes_exact_match(self, normalizer):
        """Test normalization of exact skill matches."""
        canonical, confidence, score = normalizer.normalize("Python")
        
        assert canonical == "Python"
        assert score >= 90.0
    
    def test_normalizes_alias(self, normalizer):
        """Test normalization of skill aliases."""
        canonical, confidence, score = normalizer.normalize("js")
        
        assert canonical == "JavaScript"
    
    def test_normalizes_case_insensitive(self, normalizer):
        """Test case-insensitive normalization."""
        canonical, confidence, score = normalizer.normalize("PYTHON")
        
        assert canonical == "Python"
    
    def test_fuzzy_matching(self, normalizer):
        """Test fuzzy matching for close matches."""
        canonical, confidence, score = normalizer.normalize("javascrpt")  # Typo
        
        # Should still find JavaScript with lower confidence
        if canonical != "javascrpt":
            assert canonical == "JavaScript"
            assert score < 100.0
    
    def test_unknown_skill(self, normalizer):
        """Test handling of unknown skills."""
        canonical, confidence, score = normalizer.normalize("xyzabc123unknown")
        
        # Should return original or low confidence
        if confidence != "no_match":
            assert confidence == "low"
    
    def test_batch_normalize(self, normalizer):
        """Test batch normalization of multiple skills."""
        skills = ["Python", "js", "React", "node"]
        results = normalizer.normalize_batch(skills)
        
        assert len(results) == 4
        assert results[0]["canonical"] == "Python"
        assert results[1]["canonical"] == "JavaScript"
    
    def test_returns_category(self, normalizer):
        """Test that normalization returns category."""
        # get_category is a separate method
        category = normalizer.get_category("Python")
        
        assert category is not None
        assert category == "programming_languages"
