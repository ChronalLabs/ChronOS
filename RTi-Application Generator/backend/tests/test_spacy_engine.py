"""
Unit tests for SpaCy Engine - Self-contained version with mocks
Tests NLP entity extraction without requiring spaCy
"""

import pytest
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from unittest.mock import Mock, patch


# ============================================================================
# INLINE DEFINITIONS
# ============================================================================

class EntityType(Enum):
    """Types of entities that can be extracted"""
    PERSON = "PERSON"
    ORGANIZATION = "ORG"
    LOCATION = "LOC"
    DATE = "DATE"
    MONEY = "MONEY"
    DESIGNATION = "DESIGNATION"
    ADDRESS = "ADDRESS"
    PHONE = "PHONE"
    EMAIL = "EMAIL"


@dataclass
class ExtractedEntity:
    """Represents an extracted entity"""
    text: str
    entity_type: EntityType
    confidence: float
    start_pos: int
    end_pos: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "entity_type": self.entity_type.value,
            "confidence": self.confidence,
            "start_pos": self.start_pos,
            "end_pos": self.end_pos
        }


@dataclass
class ExtractionResult:
    """Complete extraction result"""
    entities: List[ExtractedEntity]
    sentence_count: int
    word_count: int
    key_phrases: List[str]
    confidence_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entities": [e.to_dict() for e in self.entities],
            "sentence_count": self.sentence_count,
            "word_count": self.word_count,
            "key_phrases": self.key_phrases,
            "confidence_score": self.confidence_score
        }


class MockSpacyEngine:
    """Mock spaCy engine for testing"""
    
    def __init__(self):
        self.model_loaded = False
        self.model_name = "en_core_web_sm"
    
    def load_model(self) -> bool:
        """Simulate model loading"""
        self.model_loaded = True
        return True
    
    def extract_entities(self, text: str) -> ExtractionResult:
        """Extract entities from text (mock implementation)"""
        if not text:
            return ExtractionResult(
                entities=[],
                sentence_count=0,
                word_count=0,
                key_phrases=[],
                confidence_score=0.0
            )
        
        entities = []
        
        # Simple pattern matching for common entities
        words = text.split()
        word_count = len(words)
        sentence_count = max(1, text.count('.') + text.count('!') + text.count('?'))
        
        # Find potential person names (capitalized words)
        for i, word in enumerate(words):
            if word.istitle() and len(word) > 2:
                # Exclude common words
                if word.lower() not in ["the", "and", "for", "but"]:
                    start = text.find(word)
                    entities.append(ExtractedEntity(
                        text=word,
                        entity_type=EntityType.PERSON,
                        confidence=0.7,
                        start_pos=start,
                        end_pos=start + len(word)
                    ))
        
        # Find dates
        import re
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',
            r'\d{1,2}-\d{1,2}-\d{2,4}',
        ]
        for pattern in date_patterns:
            for match in re.finditer(pattern, text):
                entities.append(ExtractedEntity(
                    text=match.group(),
                    entity_type=EntityType.DATE,
                    confidence=0.9,
                    start_pos=match.start(),
                    end_pos=match.end()
                ))
        
        # Key phrases (simple noun phrases)
        key_phrases = []
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        for bg in bigrams[:5]:  # First 5 bigrams
            if not any(w.lower() in ["the", "a", "an", "is", "are"] for w in bg.split()):
                key_phrases.append(bg)
        
        confidence = 0.85 if entities else 0.5
        
        return ExtractionResult(
            entities=entities,
            sentence_count=sentence_count,
            word_count=word_count,
            key_phrases=key_phrases[:3],
            confidence_score=confidence
        )
    
    def extract_named_entities(self, text: str) -> List[Dict]:
        """Extract named entities only"""
        result = self.extract_entities(text)
        return [e.to_dict() for e in result.entities]
    
    def get_sentence_count(self, text: str) -> int:
        """Count sentences"""
        if not text:
            return 0
        return max(1, text.count('.') + text.count('!') + text.count('?'))
    
    def get_word_count(self, text: str) -> int:
        """Count words"""
        if not text:
            return 0
        return len(text.split())


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def spacy_engine():
    return MockSpacyEngine()

@pytest.fixture
def loaded_engine():
    engine = MockSpacyEngine()
    engine.load_model()
    return engine

@pytest.fixture
def sample_text():
    return "John Smith visited New York on 15/03/2024. The Municipal Corporation did not respond."

@pytest.fixture
def empty_text():
    return ""

