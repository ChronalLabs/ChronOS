"""
NLP Services Package
Handles all NLP/ML operations following MODEL_USAGE_POLICY

Components:
- spacy_engine: Named Entity Recognition and phrase matching
- distilbert_semantic: Semantic similarity ranking (NOT generation)
- confidence_gate: Controls when AI predictions require user confirmation
"""

# Import spaCy NLP functions directly
from .spacy_engine import (
    extract_entities,
    extract_entities_detailed,
    extract_key_phrases,
    extract_matched_phrases,
    analyze_sentiment_basic,
    analyze_urgency,
    full_analysis,
    preload_models as preload_spacy,
    get_nlp,
    NLPResult,
    ExtractedEntity,
    EntityType,
)

# Import DistilBERT functions
from .distilbert_semantic import (
    compute_similarity,
    rank_by_similarity,
    rank_by_similarity_detailed,
    batch_compute_similarities,
    classify_query_type,
    preload_model as preload_distilbert,
    get_embedding,
    is_model_loaded,
    clear_cache,
    get_cache_stats,
    SimilarityResult,
    SemanticAnalysisResult,
)

# Import confidence gate functions
from .confidence_gate import (
    gate_result,
    should_use_nlp,
    ConfidenceLevel,
    GatedResult,
)

# Import translator functions
from .translator import (
    translate_to_hindi,
    get_translator,
)

# Export main functions
__all__ = [
    "extract_entities",
    "extract_key_phrases", 
    "analyze_sentiment_basic",
    "full_analysis",
    "compute_similarity",
    "rank_by_similarity",
    "gate_result",
    "should_use_nlp",
    "ConfidenceLevel",
    "preload_spacy",
    "preload_all_models",
    "translate_to_hindi",
    "get_translator",
]

from .confidence_gate import (
    ConfidenceLevel,
    DecisionSource,
    GatedResult,
    GatingDecision,
    Thresholds,
    get_confidence_level,
    should_use_nlp,
    should_use_distilbert,
    make_gating_decision,
    gate_result,
    combine_confidences,
    should_ask_user,
    format_alternatives_for_user,
    log_gating_decision,
    get_audit_log,
)

__all__ = [
    # spaCy engine
    "extract_entities",
    "extract_entities_detailed",
    "extract_key_phrases",
    "extract_matched_phrases",
    "analyze_sentiment_basic",
    "analyze_urgency",
    "full_analysis",
    "preload_spacy",
    "get_nlp",
    "NLPResult",
    "ExtractedEntity",
    "EntityType",
    
    # DistilBERT semantic
    "compute_similarity",
    "rank_by_similarity",
    "rank_by_similarity_detailed",
    "batch_compute_similarities",
    "classify_query_type",
    "preload_distilbert",
    "get_embedding",
    "is_model_loaded",
    "clear_cache",
    "get_cache_stats",
    "SimilarityResult",
    "SemanticAnalysisResult",

    # Translation
    "translate_to_hindi",
    "get_translator",
    
    # Confidence gate
    "ConfidenceLevel",
    "DecisionSource",
    "GatedResult",
    "GatingDecision",
    "Thresholds",
    "get_confidence_level",
    "should_use_nlp",
    "should_use_distilbert",
    "make_gating_decision",
    "gate_result",
    "combine_confidences",
    "should_ask_user",
    "format_alternatives_for_user",
    "log_gating_decision",
    "get_audit_log",
]


def preload_all_models():
    """Preload all NLP models for faster inference"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info("Preloading all NLP models...")
    
    try:
        preload_spacy()
        logger.info("✓ spaCy models loaded")
    except Exception as e:
        logger.error(f"✗ spaCy loading failed: {e}")
    
    try:
        preload_distilbert()
        logger.info("✓ DistilBERT model loaded")
    except Exception as e:
        logger.error(f"✗ DistilBERT loading failed: {e}")
    
    logger.info("NLP model preloading complete")
