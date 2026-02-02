"""
Tone Adjuster
Adjusts document tone based on user preference
"""

from typing import Dict, List
import re


# Common casual abbreviations to fix (applied to all tones)
CASUAL_FIXES = {
    "plz": "please",
    "pls": "please",
    "thx": "thanks",
    "thnks": "thanks",
    "u": "you",
    "r": "are",
    "ur": "your",
    "bcoz": "because",
    "cuz": "because",
    "coz": "because",
    "fav": "favorable",
    "info": "information",
    "abt": "about",
    "msg": "message",
    "min": "minimum",
    "max": "maximum",
    "approx": "approximately",
    "yr": "year",
    "yrs": "years",
    "no.": "number",
}

# Tone-specific word replacements
TONE_REPLACEMENTS = {
    "formal": {
        "want": "wish",
        "need": "require",
        "ask": "request",
        "tell": "inform",
        "give": "provide",
        "get": "obtain",
        "help": "assist",
        "problem": "issue",
        "fix": "resolve",
        "bad": "unsatisfactory",
        "good": "satisfactory"
    },
    "assertive": {
        "request": "demand",
        "wish": "insist",
        "hope": "expect",
        "kindly": "immediately",
        "at your convenience": "without delay",
        "if possible": "as required by law"
    }
}

# Tone-specific phrases
TONE_PHRASES = {
    "neutral": {
        "opening": "I am writing to",
        "request": "I request you to kindly",
        "closing": "Thanking you"
    },
    "formal": {
        "opening": "I hereby wish to bring to your kind attention",
        "request": "I humbly request your good office to",
        "closing": "With respectful regards"
    },
    "assertive": {
        "opening": "I am compelled to bring to your notice",
        "request": "I demand immediate action regarding",
        "closing": "I expect prompt action failing which I shall be constrained to approach higher authorities"
    }
}


def adjust_tone(text: str, target_tone: str) -> str:
    """
    Adjust text tone to match target.
    
    target_tone: 'neutral', 'formal', 'assertive'
    """
    if not text:
        return text

    result = text
    
    # 1. Expand common abbreviations (Always done first)
    for abbr, full in CASUAL_FIXES.items():
        # Match standalone words only (e.g. don't replace 'u' in 'house')
        pattern = re.compile(r'\b' + re.escape(abbr) + r'\b', re.IGNORECASE)
        result = pattern.sub(lambda m: full if m.group().islower() else full.capitalize(), result)

    if target_tone not in ["neutral", "formal", "assertive"]:
        return result
    
    # 2. Apply tone-specific replacements
    if target_tone in TONE_REPLACEMENTS:
        for old, new in TONE_REPLACEMENTS[target_tone].items():
            # Case-insensitive replacement, preserving case
            pattern = re.compile(r'\b' + re.escape(old) + r'\b', re.IGNORECASE)
            result = pattern.sub(lambda m: new if m.group().islower() else new.capitalize(), result)
    
    return result


def get_tone_phrases(tone: str) -> Dict[str, str]:
    """Get phrases appropriate for the selected tone"""
    return TONE_PHRASES.get(tone, TONE_PHRASES["neutral"])


def suggest_tone(issue_type: str, urgency: str) -> str:
    """
    Suggest appropriate tone based on issue type and urgency.
    """
    if urgency == "critical":
        return "assertive"
    elif issue_type in ["corruption", "harassment", "misconduct"]:
        return "assertive"
    elif issue_type in ["rti", "information_request"]:
        return "formal"
    else:
        return "neutral"
