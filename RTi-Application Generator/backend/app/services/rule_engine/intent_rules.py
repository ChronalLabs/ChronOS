"""
Intent Rules - Rule Engine for Document Type Classification
PRIMARY decision layer - runs before any AI/NLP

Following MODEL_USAGE_POLICY:
- Rule engine is PRIMARY - all decisions go through here first
- AI/NLP only used when rules cannot determine the answer
- Never bypass rules with AI predictions
"""

from typing import Tuple, Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import re
import logging

logger = logging.getLogger(__name__)


class IntentType(Enum):
    """Supported document intent types"""
    RTI = "rti"                          # Right to Information request
    COMPLAINT = "complaint"              # Public grievance/complaint
    APPEAL = "appeal"                    # Appeal against RTI/decision
    FOLLOW_UP = "follow_up"              # Follow up on existing application
    ESCALATION = "escalation"            # Escalate to higher authority
    UNKNOWN = "unknown"                  # Cannot determine


class DocumentSubType(Enum):
    """Sub-types for each intent"""
    # RTI sub-types
    INFORMATION_REQUEST = "information_request"
    RECORDS_REQUEST = "records_request"
    INSPECTION_REQUEST = "inspection_request"
    
    # Complaint sub-types
    GRIEVANCE = "grievance"
    CORRUPTION_COMPLAINT = "corruption_complaint"
    SERVICE_COMPLAINT = "service_complaint"
    
    # Appeal sub-types
    FIRST_APPEAL = "first_appeal"
    SECOND_APPEAL = "second_appeal"
    
    # Other
    GENERAL = "general"


@dataclass
class IntentMatch:
    """Detailed intent match result"""
    keyword: str
    category: str
    weight: float
    position: int  # Position in text for context


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


# ============================================================================
# KEYWORD DEFINITIONS
# ============================================================================

# RTI keywords with weights
RTI_KEYWORDS = {
    # High confidence (0.3 weight each)
    "right to information": 0.3,
    "rti": 0.3,
    "section 6": 0.3,
    "rti act": 0.3,
    "information act 2005": 0.3,
    
    # Medium confidence (0.2 weight each)
    "public information officer": 0.2,
    "pio": 0.2,
    "information request": 0.2,
    "certified copies": 0.2,
    "official records": 0.2,
    "public authority": 0.2,
    
    # Low confidence (0.1 weight each)
    "information": 0.1,
    "records": 0.1,
    "documents": 0.1,
    "copies": 0.1,
    "inspection": 0.1,
    "disclosure": 0.1,
}

# Complaint keywords with weights
COMPLAINT_KEYWORDS = {
    # High confidence (0.3 weight each)
    "complaint": 0.3,
    "grievance": 0.3,
    "pgportal": 0.3,
    "public grievance": 0.3,
    
    # Medium confidence (0.2 weight each)
    "harassment": 0.2,
    "corruption": 0.2,
    "bribe": 0.2,
    "negligence": 0.2,
    "misconduct": 0.2,
    "fraud": 0.2,
    "delay in service": 0.2,
    
    # Low confidence (0.1 weight each)
    "problem": 0.1,
    "issue": 0.1,
    "not working": 0.1,
    "broken": 0.1,
    "damaged": 0.1,
    "poor service": 0.1,
    "unsatisfactory": 0.1,
}

# Appeal keywords with weights
APPEAL_KEYWORDS = {
    # High confidence (0.3 weight each)
    "first appeal": 0.3,
    "second appeal": 0.3,
    "appeal under section 19": 0.3,
    "appellate authority": 0.3,
    "information commission": 0.3,
    
    # Medium confidence (0.2 weight each)
    "appeal": 0.2,
    "review": 0.2,
    "reconsider": 0.2,
    "rejected": 0.2,
    "denial": 0.2,
    "refusal": 0.2,
    
    # Low confidence (0.1 weight each)
    "not satisfied": 0.1,
    "incomplete information": 0.1,
    "wrong information": 0.1,
}

# Follow-up keywords
FOLLOW_UP_KEYWORDS = {
    "follow up": 0.3,
    "follow-up": 0.3,
    "status": 0.2,
    "pending application": 0.2,
    "application status": 0.2,
    "reminder": 0.2,
    "no response": 0.2,
    "waiting": 0.1,
    "since": 0.1,
    "months": 0.1,
}

# Escalation keywords
ESCALATION_KEYWORDS = {
    "escalate": 0.3,
    "escalation": 0.3,
    "higher authority": 0.3,
    "chief secretary": 0.2,
    "minister": 0.2,
    "commissioner": 0.2,
    "no action taken": 0.2,
    "ignored": 0.1,
    "unanswered": 0.1,
}

