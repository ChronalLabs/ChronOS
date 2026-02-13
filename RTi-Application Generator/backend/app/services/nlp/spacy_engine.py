"""
spaCy NLP Engine
Handles Named Entity Recognition, phrase matching, and linguistic analysis
SECONDARY to rule engine - only used when rules don't match

Following MODEL_USAGE_POLICY:
- Used ONLY for NER and phrase matching
- No classification decisions (handled by rule engine)
- Supports audit trail for all extractions
"""

import spacy
from spacy.matcher import PhraseMatcher, Matcher
import logging

logger = logging.getLogger(__name__)

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import re

# spaCy availability flag - True since we're using Python 3.13 compatible version
SPACY_AVAILABLE = True

# Load model (will be initialized on first use)
_nlp = None
_phrase_matcher = None
_pattern_matcher = None


class EntityType(Enum):
    """Standardized entity types for civic documents"""
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    DATE = "date"
    MONEY = "money"
    REFERENCE_NUMBER = "reference_number"
    PHONE = "phone"
    EMAIL = "email"
    ADDRESS = "address"


@dataclass
class ExtractedEntity:
    """Entity with metadata for audit trail"""
    text: str
    entity_type: EntityType
    confidence: float
    start_char: int
    end_char: int
    source: str = "spacy"  # 'spacy', 'regex', 'pattern'
    
    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "type": self.entity_type.value,
            "confidence": self.confidence,
            "span": [self.start_char, self.end_char],
            "source": self.source
        }


@dataclass
class NLPResult:
    """Complete NLP analysis result with audit trail"""
    entities: List[ExtractedEntity]
    key_phrases: List[str]
    sentiment: str
    urgency_level: str
    word_count: int
    processing_time_ms: float
    model_version: str
    audit_trail: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "entities": {
                ent.entity_type.value: [e.to_dict() for e in self.entities if e.entity_type == ent.entity_type]
                for ent in set(e.entity_type for e in self.entities)
            },
            "key_phrases": self.key_phrases,
            "sentiment": self.sentiment,
            "urgency_level": self.urgency_level,
            "word_count": self.word_count,
            "processing_time_ms": self.processing_time_ms,
            "model_version": self.model_version,
            "audit_trail": self.audit_trail
        }


def get_nlp():
    """Lazy load spaCy model with error handling"""
    global _nlp
    if not SPACY_AVAILABLE:
        raise RuntimeError("spaCy not available due to compatibility issues")
    
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
            logger.info(f"Loaded spaCy model: en_core_web_sm")
        except OSError:
            raise RuntimeError(
                "spaCy model not found. Run: python -m spacy download en_core_web_sm"
            )
    return _nlp


def get_phrase_matcher() -> PhraseMatcher:
    """Initialize phrase matcher with civic-specific patterns"""
    global _phrase_matcher
    if not SPACY_AVAILABLE:
        raise RuntimeError("spaCy not available for phrase matching")
        
    if _phrase_matcher is None:
        nlp = get_nlp()
        _phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        
        # Government departments
        departments = [
            "electricity board", "water board", "municipal corporation",
            "police station", "tehsil office", "district collector",
            "block development office", "gram panchayat", "nagar palika",
            "pwd", "phed", "rto", "education department", "health department"
        ]
        
        # RTI-related phrases
        rti_phrases = [
            "right to information", "rti act", "section 6", "section 8",
            "public information officer", "pio", "first appellate authority",
            "state information commission", "central information commission"
        ]
        
        # Complaint markers
        complaint_phrases = [
            "grievance", "complaint", "harassment", "corruption",
            "bribe", "negligence", "misconduct", "poor service"
        ]
        
        # Add patterns
        _phrase_matcher.add("DEPARTMENT", [nlp.make_doc(text) for text in departments])
        _phrase_matcher.add("RTI_TERM", [nlp.make_doc(text) for text in rti_phrases])
        _phrase_matcher.add("COMPLAINT_MARKER", [nlp.make_doc(text) for text in complaint_phrases])
    
    return _phrase_matcher


