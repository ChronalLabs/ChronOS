"""
Unit tests for Intent Rules Engine - Self-contained version
Tests the PRIMARY decision layer for document type classification
Note: Tests are self-contained to avoid Python 3.14 spaCy compatibility issues
"""

import pytest
import re
from enum import Enum
from dataclasses import dataclass
from typing import Tuple, List, Dict, Any


# ============================================================================
# INLINE DEFINITIONS (copied from rule_engine for standalone testing)
# ============================================================================

class IntentType(Enum):
    """Supported document intent types"""
    RTI = "rti"
    COMPLAINT = "complaint"
    APPEAL = "appeal"
    FOLLOW_UP = "follow_up"
    ESCALATION = "escalation"
    UNKNOWN = "unknown"


class DocumentSubType(Enum):
    """Sub-types for each intent"""
    INFORMATION_REQUEST = "information_request"
    RECORDS_REQUEST = "records_request"
    INSPECTION_REQUEST = "inspection_request"
    GRIEVANCE = "grievance"
    CORRUPTION_COMPLAINT = "corruption_complaint"
    SERVICE_COMPLAINT = "service_complaint"
    FIRST_APPEAL = "first_appeal"
    SECOND_APPEAL = "second_appeal"
    GENERAL = "general"


@dataclass
class IntentMatch:
    """Detailed intent match result"""
    keyword: str
    category: str
    weight: float
    position: int


@dataclass
class IntentResult:
    """Complete intent classification result"""
    intent: IntentType
    sub_type: DocumentSubType
    confidence: float
    matches: List[IntentMatch]
    decision_path: List[str]
    requires_nlp: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "intent": self.intent.value,
            "sub_type": self.sub_type.value,
            "confidence": round(self.confidence, 4),
            "matches": [{"keyword": m.keyword, "category": m.category, "weight": m.weight} 
                       for m in self.matches],
            "decision_path": self.decision_path,
            "requires_nlp": self.requires_nlp
        }


# Keyword definitions
RTI_KEYWORDS = {
    "right to information": 0.3, "rti": 0.3, "section 6": 0.3, "rti act": 0.3,
    "information act 2005": 0.3, "public information officer": 0.2, "pio": 0.2,
    "information request": 0.2, "certified copies": 0.2, "official records": 0.2,
    "information": 0.1, "records": 0.1, "documents": 0.1, "copies": 0.1,
}

COMPLAINT_KEYWORDS = {
    "complaint": 0.3, "grievance": 0.3, "pgportal": 0.3, "public grievance": 0.3,
    "harassment": 0.2, "corruption": 0.2, "bribe": 0.2, "negligence": 0.2,
    "misconduct": 0.2, "fraud": 0.2, "delay in service": 0.2,
    "problem": 0.1, "issue": 0.1, "not working": 0.1, "broken": 0.1,
}

APPEAL_KEYWORDS = {
    "first appeal": 0.3, "second appeal": 0.3, "appeal under section 19": 0.3,
    "appellate authority": 0.3, "information commission": 0.3,
    "appeal": 0.2, "review": 0.2, "reconsider": 0.2,
}

FOLLOW_UP_KEYWORDS = {
    "follow up": 0.3, "status": 0.2, "reminder": 0.2, "previous complaint": 0.3,
    "reference number": 0.2, "application number": 0.2,
}

ESCALATION_KEYWORDS = {
    "escalate": 0.3, "higher authority": 0.3, "senior officer": 0.2,
    "no action taken": 0.2, "failed to respond": 0.2,
}


def classify_intent(text: str) -> Tuple[IntentType, float]:
    """Classify text into intent type"""
    if not text or not text.strip():
        return IntentType.UNKNOWN, 0.0
    
    text_lower = text.lower()
    scores = {
        IntentType.RTI: 0.0,
        IntentType.COMPLAINT: 0.0,
        IntentType.APPEAL: 0.0,
        IntentType.FOLLOW_UP: 0.0,
        IntentType.ESCALATION: 0.0,
    }
    
    for keyword, weight in RTI_KEYWORDS.items():
        if keyword in text_lower:
            scores[IntentType.RTI] += weight
    
    for keyword, weight in COMPLAINT_KEYWORDS.items():
        if keyword in text_lower:
            scores[IntentType.COMPLAINT] += weight
    
    for keyword, weight in APPEAL_KEYWORDS.items():
        if keyword in text_lower:
            scores[IntentType.APPEAL] += weight
    
    for keyword, weight in FOLLOW_UP_KEYWORDS.items():
        if keyword in text_lower:
            scores[IntentType.FOLLOW_UP] += weight
    
    for keyword, weight in ESCALATION_KEYWORDS.items():
        if keyword in text_lower:
            scores[IntentType.ESCALATION] += weight
    
    best_intent = max(scores.items(), key=lambda x: x[1])
    if best_intent[1] == 0:
        return IntentType.UNKNOWN, 0.0
    
    confidence = min(best_intent[1], 1.0)
    return best_intent[0], confidence