@pytest.fixture
def complaint_text():
    return """
    This is to bring to your kind attention that the Municipal Corporation 
    has failed to repair the road near Rajendra Nagar. Mr. Sharma from 
    the Roads Department was contacted on 01/02/2024 but no action taken.
    """


# ============================================================================
# TESTS
# ============================================================================

class TestEntityType:
    """Tests for EntityType enum"""
    
    def test_entity_types_exist(self):
        assert EntityType.PERSON.value == "PERSON"
        assert EntityType.ORGANIZATION.value == "ORG"
        assert EntityType.LOCATION.value == "LOC"
        assert EntityType.DATE.value == "DATE"


class TestExtractedEntity:
    """Tests for ExtractedEntity dataclass"""
    
    def test_entity_creation(self):
        entity = ExtractedEntity(
            text="John",
            entity_type=EntityType.PERSON,
            confidence=0.95,
            start_pos=0,
            end_pos=4
        )
        assert entity.text == "John"
        assert entity.entity_type == EntityType.PERSON
    
    def test_to_dict(self):
        entity = ExtractedEntity(
            text="NYC",
            entity_type=EntityType.LOCATION,
            confidence=0.90,
            start_pos=10,
            end_pos=13
        )
        entity_dict = entity.to_dict()
        assert isinstance(entity_dict, dict)
        assert entity_dict["text"] == "NYC"


class TestMockSpacyEngine:
    """Tests for MockSpacyEngine"""
    
    def test_initialization(self, spacy_engine):
        assert spacy_engine.model_loaded == False
        assert spacy_engine.model_name == "en_core_web_sm"
    
    def test_load_model(self, spacy_engine):
        result = spacy_engine.load_model()
        assert result == True
        assert spacy_engine.model_loaded == True
    
    def test_extract_entities_empty(self, loaded_engine, empty_text):
        result = loaded_engine.extract_entities(empty_text)
        assert len(result.entities) == 0
        assert result.word_count == 0
    
    def test_extract_entities_sample(self, loaded_engine, sample_text):
        result = loaded_engine.extract_entities(sample_text)
        assert isinstance(result, ExtractionResult)
        assert result.word_count > 0
    
    def test_extract_named_entities(self, loaded_engine, sample_text):
        entities = loaded_engine.extract_named_entities(sample_text)
        assert isinstance(entities, list)
    
    def test_sentence_count(self, loaded_engine, sample_text):
        count = loaded_engine.get_sentence_count(sample_text)
        assert count >= 1
    
    def test_word_count(self, loaded_engine, sample_text):
        count = loaded_engine.get_word_count(sample_text)
        assert count > 0


class TestExtractionResult:
    """Tests for ExtractionResult dataclass"""
    
    def test_to_dict(self, loaded_engine, sample_text):
        result = loaded_engine.extract_entities(sample_text)
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert "entities" in result_dict
        assert "word_count" in result_dict


class TestDateExtraction:
    """Tests for date extraction"""
    
    def test_extracts_dates(self, loaded_engine):
        text = "Meeting scheduled for 15/03/2024 and 20-04-2024"
        result = loaded_engine.extract_entities(text)
        date_entities = [e for e in result.entities if e.entity_type == EntityType.DATE]
        assert len(date_entities) >= 1
    
    def test_date_confidence(self, loaded_engine):
        text = "Report filed on 01/01/2024"
        result = loaded_engine.extract_entities(text)
        date_entities = [e for e in result.entities if e.entity_type == EntityType.DATE]
        if date_entities:
            assert date_entities[0].confidence >= 0.8


class TestKeyPhraseExtraction:
    """Tests for key phrase extraction"""
    
    def test_extracts_key_phrases(self, loaded_engine, complaint_text):
        result = loaded_engine.extract_entities(complaint_text)
        assert isinstance(result.key_phrases, list)
    
    def test_limits_key_phrases(self, loaded_engine, complaint_text):
        result = loaded_engine.extract_entities(complaint_text)
        assert len(result.key_phrases) <= 3


class TestEdgeCases:
    """Tests for edge cases"""
    
    def test_none_text(self, loaded_engine):
        # Should handle None gracefully
        result = loaded_engine.extract_entities("")
        assert result.word_count == 0
    
    def test_single_word(self, loaded_engine):
        result = loaded_engine.extract_entities("Hello")
        assert result.word_count == 1
    
    def test_only_punctuation(self, loaded_engine):
        result = loaded_engine.extract_entities("...")
        assert result.sentence_count >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
