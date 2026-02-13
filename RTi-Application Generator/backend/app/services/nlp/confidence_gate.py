"""
Confidence Gate
Controls when AI predictions are used vs when user confirmation is required

Following MODEL_USAGE_POLICY:
- Any AI prediction below 70% confidence MUST trigger user confirmation
- Low confidence results should show alternatives
- Users can always override AI suggestions
- All gating decisions are logged for audit trail
"""

from typing import Dict, Any, Optional, List, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ConfidenceLevel(Enum):
    """Confidence levels with clear thresholds"""
    HIGH = "high"           # > 0.9 - Auto-apply
    MEDIUM = "medium"       # 0.7 - 0.9 - Suggest with highlight
    LOW = "low"             # 0.5 - 0.7 - Show alternatives, require confirmation
    VERY_LOW = "very_low"   # < 0.5 - Manual input required


class DecisionSource(Enum):
    """Source of the decision"""
    RULE_ENGINE = "rule_engine"          # Deterministic rules
    SPACY_NLP = "spacy_nlp"              # spaCy entity extraction
    DISTILBERT = "distilbert"            # Semantic similarity
    USER_INPUT = "user_input"            # User provided/confirmed
    FALLBACK = "fallback"                # Default when nothing matches


@dataclass
class GatedResult:
    """Result with confidence gating applied"""
    value: Any
    confidence: float
    level: ConfidenceLevel
    requires_confirmation: bool
    alternatives: List[Dict[str, Any]]
    explanation: str
    source: DecisionSource
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    audit_id: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "confidence": round(self.confidence, 4),
            "confidence_level": self.level.value,
            "requires_confirmation": self.requires_confirmation,
            "alternatives": self.alternatives,
            "explanation": self.explanation,
            "source": self.source.value,
            "timestamp": self.timestamp,
            "audit_id": self.audit_id
        }


@dataclass 
class GatingDecision:
    """Complete gating decision with audit trail"""
    input_confidence: float
    input_source: DecisionSource
    output_level: ConfidenceLevel
    should_use_nlp: bool
    should_use_distilbert: bool
    requires_user_confirmation: bool
    reason: str
    thresholds_used: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_confidence": round(self.input_confidence, 4),
            "input_source": self.input_source.value,
            "output_level": self.output_level.value,
            "should_use_nlp": self.should_use_nlp,
            "should_use_distilbert": self.should_use_distilbert,
            "requires_user_confirmation": self.requires_user_confirmation,
            "reason": self.reason,
            "thresholds": self.thresholds_used
        }


# Configurable thresholds
class Thresholds:
    """Confidence thresholds (can be overridden via config)"""
    HIGH = 0.90
    MEDIUM = 0.70
    LOW = 0.50
    
    # When to escalate to next AI layer
    USE_NLP_BELOW = 0.70      # Use spaCy NLP when rule confidence is below this
    USE_DISTILBERT_BELOW = 0.60  # Use DistilBERT when spaCy confidence is below this
    
    # Minimum for auto-application
    AUTO_APPLY_ABOVE = 0.90
    
    @classmethod
    def update(cls, config: Dict[str, float]):
        """Update thresholds from config"""
        if "high" in config:
            cls.HIGH = config["high"]
        if "medium" in config:
            cls.MEDIUM = config["medium"]
        if "low" in config:
            cls.LOW = config["low"]
        if "use_nlp_below" in config:
            cls.USE_NLP_BELOW = config["use_nlp_below"]
        if "use_distilbert_below" in config:
            cls.USE_DISTILBERT_BELOW = config["use_distilbert_below"]
        if "auto_apply_above" in config:
            cls.AUTO_APPLY_ABOVE = config["auto_apply_above"]
        
        logger.info(f"Thresholds updated: HIGH={cls.HIGH}, MEDIUM={cls.MEDIUM}, LOW={cls.LOW}")


def get_confidence_level(confidence: float) -> ConfidenceLevel:
    """Determine confidence level from score"""
    if confidence >= Thresholds.HIGH:
        return ConfidenceLevel.HIGH
    elif confidence >= Thresholds.MEDIUM:
        return ConfidenceLevel.MEDIUM
    elif confidence >= Thresholds.LOW:
        return ConfidenceLevel.LOW
    else:
        return ConfidenceLevel.VERY_LOW


