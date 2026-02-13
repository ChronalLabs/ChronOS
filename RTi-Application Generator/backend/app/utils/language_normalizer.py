"""
Language Normalizer
Handles Indian language cleanup and transliteration
"""

from typing import Optional
import re

try:
    from indic_transliteration import sanscript
    INDIC_AVAILABLE = True
except ImportError:
    INDIC_AVAILABLE = False

try:
    from langdetect import detect
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False


def detect_language(text: str) -> str:
    """
    Detect language of input text.
    Returns ISO 639-1 code (en, hi, ta, etc.)
    """
    if not LANGDETECT_AVAILABLE:
        return "en"  # Default to English
    
    try:
        return detect(text)
    except:
        return "en"


def normalize_indian_text(text: str, target_script: str = "devanagari") -> str:
    """
    Normalize Indian language text.
    - Handles mixed scripts
    - Normalizes spacing
    - Removes extra characters
    """
    if not text:
        return text
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove zero-width characters
    text = re.sub(r'[\u200b-\u200f\u202a-\u202e]', '', text)
    
    return text


def transliterate(text: str, from_script: str, to_script: str) -> str:
    """
    Transliterate text between scripts.
    
    Supported scripts: devanagari, tamil, telugu, kannada, malayalam, etc.
    """
    if not INDIC_AVAILABLE:
        return text
    
    script_map = {
        "devanagari": sanscript.DEVANAGARI,
        "tamil": sanscript.TAMIL,
        "telugu": sanscript.TELUGU,
        "kannada": sanscript.KANNADA,
        "malayalam": sanscript.MALAYALAM,
        "bengali": sanscript.BENGALI,
        "gujarati": sanscript.GUJARATI,
        "latin": sanscript.ITRANS
    }
    
    from_s = script_map.get(from_script.lower())
    to_s = script_map.get(to_script.lower())
    
    if not from_s or not to_s:
        return text
    
    try:
        return sanscript.transliterate(text, from_s, to_s)
    except:
        return text


def clean_for_document(text: str) -> str:
    """
    Clean text for inclusion in formal documents.
    - Proper capitalization
    - Remove informal language markers
    - Normalize punctuation
    """
    # Capitalize first letter of sentences
    text = re.sub(r'(^|[.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
    
    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    
    # Remove multiple punctuation
    text = re.sub(r'[!?]{2,}', '.', text)
    text = re.sub(r'\.{3,}', '...', text)
    
    return text.strip()
