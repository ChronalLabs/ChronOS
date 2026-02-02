"""
Rule Engine Package
PRIMARY decision layer - runs before any AI/NLP

Following MODEL_USAGE_POLICY:
- All structural decisions MUST go through the rule engine first
- AI/NLP is ONLY used when rules cannot determine the answer
- Never bypass rules with AI predictions

Components:
- intent_rules: Document type classification (RTI/Complaint/Appeal)
- issue_rules: Issue-to-department mapping
- legal_triggers: RTI Act sections and grievance markers
"""

from .intent_rules import (
    IntentType,
    DocumentSubType,
    IntentMatch,
    IntentResult,
    classify_intent,
    classify_intent_detailed,
    get_intent_suggestions,
    validate_intent,
    get_required_fields,
)

from .issue_rules import (
    IssueCategory,
    DepartmentInfo,
    IssueMatch,
    map_issue_to_department,
    map_issue_detailed,
    get_department_by_category,
    get_escalation_path,
    get_all_categories,
    suggest_categories,
)

from .legal_triggers import (
    SeverityLevel,
    LegalCategory,
    LegalReference,
    GrievanceMarker,
    LegalAnalysisResult,
    detect_legal_triggers,
    analyze_legal_context,
    get_applicable_timeline,
    get_rti_section_details,
    get_all_rti_sections,
    calculate_severity,
    should_escalate,
    get_recommended_actions,
)

__all__ = [
    # Intent rules
    "IntentType",
    "DocumentSubType",
    "IntentMatch",
    "IntentResult",
    "classify_intent",
    "classify_intent_detailed",
    "get_intent_suggestions",
    "validate_intent",
    "get_required_fields",
    
    # Issue rules
    "IssueCategory",
    "DepartmentInfo",
    "IssueMatch",
    "map_issue_to_department",
    "map_issue_detailed",
    "get_department_by_category",
    "get_escalation_path",
    "get_all_categories",
    "suggest_categories",
    
    # Legal triggers
    "SeverityLevel",
    "LegalCategory",
    "LegalReference",
    "GrievanceMarker",
    "LegalAnalysisResult",
    "detect_legal_triggers",
    "analyze_legal_context",
    "get_applicable_timeline",
    "get_rti_section_details",
    "get_all_rti_sections",
    "calculate_severity",
    "should_escalate",
    "get_recommended_actions",
]


def analyze_complete(text: str) -> dict:
    """
    Perform complete rule engine analysis on text.
    
    Returns:
        dict with intent, issue_mapping, and legal_analysis
    """
    intent_result = classify_intent_detailed(text)
    issue_result = map_issue_detailed(text)
    legal_result = analyze_legal_context(text)
    
    return {
        "intent": intent_result.to_dict(),
        "issue_mapping": {
            "matches": [m.to_dict() for m in issue_result[:3]],
            "primary": issue_result[0].to_dict() if issue_result else None
        },
        "legal_analysis": legal_result.to_dict(),
        "requires_nlp": intent_result.requires_nlp or (
            issue_result[0].confidence < 0.7 if issue_result else True
        )
    }