def get_pattern_matcher() -> Matcher:
    """Initialize pattern matcher for structured data extraction"""
    global _pattern_matcher
    if _pattern_matcher is None:
        nlp = get_nlp()
        _pattern_matcher = Matcher(nlp.vocab)
        
        # Reference number patterns (e.g., "Ref. No. ABC/123/2024")
        _pattern_matcher.add("REFERENCE_NUMBER", [
            [{"LOWER": {"IN": ["ref", "reference", "complaint", "application"]}},
             {"IS_PUNCT": True, "OP": "?"},
             {"LOWER": {"IN": ["no", "number", "id"]}},
             {"IS_PUNCT": True, "OP": "?"},
             {"LIKE_NUM": True}],
            [{"TEXT": {"REGEX": r"[A-Z]{2,}/\d+/\d+"}}]
        ])
        
        # Date patterns
        _pattern_matcher.add("DATE_PATTERN", [
            [{"SHAPE": "dd"}, {"IS_PUNCT": True}, {"SHAPE": "dd"}, {"IS_PUNCT": True}, {"SHAPE": "dddd"}],
            [{"SHAPE": "dd"}, {"LOWER": {"IN": ["jan", "feb", "mar", "apr", "may", "jun", 
                                                  "jul", "aug", "sep", "oct", "nov", "dec",
                                                  "january", "february", "march", "april",
                                                  "may", "june", "july", "august", "september",
                                                  "october", "november", "december"]}},
             {"SHAPE": "dddd", "OP": "?"}]
        ])
    
    return _pattern_matcher


# Indian location patterns for better NER
INDIAN_STATES = [
    "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh",
    "goa", "gujarat", "haryana", "himachal pradesh", "jharkhand", "karnataka",
    "kerala", "madhya pradesh", "maharashtra", "manipur", "meghalaya", "mizoram",
    "nagaland", "odisha", "punjab", "rajasthan", "sikkim", "tamil nadu",
    "telangana", "tripura", "uttar pradesh", "uttarakhand", "west bengal",
    "delhi", "jammu and kashmir", "ladakh", "chandigarh", "puducherry"
]

INDIAN_CITIES = [
    "mumbai", "delhi", "bangalore", "bengaluru", "hyderabad", "chennai",
    "kolkata", "pune", "ahmedabad", "jaipur", "lucknow", "kanpur",
    "nagpur", "indore", "thane", "bhopal", "visakhapatnam", "patna",
    "vadodara", "ghaziabad", "ludhiana", "agra", "nashik", "ranchi"
]


