"""
Legal Triggers - RTI Act sections, grievance markers, and legal references
Comprehensive detection for proper legal document generation

Following MODEL_USAGE_POLICY:
- No AI-generated legal advice
- Templates are human-written
- This module provides legal context, not legal advice
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import re
import logging

logger = logging.getLogger(__name__)


class SeverityLevel(Enum):
    """Severity levels for grievances"""
    CRITICAL = "critical"    # Immediate action needed
    HIGH = "high"            # Urgent, escalation recommended
    MEDIUM = "medium"        # Standard processing
    LOW = "low"              # Information/query


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
    applicable_to: List[str]  # List of document types
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


# ============================================================================
# RTI ACT 2005 PROVISIONS
# ============================================================================

RTI_SECTIONS = {
    "section_2": LegalReference(
        section="Section 2",
        title="Definitions",
        description="Definitions of 'information', 'public authority', 'record', etc.",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti"],
        citation="Right to Information Act, 2005 - Section 2"
    ),
    "section_3": LegalReference(
        section="Section 3",
        title="Right to Information",
        description="All citizens have the right to information subject to provisions of this Act",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti"],
        citation="Right to Information Act, 2005 - Section 3"
    ),
    "section_4": LegalReference(
        section="Section 4",
        title="Obligations of Public Authorities",
        description="Suo motu disclosure obligations of public authorities",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti"],
        citation="Right to Information Act, 2005 - Section 4"
    ),
    "section_6": LegalReference(
        section="Section 6",
        title="Request for obtaining information",
        description="Standard procedure for filing RTI application",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti", "information_request"],
        citation="Right to Information Act, 2005 - Section 6(1)"
    ),
    "section_7": LegalReference(
        section="Section 7",
        title="Disposal of request",
        description="Timeline: 30 days (or 48 hours if life/liberty). Fees and transfer provisions.",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti"],
        citation="Right to Information Act, 2005 - Section 7"
    ),
    "section_8": LegalReference(
        section="Section 8",
        title="Exemption from disclosure",
        description="10 categories of information exempt from disclosure",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti", "appeal"],
        citation="Right to Information Act, 2005 - Section 8"
    ),
    "section_9": LegalReference(
        section="Section 9",
        title="Grounds for rejection",
        description="Request may be rejected if it infringes copyright",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti"],
        citation="Right to Information Act, 2005 - Section 9"
    ),
    "section_10": LegalReference(
        section="Section 10",
        title="Severability",
        description="Partial disclosure: Access to non-exempt parts",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti", "appeal"],
        citation="Right to Information Act, 2005 - Section 10"
    ),
    "section_11": LegalReference(
        section="Section 11",
        title="Third party information",
        description="Procedure when information relates to third party",
        category=LegalCategory.RTI_ACT,
        applicable_to=["rti"],
        citation="Right to Information Act, 2005 - Section 11"
    ),
    "section_19": LegalReference(
        section="Section 19",
        title="Appeal",
        description="First appeal within 30 days, Second appeal within 90 days",
        category=LegalCategory.RTI_ACT,
        applicable_to=["appeal", "first_appeal", "second_appeal"],
        citation="Right to Information Act, 2005 - Section 19"
    ),
    "section_20": LegalReference(
        section="Section 20",
        title="Penalties",
        description="Penalty of Rs. 250/day up to Rs. 25,000 for PIO delays",
        category=LegalCategory.RTI_ACT,
        applicable_to=["appeal"],
        citation="Right to Information Act, 2005 - Section 20"
    ),
}

# Triggers for each RTI section
RTI_SECTION_TRIGGERS = {
    "section_3": ["right to information", "citizen right", "fundamental right"],
    "section_4": ["suo motu", "proactive disclosure", "website", "public domain"],
    "section_6": ["application", "request", "seeking information", "file rti"],
    "section_7": ["30 days", "time limit", "no response", "timeline", "48 hours", "life", "liberty"],
    "section_8": ["exemption", "cannot disclose", "refused", "secret", "confidential", 
                  "national security", "cabinet papers"],
    "section_10": ["partial", "severable", "redacted"],
    "section_11": ["third party", "private company", "confidential business"],
    "section_19": ["appeal", "first appeal", "second appeal", "appellate", "information commission"],
    "section_20": ["penalty", "punishment", "rs 250", "compensation"],
}


# ============================================================================
# GRIEVANCE MARKERS
# ============================================================================

GRIEVANCE_MARKERS = {
    "service_delay": {
        "triggers": [
            "delay", "pending", "waiting", "no action", "months",
            "since long", "still waiting", "not processed", "no progress"
        ],
        "severity": SeverityLevel.MEDIUM,
        "action": "File grievance with timeline reference",
        "escalate_after_days": 30
    },
    "corruption": {
        "triggers": [
            "bribe", "corruption", "money demanded", "illegal payment",
            "extortion", "asked for money", "speed money", "under table",
            "commission", "gratification"
        ],
        "severity": SeverityLevel.CRITICAL,
        "action": "File anti-corruption complaint with vigilance department",
        "escalate_after_days": 0  # Immediate
    },
    "misconduct": {
        "triggers": [
            "rude behavior", "harassment", "misconduct", "misbehavior",
            "abuse", "threatening", "discrimination", "insulting",
            "unprofessional", "arrogant"
        ],
        "severity": SeverityLevel.HIGH,
        "action": "Report to department head with conduct complaint",
        "escalate_after_days": 7
    },
    "infrastructure": {
        "triggers": [
            "broken", "damaged", "not working", "poor condition",
            "dilapidated", "dangerous", "hazardous", "unsafe"
        ],
        "severity": SeverityLevel.MEDIUM,
        "action": "Report to maintenance/engineering department",
        "escalate_after_days": 15
    },
    "denial_of_service": {
        "triggers": [
            "refused", "denied", "rejected without reason", "not allowed",
            "prevented", "stopped", "barred"
        ],
        "severity": SeverityLevel.HIGH,
        "action": "Demand written reasons, file grievance",
        "escalate_after_days": 7
    },
    "negligence": {
        "triggers": [
            "negligence", "careless", "irresponsible", "ignored",
            "overlooked", "forgot", "lost my file", "misplaced"
        ],
        "severity": SeverityLevel.MEDIUM,
        "action": "File formal complaint with documentation",
        "escalate_after_days": 15
    },
    "fraud": {
        "triggers": [
            "fraud", "fake", "forged", "cheated", "scam",
            "duplicate", "false document", "identity theft"
        ],
        "severity": SeverityLevel.CRITICAL,
        "action": "File FIR and report to vigilance",
        "escalate_after_days": 0
    },
    "urgency_life_liberty": {
        "triggers": [
            "life threatening", "emergency", "medical emergency",
            "dying", "death", "hospital", "urgent medical",
            "liberty", "illegal detention", "arrest"
        ],
        "severity": SeverityLevel.CRITICAL,
        "action": "Invoke Section 7(1) for 48-hour response",
        "escalate_after_days": 0
    }
}


# ============================================================================
# SERVICE GUARANTEE / CITIZEN CHARTER TIMELINES
# ============================================================================

SERVICE_TIMELINES = {
    "rti_response": {"days": 30, "reference": "RTI Act Section 7(1)"},
    "rti_life_liberty": {"days": 2, "reference": "RTI Act Section 7(1) proviso"},
    "first_appeal": {"days": 30, "reference": "RTI Act Section 19(1)"},
    "second_appeal": {"days": 90, "reference": "RTI Act Section 19(3)"},
    "grievance_acknowledgment": {"days": 3, "reference": "CPGRAMS guidelines"},
    "grievance_resolution": {"days": 60, "reference": "CPGRAMS guidelines"},
    "police_fir": {"days": 0, "reference": "CrPC - Zero FIR"},
    "birth_certificate": {"days": 21, "reference": "State Service Guarantee"},
    "death_certificate": {"days": 7, "reference": "State Service Guarantee"},
    "caste_certificate": {"days": 30, "reference": "State Service Guarantee"},
    "income_certificate": {"days": 15, "reference": "State Service Guarantee"},
    "domicile_certificate": {"days": 30, "reference": "State Service Guarantee"},
}


def detect_legal_triggers(text: str) -> Dict:
    """
    Detect legal triggers in user text.
    Returns relevant sections and markers.
    
    Simple interface for backward compatibility.
    """
    result = analyze_legal_context(text)
    
    return {
        "rti_sections": [
            {
                "section": s.section,
                "title": s.title,
                "description": s.description
            }
            for s in result.rti_sections
        ],
        "grievance_markers": [
            {
                "type": m.type,
                "severity": m.severity.value
            }
            for m in result.grievance_markers
        ],
        "suggested_citations": result.suggested_citations
    }


def analyze_legal_context(text: str) -> LegalAnalysisResult:
    """
    Comprehensive legal analysis of text.
    Returns full LegalAnalysisResult with all details.
    """
    text_lower = text.lower()
    
    # Find RTI sections
    rti_sections = []
    suggested_citations = []
    
    for section_id, triggers in RTI_SECTION_TRIGGERS.items():
        for trigger in triggers:
            if trigger in text_lower:
                section = RTI_SECTIONS.get(section_id)
                if section and section not in rti_sections:
                    rti_sections.append(section)
                    suggested_citations.append(section.citation)
                break
    
    # Find grievance markers
    grievance_markers = []
    max_severity = SeverityLevel.LOW
    
    for marker_id, marker_data in GRIEVANCE_MARKERS.items():
        triggers_found = [t for t in marker_data["triggers"] if t in text_lower]
        if triggers_found:
            severity = marker_data["severity"]
            grievance_markers.append(GrievanceMarker(
                type=marker_id,
                triggers_matched=triggers_found,
                severity=severity,
                recommended_action=marker_data["action"],
                escalation_needed=marker_data["escalate_after_days"] == 0
            ))
            
            # Track maximum severity
            severity_order = {
                SeverityLevel.LOW: 0,
                SeverityLevel.MEDIUM: 1,
                SeverityLevel.HIGH: 2,
                SeverityLevel.CRITICAL: 3
            }
            if severity_order[severity] > severity_order[max_severity]:
                max_severity = severity
    
    # Determine applicable timeline
    timeline = None
    if any("life" in t or "liberty" in t or "emergency" in t for t in text_lower.split()):
        timeline = "48 hours (Section 7(1) proviso - life/liberty)"
    elif any(s.section == "Section 6" for s in rti_sections):
        timeline = "30 days (Section 7(1))"
    elif any(s.section == "Section 19" for s in rti_sections):
        if "second appeal" in text_lower:
            timeline = "90 days from First Appeal (Section 19(3))"
        else:
            timeline = "30 days from decision (Section 19(1))"
    
    # Generate legal notes
    legal_notes = []
    
    if rti_sections:
        legal_notes.append("This appears to be an RTI-related matter under the RTI Act, 2005")
    
    if max_severity == SeverityLevel.CRITICAL:
        legal_notes.append("⚠️ CRITICAL: This matter requires immediate attention")
        legal_notes.append("Consider filing FIR if criminal activity is involved")
    
    if any(m.type == "corruption" for m in grievance_markers):
        legal_notes.append("Consider reporting to Anti-Corruption Bureau / Vigilance Department")
        legal_notes.append("Preserve all evidence including recordings if legally obtained")
    
    if any(m.type == "urgency_life_liberty" for m in grievance_markers):
        legal_notes.append("48-hour timeline applicable under RTI Act Section 7(1)")
        legal_notes.append("For emergencies, also contact emergency services (100/108)")
    
    return LegalAnalysisResult(
        rti_sections=rti_sections,
        grievance_markers=grievance_markers,
        suggested_citations=suggested_citations,
        overall_severity=max_severity,
        timeline_applicable=timeline,
        legal_notes=legal_notes
    )


def get_applicable_timeline(document_type: str, is_life_liberty: bool = False) -> Dict[str, Any]:
    """Get applicable timeline for a document type"""
    if document_type == "rti" and is_life_liberty:
        return SERVICE_TIMELINES["rti_life_liberty"]
    
    timeline_map = {
        "rti": "rti_response",
        "information_request": "rti_response",
        "first_appeal": "first_appeal",
        "second_appeal": "second_appeal",
        "complaint": "grievance_resolution",
        "grievance": "grievance_resolution",
    }
    
    timeline_key = timeline_map.get(document_type, "grievance_resolution")
    return SERVICE_TIMELINES.get(timeline_key, {"days": 30, "reference": "Standard"})


def get_rti_section_details(section_id: str) -> Optional[Dict[str, Any]]:
    """Get detailed information about an RTI section"""
    section = RTI_SECTIONS.get(section_id)
    return section.to_dict() if section else None


def get_all_rti_sections() -> List[Dict[str, Any]]:
    """Get all RTI sections for reference"""
    return [s.to_dict() for s in RTI_SECTIONS.values()]


def calculate_severity(markers: List[GrievanceMarker]) -> SeverityLevel:
    """Calculate overall severity from multiple markers"""
    if not markers:
        return SeverityLevel.LOW
    
    severity_order = {
        SeverityLevel.LOW: 0,
        SeverityLevel.MEDIUM: 1,
        SeverityLevel.HIGH: 2,
        SeverityLevel.CRITICAL: 3
    }
    
    max_level = max(markers, key=lambda m: severity_order[m.severity])
    return max_level.severity


def should_escalate(markers: List[GrievanceMarker]) -> bool:
    """Determine if escalation is recommended"""
    return any(m.escalation_needed for m in markers)


def get_recommended_actions(text: str) -> List[str]:
    """Get list of recommended actions based on content analysis"""
    result = analyze_legal_context(text)
    
    actions = []
    
    # Add marker-specific actions
    for marker in result.grievance_markers:
        if marker.recommended_action not in actions:
            actions.append(marker.recommended_action)
    
    # Add general actions based on severity
    if result.overall_severity == SeverityLevel.CRITICAL:
        actions.insert(0, "URGENT: Take immediate action")
    
    # Add RTI-specific actions
    if result.rti_sections:
        if any(s.section == "Section 19" for s in result.rti_sections):
            actions.append("File appeal with supporting documents")
        else:
            actions.append("File RTI application with Rs. 10 fee")
    
    return actions
