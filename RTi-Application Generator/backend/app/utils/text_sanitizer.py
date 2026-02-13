"""
Text Sanitizer
PII safety and text cleanup utilities
"""

import re
from typing import List, Tuple


# Patterns for PII detection (for warning, not storage)
PII_PATTERNS = {
    "aadhaar": r'\b\d{4}\s?\d{4}\s?\d{4}\b',
    "pan": r'\b[A-Z]{5}\d{4}[A-Z]\b',
    "phone": r'\b(?:\+91[\-\s]?)?[6-9]\d{9}\b',
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "bank_account": r'\b\d{9,18}\b',
    "ifsc": r'\b[A-Z]{4}0[A-Z0-9]{6}\b'
}


def detect_pii(text: str) -> List[Tuple[str, str]]:
    """
    Detect potential PII in text.
    Returns list of (pii_type, matched_text) tuples.
    
    NOTE: This is for warning users, not for storing/processing PII.
    """
    found = []
    
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            found.append((pii_type, match))
    
    return found


def warn_about_pii(text: str) -> dict:
    """
    Check text for PII and return warnings.
    """
    pii_found = detect_pii(text)
    
    if not pii_found:
        return {"has_pii": False, "warnings": []}
    
    warnings = []
    pii_types = set(p[0] for p in pii_found)
    
    warning_messages = {
        "aadhaar": "⚠️ Aadhaar number detected. Consider if this is necessary.",
        "pan": "⚠️ PAN number detected. Consider if this is necessary.",
        "phone": "📱 Phone number detected. This will be included in your application.",
        "email": "📧 Email detected. This will be included in your application.",
        "bank_account": "⚠️ Possible bank account number detected. Remove if not required.",
        "ifsc": "⚠️ IFSC code detected. Remove if not required."
    }
    
    for pii_type in pii_types:
        if pii_type in warning_messages:
            warnings.append(warning_messages[pii_type])
    
    return {
        "has_pii": True,
        "warnings": warnings,
        "types_found": list(pii_types)
    }


def sanitize_for_logging(text: str) -> str:
    """
    Sanitize text for logging by masking PII.
    Used for audit logs - never store actual PII.
    """
    sanitized = text
    
    # Mask Aadhaar
    sanitized = re.sub(r'\b(\d{4})\s?(\d{4})\s?(\d{4})\b', r'XXXX XXXX \3', sanitized)
    
    # Mask PAN
    sanitized = re.sub(r'\b[A-Z]{5}\d{4}[A-Z]\b', 'XXXXX0000X', sanitized)
    
    # Mask phone (keep last 4)
    sanitized = re.sub(r'\b(?:\+91[\-\s]?)?([6-9]\d{5})(\d{4})\b', r'XXXXXX\2', sanitized)
    
    # Mask email (keep domain)
    sanitized = re.sub(r'\b[A-Za-z0-9._%+-]+(@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b', r'****\1', sanitized)
    
    return sanitized


def clean_input(text: str) -> str:
    """
    Clean user input text.
    - Remove control characters
    - Normalize whitespace
    - Remove potentially dangerous content
    """
    if not text:
        return ""
    
    # Remove control characters (except newline, tab)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove HTML/script tags
    text = re.sub(r'<[^>]+>', '', text)
    
    return text.strip()