def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract named entities from text using spaCy + custom patterns.
    
    Returns dict with entity types as keys:
    - PERSON: Names
    - ORG: Organizations  
    - GPE: Locations (cities, states)
    - DATE: Dates
    - MONEY: Monetary values
    
    Enhanced with:
    - Indian location recognition
    - Reference number extraction
    - Phone/email patterns
    """
    if not SPACY_AVAILABLE:
        logger.warning("spaCy not available, returning empty entities")
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
    
    nlp = get_nlp()
    doc = nlp(text)
    
    entities: Dict[str, List[str]] = {}
    
    # Extract spaCy NER entities
    for ent in doc.ents:
        label = ent.label_
        if label not in entities:
            entities[label] = []
        if ent.text not in entities[label]:
            entities[label].append(ent.text)
    
    # Enhance with Indian locations
    text_lower = text.lower()
    
    if "GPE" not in entities:
        entities["GPE"] = []
    
    for state in INDIAN_STATES:
        if state in text_lower:
            formatted = state.title()
            if formatted not in entities["GPE"]:
                entities["GPE"].append(formatted)
    
    for city in INDIAN_CITIES:
        if city in text_lower:
            formatted = city.title()
            if formatted not in entities["GPE"]:
                entities["GPE"].append(formatted)
    
    # Extract reference numbers via regex
    ref_patterns = [
        r'(?:ref|reference|complaint|application)[\s.:#-]*(?:no|number|id)?[\s.:#-]*([A-Z0-9/-]+)',
        r'\b([A-Z]{2,}/\d+/\d{4})\b',
        r'\b(\d{4}/[A-Z]+/\d+)\b'
    ]
    
    entities["REFERENCE"] = []
    for pattern in ref_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match and match not in entities["REFERENCE"]:
                entities["REFERENCE"].append(match.upper())
    
    # Extract phone numbers
    phone_pattern = r'(?:\+91[\s-]?)?[6-9]\d{9}'
    phones = re.findall(phone_pattern, text)
    if phones:
        entities["PHONE"] = list(set(phones))
    
    # Extract emails
    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
    emails = re.findall(email_pattern, text)
    if emails:
        entities["EMAIL"] = list(set(emails))
    
    return entities


def extract_entities_detailed(text: str) -> List[ExtractedEntity]:
    """
    Extract entities with full metadata for audit trail.
    Returns list of ExtractedEntity objects with confidence scores.
    """
    import time
    nlp = get_nlp()
    doc = nlp(text)
    
    entities: List[ExtractedEntity] = []
    
    # spaCy NER entities
    label_to_type = {
        "PERSON": EntityType.PERSON,
        "ORG": EntityType.ORGANIZATION,
        "GPE": EntityType.LOCATION,
        "LOC": EntityType.LOCATION,
        "DATE": EntityType.DATE,
        "MONEY": EntityType.MONEY
    }
    
    for ent in doc.ents:
        if ent.label_ in label_to_type:
            entities.append(ExtractedEntity(
                text=ent.text,
                entity_type=label_to_type[ent.label_],
                confidence=0.85,  # spaCy doesn't provide confidence, using default
                start_char=ent.start_char,
                end_char=ent.end_char,
                source="spacy_ner"
            ))
    
    # Pattern-based extraction with regex
    text_lower = text.lower()
    
    # Indian states with positions
    for state in INDIAN_STATES:
        for match in re.finditer(re.escape(state), text_lower):
            entities.append(ExtractedEntity(
                text=state.title(),
                entity_type=EntityType.LOCATION,
                confidence=0.95,  # Exact match = high confidence
                start_char=match.start(),
                end_char=match.end(),
                source="pattern_indian_state"
            ))
    
    # Phone numbers
    for match in re.finditer(r'(?:\+91[\s-]?)?[6-9]\d{9}', text):
        entities.append(ExtractedEntity(
            text=match.group(),
            entity_type=EntityType.PHONE,
            confidence=0.9,
            start_char=match.start(),
            end_char=match.end(),
            source="regex_phone"
        ))
    
    # Email addresses
    for match in re.finditer(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', text):
        entities.append(ExtractedEntity(
            text=match.group(),
            entity_type=EntityType.EMAIL,
            confidence=0.95,
            start_char=match.start(),
            end_char=match.end(),
            source="regex_email"
        ))
    
    # Reference numbers
    ref_pattern = r'(?:ref|reference|complaint|application)[\s.:#-]*(?:no|number|id)?[\s.:#-]*([A-Z0-9/-]+)'
    for match in re.finditer(ref_pattern, text, re.IGNORECASE):
        entities.append(ExtractedEntity(
            text=match.group(1).upper(),
            entity_type=EntityType.REFERENCE_NUMBER,
            confidence=0.8,
            start_char=match.start(1),
            end_char=match.end(1),
            source="regex_reference"
        ))
    
    # Deduplicate by position
    seen_spans = set()
    unique_entities = []
    for ent in entities:
        span = (ent.start_char, ent.end_char)
        if span not in seen_spans:
            seen_spans.add(span)
            unique_entities.append(ent)
    
    return unique_entities


def extract_key_phrases(text: str, top_n: int = 10) -> List[str]:
    """
    Extract key noun phrases from text.
    Enhanced with better filtering and ranking.
    """
    if not SPACY_AVAILABLE:
        logger.warning("spaCy not available, using basic phrase extraction")
        # Simple fallback: extract words over 4 characters
        words = text.split()
        return [word for word in words if len(word) > 4][:top_n]
    
    nlp = get_nlp()
    doc = nlp(text)
    
    # Extract noun chunks with scoring
    phrases_with_scores = []
    
    for chunk in doc.noun_chunks:
        # Filter criteria
        if len(chunk.text) < 3:
            continue
        if chunk.root.pos_ not in ["NOUN", "PROPN"]:
            continue
        if chunk.root.is_stop:
            continue
        
        # Score based on length and position
        score = len(chunk.text.split())  # Longer phrases score higher
        if chunk.root.pos_ == "PROPN":
            score += 1  # Proper nouns get bonus
        
        phrases_with_scores.append((chunk.text.lower().strip(), score))
    
    # Sort by score, deduplicate
    phrases_with_scores.sort(key=lambda x: x[1], reverse=True)
    seen = set()
    unique_phrases = []
    
    for phrase, _ in phrases_with_scores:
        if phrase not in seen:
            seen.add(phrase)
            unique_phrases.append(phrase)
        if len(unique_phrases) >= top_n:
            break
    
    return unique_phrases


def extract_matched_phrases(text: str) -> Dict[str, List[str]]:
    """
    Extract civic-specific phrases using PhraseMatcher.
    Returns categorized matches.
    """
    nlp = get_nlp()
    matcher = get_phrase_matcher()
    doc = nlp(text)
    
    matches = matcher(doc)
    
    results: Dict[str, List[str]] = {
        "DEPARTMENT": [],
        "RTI_TERM": [],
        "COMPLAINT_MARKER": []
    }
    
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        span_text = doc[start:end].text
        if span_text.lower() not in [m.lower() for m in results.get(label, [])]:
            results[label].append(span_text)
    
    return results


def analyze_sentiment_basic(text: str) -> str:
    """
    Basic sentiment analysis using keyword matching.
    Returns: 'urgent', 'frustrated', 'neutral', 'formal'
    
    Note: This is rule-based, not ML-based (per MODEL_USAGE_POLICY).
    """
    # This function doesn't use spaCy, so it works without it
    text_lower = text.lower()
    
    urgent_words = [
        "urgent", "immediately", "emergency", "asap", "critical",
        "life threatening", "danger", "dire", "pressing", "time-sensitive"
    ]
    frustrated_words = [
        "frustrated", "angry", "disappointed", "fed up", "worst",
        "terrible", "pathetic", "disgusted", "outraged", "unacceptable"
    ]
    formal_words = [
        "respectfully", "humbly", "request", "kindly", "pursuant",
        "hereby", "aforementioned", "undersigned"
    ]
    
    urgent_count = sum(1 for word in urgent_words if word in text_lower)
    frustrated_count = sum(1 for word in frustrated_words if word in text_lower)
    formal_count = sum(1 for word in formal_words if word in text_lower)
    
    # Priority: urgent > frustrated > formal > neutral
    if urgent_count >= 2:
        return "urgent"
    elif frustrated_count >= 2:
        return "frustrated"
    elif formal_count >= 2:
        return "formal"
    elif urgent_count > 0:
        return "urgent"
    elif frustrated_count > 0:
        return "frustrated"
    else:
        return "neutral"


def analyze_urgency(text: str) -> Tuple[str, float]:
    """
    Analyze urgency level of the text.
    Returns (urgency_level, confidence)
    
    Levels: 'critical', 'high', 'medium', 'low'
    """
    text_lower = text.lower()
    
    # Critical indicators
    critical_patterns = [
        r'life.{0,20}(?:risk|danger|threat)',
        r'medical.{0,10}emergency',
        r'immediate.{0,10}(?:action|attention)',
        r'(?:dying|death|dead)',
        r'(?:harassment|assault|attack)',
    ]
    
    # High urgency indicators
    high_patterns = [
        r'urgent(?:ly)?',
        r'as soon as possible',
        r'asap',
        r'time.{0,10}sensitive',
        r'deadline',
        r'pending.{0,10}(?:months|years)',
    ]
    
    # Medium urgency indicators
    medium_patterns = [
        r'(?:weeks?|days?).{0,10}(?:waiting|pending)',
        r'follow.{0,5}up',
        r'reminder',
        r'no.{0,10}response',
    ]
    
    # Check patterns
    critical_matches = sum(1 for p in critical_patterns if re.search(p, text_lower))
    high_matches = sum(1 for p in high_patterns if re.search(p, text_lower))
    medium_matches = sum(1 for p in medium_patterns if re.search(p, text_lower))
    
    if critical_matches > 0:
        return ("critical", min(0.95, 0.7 + critical_matches * 0.1))
    elif high_matches >= 2:
        return ("high", min(0.9, 0.6 + high_matches * 0.1))
    elif high_matches > 0 or medium_matches >= 2:
        return ("medium", min(0.85, 0.5 + (high_matches + medium_matches) * 0.1))
    else:
        return ("low", 0.7)


def full_analysis(text: str) -> NLPResult:
    """
    Perform complete NLP analysis on text.
    Returns comprehensive result with audit trail.
    """
    import time
    start_time = time.time()
    
    nlp = get_nlp()
    doc = nlp(text)
    
    # Collect all analysis
    entities = extract_entities_detailed(text)
    key_phrases = extract_key_phrases(text, top_n=10)
    sentiment = analyze_sentiment_basic(text)
    urgency_level, urgency_conf = analyze_urgency(text)
    matched_phrases = extract_matched_phrases(text)
    
    processing_time = (time.time() - start_time) * 1000
    
    # Build audit trail
    audit_trail = [
        {"step": "tokenization", "token_count": len(doc)},
        {"step": "ner_extraction", "entity_count": len(entities)},
        {"step": "phrase_extraction", "phrase_count": len(key_phrases)},
        {"step": "sentiment_analysis", "result": sentiment},
        {"step": "urgency_analysis", "result": urgency_level, "confidence": urgency_conf},
        {"step": "phrase_matching", "matches": {k: len(v) for k, v in matched_phrases.items()}}
    ]
    
    return NLPResult(
        entities=entities,
        key_phrases=key_phrases,
        sentiment=sentiment,
        urgency_level=urgency_level,
        word_count=len(doc),
        processing_time_ms=round(processing_time, 2),
        model_version="en_core_web_sm",
        audit_trail=audit_trail
    )


def preload_models():
    """Pre-load all models for faster first inference"""
    logger.info("Pre-loading spaCy models...")
    get_nlp()
    get_phrase_matcher()
    get_pattern_matcher()
    logger.info("spaCy models loaded successfully")