# Sub-type indicators
SUB_TYPE_INDICATORS = {
    DocumentSubType.INFORMATION_REQUEST: [
        "seeking information", "want to know", "provide information",
        "what is", "how much", "list of", "details of"
    ],
    DocumentSubType.RECORDS_REQUEST: [
        "copies of", "certified copies", "attested copies",
        "documents related", "records of", "files"
    ],
    DocumentSubType.INSPECTION_REQUEST: [
        "inspect", "inspection", "examine", "view", "access to files"
    ],
    DocumentSubType.CORRUPTION_COMPLAINT: [
        "bribe", "corruption", "illegal payment", "extortion",
        "demanded money", "asked for bribe"
    ],
    DocumentSubType.SERVICE_COMPLAINT: [
        "poor service", "bad service", "not working", "broken",
        "delay", "pending", "waiting"
    ],
    DocumentSubType.FIRST_APPEAL: [
        "first appeal", "30 days", "appeal to", "appellate"
    ],
    DocumentSubType.SECOND_APPEAL: [
        "second appeal", "information commission", "cic", "sic"
    ],
}


def _find_keyword_matches(text: str, keywords: Dict[str, float], category: str) -> List[IntentMatch]:
    """Find all keyword matches in text with positions"""
    text_lower = text.lower()
    matches = []
    
    for keyword, weight in keywords.items():
        # Use word boundary matching for single words
        if ' ' not in keyword:
            pattern = rf'\b{re.escape(keyword)}\b'
        else:
            pattern = re.escape(keyword)
        
        for match in re.finditer(pattern, text_lower):
            matches.append(IntentMatch(
                keyword=keyword,
                category=category,
                weight=weight,
                position=match.start()
            ))
    
    return matches


def _calculate_weighted_score(matches: List[IntentMatch]) -> float:
    """Calculate weighted confidence score from matches"""
    if not matches:
        return 0.0
    
    # Sum weights, cap at 0.95
    total_weight = sum(m.weight for m in matches)
    
    # Bonus for multiple matches (up to 0.1)
    match_bonus = min(0.1, len(matches) * 0.02)
    
    # Base confidence + match bonus, capped at 0.95
    confidence = min(0.95, 0.4 + total_weight + match_bonus)
    
    return confidence


def _determine_sub_type(text: str, intent: IntentType) -> DocumentSubType:
    """Determine document sub-type based on content"""
    text_lower = text.lower()
    
    if intent == IntentType.RTI:
        for sub_type in [DocumentSubType.INSPECTION_REQUEST, 
                         DocumentSubType.RECORDS_REQUEST,
                         DocumentSubType.INFORMATION_REQUEST]:
            indicators = SUB_TYPE_INDICATORS.get(sub_type, [])
            if any(ind in text_lower for ind in indicators):
                return sub_type
        return DocumentSubType.INFORMATION_REQUEST
    
    elif intent == IntentType.COMPLAINT:
        if any(ind in text_lower for ind in SUB_TYPE_INDICATORS[DocumentSubType.CORRUPTION_COMPLAINT]):
            return DocumentSubType.CORRUPTION_COMPLAINT
        elif any(ind in text_lower for ind in SUB_TYPE_INDICATORS[DocumentSubType.SERVICE_COMPLAINT]):
            return DocumentSubType.SERVICE_COMPLAINT
        return DocumentSubType.GRIEVANCE
    
    elif intent == IntentType.APPEAL:
        if any(ind in text_lower for ind in SUB_TYPE_INDICATORS[DocumentSubType.SECOND_APPEAL]):
            return DocumentSubType.SECOND_APPEAL
        return DocumentSubType.FIRST_APPEAL
    
    return DocumentSubType.GENERAL


def classify_intent(text: str) -> Tuple[str, float]:
    """
    Classify user intent based on weighted keyword matching.
    Returns (intent, confidence)
    
    This is the PRIMARY decision function.
    AI/NLP should only be used if confidence < 0.7
    
    Priority:
    1. Weighted keyword match = confidence based on weights
    2. No match = unknown (defer to NLP)
    """
    result = classify_intent_detailed(text)
    return (result.intent.value, result.confidence)


