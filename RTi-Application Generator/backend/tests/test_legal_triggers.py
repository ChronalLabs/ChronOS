"""
Unit tests for Legal Triggers Engine - Self-contained version
Tests RTI Act sections and grievance markers detection
"""

import pytest
import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


# ============================================================================
# INLINE DEFINITIONS
# ============================================================================

class SeverityLevel(Enum):
    """Severity levels for grievances"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class LegalCategory(Enum):
    """Categories of legal provisions"""
    RTI_ACT = "rti_act"
    GRIEVANCE = "grievance"
    CONSUMER = "consumer"
    SERVICE_GUARANTEE = "service_guarantee"
    CITIZEN_CHARTER = "citizen_charter"


@dataclass
class LegalReference:
    """Detailed legal reference"""
    section: str
    title: str
    description: str
    category: LegalCategory
    applicable_to: List[str]
    citation: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "section": self.section,
            "title": self.title,
            "description": self.description,
            "category": self.category.value,
            "applicable_to": self.applicable_to,
            "citation": self.citation
        }


@dataclass
class GrievanceMarker:
    """Grievance indicator with severity"""
    type: str
    triggers_matched: List[str]
    severity: SeverityLevel
    recommended_action: str
    escalation_needed: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "triggers_matched": self.triggers_matched,
            "severity": self.severity.value,
            "recommended_action": self.recommended_action,
            "escalation_needed": self.escalation_needed
        }


@dataclass
class LegalAnalysisResult:
    """Complete legal analysis result"""
    rti_sections: List[LegalReference]
    grievance_markers: List[GrievanceMarker]
    suggested_citations: List[str]
    overall_severity: SeverityLevel
    timeline_applicable: Optional[str]
    legal_notes: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rti_sections": [s.to_dict() for s in self.rti_sections],
            "grievance_markers": [m.to_dict() for m in self.grievance_markers],
            "suggested_citations": self.suggested_citations,
            "overall_severity": self.overall_severity.value,
            "timeline_applicable": self.timeline_applicable,
            "legal_notes": self.legal_notes
        }


# RTI Act sections
RTI_SECTIONS = {
    "section_6": LegalReference(
        section="Section 6",
        title="Request for Information",
        description="Standard procedure for filing RTI application",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti"],
        citation="RTI Act 2005, Section 6(1)"
    ),
    "section_7": LegalReference(
        section="Section 7",
        title="Disposal of request",
        description="Timeline: 30 days (or 48 hours if life/liberty)",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti"],
        citation="RTI Act 2005, Section 7"
    ),
    "section_8": LegalReference(
        section="Section 8",
        title="Exemption from disclosure",
        description="Categories of information exempt from disclosure",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti", "appeal"],
        citation="RTI Act 2005, Section 8"
    ),
    "section_19": LegalReference(
        section="Section 19",
        title="Appeal",
        description="First and second appeal provisions",
        category=LegalCategory.RTI_ACT,
        applicable_to=["appeal"],
        citation="RTI Act 2005, Section 19"
    ),
}

# Grievance markers
GRIEVANCE_MARKERS = {
    "urgency": {
        "triggers": ["urgent", "emergency", "immediate", "asap", "life at risk"],
        "severity": SeverityLevel.HIGH,
        "recommended_action": "Escalate immediately",
        "escalation_needed": True
    },
    "corruption": {
        "triggers": ["bribe", "corruption", "illegal payment", "under the table"],
        "severity": SeverityLevel.CRITICAL,
        "recommended_action": "Report to vigilance department",
        "escalation_needed": True
    },
    "delay": {
        "triggers": ["delayed", "no response", "pending", "waiting"],
        "severity": SeverityLevel.MEDIUM,
        "recommended_action": "Send reminder with timeline",
        "escalation_needed": False
    },
    "harassment": {
        "triggers": ["harassment", "threatened", "intimidation", "coercion"],
        "severity": SeverityLevel.HIGH,
        "recommended_action": "Report to senior authority",
        "escalation_needed": True
    },
}


def detect_rti_sections(text: str) -> List[LegalReference]:
    """Detect RTI Act sections mentioned in text"""
    if not text:
        return []
    
    text_lower = text.lower()
    sections = []
    
    # Check for section mentions
    section_patterns = {
        "section_6": [r"section\s*6", r"rti\s+act", r"right\s+to\s+information"],
        "section_7": [r"section\s*7", r"30\s*days?", r"timeline"],
        "section_8": [r"section\s*8", r"exempt"],
        "section_19": [r"section\s*19", r"appeal", r"appellate"],
    }
    
    for section_key, patterns in section_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                if section_key in RTI_SECTIONS:
                    sections.append(RTI_SECTIONS[section_key])
                break
    
    return sections


def detect_grievance_markers(text: str) -> List[GrievanceMarker]:
    """Detect grievance markers in text"""
    if not text:
        return []
    
    text_lower = text.lower()
    markers = []
    
    for marker_type, config in GRIEVANCE_MARKERS.items():
        matched = []
        for trigger in config["triggers"]:
            if trigger in text_lower:
                matched.append(trigger)
        
        if matched:
            markers.append(GrievanceMarker(
                type=marker_type,
                triggers_matched=matched,
                severity=config["severity"],
                recommended_action=config["recommended_action"],
                escalation_needed=config["escalation_needed"]
            ))
    
    return markers


def get_applicable_timeline(doc_type: str) -> str:
    """Get applicable timeline for document type"""
    timelines = {
        "rti": "30 days from date of application",
        "urgent": "48 hours if life/liberty at stake",
        "first_appeal": "30 days from decision date",
        "second_appeal": "90 days from first appeal decision",
    }
    return timelines.get(doc_type, "As per department guidelines")


def analyze_legal_triggers(text: str) -> LegalAnalysisResult:
    """Complete legal analysis"""
    rti_sections = detect_rti_sections(text)
    grievance_markers = detect_grievance_markers(text)
    
    # Determine overall severity
    if grievance_markers:
        severities = [m.severity for m in grievance_markers]
        if SeverityLevel.CRITICAL in severities:
            overall_severity = SeverityLevel.CRITICAL
        elif SeverityLevel.HIGH in severities:
            overall_severity = SeverityLevel.HIGH
        else:
            overall_severity = SeverityLevel.MEDIUM
    else:
        overall_severity = SeverityLevel.LOW
    
    # Build citations
    citations = [s.citation for s in rti_sections]
    if not citations:
        citations = ["General grievance provisions apply"]
    
    # Determine timeline
    timeline = "30 days" if rti_sections else "As per department guidelines"
    if any(m.severity == SeverityLevel.CRITICAL for m in grievance_markers):
        timeline = "Immediate action required"
    
    return LegalAnalysisResult(
        rti_sections=rti_sections,
        grievance_markers=grievance_markers,
        suggested_citations=citations,
        overall_severity=overall_severity,
        timeline_applicable=timeline,
        legal_notes=["This is information only, not legal advice"]
    )


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_rti_text():
    return "I request information under Section 6 of RTI Act 2005"

@pytest.fixture
def sample_complaint_text():
    return "I want to file a grievance about poor road conditions"

@pytest.fixture
def sample_urgent_complaint():
    return "URGENT: Emergency! Lives at risk due to fire hazard!"

@pytest.fixture
def sample_corruption_complaint():
    return "Officials demanding bribe for registration. This is corruption."


# ============================================================================
# TESTS
# ============================================================================

class TestSeverityLevel:
    """Tests for SeverityLevel enum"""
    
    def test_severity_levels_exist(self):
        assert SeverityLevel.CRITICAL.value == "critical"
        assert SeverityLevel.HIGH.value == "high"
        assert SeverityLevel.MEDIUM.value == "medium"
        assert SeverityLevel.LOW.value == "low"
    
    def test_severity_count(self):
        assert len(SeverityLevel) == 4


class TestLegalCategory:
    """Tests for LegalCategory enum"""
    
    def test_categories_exist(self):
        assert LegalCategory.RTI_ACT.value == "rti_act"
        assert LegalCategory.GRIEVANCE.value == "grievance"


class TestLegalReference:
    """Tests for LegalReference dataclass"""
    
    def test_legal_reference_creation(self):
        ref = LegalReference(
            section="Section 6",
            title="Test",
            description="Test desc",
            category=LegalCategory.RTI_ACT,
            applicable_to=["rti"],
            citation="Test citation"
        )
        assert ref.section == "Section 6"
    
    def test_to_dict_works(self):
        ref = RTI_SECTIONS["section_6"]
        ref_dict = ref.to_dict()
        assert isinstance(ref_dict, dict)
        assert "section" in ref_dict


class TestRTISections:
    """Tests for RTI Act sections configuration"""
    
    def test_section_6_defined(self):
        assert "section_6" in RTI_SECTIONS
        sec = RTI_SECTIONS["section_6"]
        assert sec.section == "Section 6"
    
    def test_section_7_timeline(self):
        assert "section_7" in RTI_SECTIONS
        sec = RTI_SECTIONS["section_7"]
        assert "30" in sec.description
    
    def test_section_8_exemptions(self):
        assert "section_8" in RTI_SECTIONS
        sec = RTI_SECTIONS["section_8"]
        assert "exempt" in sec.description.lower()


class TestDetectRTISections:
    """Tests for detect_rti_sections function"""
    
    def test_section_6_detection(self, sample_rti_text):
        sections = detect_rti_sections(sample_rti_text)
        assert len(sections) >= 1
    
    def test_empty_text(self):
        sections = detect_rti_sections("")
        assert sections == []
    
    def test_complaint_has_fewer_sections(self, sample_complaint_text):
        sections = detect_rti_sections(sample_complaint_text)
        assert len(sections) <= 1


class TestDetectGrievanceMarkers:
    """Tests for detect_grievance_markers function"""
    
    def test_urgency_detection(self, sample_urgent_complaint):
        markers = detect_grievance_markers(sample_urgent_complaint)
        assert len(markers) >= 1
        severities = [m.severity for m in markers]
        assert any(s in [SeverityLevel.HIGH, SeverityLevel.CRITICAL] for s in severities)
    
    def test_corruption_detection(self, sample_corruption_complaint):
        markers = detect_grievance_markers(sample_corruption_complaint)
        assert len(markers) >= 1
    
    def test_empty_text(self):
        markers = detect_grievance_markers("")
        assert markers == []


class TestAnalyzeLegalTriggers:
    """Tests for analyze_legal_triggers function"""
    
    def test_returns_result(self, sample_rti_text):
        result = analyze_legal_triggers(sample_rti_text)
        assert isinstance(result, LegalAnalysisResult)
    
    def test_result_fields(self, sample_rti_text):
        result = analyze_legal_triggers(sample_rti_text)
        assert hasattr(result, 'rti_sections')
        assert hasattr(result, 'grievance_markers')
        assert hasattr(result, 'overall_severity')
    
    def test_urgent_complaint_severity(self, sample_urgent_complaint):
        result = analyze_legal_triggers(sample_urgent_complaint)
        assert result.overall_severity in [SeverityLevel.HIGH, SeverityLevel.CRITICAL]
    
    def test_to_dict_works(self, sample_rti_text):
        result = analyze_legal_triggers(sample_rti_text)
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)


class TestGetApplicableTimeline:
    """Tests for get_applicable_timeline function"""
    
    def test_rti_timeline(self):
        timeline = get_applicable_timeline("rti")
        assert "30" in timeline
    
    def test_urgent_timeline(self):
        timeline = get_applicable_timeline("urgent")
        assert "48" in timeline
    
    def test_default_timeline(self):
        timeline = get_applicable_timeline("unknown")
        assert timeline is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
