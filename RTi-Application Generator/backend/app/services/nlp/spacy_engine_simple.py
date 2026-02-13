"""
Simplified spaCy Engine - Fallback version when spaCy is not available
"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

def extract_entities(text: str) -> Dict[str, List[str]]:
    """Basic entity extraction fallback"""
    return {
        "PERSON": [],
        "ORG": [],
        "GPE": [],
        "DATE": [],
        "MONEY": [],
        "REFERENCE_NUMBER": [],
        "PHONE": [],
        "EMAIL": []
    }

def extract_key_phrases(text: str, top_n: int = 10) -> List[str]:
    """Basic key phrase extraction"""
    words = text.split()
    return [word.lower() for word in words if len(word) > 4][:top_n]

def analyze_sentiment_basic(text: str) -> str:
    """Basic sentiment analysis using keyword matching"""
    text_lower = text.lower()
    
    urgent_words = [
        "urgent", "immediately", "emergency", "asap", "critical",
        "life threatening", "danger", "dire", "pressing", "time-sensitive"
    ]
    frustrated_words = [
        "frustrated", "angry", "annoyed", "disappointed", "unsatisfied",
        "terrible", "awful", "horrible", "disgusted", "fed up", "sick of"
    ]
    formal_words = [
        "kindly", "respectfully", "humbly", "gratefully", "sincerely",
        "please consider", "request", "would appreciate"
    ]
    
    # Count matches
    urgent_score = sum(1 for word in urgent_words if word in text_lower)
    frustrated_score = sum(1 for word in frustrated_words if word in text_lower)  
    formal_score = sum(1 for word in formal_words if word in text_lower)
    
    # Determine sentiment
    if urgent_score > 1:
        return "urgent"
    elif frustrated_score > formal_score:
        return "frustrated"
    elif formal_score > 0:
        return "formal"
    else:
        return "neutral"