def should_use_nlp(rule_confidence: float) -> bool:
    """
    Decide if NLP (spaCy) should be invoked.
    Only use NLP if rule engine has low confidence.
    
    Per MODEL_USAGE_POLICY: Rule engine is PRIMARY.
    """
    return rule_confidence < Thresholds.USE_NLP_BELOW


def should_use_distilbert(nlp_confidence: float) -> bool:
    """
    Decide if DistilBERT should be invoked.
    Only use when spaCy confidence is insufficient.
    
    Per MODEL_USAGE_POLICY: DistilBERT is ONLY for similarity ranking.
    """
    return nlp_confidence < Thresholds.USE_DISTILBERT_BELOW


def make_gating_decision(
    confidence: float,
    source: DecisionSource
) -> GatingDecision:
    """
    Make a gating decision based on confidence and source.
    Returns complete decision with audit information.
    """
    level = get_confidence_level(confidence)
    
    # Determine what actions to take
    use_nlp = source == DecisionSource.RULE_ENGINE and should_use_nlp(confidence)
    use_distilbert = source == DecisionSource.SPACY_NLP and should_use_distilbert(confidence)
    requires_confirmation = level in [ConfidenceLevel.LOW, ConfidenceLevel.VERY_LOW]
    
    # Generate reason
    if level == ConfidenceLevel.HIGH:
        reason = f"High confidence ({confidence:.0%}) from {source.value} - auto-applying"
    elif level == ConfidenceLevel.MEDIUM:
        if use_nlp:
            reason = f"Medium confidence ({confidence:.0%}) from rules - enhancing with NLP"
        else:
            reason = f"Medium confidence ({confidence:.0%}) - suggesting with verification"
    elif level == ConfidenceLevel.LOW:
        if use_distilbert:
            reason = f"Low confidence ({confidence:.0%}) - using semantic similarity for alternatives"
        else:
            reason = f"Low confidence ({confidence:.0%}) - user confirmation required"
    else:
        reason = f"Very low confidence ({confidence:.0%}) - manual input recommended"
    
    return GatingDecision(
        input_confidence=confidence,
        input_source=source,
        output_level=level,
        should_use_nlp=use_nlp,
        should_use_distilbert=use_distilbert,
        requires_user_confirmation=requires_confirmation,
        reason=reason,
        thresholds_used={
            "high": Thresholds.HIGH,
            "medium": Thresholds.MEDIUM,
            "low": Thresholds.LOW,
            "use_nlp_below": Thresholds.USE_NLP_BELOW,
            "use_distilbert_below": Thresholds.USE_DISTILBERT_BELOW
        }
    )


def gate_result(
    value: Any,
    confidence: float,
    source: DecisionSource = DecisionSource.RULE_ENGINE,
    alternatives: List[Dict[str, Any]] = None,
    context: str = ""
) -> GatedResult:
    """
    Apply confidence gating to a result.
    Determines if user confirmation is needed and generates explanation.
    
    Args:
        value: The primary result value
        confidence: Confidence score (0.0 to 1.0)
        source: Where this result came from
        alternatives: Other options to show user
        context: Additional context for explanation
    
    Returns:
        GatedResult with all gating information
    """
    import uuid
    
    level = get_confidence_level(confidence)
    requires_confirmation = level in [ConfidenceLevel.LOW, ConfidenceLevel.VERY_LOW]
    
    # Generate explanation based on level and source
    explanations = {
        ConfidenceLevel.HIGH: f"High confidence ({confidence:.0%}) from {source.value} - applied automatically",
        ConfidenceLevel.MEDIUM: f"Medium confidence ({confidence:.0%}) from {source.value} - please verify this is correct",
        ConfidenceLevel.LOW: f"Low confidence ({confidence:.0%}) from {source.value} - please select from options or provide manually",
        ConfidenceLevel.VERY_LOW: f"Very low confidence ({confidence:.0%}) - manual input is recommended"
    }
    
    explanation = explanations[level]
    if context:
        explanation += f". {context}"
    
    # Log gating decision
    audit_id = str(uuid.uuid4())[:8]
    logger.info(f"[{audit_id}] Gated result: confidence={confidence:.2%}, level={level.value}, "
                f"requires_confirmation={requires_confirmation}, source={source.value}")
    
    return GatedResult(
        value=value,
        confidence=confidence,
        level=level,
        requires_confirmation=requires_confirmation,
        alternatives=alternatives or [],
        explanation=explanation,
        source=source,
        audit_id=audit_id
    )


