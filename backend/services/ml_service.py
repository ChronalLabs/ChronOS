"""
ML Service - Handles all ML model loading and business logic
"""

import sys
import importlib
from pathlib import Path
from typing import Dict, Any, Optional

# Add ML directory to path
ML_DIR = Path(__file__).parent.parent.parent / "ml"
sys.path.insert(0, str(ML_DIR))


class MLService:
    """
    Singleton service for ML model management and inference.
    Implements lazy loading to avoid loading all models at startup.
    """
    
    _instance: Optional["MLService"] = None
    
    def __new__(cls) -> "MLService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._models: Dict[str, Any] = {
            "intent_extractor": None,
            "ner": None,
            "ambiguity_detector": None,
            "classifier": None,
            "mapper": None,
            "explainer": None,
            "risk_detector": None,
        }
        self._initialized = True
    
    @property
    def ml_directory(self) -> str:
        return str(ML_DIR)
    
    def get_model(self, name: str) -> Any:
        """Lazy load and return ML model by name"""
        if name not in self._models:
            raise ValueError(f"Unknown model: {name}")
        
        if self._models[name] is None:
            print(f"Loading ML model: {name}...")
            self._models[name] = self._load_model(name)
        
        return self._models[name]
    
    # Model to module/class mapping for dynamic loading
    _MODEL_CONFIG = {
        "intent_extractor": ("models.intent_extractor", "PolicyIntentExtractor"),
        "ner": ("models.policy_ner", "PolicyNER"),
        "ambiguity_detector": ("models.ambiguity_detector", "AmbiguityDetector"),
        "classifier": ("models.policy_classifier", "PolicyClassifier"),
        "mapper": ("models.policy_mapper", "PolicyParameterMapper"),
        "explainer": ("models.impact_explainer", "ImpactExplainer"),
        "risk_detector": ("models.risk_detector", "RiskDetector"),
    }
    
    def _load_model(self, name: str) -> Any:
        """Load a specific ML model dynamically"""
        if name not in self._MODEL_CONFIG:
            raise ValueError(f"No loader defined for model: {name}")
        
        module_name, class_name = self._MODEL_CONFIG[name]
        module = importlib.import_module(module_name)
        model_class = getattr(module, class_name)
        return model_class()
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all ML models"""
        return {
            "ml_enabled": True,
            "models_loaded": {k: v is not None for k, v in self._models.items()},
            "ml_directory": self.ml_directory,
            "models_available": list(self._models.keys())
        }
    
    # ===== Business Logic Methods =====
    
    def extract_intent(self, text: str) -> Dict[str, Any]:
        """Extract policy intent and key concepts"""
        extractor = self.get_model("intent_extractor")
        results = extractor.extract_intent(text)
        
        # Extract concepts from key sentences (intent_extractor doesn't return intent_concepts)
        concepts = self._extract_concepts_from_text(text, results.get("key_sentences", []))
        
        return {
            "key_sentences": [
                {"sentence": s["sentence"], "importance": round(s["importance"], 3)}
                for s in results.get("key_sentences", [])
            ],
            "concepts": concepts
        }
    
    def _extract_concepts_from_text(self, text: str, key_sentences: list) -> list:
        """Extract key concepts/themes from policy text"""
        # Common policy-related concept keywords to look for
        concept_keywords = [
            "safety", "construction", "development", "infrastructure", "traffic",
            "environmental", "budget", "timeline", "compliance", "regulation",
            "residential", "commercial", "industrial", "noise", "pollution",
            "permit", "inspection", "maintenance", "emergency", "security",
            "zoning", "planning", "public", "community", "transportation",
            "housing", "economic", "sustainability", "energy", "water"
        ]
        
        text_lower = text.lower()
        found_concepts = []
        
        # Find concepts that appear in the text
        for concept in concept_keywords:
            if concept in text_lower:
                found_concepts.append(concept.title())
        
        # Add concepts from key sentences
        for sent in key_sentences[:3]:
            sentence = sent.get("sentence", "").lower()
            for concept in concept_keywords:
                if concept in sentence and concept.title() not in found_concepts:
                    found_concepts.append(concept.title())
        
        # Return top concepts (limit to 8)
        return found_concepts[:8] if found_concepts else ["Policy Analysis", "General"]
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract named entities from policy text"""
        ner = self.get_model("ner")
        return ner.summarize_extraction(text)
    
    def analyze_ambiguity(self, text: str) -> Dict[str, Any]:
        """Analyze ambiguity in policy text"""
        detector = self.get_model("ambiguity_detector")
        results = detector.ambiguity_score(text)
        return {
            "score": results["overall_score"],
            "trust_level": results["trust_level"],
            "by_severity": results["by_severity"],
            "total_phrases": results["total_ambiguous_phrases"],
            "findings": results["findings"]
        }
    
    def classify_policy(self, text: str) -> Dict[str, Any]:
        """Classify policy focus (speed vs safety)"""
        classifier = self.get_model("classifier")
        return classifier.classify_policy_focus(text)
    
    def map_parameters(self, ner_results: Dict, classification: Dict, ambiguity_score: float) -> Dict[str, Any]:
        """Map extracted data to simulation parameters"""
        mapper = self.get_model("mapper")
        return mapper.integrate_extraction(ner_results, classification, ambiguity_score)
    
    def detect_risks(
        self,
        time_saved: float,
        risk_increase: float,
        cost_increase: float,
        incidents_increase: float,
        zone: str,
        policy_name: str
    ) -> Dict[str, Any]:
        """Detect unsafe tradeoffs in policy"""
        risk_detector = self.get_model("risk_detector")
        return risk_detector.detect_unsafe_tradeoffs(
            time_saved=time_saved,
            risk_increase=risk_increase,
            cost_increase=cost_increase,
            incidents_increase=incidents_increase,
            zone=zone,
            policy_name=policy_name
        )
    
    def full_analysis(self, text: str, policy_name: str = "Uploaded Policy") -> Dict[str, Any]:
        """
        Run full ML pipeline analysis on policy text.
        Returns comprehensive analysis from all ML tasks.
        """
        # Task 2: Intent Extraction
        intent_results = self.extract_intent(text)
        intent_data = {
            "key_sentences": [
                {"sentence": s["sentence"][:200], "importance": s["importance"]}
                for s in intent_results["key_sentences"]
            ],
            "concepts": intent_results["concepts"]
        }
        
        # Task 3: NER
        ner_results = self.extract_entities(text)
        entities_data = {k: v[:5] for k, v in ner_results.items()}
        
        # Task 4: Ambiguity Detection
        ambiguity_data = self.analyze_ambiguity(text)
        ambiguity_response = {
            "score": round(ambiguity_data["score"], 1),
            "trust_level": ambiguity_data["trust_level"],
            "by_severity": ambiguity_data["by_severity"],
            "total_phrases": ambiguity_data["total_phrases"],
            "top_findings": [
                {"phrase": f["phrase"], "severity": f["severity"], "context": f["context"][:100]}
                for f in ambiguity_data["findings"][:5]
            ]
        }
        
        # Task 5: Classification
        classification = self.classify_policy(text)
        classification_data = {
            "primary": classification["primary_classification"],
            "confidence": round(classification["confidence"], 3),
            "recommendation": classification["recommendation"]
        }
        
        # Task 6: Parameter Mapping
        sim_params = self.map_parameters(ner_results, classification, ambiguity_data["score"])
        parameters_data = {
            "metadata": sim_params["policy_metadata"],
            "safety_profile": sim_params["safety_profile"],
            "speed_profile": sim_params["speed_profile"],
            "zone_constraints": sim_params["zone_constraints"],
            "simulation_params": sim_params["simulation_parameters"]
        }
        
        # Task 8: Risk Detection
        zone = self._determine_zone(ner_results)
        is_safety_focused = "safety" in classification["primary_classification"].lower()
        
        risk_assessment = self.detect_risks(
            time_saved=20,
            risk_increase=5 if is_safety_focused else 15,
            cost_increase=10,
            incidents_increase=0.1 if is_safety_focused else 0.5,
            zone=zone,
            policy_name=policy_name
        )
        
        risk_data = {
            "level": risk_assessment["risk_level"],
            "flags": [
                {"type": f["type"], "severity": f["severity"], "message": f["message"]}
                for f in risk_assessment["flags"]
            ],
            "is_acceptable": risk_assessment["is_acceptable"],
            "recommendation": risk_assessment["recommendation"]
        }
        
        # Overall Summary
        overall_summary = {
            "policy_name": policy_name,
            "text_length": len(text),
            "classification": classification_data["primary"][:50],
            "confidence": classification_data["confidence"],
            "ambiguity_score": ambiguity_response["score"],
            "trust_level": ambiguity_response["trust_level"],
            "risk_level": risk_data["level"],
            "entity_types_found": list(entities_data.keys()),
            "total_entities": sum(len(v) for v in entities_data.values()),
            "ready_for_simulation": risk_data["is_acceptable"] and ambiguity_response["score"] < 50
        }
        
        return {
            "success": True,
            "policy_name": policy_name,
            "intent": intent_data,
            "entities": entities_data,
            "ambiguity": ambiguity_response,
            "classification": classification_data,
            "parameters": parameters_data,
            "risk_assessment": risk_data,
            "overall_summary": overall_summary
        }
    
    def _determine_zone(self, ner_results: Dict) -> str:
        """Determine zone type from NER results"""
        zone = "commercial"
        if "ZONE" in ner_results and ner_results["ZONE"]:
            zone_text = ner_results["ZONE"][0].lower()
            if "residential" in zone_text:
                zone = "residential"
            elif "industrial" in zone_text:
                zone = "industrial"
        return zone
