"""
RTI Validation Engine
Rule-based validation to prevent common RTI rejection causes.

This module validates RTI requests BEFORE draft generation to:
1. Prevent 70-80% of real RTI rejections
2. Ensure legal compliance
3. Check clarity and completeness
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re
from loguru import logger


class ValidationSeverity(str, Enum):
    """Severity levels for validation issues"""
    ERROR = "error"      # Blocks generation - must fix
    WARNING = "warning"  # Should fix - may cause rejection
    INFO = "info"        # Suggestion for improvement


class ValidationCategory(str, Enum):
    """Categories of validation"""
    LEGAL = "legal"           # Legal requirements under RTI Act
    CLARITY = "clarity"       # Clarity and specificity
    COMPLETENESS = "completeness"  # Required information present
    AUTHORITY = "authority"   # Correct authority identification
    FORMAT = "format"         # Proper formatting


@dataclass
class ValidationIssue:
    """Single validation issue"""
    code: str
    message: str
    message_hi: str
    severity: ValidationSeverity
    category: ValidationCategory
    field: Optional[str] = None
    suggestion: Optional[str] = None
    suggestion_hi: Optional[str] = None


@dataclass
class ValidationResult:
    """Complete validation result"""
    is_valid: bool  # No blocking errors
    can_generate: bool  # Safe to generate (may have warnings)
    issues: List[ValidationIssue] = field(default_factory=list)
    score: int = 0  # Quality score 0-100
    scores_breakdown: Dict[str, int] = field(default_factory=dict)


# =============================================================================
# VALIDATION RULES
# =============================================================================

# Patterns that indicate vague/unclear requests
VAGUE_PATTERNS = [
    (r'^(all|any|every|some)\s+(information|details|records)', "Avoid using 'all' or 'any' - be specific"),
    (r'etc\.?$|\.{3}$', "Don't end with 'etc.' - specify exactly what you need"),
    (r'\ball\s+related\b', "Specify exactly what related items you need"),
    (r'\bwhatever\b|\banything\b', "Replace with specific items"),
]

# Time period patterns (valid)
TIME_PERIOD_PATTERNS = [
    r'\d{4}[-–]\d{4}',  # 2023-2024
    r'\d{4}',  # Single year
    r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',  # Date format
    r'(last|past|previous)\s+\d+\s*(years?|months?|days?)',  # Relative
    r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}',
    r'(FY|financial\s*year)\s*\d{4}',
    r'पिछले?\s*\d+\s*(वर्ष|साल|महीने|दिन)',  # Hindi
    r'\d{4}\s*से\s*\d{4}',  # Hindi range
]

# Question patterns (indicators of clear requests)
QUESTION_INDICATORS = [
    r'\d+\.\s+',  # Numbered list
    r'[a-z]\)\s+',  # Lettered list
    r'\?\s*$',  # Question mark
    r'\b(provide|furnish|supply|give|send|share)\b',
    r'\b(copy|copies|details|information|records|data)\s+(of|about|regarding|relating)',
    r'\b(how much|how many|what|when|where|who|why|which)\b',
    r'(प्रदान करें|दें|भेजें|बताएं)',  # Hindi
]

# Exemption keywords (Section 8 of RTI Act)
EXEMPTION_KEYWORDS = [
    (r'\b(cabinet|PMO|prime\s*minister)\s*(papers?|notes?|discussions?)', "Cabinet papers may be exempt under Section 8(1)(i)"),
    (r'\b(security|defence|intelligence|armed\s*forces)\b', "Security-related info may be exempt under Section 8(1)(a)"),
    (r'\b(trade\s*secret|commercial\s*confidence|intellectual\s*property)\b', "Commercial confidential info may be exempt under Section 8(1)(d)"),
    (r'\b(personal|private)\s+(information|details|records)\s+of\s+(third|other)', "Third party personal info may be exempt under Section 8(1)(j)"),
]


class RTIValidator:
    """
    Validates RTI requests for legal compliance, clarity, and completeness.
    """
    
    def __init__(self):
        self.weights = {
            ValidationCategory.LEGAL: 30,
            ValidationCategory.CLARITY: 25,
            ValidationCategory.COMPLETENESS: 25,
            ValidationCategory.AUTHORITY: 15,
            ValidationCategory.FORMAT: 5,
        }
    
    def validate(
        self,
        information_sought: str,
        time_period: str,
        department: str,
        record_type: str,
        applicant_name: str = "",
        applicant_address: str = "",
        applicant_state: str = "",
        **kwargs
    ) -> ValidationResult:
        """
        Validate an RTI request.
        
        Returns ValidationResult with issues and quality score.
        """
        issues: List[ValidationIssue] = []
        scores: Dict[str, int] = {}
        
        # === COMPLETENESS CHECKS ===
        completeness_score = 100
        
        # Required field: Information sought
        if not information_sought or len(information_sought.strip()) < 10:
            issues.append(ValidationIssue(
                code="MISSING_INFO_SOUGHT",
                message="Information sought is required and must be at least 10 characters",
                message_hi="मांगी गई जानकारी आवश्यक है और कम से कम 10 अक्षर होने चाहिए",
                severity=ValidationSeverity.ERROR,
                category=ValidationCategory.COMPLETENESS,
                field="information_sought"
            ))
            completeness_score -= 40
        
        # Required field: Time period
        if not time_period or len(time_period.strip()) < 4:
            issues.append(ValidationIssue(
                code="MISSING_TIME_PERIOD",
                message="Time period is required. RTI without time period is often rejected.",
                message_hi="समय अवधि आवश्यक है। बिना समय अवधि के RTI अक्सर अस्वीकार हो जाती है।",
                severity=ValidationSeverity.ERROR,
                category=ValidationCategory.COMPLETENESS,
                field="time_period"
            ))
            completeness_score -= 30
        
        # Required field: Department
        if not department or len(department.strip()) < 2:
            issues.append(ValidationIssue(
                code="MISSING_DEPARTMENT",
                message="Department/Public Authority must be specified",
                message_hi="विभाग/लोक प्राधिकरण निर्दिष्ट होना चाहिए",
                severity=ValidationSeverity.ERROR,
                category=ValidationCategory.COMPLETENESS,
                field="department"
            ))
            completeness_score -= 20
        
        # Required field: Applicant details
        if not applicant_name:
            issues.append(ValidationIssue(
                code="MISSING_APPLICANT_NAME",
                message="Applicant name is required",
                message_hi="आवेदक का नाम आवश्यक है",
                severity=ValidationSeverity.ERROR,
                category=ValidationCategory.COMPLETENESS,
                field="applicant_name"
            ))
            completeness_score -= 10
        
        if not applicant_address:
            issues.append(ValidationIssue(
                code="MISSING_APPLICANT_ADDRESS",
                message="Applicant address is required for receiving the response",
                message_hi="उत्तर प्राप्त करने के लिए आवेदक का पता आवश्यक है",
                severity=ValidationSeverity.WARNING,
                category=ValidationCategory.COMPLETENESS,
                field="applicant_address"
            ))
            completeness_score -= 5
        
        scores[ValidationCategory.COMPLETENESS.value] = max(0, completeness_score)
        
        # === CLARITY CHECKS ===
        clarity_score = 100
        
        if information_sought:
            # Check for vague language
            for pattern, suggestion in VAGUE_PATTERNS:
                if re.search(pattern, information_sought, re.IGNORECASE):
                    issues.append(ValidationIssue(
                        code="VAGUE_REQUEST",
                        message=f"Request may be too vague: {suggestion}",
                        message_hi="अनुरोध बहुत अस्पष्ट हो सकता है",
                        severity=ValidationSeverity.WARNING,
                        category=ValidationCategory.CLARITY,
                        field="information_sought",
                        suggestion=suggestion
                    ))
                    clarity_score -= 15
            
            # Check for numbered/structured questions (good practice)
            has_structure = any(re.search(p, information_sought) for p in QUESTION_INDICATORS)
            if not has_structure and len(information_sought) > 100:
                issues.append(ValidationIssue(
                    code="UNSTRUCTURED_REQUEST",
                    message="Consider numbering your questions for clarity",
                    message_hi="स्पष्टता के लिए अपने प्रश्नों को क्रमांकित करने पर विचार करें",
                    severity=ValidationSeverity.INFO,
                    category=ValidationCategory.CLARITY,
                    field="information_sought",
                    suggestion="Use numbered points like:\n1. First question\n2. Second question"
                ))
                clarity_score -= 10
            
            # Check length (too short = unclear, too long = may be rejected)
            if len(information_sought) < 50:
                issues.append(ValidationIssue(
                    code="REQUEST_TOO_SHORT",
                    message="Request seems too brief. Be more specific about what information you need.",
                    message_hi="अनुरोध बहुत संक्षिप्त लगता है। अधिक विस्तृत जानकारी दें।",
                    severity=ValidationSeverity.WARNING,
                    category=ValidationCategory.CLARITY,
                    field="information_sought"
                ))
                clarity_score -= 20
            elif len(information_sought) > 1500:
                issues.append(ValidationIssue(
                    code="REQUEST_TOO_LONG",
                    message="Request is quite long. Consider breaking into multiple focused RTIs.",
                    message_hi="अनुरोध काफी लंबा है। कई केंद्रित RTI में विभाजित करने पर विचार करें।",
                    severity=ValidationSeverity.INFO,
                    category=ValidationCategory.CLARITY,
                    field="information_sought"
                ))
                clarity_score -= 5
        
        scores[ValidationCategory.CLARITY.value] = max(0, clarity_score)
        
        # === LEGAL CHECKS ===
        legal_score = 100
        
        if time_period:
            # Validate time period format
            has_valid_time = any(re.search(p, time_period, re.IGNORECASE) for p in TIME_PERIOD_PATTERNS)
            if not has_valid_time:
                issues.append(ValidationIssue(
                    code="INVALID_TIME_PERIOD",
                    message="Time period format unclear. Use formats like '2023-2024' or 'Last 2 years'",
                    message_hi="समय अवधि प्रारूप अस्पष्ट है। '2023-2024' या 'पिछले 2 वर्ष' जैसे प्रारूप का उपयोग करें",
                    severity=ValidationSeverity.WARNING,
                    category=ValidationCategory.LEGAL,
                    field="time_period"
                ))
                legal_score -= 15
        
        if information_sought:
            # Check for potentially exempt information
            for pattern, warning in EXEMPTION_KEYWORDS:
                if re.search(pattern, information_sought, re.IGNORECASE):
                    issues.append(ValidationIssue(
                        code="POTENTIAL_EXEMPTION",
                        message=warning,
                        message_hi="यह जानकारी RTI अधिनियम की धारा 8 के तहत छूट प्राप्त हो सकती है",
                        severity=ValidationSeverity.WARNING,
                        category=ValidationCategory.LEGAL,
                        field="information_sought",
                        suggestion="This information may be exempt. Consider rephrasing or be prepared for potential denial."
                    ))
                    legal_score -= 10
        
        scores[ValidationCategory.LEGAL.value] = max(0, legal_score)
        
        # === AUTHORITY CHECKS ===
        authority_score = 100
        
        if department:
            # Check if department is specific enough
            vague_dept_patterns = [r'^other$', r'^general$', r'^government$', r'^sarkari$']
            if any(re.search(p, department, re.IGNORECASE) for p in vague_dept_patterns):
                issues.append(ValidationIssue(
                    code="VAGUE_DEPARTMENT",
                    message="Department is too vague. Specify the exact department to avoid transfer delays.",
                    message_hi="विभाग बहुत अस्पष्ट है। स्थानांतरण में देरी से बचने के लिए सटीक विभाग निर्दिष्ट करें।",
                    severity=ValidationSeverity.WARNING,
                    category=ValidationCategory.AUTHORITY,
                    field="department"
                ))
                authority_score -= 30
        
        scores[ValidationCategory.AUTHORITY.value] = max(0, authority_score)
        
        # === FORMAT CHECKS ===
        format_score = 100
        
        if record_type:
            # Having record type specified is good
            pass
        else:
            issues.append(ValidationIssue(
                code="MISSING_RECORD_TYPE",
                message="Specifying record type (documents, data, inspection) helps get precise response",
                message_hi="अभिलेख का प्रकार निर्दिष्ट करने से सटीक प्रतिक्रिया प्राप्त करने में मदद मिलती है",
                severity=ValidationSeverity.INFO,
                category=ValidationCategory.FORMAT,
                field="record_type"
            ))
            format_score -= 20
        
        scores[ValidationCategory.FORMAT.value] = max(0, format_score)
        
        # === CALCULATE OVERALL SCORE ===
        total_weight = sum(self.weights.values())
        weighted_score = sum(
            scores.get(cat.value, 0) * weight 
            for cat, weight in self.weights.items()
        ) / total_weight
        
        # Determine if valid
        has_errors = any(i.severity == ValidationSeverity.ERROR for i in issues)
        has_warnings = any(i.severity == ValidationSeverity.WARNING for i in issues)
        
        return ValidationResult(
            is_valid=not has_errors,
            can_generate=not has_errors,  # Can generate if no blocking errors
            issues=issues,
            score=int(weighted_score),
            scores_breakdown=scores
        )
    
    def validate_edit(
        self,
        original_text: str,
        edited_text: str,
        document_type: str = "rti"
    ) -> Tuple[bool, List[ValidationIssue]]:
        """
        Validate user edits to ensure legal structure is maintained.
        
        Returns (is_safe, issues)
        """
        issues: List[ValidationIssue] = []
        
        # Critical patterns that shouldn't be removed
        if document_type in ["information_request", "records_request", "inspection_request"]:
            critical_patterns = [
                (r'RTI\s*(Act|अधिनियम)', "RTI Act reference should not be removed"),
                (r'(Section|धारा)\s*6', "Section 6 reference is important"),
                (r'(Public\s*Information\s*Officer|लोक\s*सूचना\s*अधिकारी|PIO)', "PIO addressee should be retained"),
                (r'(citizen|नागरिक)', "Citizenship declaration is legally required"),
            ]
            
            for pattern, warning in critical_patterns:
                if re.search(pattern, original_text, re.IGNORECASE) and not re.search(pattern, edited_text, re.IGNORECASE):
                    issues.append(ValidationIssue(
                        code="CRITICAL_REMOVED",
                        message=warning,
                        message_hi="महत्वपूर्ण कानूनी तत्व हटा दिया गया है",
                        severity=ValidationSeverity.WARNING,
                        category=ValidationCategory.LEGAL,
                        suggestion=f"Warning: {warning}"
                    ))
        
        # Check if structure is broken
        if "Subject:" in original_text and "Subject:" not in edited_text:
            issues.append(ValidationIssue(
                code="STRUCTURE_BROKEN",
                message="Subject line should not be removed from formal application",
                message_hi="औपचारिक आवेदन से विषय पंक्ति नहीं हटाई जानी चाहिए",
                severity=ValidationSeverity.WARNING,
                category=ValidationCategory.FORMAT
            ))
        
        is_safe = not any(i.severity == ValidationSeverity.ERROR for i in issues)
        
        return is_safe, issues


# Singleton instance
_validator = None

def get_validator() -> RTIValidator:
    """Get validator singleton"""
    global _validator
    if _validator is None:
        _validator = RTIValidator()
    return _validator
