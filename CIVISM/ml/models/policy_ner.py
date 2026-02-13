"""
Policy Named Entity Recognition (Task 3)
Extract structured information: zones, construction types, time references, safety keywords
"""

import spacy
from spacy.matcher import PhraseMatcher, Matcher
from typing import List, Dict


class PolicyNER:
    """Named Entity Recognition for policy documents"""
    
    def __init__(self, model="en_core_web_sm"):
        """Load spaCy model"""
        self.nlp = spacy.load(model)
        self._setup_custom_patterns()
        print(f"✓ spaCy model '{model}' loaded")
    
    def _setup_custom_patterns(self):
        """
        Add domain-specific patterns for construction policies
        This is CRITICAL for accurate extraction
        """
        # PhraseMatcher for multi-word terms
        phrase_matcher = PhraseMatcher(self.nlp.vocab)
        
        # Define policy-specific phrases
        CONSTRUCTION_TYPES = [
            "residential construction",
            "commercial construction",
            "road construction",
            "infrastructure work",
            "demolition work",
            "foundation work",
            "night construction",
            "emergency repair"
        ]
        
        ZONE_TERMS = [
            "residential zone",
            "commercial zone",
            "industrial zone",
            "construction zone",
            "no-construction zone",
            "restricted area"
        ]
        
        SAFETY_KEYWORDS = [
            "safety inspection",
            "hazard control",
            "emergency protocol",
            "structural integrity",
            "worker protection",
            "equipment safety",
            "environmental impact"
        ]
        
        TIME_EXPRESSIONS = [
            "peak hours",
            "off-peak hours",
            "night hours",
            "daytime",
            "business hours",
            "weekends",
            "public holidays"
        ]
        
        # Add patterns to matcher
        phrase_matcher.add("CONSTRUCTION_TYPE",
                          [self.nlp(text) for text in CONSTRUCTION_TYPES])
        phrase_matcher.add("ZONE", [self.nlp(text) for text in ZONE_TERMS])
        phrase_matcher.add("SAFETY_KEYWORD",
                          [self.nlp(text) for text in SAFETY_KEYWORDS])
        phrase_matcher.add("TIME_EXPRESSION",
                          [self.nlp(text) for text in TIME_EXPRESSIONS])
        
        # Add token-based patterns for flexibility
        token_matcher = Matcher(self.nlp.vocab)
        
        # Pattern: "[number] meters" or similar
        token_matcher.add("MEASUREMENT", [
            [{"IS_DIGIT": True}, {"LOWER": "meters"}],
            [{"IS_DIGIT": True}, {"LOWER": "feet"}],
            [{"IS_DIGIT": True}, {"LOWER": "days"}],
            [{"IS_DIGIT": True}, {"LOWER": "hours"}]
        ])
        
        self.phrase_matcher = phrase_matcher
        self.token_matcher = token_matcher
    
    def extract_entities(self, text: str) -> Dict:
        """
        Extract both standard NER and custom policy entities
        
        Args:
            text (str): Policy text
            
        Returns:
            dict: Structured entity extraction
        """
        doc = self.nlp(text)
        
        # Standard spaCy NER
        standard_entities = [
            {
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            }
            for ent in doc.ents
        ]
        
        # Custom phrase patterns
        phrase_matches = self.phrase_matcher(doc)
        phrase_entities = [
            {
                'text': doc[start:end].text,
                'label': self.nlp.vocab.strings[match_id],
                'start': start,
                'end': end
            }
            for match_id, start, end in phrase_matches
        ]
        
        # Token-based patterns
        token_matches = self.token_matcher(doc)
        token_entities = [
            {
                'text': doc[start:end].text,
                'label': self.nlp.vocab.strings[match_id],
                'start': start,
                'end': end
            }
            for match_id, start, end in token_matches
        ]
        
        return {
            'standard_entities': standard_entities,
            'policy_entities': phrase_entities,
            'measurements': token_entities,
            'all_entities': standard_entities + phrase_entities + token_entities
        }
    
    def extract_by_type(self, text: str, entity_type: str) -> List[str]:
        """
        Extract specific entity type
        
        Args:
            text (str): Policy text
            entity_type (str): Type to extract (e.g., "ZONE", "CONSTRUCTION_TYPE")
            
        Returns:
            List[str]: Extracted entities of that type
        """
        doc = self.nlp(text)
        
        # Standard NER filter
        standard = [ent.text for ent in doc.ents if ent.label_ == entity_type]
        
        # Custom pattern filter
        matches = self.phrase_matcher(doc)
        custom = [
            doc[start:end].text
            for match_id, start, end in matches
            if self.nlp.vocab.strings[match_id] == entity_type
        ]
        
        return list(set(standard + custom))  # Remove duplicates
    
    def summarize_extraction(self, text: str) -> Dict:
        """
        Generate summary of all extracted entities
        
        Args:
            text (str): Policy text
            
        Returns:
            dict: Categorized entity summary
        """
        extraction = self.extract_entities(text)
        
        # Group by type
        summary = {}
        for entity in extraction['all_entities']:
            entity_type = entity['label']
            if entity_type not in summary:
                summary[entity_type] = []
            summary[entity_type].append(entity['text'])
        
        # Remove duplicates
        for key in summary:
            summary[key] = list(set(summary[key]))
        
        return summary


# Quick test
if __name__ == "__main__":
    ner = PolicyNER()
    
    policy = """
    Night construction in residential zones is prohibited between 8 PM and 6 AM.
    Commercial construction sites must have weekly safety inspections.
    All demolition work requires structural integrity assessment.
    Road construction can continue during off-peak hours with emergency protocols.
    """
    
    print("\n📊 Entity Summary:")
    summary = ner.summarize_extraction(policy)
    for entity_type, values in summary.items():
        print(f"  {entity_type}: {', '.join(values)}")
