"""
Semantic analyzer using spaCy.
Uses NLP for verb-object-role analysis and experience depth signals.
AI assists only - never makes decisions.
"""
from typing import Optional
import spacy


# Lazy load spaCy model
_nlp = None


def get_nlp():
    """Get or load the spaCy model."""
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Model not downloaded, return None
            _nlp = None
    return _nlp


def analyze_text(text: str) -> dict:
    """
    Analyze text for semantic signals.
    
    Args:
        text: Resume or JD text to analyze
    
    Returns:
        Dictionary with extracted signals (suggestions only)
    """
    nlp = get_nlp()
    if nlp is None:
        return {"error": "spaCy model not loaded", "signals": []}
    
    doc = nlp(text)
    
    signals = {
        "entities": extract_entities(doc),
        "verb_phrases": extract_verb_phrases(doc),
        "technical_terms": extract_technical_terms(doc),
        "experience_indicators": extract_experience_indicators(doc),
    }
    
    return signals


def extract_entities(doc) -> list[dict]:
    """
    Extract named entities from document.
    
    Returns organization names, dates, locations that might be relevant.
    """
    entities = []
    
    for ent in doc.ents:
        if ent.label_ in ["ORG", "DATE", "GPE", "PRODUCT"]:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
            })
    
    return entities


def extract_verb_phrases(doc) -> list[dict]:
    """
    Extract verb phrases indicating actions and responsibilities.
    
    Looks for patterns like "developed X", "led team to Y", "managed Z".
    """
    verb_phrases = []
    
    action_verbs = {
        "develop", "build", "create", "design", "implement", "lead",
        "manage", "architect", "optimize", "improve", "deploy", "scale",
        "automate", "integrate", "maintain", "test", "debug", "refactor",
        "mentor", "train", "collaborate", "research", "analyze",
    }
    
    for token in doc:
        if token.pos_ == "VERB" and token.lemma_.lower() in action_verbs:
            # Get the object of the verb
            objects = [child for child in token.children if child.dep_ in ["dobj", "pobj"]]
            
            phrase = {
                "verb": token.lemma_,
                "text": token.text,
                "objects": [obj.text for obj in objects],
                "context": _get_context(token, doc),
            }
            verb_phrases.append(phrase)
    
    return verb_phrases


def extract_technical_terms(doc) -> list[str]:
    """
    Extract potential technical terms for skill detection.
    
    Uses noun phrases and common patterns.
    """
    terms = set()
    
    # Extract noun chunks
    for chunk in doc.noun_chunks:
        # Filter for likely technical terms (capitalized or known patterns)
        text = chunk.text.strip()
        if len(text) > 2:
            # Check if likely technical (contains uppercase or common tech patterns)
            if any(c.isupper() for c in text[1:]) or text.lower() in _TECH_KEYWORDS:
                terms.add(text)
    
    return list(terms)


def extract_experience_indicators(doc) -> list[dict]:
    """
    Extract experience depth indicators.
    
    Looks for duration, scale, and leadership signals.
    """
    indicators = []
    
    text = doc.text.lower()
    
    # Duration patterns
    duration_patterns = [
        (r"\d+\+?\s*years?", "duration"),
        (r"\d+\s*months?", "duration"),
    ]
    
    # Scale patterns
    scale_patterns = [
        (r"team of \d+", "scale"),
        (r"\d+ (engineers|developers|team members)", "scale"),
        (r"(millions?|thousands?|billions?) of (users|requests|records)", "scale"),
    ]
    
    # Leadership patterns
    leadership_patterns = [
        (r"led (a |the )?team", "leadership"),
        (r"managed (a |the )?team", "leadership"),
        (r"mentored", "leadership"),
        (r"supervised", "leadership"),
    ]
    
    import re
    all_patterns = duration_patterns + scale_patterns + leadership_patterns
    
    for pattern, category in all_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            indicators.append({
                "text": match.group(),
                "category": category,
                "start": match.start(),
                "end": match.end(),
            })
    
    return indicators


def _get_context(token, doc, window: int = 10) -> str:
    """Get surrounding context for a token."""
    start = max(0, token.i - window)
    end = min(len(doc), token.i + window + 1)
    return doc[start:end].text


# Common technical keywords for detection
_TECH_KEYWORDS = {
    "python", "javascript", "java", "react", "node", "aws", "docker",
    "kubernetes", "sql", "mongodb", "redis", "api", "rest", "graphql",
    "machine learning", "deep learning", "tensorflow", "pytorch",
    "agile", "scrum", "ci/cd", "devops", "microservices",
}
