"""
Unit tests for Confidence Gate - Self-contained version
Tests confidence-based gating and decision system
"""

import pytest
from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional


# ============================================================================
# INLINE DEFINITIONS
# ============================================================================

class ConfidenceLevel(Enum):
    """Confidence levels for NLP results"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNCERTAIN = "uncertain"


class DecisionSource(Enum):
    """Source of the decision"""
    RULES = "rules"
    NLP = "nlp"
    HYBRID = "hybrid"
    FALLBACK = "fallback"


@dataclass
class Thresholds:
    """Configurable thresholds"""
    high: float = 0.85
    medium: float = 0.65
    low: float = 0.40
    
    @staticmethod
    def default() -> "Thresholds":
        return Thresholds()


@dataclass
class GatedResult:
    """Result with confidence gating applied"""
    value: Any
    confidence: float
    confidence_level: ConfidenceLevel
    source: DecisionSource
    fallback_used: bool
    metadata: Optional[dict] = None
    
    def to_dict(self) -> dict:
        return {
            "value": str(self.value),
            "confidence": self.confidence,
            "confidence_level": self.confidence_level.value,
            "source": self.source.value,
            "fallback_used": self.fallback_used,
            "metadata": self.metadata
        }


def get_confidence_level(score: float, thresholds: Optional[Thresholds] = None) -> ConfidenceLevel:
    """Convert numeric confidence to level"""
    if thresholds is None:
        thresholds = Thresholds.default()
    
    if score >= thresholds.high:
        return ConfidenceLevel.HIGH
    elif score >= thresholds.medium:
        return ConfidenceLevel.MEDIUM
    elif score >= thresholds.low:
        return ConfidenceLevel.LOW
    else:
        return ConfidenceLevel.UNCERTAIN


def gate_result(
    nlp_result: Any,
    nlp_confidence: float,
    rule_result: Any,
    rule_confidence: float,
    threshold: float = 0.65
) -> GatedResult:
    """Apply confidence gating to choose between NLP and rule results"""
    
    # If NLP confidence is high, use NLP
    if nlp_confidence >= threshold and nlp_confidence > rule_confidence:
        return GatedResult(
            value=nlp_result,
            confidence=nlp_confidence,
            confidence_level=get_confidence_level(nlp_confidence),
            source=DecisionSource.NLP,
            fallback_used=False
        )
    
    # If rule confidence is high, use rules
    elif rule_confidence >= threshold:
        return GatedResult(
            value=rule_result,
            confidence=rule_confidence,
            confidence_level=get_confidence_level(rule_confidence),
            source=DecisionSource.RULES,
            fallback_used=False
        )
    
    # Use hybrid if both have some confidence
    elif nlp_confidence > 0.3 and rule_confidence > 0.3:
        avg_confidence = (nlp_confidence + rule_confidence) / 2
        return GatedResult(
            value=nlp_result if nlp_confidence > rule_confidence else rule_result,
            confidence=avg_confidence,
            confidence_level=get_confidence_level(avg_confidence),
            source=DecisionSource.HYBRID,
            fallback_used=False
        )
    
    # Fallback
    else:
        return GatedResult(
            value=rule_result or nlp_result,
            confidence=max(nlp_confidence, rule_confidence),
            confidence_level=ConfidenceLevel.UNCERTAIN,
            source=DecisionSource.FALLBACK,
            fallback_used=True
        )


def make_gating_decision(
    primary_confidence: float,
    secondary_confidence: float,
    prefer_primary: bool = True
) -> tuple:
    """Determine which result to use"""
    if primary_confidence >= 0.85:
        return ("primary", "high_confidence")
    elif secondary_confidence >= 0.85:
        return ("secondary", "high_confidence")
    elif primary_confidence >= 0.65:
        return ("primary", "medium_confidence")
    elif secondary_confidence >= 0.65:
        return ("secondary", "medium_confidence")
    elif prefer_primary:
        return ("primary", "low_confidence_fallback")
    else:
        return ("secondary", "low_confidence_fallback")


def should_use_nlp(rule_confidence: float, nlp_available: bool = True) -> bool:
    """Determine if NLP should be used"""
    if not nlp_available:
        return False
    return rule_confidence < 0.85


def combine_confidences(confidences: list) -> float:
    """Combine multiple confidence scores"""
    if not confidences:
        return 0.0
    return sum(confidences) / len(confidences)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def default_thresholds():
    return Thresholds.default()

@pytest.fixture
def strict_thresholds():
    return Thresholds(high=0.95, medium=0.80, low=0.60)


# ============================================================================
# TESTS
# ============================================================================

class TestConfidenceLevel:
    """Tests for ConfidenceLevel enum"""
    
    def test_levels_exist(self):
        assert ConfidenceLevel.HIGH.value == "high"
        assert ConfidenceLevel.MEDIUM.value == "medium"
        assert ConfidenceLevel.LOW.value == "low"
        assert ConfidenceLevel.UNCERTAIN.value == "uncertain"


class TestDecisionSource:
    """Tests for DecisionSource enum"""
    
    def test_sources_exist(self):
        assert DecisionSource.RULES.value == "rules"
        assert DecisionSource.NLP.value == "nlp"
        assert DecisionSource.HYBRID.value == "hybrid"
        assert DecisionSource.FALLBACK.value == "fallback"


class TestThresholds:
    """Tests for Thresholds dataclass"""
    
    def test_default_thresholds(self, default_thresholds):
        assert default_thresholds.high == 0.85
        assert default_thresholds.medium == 0.65
        assert default_thresholds.low == 0.40
    
    def test_custom_thresholds(self, strict_thresholds):
        assert strict_thresholds.high == 0.95
        assert strict_thresholds.medium == 0.80


class TestGetConfidenceLevel:
    """Tests for get_confidence_level function"""
    
    def test_high_confidence(self, default_thresholds):
        assert get_confidence_level(0.90, default_thresholds) == ConfidenceLevel.HIGH
        assert get_confidence_level(0.85, default_thresholds) == ConfidenceLevel.HIGH
    
    def test_medium_confidence(self, default_thresholds):
        assert get_confidence_level(0.70, default_thresholds) == ConfidenceLevel.MEDIUM
        assert get_confidence_level(0.65, default_thresholds) == ConfidenceLevel.MEDIUM
    
    def test_low_confidence(self, default_thresholds):
        assert get_confidence_level(0.50, default_thresholds) == ConfidenceLevel.LOW
        assert get_confidence_level(0.40, default_thresholds) == ConfidenceLevel.LOW
    
    def test_uncertain(self, default_thresholds):
        assert get_confidence_level(0.30, default_thresholds) == ConfidenceLevel.UNCERTAIN
        assert get_confidence_level(0.0, default_thresholds) == ConfidenceLevel.UNCERTAIN
    
    def test_boundary_values(self):
        assert get_confidence_level(0.84) == ConfidenceLevel.MEDIUM
        assert get_confidence_level(0.85) == ConfidenceLevel.HIGH
        assert get_confidence_level(0.64) == ConfidenceLevel.LOW
        assert get_confidence_level(0.65) == ConfidenceLevel.MEDIUM


class TestGateResult:
    """Tests for gate_result function"""
    
    def test_prefers_nlp_when_high_confidence(self):
        result = gate_result(
            nlp_result="NLP_VALUE",
            nlp_confidence=0.90,
            rule_result="RULE_VALUE",
            rule_confidence=0.70
        )
        assert result.value == "NLP_VALUE"
        assert result.source == DecisionSource.NLP
    
    def test_prefers_rules_when_nlp_low(self):
        result = gate_result(
            nlp_result="NLP_VALUE",
            nlp_confidence=0.50,
            rule_result="RULE_VALUE",
            rule_confidence=0.80
        )
        assert result.value == "RULE_VALUE"
        assert result.source == DecisionSource.RULES
    
    def test_fallback_when_both_low(self):
        result = gate_result(
            nlp_result="NLP_VALUE",
            nlp_confidence=0.20,
            rule_result="RULE_VALUE",
            rule_confidence=0.25
        )
        assert result.fallback_used == True
        assert result.source == DecisionSource.FALLBACK
    
    def test_custom_threshold(self):
        result = gate_result(
            nlp_result="NLP_VALUE",
            nlp_confidence=0.75,
            rule_result="RULE_VALUE",
            rule_confidence=0.60,
            threshold=0.70
        )
        assert result.value == "NLP_VALUE"


class TestGatedResult:
    """Tests for GatedResult dataclass"""
    
    def test_to_dict(self):
        result = GatedResult(
            value="test",
            confidence=0.85,
            confidence_level=ConfidenceLevel.HIGH,
            source=DecisionSource.NLP,
            fallback_used=False
        )
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict["value"] == "test"
        assert result_dict["confidence"] == 0.85


class TestMakeGatingDecision:
    """Tests for make_gating_decision function"""
    
    def test_high_primary(self):
        result = make_gating_decision(0.90, 0.60)
        assert result == ("primary", "high_confidence")
    
    def test_high_secondary(self):
        result = make_gating_decision(0.50, 0.90)
        assert result == ("secondary", "high_confidence")
    
    def test_medium_primary(self):
        result = make_gating_decision(0.70, 0.50)
        assert result == ("primary", "medium_confidence")
    
    def test_fallback_primary(self):
        result = make_gating_decision(0.30, 0.30, prefer_primary=True)
        assert result == ("primary", "low_confidence_fallback")
    
    def test_fallback_secondary(self):
        result = make_gating_decision(0.30, 0.30, prefer_primary=False)
        assert result == ("secondary", "low_confidence_fallback")


class TestShouldUseNlp:
    """Tests for should_use_nlp function"""
    
    def test_use_nlp_when_rules_uncertain(self):
        assert should_use_nlp(0.50, nlp_available=True) == True
    
    def test_skip_nlp_when_rules_confident(self):
        assert should_use_nlp(0.90, nlp_available=True) == False
    
    def test_skip_nlp_when_unavailable(self):
        assert should_use_nlp(0.50, nlp_available=False) == False


class TestCombineConfidences:
    """Tests for combine_confidences function"""
    
    def test_average_calculation(self):
        result = combine_confidences([0.80, 0.90, 1.0])
        assert abs(result - 0.90) < 0.01
    
    def test_empty_list(self):
        result = combine_confidences([])
        assert result == 0.0
    
    def test_single_value(self):
        result = combine_confidences([0.75])
        assert result == 0.75


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