def classify_intent_detailed(text: str) -> IntentResult:
    """
    Detailed intent classification with full audit trail.
    Returns IntentResult with all decision information.
    """
    decision_path = []
    
    # Find matches for each intent type
    rti_matches = _find_keyword_matches(text, RTI_KEYWORDS, "rti")
    complaint_matches = _find_keyword_matches(text, COMPLAINT_KEYWORDS, "complaint")
    appeal_matches = _find_keyword_matches(text, APPEAL_KEYWORDS, "appeal")
    follow_up_matches = _find_keyword_matches(text, FOLLOW_UP_KEYWORDS, "follow_up")
    escalation_matches = _find_keyword_matches(text, ESCALATION_KEYWORDS, "escalation")
    
    decision_path.append(f"Found {len(rti_matches)} RTI matches")
    decision_path.append(f"Found {len(complaint_matches)} complaint matches")
    decision_path.append(f"Found {len(appeal_matches)} appeal matches")
    decision_path.append(f"Found {len(follow_up_matches)} follow-up matches")
    decision_path.append(f"Found {len(escalation_matches)} escalation matches")
    
    # Calculate scores
    scores = {
        IntentType.RTI: (_calculate_weighted_score(rti_matches), rti_matches),
        IntentType.COMPLAINT: (_calculate_weighted_score(complaint_matches), complaint_matches),
        IntentType.APPEAL: (_calculate_weighted_score(appeal_matches), appeal_matches),
        IntentType.FOLLOW_UP: (_calculate_weighted_score(follow_up_matches), follow_up_matches),
        IntentType.ESCALATION: (_calculate_weighted_score(escalation_matches), escalation_matches),
    }
    
    # Find highest scoring intent
    best_intent = max(scores.keys(), key=lambda x: scores[x][0])
    best_score = scores[best_intent][0]
    best_matches = scores[best_intent][1]
    
    decision_path.append(f"Best intent: {best_intent.value} with score {best_score:.2%}")
    
    # Check for ambiguity (multiple high scores)
    high_scores = [(i, s[0]) for i, s in scores.items() if s[0] > 0.5]
    if len(high_scores) > 1:
        # Sort by score
        high_scores.sort(key=lambda x: x[1], reverse=True)
        if high_scores[0][1] - high_scores[1][1] < 0.1:
            # Too close - reduce confidence
            best_score = min(best_score, 0.6)
            decision_path.append(f"Ambiguous: {high_scores[0][0].value} vs {high_scores[1][0].value}")
    
    # Handle unknown
    if best_score < 0.3:
        best_intent = IntentType.UNKNOWN
        best_matches = []
        decision_path.append("Score too low - marking as unknown")
    
    # Determine sub-type
    sub_type = _determine_sub_type(text, best_intent)
    decision_path.append(f"Sub-type determined: {sub_type.value}")
    
    # Should NLP be invoked?
    requires_nlp = best_score < 0.7
    if requires_nlp:
        decision_path.append("Low confidence - NLP assistance recommended")
    
    return IntentResult(
        intent=best_intent,
        sub_type=sub_type,
        confidence=best_score,
        matches=best_matches,
        decision_path=decision_path,
        requires_nlp=requires_nlp
    )


def get_intent_suggestions(text: str, top_n: int = 3) -> List[Dict[str, Any]]:
    """
    Get top intent suggestions with scores.
    Useful when confidence is low and user needs to choose.
    """
    # Find matches for each intent type
    scores = {
        "rti": _calculate_weighted_score(_find_keyword_matches(text, RTI_KEYWORDS, "rti")),
        "complaint": _calculate_weighted_score(_find_keyword_matches(text, COMPLAINT_KEYWORDS, "complaint")),
        "appeal": _calculate_weighted_score(_find_keyword_matches(text, APPEAL_KEYWORDS, "appeal")),
        "follow_up": _calculate_weighted_score(_find_keyword_matches(text, FOLLOW_UP_KEYWORDS, "follow_up")),
        "escalation": _calculate_weighted_score(_find_keyword_matches(text, ESCALATION_KEYWORDS, "escalation")),
    }
    
    # Sort by score
    sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    suggestions = []
    for intent, score in sorted_intents[:top_n]:
        if score > 0:
            suggestions.append({
                "intent": intent,
                "confidence": round(score, 2),
                "description": _get_intent_description(intent)
            })
    
    # Always include at least manual option
    if not suggestions or suggestions[0]["confidence"] < 0.5:
        suggestions.append({
            "intent": "manual",
            "confidence": 0,
            "description": "Let me specify the document type manually"
        })
    
    return suggestions


def _get_intent_description(intent: str) -> str:
    """Get human-readable description for intent"""
    descriptions = {
        "rti": "Request for information under RTI Act 2005",
        "complaint": "File a complaint or grievance",
        "appeal": "Appeal against an RTI response or decision",
        "follow_up": "Follow up on a pending application",
        "escalation": "Escalate matter to higher authority",
        "unknown": "Unable to determine - please specify"
    }
    return descriptions.get(intent, "")


def validate_intent(intent: str) -> bool:
    """Check if intent is valid"""
    valid_intents = {"rti", "complaint", "appeal", "follow_up", "escalation"}
    return intent.lower() in valid_intents


def get_required_fields(intent: str, sub_type: str) -> List[Dict[str, Any]]:
    """Get list of required fields for a document type"""
    base_fields = [
        {"name": "applicant_name", "label": "Your Name", "required": True},
        {"name": "address", "label": "Address", "required": True},
        {"name": "contact", "label": "Phone/Email", "required": True},
    ]
    
    intent_fields = {
        "rti": [
            {"name": "authority", "label": "Public Authority", "required": True},
            {"name": "information_sought", "label": "Information Required", "required": True},
            {"name": "period", "label": "Time Period (if applicable)", "required": False},
        ],
        "complaint": [
            {"name": "department", "label": "Department", "required": True},
            {"name": "issue_description", "label": "Issue Description", "required": True},
            {"name": "incident_date", "label": "Date of Incident", "required": False},
            {"name": "previous_complaints", "label": "Previous Complaint References", "required": False},
        ],
        "appeal": [
            {"name": "original_application", "label": "Original RTI Application No.", "required": True},
            {"name": "pio_response", "label": "PIO Response (if any)", "required": False},
            {"name": "grounds_for_appeal", "label": "Grounds for Appeal", "required": True},
        ],
    }
    
    return base_fields + intent_fields.get(intent, [])