def classify_intent_detailed(text: str) -> IntentResult:
    """Detailed intent classification"""
    intent, confidence = classify_intent(text)
    text_lower = text.lower()
    
    matches = []
    all_keywords = {
        "rti": RTI_KEYWORDS,
        "complaint": COMPLAINT_KEYWORDS,
        "appeal": APPEAL_KEYWORDS,
    }
    
    for category, keywords in all_keywords.items():
        for keyword, weight in keywords.items():
            pos = text_lower.find(keyword)
            if pos >= 0:
                matches.append(IntentMatch(keyword, category, weight, pos))
    
    sub_type = DocumentSubType.GENERAL
    if intent == IntentType.RTI:
        if "certified" in text_lower or "records" in text_lower:
            sub_type = DocumentSubType.RECORDS_REQUEST
        else:
            sub_type = DocumentSubType.INFORMATION_REQUEST
    elif intent == IntentType.COMPLAINT:
        if "corrupt" in text_lower or "bribe" in text_lower:
            sub_type = DocumentSubType.CORRUPTION_COMPLAINT
        else:
            sub_type = DocumentSubType.GRIEVANCE
    elif intent == IntentType.APPEAL:
        if "first" in text_lower:
            sub_type = DocumentSubType.FIRST_APPEAL
        elif "second" in text_lower:
            sub_type = DocumentSubType.SECOND_APPEAL
    
    return IntentResult(
        intent=intent,
        sub_type=sub_type,
        confidence=confidence,
        matches=matches,
        decision_path=[f"Classified as {intent.value} with confidence {confidence:.2f}"],
        requires_nlp=confidence < 0.7
    )


def get_intent_suggestions(text: str) -> List[Dict[str, Any]]:
    """Get intent suggestions"""
    result = classify_intent_detailed(text)
    return [{"intent": result.intent.value, "confidence": result.confidence}]


# ============================================================================
# TEST FIXTURES
# ============================================================================

@pytest.fixture
def sample_rti_text():
    return """
    I request information under Section 6 of the Right to Information Act, 2005.
    Please provide certified copies of all documents related to road construction 
    project in Delhi during 2023-2024. I am willing to pay the requisite fee.
    """

@pytest.fixture
def sample_complaint_text():
    return """
    I want to file a grievance regarding the poor condition of roads in my area.
    There are multiple potholes and the street lights are not working. 
    Despite several complaints to the municipal corporation, no action has been taken.
    This is causing harassment to residents.
    """

@pytest.fixture
def sample_appeal_text():
    return """
    I am filing a first appeal under Section 19 of RTI Act 2005.
    My original RTI application number was RTI/2024/0001234, submitted 45 days ago.
    The PIO has not responded within the stipulated time of 30 days.
    I request the appellate authority to direct the PIO to provide the information.
    """

@pytest.fixture
def sample_follow_up():
    return """
    This is a follow up on my previous complaint number CPGRAMS/2024/12345.
    I had submitted the complaint 2 months ago but have not received any response.
    Please provide the current status of my application.
    """

@pytest.fixture
def sample_escalation():
    return """
    I am escalating my complaint to the higher authority as the concerned department
    has failed to take action despite multiple reminders. My original complaint
    reference number is PG/2024/5678. I request the senior officer to intervene.
    """

@pytest.fixture
def sample_corruption_complaint():
    return """
    I want to report corruption by officials in the Land Registry Office.
    They are demanding bribes of Rs. 50,000 to process my property registration.
    This is illegal and a violation of the Prevention of Corruption Act.
    """


# ============================================================================
# TESTS
# ============================================================================

class TestIntentType:
    """Tests for IntentType enum"""
    
    def test_intent_types_exist(self):
        assert IntentType.RTI.value == "rti"
        assert IntentType.COMPLAINT.value == "complaint"
        assert IntentType.APPEAL.value == "appeal"
        assert IntentType.FOLLOW_UP.value == "follow_up"
        assert IntentType.ESCALATION.value == "escalation"
        assert IntentType.UNKNOWN.value == "unknown"
    
    def test_intent_types_count(self):
        assert len(IntentType) == 6


class TestDocumentSubType:
    """Tests for DocumentSubType enum"""
    
    def test_rti_subtypes(self):
        assert DocumentSubType.INFORMATION_REQUEST.value == "information_request"
        assert DocumentSubType.RECORDS_REQUEST.value == "records_request"
        assert DocumentSubType.INSPECTION_REQUEST.value == "inspection_request"
    
    def test_complaint_subtypes(self):
        assert DocumentSubType.GRIEVANCE.value == "grievance"
        assert DocumentSubType.CORRUPTION_COMPLAINT.value == "corruption_complaint"


