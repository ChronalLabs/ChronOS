"""
Hindi Language Support
Keywords, translations, and language detection for Hindi input

Supports:
- Hindi (Devanagari script)
- Hinglish (Hindi words in Roman script)
- Mixed Hindi-English text
"""

import re
from typing import Dict, List, Tuple, Optional
from enum import Enum


class DetectedLanguage(Enum):
    ENGLISH = "english"
    HINDI = "hindi"
    HINGLISH = "hinglish"  # Mixed Hindi-English
    UNKNOWN = "unknown"


# ============================================================================
# HINDI RTI KEYWORDS (Devanagari + Romanized)
# ============================================================================

HINDI_RTI_KEYWORDS = {
    # High confidence - Devanagari
    "सूचना का अधिकार": 0.3,
    "आरटीआई": 0.3,
    "सूचना अधिनियम": 0.3,
    "धारा 6": 0.3,
    "जन सूचना अधिकारी": 0.25,
    
    # High confidence - Romanized (Hinglish)
    "soochna ka adhikar": 0.3,
    "suchna ka adhikar": 0.3,
    "rti": 0.3,
    "jan soochna adhikari": 0.25,
    
    # Medium confidence - Devanagari
    "सूचना": 0.2,
    "जानकारी": 0.2,
    "दस्तावेज": 0.2,
    "रिकॉर्ड": 0.2,
    "प्रमाणित प्रति": 0.2,
    "नकल": 0.2,
    "विवरण": 0.2,
    
    # Medium confidence - Romanized
    "soochna": 0.2,
    "suchna": 0.2,
    "jaankari": 0.2,
    "jankari": 0.2,
    "dastavez": 0.2,
    "record": 0.15,
    "nakal": 0.2,
    "vivaran": 0.2,
    
    # Low confidence
    "जाने": 0.1,
    "बताएं": 0.1,
    "कितना": 0.1,
    "क्या हुआ": 0.1,
    "kitna": 0.1,
    "kya hua": 0.1,
    "bataye": 0.1,
    "jane": 0.1,
}


# ============================================================================
# HINDI COMPLAINT KEYWORDS (Devanagari + Romanized)
# ============================================================================

HINDI_COMPLAINT_KEYWORDS = {
    # High confidence - Devanagari
    "शिकायत": 0.3,
    "समस्या": 0.3,
    "परेशानी": 0.3,
    "कार्रवाई करें": 0.3,
    "जन शिकायत": 0.3,
    
    # High confidence - Romanized
    "shikayat": 0.3,
    "shikaayat": 0.3,
    "samasya": 0.3,
    "pareshani": 0.3,
    "karwai kare": 0.3,
    "jan shikayat": 0.3,
    
    # Medium confidence - Devanagari
    "भ्रष्टाचार": 0.25,
    "रिश्वत": 0.25,
    "घूस": 0.25,
    "उत्पीड़न": 0.25,
    "लापरवाही": 0.2,
    "देरी": 0.2,
    "खराब": 0.2,
    "टूटा": 0.2,
    "बंद": 0.2,
    "काम नहीं": 0.2,
    
    # Medium confidence - Romanized
    "bhrashtachar": 0.25,
    "rishwat": 0.25,
    "ghoos": 0.25,
    "utpidan": 0.25,
    "laparwahi": 0.2,
    "deri": 0.2,
    "kharab": 0.2,
    "toota": 0.2,
    "band": 0.15,
    "kaam nahi": 0.2,
    
    # Low confidence
    "दिक्कत": 0.1,
    "तकलीफ": 0.1,
    "मुश्किल": 0.1,
    "dikkat": 0.1,
    "takleef": 0.1,
    "mushkil": 0.1,
}


# ============================================================================
# HINDI ISSUE CATEGORY KEYWORDS
# ============================================================================