def combine_confidences(
    confidences: List[Tuple[float, DecisionSource, float]]
) -> Tuple[float, DecisionSource]:
    """
    Combine multiple confidence scores with weights.
    
    Args:
        confidences: List of (confidence, source, weight) tuples
    
    Returns:
        (combined_confidence, primary_source)
    """
    if not confidences:
        return (0.0, DecisionSource.FALLBACK)
    
    # Weighted average
    total_weight = sum(w for _, _, w in confidences)
    if total_weight == 0:
        return (0.0, DecisionSource.FALLBACK)
    
    weighted_sum = sum(c * w for c, _, w in confidences)
    combined = weighted_sum / total_weight
    
    # Primary source is the one with highest confidence
    primary = max(confidences, key=lambda x: x[0])
    
    return (combined, primary[1])


def should_ask_user(
    confidence: float,
    is_legal_content: bool = False,
    has_alternatives: bool = True
) -> bool:
    """
    Determine if we should ask user for confirmation.
    
    Per MODEL_USAGE_POLICY:
    - Any AI prediction below 70% MUST trigger user confirmation
    - Legal content always requires confirmation
    """
    # Legal content always requires confirmation (no exceptions)
    if is_legal_content:
        return True
    
    # Below medium confidence = must confirm
    if confidence < Thresholds.MEDIUM:
        return True
    
    # High confidence with alternatives = suggest but auto-apply
    if confidence >= Thresholds.HIGH:
        return False
    
    # Medium confidence = ask if alternatives available
    return has_alternatives


def format_alternatives_for_user(
    alternatives: List[Dict[str, Any]],
    max_display: int = 5
) -> List[Dict[str, Any]]:
    """
    Format alternatives for user display.
    Sorts by confidence and limits count.
    """
    # Sort by confidence descending
    sorted_alts = sorted(
        alternatives, 
        key=lambda x: x.get("confidence", 0), 
        reverse=True
    )
    
    # Format for display
    formatted = []
    for i, alt in enumerate(sorted_alts[:max_display]):
        formatted.append({
            "rank": i + 1,
            "value": alt.get("value"),
            "confidence": round(alt.get("confidence", 0), 2),
            "label": alt.get("label", str(alt.get("value"))),
            "explanation": _explain_alternative(alt.get("confidence", 0), i + 1)
        })
    
    return formatted


def _explain_alternative(confidence: float, rank: int) -> str:
    """Generate explanation for an alternative option"""
    if confidence >= 0.9:
        return f"Option {rank}: Excellent match ({confidence:.0%})"
    elif confidence >= 0.7:
        return f"Option {rank}: Good match ({confidence:.0%})"
    elif confidence >= 0.5:
        return f"Option {rank}: Possible match ({confidence:.0%})"
    else:
        return f"Option {rank}: Weak match ({confidence:.0%})"


# Audit trail management
_audit_log: List[Dict[str, Any]] = []
_max_audit_entries = 1000


def log_gating_decision(
    decision_type: str,
    input_data: Dict[str, Any],
    output_data: Dict[str, Any],
    confidence: float,
    source: DecisionSource
) -> str:
    """
    Log a gating decision for audit trail.
    Returns audit ID.
    """
    import uuid
    
    audit_id = str(uuid.uuid4())
    
    entry = {
        "audit_id": audit_id,
        "timestamp": datetime.utcnow().isoformat(),
        "decision_type": decision_type,
        "confidence": confidence,
        "source": source.value,
        "confidence_level": get_confidence_level(confidence).value,
        "input_summary": str(input_data)[:200],  # Truncate for privacy
        "output_summary": str(output_data)[:200]
    }
    
    _audit_log.append(entry)
    
    # Maintain max size
    if len(_audit_log) > _max_audit_entries:
        _audit_log.pop(0)
    
    return audit_id


def get_audit_log(limit: int = 100) -> List[Dict[str, Any]]:
    """Get recent audit entries"""
    return _audit_log[-limit:]


def clear_audit_log():
    """Clear audit log"""
    global _audit_log
    _audit_log = []
    logger.info("Audit log cleared")
