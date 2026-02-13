"""
ML Model Manager
Centralized management for all ML/NLP models used in the application

Following MODEL_USAGE_POLICY:
- Rule Engine is PRIMARY
- spaCy: ONLY for NER and phrase matching
- DistilBERT: ONLY for semantic similarity ranking, NOT generation
- Confidence gating for all AI decisions
- Full audit trail for all model operations

NOTE: This module is designed to be run from the ml/ directory or imported
when the backend/app directory is in the Python path. The imports use
lazy loading to handle path resolution at runtime.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, List, Tuple, TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path

# Add backend to path for imports
BACKEND_PATH = Path(__file__).parent.parent / "backend" / "app"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

# Type checking imports (for IDE support - these run only during static analysis)
# At runtime, lazy imports are used instead
if TYPE_CHECKING:
    pass  # Imports moved to lazy loaders for runtime compatibility

logger = logging.getLogger(__name__)


def _import_spacy_engine():
    """Lazy import for spacy_engine module"""
    try:
        from services.nlp import spacy_engine  # type: ignore
        return spacy_engine
    except ImportError:
        try:
            from app.services.nlp import spacy_engine  # type: ignore
            return spacy_engine
        except ImportError:
            raise ImportError("Could not import spacy_engine. Ensure backend/app is in PYTHONPATH")


def _import_distilbert():
    """Lazy import for distilbert_semantic module"""
    try:
        from services.nlp import distilbert_semantic  # type: ignore
        return distilbert_semantic
    except ImportError:
        try:
            from app.services.nlp import distilbert_semantic  # type: ignore
            return distilbert_semantic
        except ImportError:
            raise ImportError("Could not import distilbert_semantic. Ensure backend/app is in PYTHONPATH")


def _import_intent_rules():
    """Lazy import for intent_rules module"""
    try:
        from services.rule_engine import intent_rules  # type: ignore
        return intent_rules
    except ImportError:
        try:
            from app.services.rule_engine import intent_rules  # type: ignore
            return intent_rules
        except ImportError:
            raise ImportError("Could not import intent_rules. Ensure backend/app is in PYTHONPATH")


def _import_issue_rules():
    """Lazy import for issue_rules module"""
    try:
        from services.rule_engine import issue_rules  # type: ignore
        return issue_rules
    except ImportError:
        try:
            from app.services.rule_engine import issue_rules  # type: ignore
            return issue_rules
        except ImportError:
            raise ImportError("Could not import issue_rules. Ensure backend/app is in PYTHONPATH")


def _import_legal_triggers():
    """Lazy import for legal_triggers module"""
    try:
        from services.rule_engine import legal_triggers  # type: ignore
        return legal_triggers
    except ImportError:
        try:
            from app.services.rule_engine import legal_triggers  # type: ignore
            return legal_triggers
        except ImportError:
            raise ImportError("Could not import legal_triggers. Ensure backend/app is in PYTHONPATH")


class ModelType(Enum):
    """Types of models managed"""
    SPACY = "spacy"
    DISTILBERT = "distilbert"
    RULE_ENGINE = "rule_engine"  # Not a model, but tracked for consistency


class ModelStatus(Enum):
    """Model loading status"""
    NOT_LOADED = "not_loaded"
    LOADING = "loading"
    LOADED = "loaded"
    ERROR = "error"


@dataclass
class ModelInfo:
    """Information about a loaded model"""
    name: str
    type: ModelType
    status: ModelStatus
    version: str
    memory_mb: float = 0.0
    load_time_ms: float = 0.0
    last_used: Optional[str] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type.value,
            "status": self.status.value,
            "version": self.version,
            "memory_mb": round(self.memory_mb, 2),
            "load_time_ms": round(self.load_time_ms, 2),
            "last_used": self.last_used,
            "error_message": self.error_message
        }


@dataclass
class InferenceResult:
    """Result from model inference"""
    model_used: ModelType
    result: Any
    confidence: float
    processing_time_ms: float
    audit_trail: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_used": self.model_used.value,
            "result": self.result,
            "confidence": round(self.confidence, 4),
            "processing_time_ms": round(self.processing_time_ms, 2),
            "audit_trail": self.audit_trail
        }


class ModelManager:
    """
    Centralized model management for the application.
    
    Responsibilities:
    1. Lazy loading of models
    2. Model health monitoring
    3. Inference routing (rule engine → spaCy → DistilBERT)
    4. Caching and performance optimization
    5. Audit logging
    """
    
    def __init__(self):
        self._models: Dict[ModelType, ModelInfo] = {}
        self._initialized = False
        self._audit_log: List[Dict] = []
        self._max_audit_entries = 1000
        
        # Initialize model info
        for model_type in [ModelType.SPACY, ModelType.DISTILBERT]:
            self._models[model_type] = ModelInfo(
                name=model_type.value,
                type=model_type,
                status=ModelStatus.NOT_LOADED,
                version="unknown"
            )
        
        # Rule engine is always "loaded" (it's just Python code)
        self._models[ModelType.RULE_ENGINE] = ModelInfo(
            name="rule_engine",
            type=ModelType.RULE_ENGINE,
            status=ModelStatus.LOADED,
            version="1.0.0"
        )
    
    def initialize(self, preload_models: bool = False) -> Dict[str, Any]:
        """
        Initialize the model manager.
        
        Args:
            preload_models: If True, load all models immediately
        """
        logger.info("Initializing ModelManager...")
        
        result = {
            "status": "initialized",
            "models": {},
            "preloaded": preload_models
        }
        
        if preload_models:
            # Load spaCy
            spacy_result = self.load_spacy()
            result["models"]["spacy"] = spacy_result
            
            # Load DistilBERT
            distilbert_result = self.load_distilbert()
            result["models"]["distilbert"] = distilbert_result
        
        self._initialized = True
        logger.info(f"ModelManager initialized: {result}")
        
        return result
    
    def load_spacy(self) -> Dict[str, Any]:
        """Load spaCy model"""
        import time
        start_time = time.time()
        
        model_info = self._models[ModelType.SPACY]
        model_info.status = ModelStatus.LOADING
        
        try:
            spacy_engine = _import_spacy_engine()
            
            # Load the model
            nlp = spacy_engine.get_nlp()
            
            # Update model info
            model_info.status = ModelStatus.LOADED
            model_info.version = "en_core_web_sm"
            model_info.load_time_ms = (time.time() - start_time) * 1000
            model_info.last_used = datetime.utcnow().isoformat()
            
            # Estimate memory (rough)
            model_info.memory_mb = 50.0  # en_core_web_sm is ~50MB
            
            logger.info(f"spaCy loaded in {model_info.load_time_ms:.2f}ms")
            
            return {"status": "loaded", "load_time_ms": model_info.load_time_ms}
            
        except Exception as e:
            model_info.status = ModelStatus.ERROR
            model_info.error_message = str(e)
            logger.error(f"Failed to load spaCy: {e}")
            return {"status": "error", "error": str(e)}
    
    def load_distilbert(self) -> Dict[str, Any]:
        """Load DistilBERT model"""
        import time
        start_time = time.time()
        
        model_info = self._models[ModelType.DISTILBERT]
        model_info.status = ModelStatus.LOADING
        
        try:
            distilbert = _import_distilbert()
            
            # Load the model
            distilbert.preload_model()
            
            # Update model info
            model_info.status = ModelStatus.LOADED
            model_info.version = "distilbert-base-uncased"
            model_info.load_time_ms = (time.time() - start_time) * 1000
            model_info.last_used = datetime.utcnow().isoformat()
            
            # Estimate memory
            model_info.memory_mb = 250.0  # DistilBERT is ~250MB
            
            logger.info(f"DistilBERT loaded in {model_info.load_time_ms:.2f}ms")
            
            return {"status": "loaded", "load_time_ms": model_info.load_time_ms}
            
        except Exception as e:
            model_info.status = ModelStatus.ERROR
            model_info.error_message = str(e)
            logger.error(f"Failed to load DistilBERT: {e}")
            return {"status": "error", "error": str(e)}
    
    def get_model_status(self, model_type: Optional[ModelType] = None) -> Dict[str, Any]:
        """Get status of one or all models"""
        if model_type:
            info = self._models.get(model_type)
            return info.to_dict() if info else {"error": "Model not found"}
        
        return {
            model_type.value: info.to_dict()
            for model_type, info in self._models.items()
        }
    
    def is_model_ready(self, model_type: ModelType) -> bool:
        """Check if a model is ready for inference"""
        info = self._models.get(model_type)
        return info is not None and info.status == ModelStatus.LOADED
    
    def classify_intent(self, text: str) -> InferenceResult:
        """
        Classify intent using the control flow:
        Rule Engine → spaCy (if needed) → DistilBERT (if needed)
        """
        import time
        start_time = time.time()
        audit_trail = []
        
        # Step 1: Rule Engine (PRIMARY)
        try:
            intent_rules = _import_intent_rules()
            
            rule_result = intent_rules.classify_intent_detailed(text)
            audit_trail.append({
                "step": "rule_engine",
                "intent": rule_result.intent.value,
                "confidence": rule_result.confidence,
                "matches": len(rule_result.matches)
            })
            
            # If high confidence, return immediately
            if rule_result.confidence >= 0.7:
                return InferenceResult(
                    model_used=ModelType.RULE_ENGINE,
                    result={
                        "intent": rule_result.intent.value,
                        "sub_type": rule_result.sub_type.value,
                        "decision_path": rule_result.decision_path
                    },
                    confidence=rule_result.confidence,
                    processing_time_ms=(time.time() - start_time) * 1000,
                    audit_trail=audit_trail
                )
            
            # Step 2: spaCy NLP for entity enhancement
            if self.is_model_ready(ModelType.SPACY) or self.load_spacy()["status"] == "loaded":
                spacy_engine = _import_spacy_engine()
                
                nlp_result = spacy_engine.full_analysis(text)
                audit_trail.append({
                    "step": "spacy_nlp",
                    "entities_found": len(nlp_result.entities),
                    "key_phrases": nlp_result.key_phrases[:5]
                })
                
                # Combine rule + NLP confidence
                combined_confidence = (rule_result.confidence + 0.1)  # Boost for NLP confirmation
                
                if combined_confidence >= 0.7:
                    return InferenceResult(
                        model_used=ModelType.SPACY,
                        result={
                            "intent": rule_result.intent.value,
                            "sub_type": rule_result.sub_type.value,
                            "entities": nlp_result.to_dict()["entities"],
                            "decision_path": rule_result.decision_path + ["Enhanced with NLP"]
                        },
                        confidence=min(0.95, combined_confidence),
                        processing_time_ms=(time.time() - start_time) * 1000,
                        audit_trail=audit_trail
                    )
            
            # Step 3: DistilBERT for semantic similarity (last resort)
            if self.is_model_ready(ModelType.DISTILBERT) or self.load_distilbert()["status"] == "loaded":
                distilbert = _import_distilbert()
                
                semantic_scores = distilbert.classify_query_type(text)
                audit_trail.append({
                    "step": "distilbert_semantic",
                    "top_scores": dict(list(semantic_scores.items())[:3])
                })
                
                # Use semantic result if significantly higher
                top_semantic = list(semantic_scores.items())[0]
                if top_semantic[1] > rule_result.confidence + 0.1:
                    return InferenceResult(
                        model_used=ModelType.DISTILBERT,
                        result={
                            "intent": top_semantic[0].split("_")[0],  # Extract base intent
                            "semantic_type": top_semantic[0],
                            "decision_path": rule_result.decision_path + ["Semantic override"]
                        },
                        confidence=top_semantic[1],
                        processing_time_ms=(time.time() - start_time) * 1000,
                        audit_trail=audit_trail
                    )
            
            # Return rule engine result with low confidence
            return InferenceResult(
                model_used=ModelType.RULE_ENGINE,
                result={
                    "intent": rule_result.intent.value,
                    "sub_type": rule_result.sub_type.value,
                    "requires_confirmation": True,
                    "decision_path": rule_result.decision_path
                },
                confidence=rule_result.confidence,
                processing_time_ms=(time.time() - start_time) * 1000,
                audit_trail=audit_trail
            )
            
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            return InferenceResult(
                model_used=ModelType.RULE_ENGINE,
                result={"error": str(e), "intent": "unknown"},
                confidence=0.0,
                processing_time_ms=(time.time() - start_time) * 1000,
                audit_trail=audit_trail + [{"step": "error", "message": str(e)}]
            )
    
    def extract_entities(self, text: str) -> InferenceResult:
        """Extract entities using spaCy"""
        import time
        start_time = time.time()
        
        try:
            # Ensure spaCy is loaded
            if not self.is_model_ready(ModelType.SPACY):
                self.load_spacy()
            
            spacy_engine = _import_spacy_engine()
            
            entities = spacy_engine.extract_entities_detailed(text)
            
            return InferenceResult(
                model_used=ModelType.SPACY,
                result={
                    "entities": [e.to_dict() for e in entities],
                    "count": len(entities)
                },
                confidence=0.85,  # Default confidence for NER
                processing_time_ms=(time.time() - start_time) * 1000,
                audit_trail=[{"step": "entity_extraction", "count": len(entities)}]
            )
            
        except Exception as e:
            logger.error(f"Entity extraction error: {e}")
            return InferenceResult(
                model_used=ModelType.SPACY,
                result={"error": str(e), "entities": []},
                confidence=0.0,
                processing_time_ms=(time.time() - start_time) * 1000,
                audit_trail=[{"step": "error", "message": str(e)}]
            )
    
    def compute_similarity(self, query: str, candidates: List[str]) -> InferenceResult:
        """Compute semantic similarity using DistilBERT"""
        import time
        start_time = time.time()
        
        try:
            # Ensure DistilBERT is loaded
            if not self.is_model_ready(ModelType.DISTILBERT):
                self.load_distilbert()
            
            distilbert = _import_distilbert()
            
            result = distilbert.rank_by_similarity_detailed(query, candidates, top_k=5)
            
            return InferenceResult(
                model_used=ModelType.DISTILBERT,
                result=result.to_dict(),
                confidence=result.top_matches[0].score if result.top_matches else 0.0,
                processing_time_ms=(time.time() - start_time) * 1000,
                audit_trail=result.audit_trail
            )
            
        except Exception as e:
            logger.error(f"Similarity computation error: {e}")
            return InferenceResult(
                model_used=ModelType.DISTILBERT,
                result={"error": str(e), "matches": []},
                confidence=0.0,
                processing_time_ms=(time.time() - start_time) * 1000,
                audit_trail=[{"step": "error", "message": str(e)}]
            )
    
    def map_issue(self, text: str) -> InferenceResult:
        """Map issue to department using rule engine + semantic fallback"""
        import time
        start_time = time.time()
        audit_trail = []
        
        try:
            # Step 1: Rule Engine
            issue_rules = _import_issue_rules()
            
            matches = issue_rules.map_issue_detailed(text)
            audit_trail.append({
                "step": "rule_engine",
                "matches_found": len(matches),
                "top_match": matches[0].category.value if matches else None
            })
            
            if matches and matches[0].confidence >= 0.7:
                return InferenceResult(
                    model_used=ModelType.RULE_ENGINE,
                    result={
                        "category": matches[0].category.value,
                        "departments": [d.name for d in matches[0].departments],
                        "escalation_path": matches[0].escalation_path,
                        "alternatives": [m.to_dict() for m in matches[1:3]]
                    },
                    confidence=matches[0].confidence,
                    processing_time_ms=(time.time() - start_time) * 1000,
                    audit_trail=audit_trail
                )
            
            # Step 2: Semantic matching for ambiguous cases
            if self.is_model_ready(ModelType.DISTILBERT) or self.load_distilbert()["status"] == "loaded":
                distilbert = _import_distilbert()
                issue_rules = _import_issue_rules()
                
                # Get category descriptions
                categories = issue_rules.get_all_categories()
                category_texts = [f"{c['value']} department handling {c['label']} issues" 
                                 for c in categories]
                
                semantic_result = distilbert.classify_query_type(text)
                audit_trail.append({
                    "step": "semantic_matching",
                    "top_scores": dict(list(semantic_result.items())[:3])
                })
            
            # Return best rule engine match with low confidence flag
            return InferenceResult(
                model_used=ModelType.RULE_ENGINE,
                result={
                    "category": matches[0].category.value if matches else "general",
                    "departments": [d.name for d in matches[0].departments] if matches else [],
                    "requires_confirmation": True,
                    "alternatives": [m.to_dict() for m in matches[:3]] if matches else []
                },
                confidence=matches[0].confidence if matches else 0.3,
                processing_time_ms=(time.time() - start_time) * 1000,
                audit_trail=audit_trail
            )
            
        except Exception as e:
            logger.error(f"Issue mapping error: {e}")
            return InferenceResult(
                model_used=ModelType.RULE_ENGINE,
                result={"error": str(e), "category": "general"},
                confidence=0.0,
                processing_time_ms=(time.time() - start_time) * 1000,
                audit_trail=audit_trail + [{"step": "error", "message": str(e)}]
            )
    
    def analyze_legal_context(self, text: str) -> InferenceResult:
        """Analyze legal triggers and references"""
        import time
        start_time = time.time()
        
        try:
            legal_triggers = _import_legal_triggers()
            
            result = legal_triggers.analyze_legal_context(text)
            
            return InferenceResult(
                model_used=ModelType.RULE_ENGINE,
                result=result.to_dict(),
                confidence=0.9,  # Rule-based, high confidence
                processing_time_ms=(time.time() - start_time) * 1000,
                audit_trail=[{
                    "step": "legal_analysis",
                    "rti_sections_found": len(result.rti_sections),
                    "grievance_markers_found": len(result.grievance_markers)
                }]
            )
            
        except Exception as e:
            logger.error(f"Legal analysis error: {e}")
            return InferenceResult(
                model_used=ModelType.RULE_ENGINE,
                result={"error": str(e)},
                confidence=0.0,
                processing_time_ms=(time.time() - start_time) * 1000,
                audit_trail=[{"step": "error", "message": str(e)}]
            )
    
    def full_analysis(self, text: str) -> Dict[str, Any]:
        """
        Perform complete analysis of input text.
        Combines all analysis steps.
        """
        import time
        start_time = time.time()
        
        results = {
            "intent": self.classify_intent(text).to_dict(),
            "entities": self.extract_entities(text).to_dict(),
            "issue_mapping": self.map_issue(text).to_dict(),
            "legal_context": self.analyze_legal_context(text).to_dict(),
            "total_processing_time_ms": 0.0
        }
        
        results["total_processing_time_ms"] = (time.time() - start_time) * 1000
        
        return results
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on all models"""
        health = {
            "status": "healthy",
            "models": {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        for model_type, info in self._models.items():
            model_health = {
                "status": info.status.value,
                "version": info.version
            }
            
            if info.status == ModelStatus.ERROR:
                model_health["error"] = info.error_message or "Unknown error"
                health["status"] = "degraded"
            
            health["models"][model_type.value] = model_health
        
        return health
    
    def shutdown(self):
        """Clean shutdown of model manager"""
        logger.info("Shutting down ModelManager...")
        
        # Clear caches
        try:
            distilbert = _import_distilbert()
            distilbert.clear_cache()
        except:
            pass
        
        self._initialized = False
        logger.info("ModelManager shut down complete")


# Global instance
_model_manager: Optional[ModelManager] = None


def get_model_manager() -> ModelManager:
    """Get or create the global ModelManager instance"""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager


def initialize_models(preload: bool = False) -> Dict[str, Any]:
    """Initialize models (convenience function)"""
    manager = get_model_manager()
    return manager.initialize(preload_models=preload)


# CLI for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ML Model Manager CLI")
    parser.add_argument("--preload", action="store_true", help="Preload all models")
    parser.add_argument("--test", type=str, help="Test text for analysis")
    parser.add_argument("--health", action="store_true", help="Run health check")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    manager = get_model_manager()
    
    if args.preload or args.test:
        print("Initializing models...")
        result = manager.initialize(preload_models=True)
        print(f"Initialization result: {result}")
    
    if args.health:
        health = manager.health_check()
        print(f"Health check: {health}")
    
    if args.test:
        print(f"\nAnalyzing: {args.test}")
        print("-" * 50)
        
        result = manager.full_analysis(args.test)
        
        import json
        print(json.dumps(result, indent=2, default=str))