HINDI_ISSUE_KEYWORDS = {
    "electricity": {
        # Devanagari
        "बिजली": 0.3, "बिज़ली": 0.3, "विद्युत": 0.3,
        "मीटर": 0.2, "बिल": 0.2, "ट्रांसफार्मर": 0.2,
        "वोल्टेज": 0.2, "कटौती": 0.25, "लोड शेडिंग": 0.25,
        "कनेक्शन": 0.2, "तार": 0.15,
        # Romanized
        "bijli": 0.3, "bijlee": 0.3, "vidyut": 0.3,
        "meter": 0.2, "bill": 0.15, "transformer": 0.2,
        "voltage": 0.2, "load shedding": 0.25,
        "connection": 0.15, "taar": 0.15,
    },
    "water": {
        # Devanagari
        "पानी": 0.3, "जल": 0.3, "नल": 0.25,
        "पाइपलाइन": 0.25, "टंकी": 0.2, "नाली": 0.2,
        "सीवर": 0.2, "जलापूर्ति": 0.3, "बोरवेल": 0.2,
        "गंदा पानी": 0.25,
        # Romanized
        "paani": 0.3, "pani": 0.3, "jal": 0.3,
        "nal": 0.25, "pipeline": 0.25, "tanki": 0.2,
        "naali": 0.2, "sewer": 0.2, "borewell": 0.2,
        "ganda pani": 0.25,
    },
    "roads": {
        # Devanagari
        "सड़क": 0.3, "गड्ढा": 0.3, "गड्ढे": 0.3,
        "रास्ता": 0.2, "फुटपाथ": 0.2, "पुल": 0.2,
        "फ्लाईओवर": 0.2, "स्ट्रीट लाइट": 0.2,
        "टूटी सड़क": 0.25, "खराब सड़क": 0.25,
        # Romanized
        "sadak": 0.3, "gadda": 0.3, "gaddha": 0.3,
        "rasta": 0.2, "footpath": 0.2, "pul": 0.2,
        "flyover": 0.2, "street light": 0.2,
        "tooti sadak": 0.25, "kharab sadak": 0.25,
    },
    "education": {
        # Devanagari
        "स्कूल": 0.3, "विद्यालय": 0.3, "कॉलेज": 0.25,
        "शिक्षा": 0.25, "दाखिला": 0.2, "प्रवेश": 0.2,
        "फीस": 0.2, "शिक्षक": 0.2, "छात्र": 0.15,
        "परीक्षा": 0.2, "छात्रवृत्ति": 0.2,
        # Romanized
        "school": 0.3, "vidyalaya": 0.3, "college": 0.25,
        "shiksha": 0.25, "daakhila": 0.2, "pravesh": 0.2,
        "fees": 0.2, "shikshak": 0.2, "chatra": 0.15,
        "pariksha": 0.2, "scholarship": 0.2,
    },
    "health": {
        # Devanagari
        "अस्पताल": 0.3, "हॉस्पिटल": 0.3, "स्वास्थ्य": 0.25,
        "डॉक्टर": 0.25, "दवाई": 0.2, "इलाज": 0.25,
        "मरीज": 0.15, "एम्बुलेंस": 0.2, "टीका": 0.2,
        "आयुष्मान": 0.25,
        # Romanized
        "aspatal": 0.3, "hospital": 0.3, "swasthya": 0.25,
        "doctor": 0.25, "dawai": 0.2, "ilaaj": 0.25,
        "mareez": 0.15, "ambulance": 0.2, "teeka": 0.2,
        "ayushman": 0.25,
    },
    "police": {
        # Devanagari
        "पुलिस": 0.3, "थाना": 0.3, "एफआईआर": 0.3,
        "चोरी": 0.25, "अपराध": 0.25, "सुरक्षा": 0.2,
        "कानून व्यवस्था": 0.25, "गुंडागर्दी": 0.25,
        # Romanized
        "police": 0.3, "thana": 0.3, "fir": 0.3,
        "chori": 0.25, "apradh": 0.25, "suraksha": 0.2,
        "kanoon vyavastha": 0.25, "gundagardi": 0.25,
    },
    "municipal": {
        # Devanagari
        "नगरपालिका": 0.3, "नगर निगम": 0.3, "कूड़ा": 0.25,
        "कचरा": 0.25, "सफाई": 0.25, "स्वच्छता": 0.25,
        "नाला": 0.2, "गटर": 0.2,
        # Romanized
        "nagarpalika": 0.3, "nagar nigam": 0.3, "kooda": 0.25,
        "kachra": 0.25, "safai": 0.25, "swachhata": 0.25,
        "nala": 0.2, "gutter": 0.2,
    },
    "ration": {
        # Devanagari
        "राशन": 0.3, "राशन कार्ड": 0.3, "खाद्य": 0.25,
        "गेहूं": 0.2, "चावल": 0.2, "केरोसिन": 0.2,
        "उचित मूल्य दुकान": 0.25, "पीडीएस": 0.25,
        # Romanized
        "ration": 0.3, "ration card": 0.3, "khadya": 0.25,
        "gehun": 0.2, "chawal": 0.2, "kerosene": 0.2,
        "fair price shop": 0.25, "pds": 0.25,
    },
    "pension": {
        # Devanagari
        "पेंशन": 0.3, "वृद्धावस्था": 0.25, "विधवा पेंशन": 0.25,
        "विकलांग पेंशन": 0.25, "सेवानिवृत्ति": 0.2,
        # Romanized
        "pension": 0.3, "vridhavastha": 0.25, "vidhwa pension": 0.25,
        "viklang pension": 0.25, "retirement": 0.2,
    },
    "transport": {
        # Devanagari
        "परिवहन": 0.3, "बस": 0.25, "लाइसेंस": 0.25,
        "आरसी": 0.2, "गाड़ी": 0.15, "वाहन": 0.2,
        "ड्राइविंग लाइसेंस": 0.25,
        # Romanized
        "parivahan": 0.3, "bus": 0.25, "license": 0.25,
        "rc": 0.2, "gaadi": 0.15, "vahan": 0.2,
        "driving license": 0.25,
    },
}


