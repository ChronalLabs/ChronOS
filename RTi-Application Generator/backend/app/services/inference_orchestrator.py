"""
Inference Orchestrator
Implements the core control flow: Rule Engine → spaCy NLP → Confidence Gate → DistilBERT (if required)
This is the SINGLE source of truth for inference decisions.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
from loguru import logger

from app.services.rule_engine.intent_rules import classify_intent
from app.services.rule_engine.legal_triggers import detect_legal_triggers
from app.services.rule_engine.issue_rules import map_issue_to_department
from app.services.nlp.spacy_engine import extract_entities, extract_key_phrases, analyze_sentiment_basic
from app.services.nlp.confidence_gate import gate_result, should_use_nlp, GatedResult, ConfidenceLevel
from app.services.nlp.distilbert_semantic import rank_by_similarity, compute_similarity


class DocumentType(str, Enum):
    """Document types that can be generated"""
    INFORMATION_REQUEST = "information_request"
    RECORDS_REQUEST = "records_request"
    INSPECTION_REQUEST = "inspection_request"
    GRIEVANCE = "grievance"
    ESCALATION = "escalation"
    FOLLOW_UP = "follow_up"


class IntentType(str, Enum):
    """User intent classification"""
    RTI = "rti"
    COMPLAINT = "complaint"
    APPEAL = "appeal"
    FOLLOW_UP = "follow_up"
    ESCALATION = "escalation"
    UNKNOWN = "unknown"


@dataclass
class InferenceResult:
    """Complete inference result with all metadata"""
    intent: IntentType
    document_type: DocumentType
    confidence: float
    confidence_level: ConfidenceLevel
    requires_confirmation: bool
    extracted_entities: Dict[str, List[str]]
    key_phrases: List[str]
    legal_triggers: Dict[str, Any]
    department_mapping: Dict[str, Any]
    sentiment: str
    suggestions: List[str]
    explanation: str
    decision_path: List[str]  # Audit trail


# RTI document type indicators
RTI_DOCUMENT_INDICATORS = {
    DocumentType.INFORMATION_REQUEST: [
        "information", "details", "data", "statistics", "records",
        "expenditure", "budget", "allocation", "spending"
    ],
    DocumentType.RECORDS_REQUEST: [
        "copies", "documents", "files", "papers", "correspondence",
        "letters", "orders", "circulars", "notifications"
    ],
    DocumentType.INSPECTION_REQUEST: [
        "inspection", "examine", "verify", "check", "physical verification",
        "site visit", "on-site", "inspect documents"
    ]
}

# Complaint document type indicators
COMPLAINT_DOCUMENT_INDICATORS = {
    DocumentType.GRIEVANCE: [
        "problem", "issue", "not working", "broken", "complaint",
        "grievance", "facing", "suffering", "harassment"
    ],
    DocumentType.ESCALATION: [
        "no response", "ignored", "multiple complaints", "escalate",
        "higher authority", "senior officer", "months", "years"
    ],
    DocumentType.FOLLOW_UP: [
        "follow up", "reminder", "pending", "status", "earlier complaint",
        "reference number", "tracking", "previous"
    ]
}


def _determine_document_type(text: str, intent: IntentType) -> Tuple[DocumentType, float]:
    """
    Determine specific document type based on intent and text analysis.
    Uses keyword matching - NO AI decision making.
    """
    text_lower = text.lower()
    
    if intent == IntentType.RTI:
        indicators = RTI_DOCUMENT_INDICATORS
        default = DocumentType.INFORMATION_REQUEST
    elif intent == IntentType.COMPLAINT:
        indicators = COMPLAINT_DOCUMENT_INDICATORS
        default = DocumentType.GRIEVANCE
    elif intent == IntentType.APPEAL:
        return DocumentType.ESCALATION, 0.9
    else:
        return DocumentType.GRIEVANCE, 0.5
    
    # Score each document type
    scores = {}
    for doc_type, keywords in indicators.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[doc_type] = score
    
    # Find best match
    if max(scores.values()) > 0:
        best_type = max(scores, key=lambda x: scores.get(x, 0))
        confidence = min(0.95, 0.6 + (scores[best_type] * 0.1))
        return best_type, confidence
    
    return default, 0.7


def _generate_suggestions(
    intent: IntentType,
    entities: Dict[str, List[str]],
    legal_triggers: Dict[str, Any]
) -> List[str]:
    """Generate helpful suggestions for the user"""
    suggestions = []
    
    # Check for missing time period
    if "DATE" not in entities or not entities["DATE"]:
        if intent == IntentType.RTI:
            suggestions.append("Consider specifying the time period for your information request (e.g., 'from January 2024 to December 2024')")
    
    # Check for missing organization
    if "ORG" not in entities or not entities["ORG"]:
        suggestions.append("Mentioning the specific department or office name will help route your application correctly")
    
    # RTI-specific suggestions
    if intent == IntentType.RTI:
        if not legal_triggers.get("rti_sections"):
            suggestions.append("Your request will be filed under Section 6(1) of the RTI Act, 2005")
        suggestions.append("RTI fee of Rs. 10 is applicable. Payment modes: IPO, DD, or online (state-specific)")
    
    # Complaint-specific suggestions
    if intent == IntentType.COMPLAINT:
        markers = legal_triggers.get("grievance_markers", [])
        high_severity = any(m.get("severity") == "high" for m in markers)
        if high_severity:
            suggestions.append("Your complaint indicates serious issues. Consider also filing with anti-corruption helpline or vigilance department")
    
    # Appeal suggestions
    if intent == IntentType.APPEAL:
        suggestions.append("First appeal must be filed within 30 days of receiving the response (or 30 days after expected response date)")
        suggestions.append("Second appeal to Information Commission is available if first appeal is rejected")
    
    return suggestions


def _build_explanation(decision_path: List[str], confidence: float) -> str:
    """Build human-readable explanation of the decision"""
    if confidence >= 0.9:
        confidence_text = "high confidence"
    elif confidence >= 0.7:
        confidence_text = "medium confidence"
    elif confidence >= 0.5:
        confidence_text = "low confidence"
    else:
        confidence_text = "very low confidence"
    
    path_text = " → ".join(decision_path)
    return f"Decision made with {confidence_text} ({confidence:.0%}). Path: {path_text}"


def run_inference(text: str, language: str = "english") -> InferenceResult:
    """
    Main inference orchestrator.
    
    CONTROL FLOW (as per specification):
    1. Rule Engine (keyword matching) - PRIMARY
    2. spaCy NLP (entity extraction, phrases)
    3. Confidence Gate (decide if more analysis needed)
    4. DistilBERT (only if confidence is low)
    5. Return result with confidence level
    
    This function NEVER makes final legal decisions - it only assists.
    """
    decision_path = []
    
    # ============================================
    # STEP 1: Rule Engine (PRIMARY DECISION LAYER)
    # ============================================
    logger.info("Step 1: Running rule engine")
    decision_path.append("Rule Engine")
    
    intent_str, rule_confidence = classify_intent(text)
    intent = IntentType(intent_str) if intent_str != "unknown" else IntentType.UNKNOWN
    
    logger.info(f"Rule engine result: intent={intent}, confidence={rule_confidence}")
    
    # Detect legal triggers
    legal_triggers = detect_legal_triggers(text)
    decision_path.append(f"Legal Triggers ({len(legal_triggers.get('rti_sections', []))} RTI, {len(legal_triggers.get('grievance_markers', []))} Grievance)")
    
    # Map to departments
    department_mapping = map_issue_to_department(text)
    
    # ============================================
    # STEP 2: spaCy NLP (Entity Extraction)
    # ============================================
    logger.info("Step 2: Running spaCy NLP")
    decision_path.append("spaCy NLP")
    
    entities = extract_entities(text)
    key_phrases = extract_key_phrases(text)
    sentiment = analyze_sentiment_basic(text)
    
    logger.info(f"spaCy extracted {len(entities)} entity types, {len(key_phrases)} phrases")
    
    # ============================================
    # STEP 3: Confidence Gate
    # ============================================
    logger.info("Step 3: Evaluating confidence gate")
    decision_path.append("Confidence Gate")
    
    # Boost confidence if legal triggers support the intent
    adjusted_confidence = rule_confidence
    
    if intent == IntentType.RTI and legal_triggers.get("rti_sections"):
        adjusted_confidence = min(0.95, adjusted_confidence + 0.1)
        decision_path.append("RTI sections confirmed (+10%)")
    
    if intent == IntentType.COMPLAINT and legal_triggers.get("grievance_markers"):
        adjusted_confidence = min(0.95, adjusted_confidence + 0.1)
        decision_path.append("Grievance markers confirmed (+10%)")
    
    # ============================================
    # STEP 4: DistilBERT (ONLY if confidence is low)
    # ============================================
    if should_use_nlp(adjusted_confidence):
        logger.info("Step 4: Confidence low, invoking DistilBERT for semantic analysis")
        decision_path.append("DistilBERT (semantic boost)")
        
        # Use semantic similarity to boost confidence
        rti_templates = [
            "I want to request information about government records",
            "Please provide copies of documents under RTI Act",
            "I am seeking information about public expenditure"
        ]
        complaint_templates = [
            "I want to file a complaint about poor service",
            "I am facing problems with government department",
            "I want to report corruption and misconduct"
        ]
        
        try:
            rti_scores = [compute_similarity(text, t) for t in rti_templates]
            complaint_scores = [compute_similarity(text, t) for t in complaint_templates]
            
            max_rti = max(rti_scores) if rti_scores else 0
            max_complaint = max(complaint_scores) if complaint_scores else 0
            
            # Use semantic results to refine intent if rule engine was uncertain
            if intent == IntentType.UNKNOWN:
                if max_rti > max_complaint and max_rti > 0.6:
                    intent = IntentType.RTI
                    adjusted_confidence = max_rti * 0.8  # Scale down for safety
                    decision_path.append(f"DistilBERT suggests RTI ({max_rti:.2f})")
                elif max_complaint > max_rti and max_complaint > 0.6:
                    intent = IntentType.COMPLAINT
                    adjusted_confidence = max_complaint * 0.8
                    decision_path.append(f"DistilBERT suggests Complaint ({max_complaint:.2f})")
                else:
                    decision_path.append("DistilBERT inconclusive")
            else:
                # Boost existing confidence slightly
                boost = max(max_rti, max_complaint) * 0.1
                adjusted_confidence = min(0.9, adjusted_confidence + boost)
                decision_path.append(f"DistilBERT boosted confidence (+{boost:.2f})")
        except Exception as e:
            logger.warning(f"DistilBERT analysis failed: {e}")
            decision_path.append("DistilBERT skipped (error)")
    else:
        logger.info("Step 4: Confidence sufficient, skipping DistilBERT")
        decision_path.append("DistilBERT skipped (confidence sufficient)")
    
    # ============================================
    # STEP 5: Determine document type
    # ============================================
    document_type, doc_type_confidence = _determine_document_type(text, intent)
    decision_path.append(f"Document type: {document_type.value}")
    
    # ============================================
    # STEP 6: Apply confidence gate for final result
    # ============================================
    gated = gate_result(
        value=intent,
        confidence=adjusted_confidence,
        alternatives=[{"type": t.value, "confidence": 0.0} for t in [IntentType.RTI, IntentType.COMPLAINT, IntentType.APPEAL]] if intent == IntentType.UNKNOWN else [],
        context=text[:100]
    )
    
    # Generate suggestions
    suggestions = _generate_suggestions(intent, entities, legal_triggers)
    
    # Build explanation
    explanation = _build_explanation(decision_path, adjusted_confidence)
    
    return InferenceResult(
        intent=intent,
        document_type=document_type,
        confidence=adjusted_confidence,
        confidence_level=gated.level,
        requires_confirmation=gated.requires_confirmation,
        extracted_entities=entities,
        key_phrases=key_phrases,
        legal_triggers=legal_triggers,
        department_mapping=department_mapping,
        sentiment=sentiment,
        suggestions=suggestions,
        explanation=explanation,
        decision_path=decision_path
    )