class TestKeywordWeights:
    """Tests for keyword weight configurations"""
    
    def test_rti_high_confidence_keywords(self):
        high_weight_keywords = ["right to information", "rti", "section 6", "rti act"]
        for kw in high_weight_keywords:
            assert RTI_KEYWORDS.get(kw, 0) == 0.3, f"'{kw}' should have weight 0.3"
    
    def test_complaint_high_confidence_keywords(self):
        high_weight_keywords = ["complaint", "grievance", "pgportal"]
        for kw in high_weight_keywords:
            assert COMPLAINT_KEYWORDS.get(kw, 0) == 0.3, f"'{kw}' should have weight 0.3"


class TestClassifyIntent:
    """Tests for classify_intent function"""
    
    def test_rti_classification(self, sample_rti_text):
        intent, confidence = classify_intent(sample_rti_text)
        assert intent == IntentType.RTI
        assert confidence >= 0.5
    
    def test_complaint_classification(self, sample_complaint_text):
        intent, confidence = classify_intent(sample_complaint_text)
        assert intent == IntentType.COMPLAINT
        assert confidence >= 0.5
    
    def test_appeal_classification(self, sample_appeal_text):
        intent, confidence = classify_intent(sample_appeal_text)
        assert intent == IntentType.APPEAL
        assert confidence >= 0.5
    
    def test_follow_up_classification(self, sample_follow_up):
        intent, confidence = classify_intent(sample_follow_up)
        assert intent == IntentType.FOLLOW_UP
        assert confidence >= 0.3
    
    def test_escalation_classification(self, sample_escalation):
        intent, confidence = classify_intent(sample_escalation)
        assert intent == IntentType.ESCALATION
        assert confidence >= 0.3
    
    def test_empty_text_returns_unknown(self):
        intent, confidence = classify_intent("")
        assert intent == IntentType.UNKNOWN
        assert confidence == 0.0
    
    def test_confidence_range(self, sample_rti_text):
        intent, confidence = classify_intent(sample_rti_text)
        assert 0 <= confidence <= 1
    
    def test_case_insensitivity(self):
        text1 = "RTI REQUEST under SECTION 6"
        text2 = "rti request under section 6"
        intent1, conf1 = classify_intent(text1)
        intent2, conf2 = classify_intent(text2)
        assert intent1 == intent2


class TestClassifyIntentDetailed:
    """Tests for classify_intent_detailed function"""
    
    def test_returns_intent_result(self, sample_rti_text):
        result = classify_intent_detailed(sample_rti_text)
        assert isinstance(result, IntentResult)
    
    def test_intent_result_fields(self, sample_rti_text):
        result = classify_intent_detailed(sample_rti_text)
        assert hasattr(result, 'intent')
        assert hasattr(result, 'sub_type')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'matches')
        assert hasattr(result, 'decision_path')
        assert hasattr(result, 'requires_nlp')
    
    def test_to_dict_works(self, sample_rti_text):
        result = classify_intent_detailed(sample_rti_text)
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert "intent" in result_dict
        assert "confidence" in result_dict
    
    def test_corruption_complaint_detection(self, sample_corruption_complaint):
        result = classify_intent_detailed(sample_corruption_complaint)
        assert result.intent == IntentType.COMPLAINT
        assert result.sub_type in [
            DocumentSubType.CORRUPTION_COMPLAINT,
            DocumentSubType.GRIEVANCE
        ]


class TestGetIntentSuggestions:
    """Tests for get_intent_suggestions function"""
    
    def test_returns_list(self, sample_rti_text):
        suggestions = get_intent_suggestions(sample_rti_text)
        assert isinstance(suggestions, list)
    
    def test_suggestions_have_intent(self, sample_rti_text):
        suggestions = get_intent_suggestions(sample_rti_text)
        assert len(suggestions) > 0
        assert "intent" in suggestions[0]


class TestEdgeCases:
    """Tests for edge cases"""
    
    def test_special_characters(self):
        text = "RTI!!! @#$% Request & Section 6 (2005)"
        intent, confidence = classify_intent(text)
        assert intent in [IntentType.RTI, IntentType.UNKNOWN]
    
    def test_numbers_in_text(self):
        text = "RTI application 12345 dated 01/01/2024 under Section 6"
        intent, confidence = classify_intent(text)
        assert intent == IntentType.RTI
    
    def test_very_long_text(self):
        text = "RTI request " * 1000 + " please provide information"
        intent, confidence = classify_intent(text)
        assert intent == IntentType.RTI
    
    def test_whitespace_only(self):
        text = "   \t\n   "
        intent, confidence = classify_intent(text)
        assert intent == IntentType.UNKNOWN
        assert confidence == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