# ============================================================================
# LANGUAGE DETECTION
# ============================================================================

# Devanagari Unicode range
DEVANAGARI_PATTERN = re.compile(r'[\u0900-\u097F]')

# Common Hinglish words (not English, but romanized Hindi)
HINGLISH_MARKERS = {
    "kya", "kaise", "kaha", "kab", "kyun", "kaun",
    "hai", "hain", "tha", "the", "thi", "hoga", "hogi",
    "mera", "meri", "mere", "apna", "apni", "apne",
    "aap", "tum", "tumhara", "unka", "iska", "uska",
    "nahi", "nahin", "mat", "sirf", "bahut", "thoda",
    "aur", "ya", "lekin", "par", "isliye", "kyunki",
    "abhi", "tab", "jab", "phir", "pehle", "baad",
    "yahan", "wahan", "idhar", "udhar",
    "karo", "karna", "karke", "kiya", "kiye",
    "dena", "lena", "jana", "aana", "rakhna",
    "chahiye", "chahte", "sakta", "sakti", "sakte",
    "wala", "wali", "wale",
    # Common complaint/RTI words
    "shikayat", "samasya", "pareshani", "soochna", "jaankari",
    "kripya", "dhanyawad", "seva", "madad", "sahayata",
}


def detect_language(text: str) -> Tuple[DetectedLanguage, float]:
    """
    Detect whether text is English, Hindi, or Hinglish.
    
    Returns:
        Tuple of (detected_language, confidence)
    """
    if not text or not text.strip():
        return DetectedLanguage.UNKNOWN, 0.0
    
    text_lower = text.lower()
    words = text_lower.split()
    total_words = len(words)
    
    if total_words == 0:
        return DetectedLanguage.UNKNOWN, 0.0
    
    # Check for Devanagari script
    devanagari_chars = len(DEVANAGARI_PATTERN.findall(text))
    total_chars = len(text.replace(" ", ""))
    
    if total_chars == 0:
        return DetectedLanguage.UNKNOWN, 0.0
    
    devanagari_ratio = devanagari_chars / total_chars
    
    # Pure Hindi (Devanagari script)
    if devanagari_ratio > 0.5:
        return DetectedLanguage.HINDI, min(0.95, 0.5 + devanagari_ratio * 0.5)
    
    # Check for Hinglish markers
    hinglish_word_count = sum(1 for word in words if word in HINGLISH_MARKERS)
    hinglish_ratio = hinglish_word_count / total_words
    
    # Mixed script (some Devanagari + Roman)
    if devanagari_ratio > 0.1 and devanagari_ratio <= 0.5:
        return DetectedLanguage.HINGLISH, 0.7 + devanagari_ratio
    
    # Romanized Hindi (Hinglish)
    if hinglish_ratio > 0.2:
        return DetectedLanguage.HINGLISH, min(0.9, 0.5 + hinglish_ratio)
    
    # Default to English
    return DetectedLanguage.ENGLISH, 0.8


def transliterate_to_english_keywords(text: str) -> str:
    """
    Convert Hindi text to searchable English keywords.
    This helps the rule engine match Hindi input to English patterns.
    """
    # Common Hindi to English translations for document generation
    translations = {
        # RTI related
        "सूचना का अधिकार": "right to information",
        "सूचना": "information",
        "जानकारी": "information details",
        "दस्तावेज": "documents",
        "प्रति": "copy",
        "नकल": "copy",
        
        # Complaint related
        "शिकायत": "complaint",
        "समस्या": "problem issue",
        "परेशानी": "problem harassment",
        "कार्रवाई": "action",
        "भ्रष्टाचार": "corruption",
        "रिश्वत": "bribe corruption",
        "लापरवाही": "negligence",
        
        # Departments
        "बिजली": "electricity power",
        "पानी": "water supply",
        "सड़क": "road",
        "स्कूल": "school education",
        "अस्पताल": "hospital health",
        "पुलिस": "police",
        "राशन": "ration pds",
        
        # Common terms
        "कृपया": "please kindly",
        "धन्यवाद": "thank you",
        "महोदय": "sir madam respected",
    }
    
    result = text
    for hindi, english in translations.items():
        result = result.replace(hindi, f" {english} ")
    
    return result


def get_hindi_keywords_for_intent(intent: str) -> Dict[str, float]:
    """Get Hindi keywords for a specific intent type."""
    if intent == "rti":
        return HINDI_RTI_KEYWORDS
    elif intent == "complaint":
        return HINDI_COMPLAINT_KEYWORDS
    return {}


def get_hindi_keywords_for_issue(category: str) -> Dict[str, float]:
    """Get Hindi keywords for a specific issue category."""
    return HINDI_ISSUE_KEYWORDS.get(category, {})
