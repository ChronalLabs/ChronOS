"""
Services Package
Core business logic for RTI & Public Complaint Generator

Package Structure:
- nlp/: NLP/ML operations (spaCy, DistilBERT, confidence gating)
- rule_engine/: Primary decision layer (intent, issues, legal triggers)
- inference_orchestrator.py: Main control flow coordinator
- draft_assembler.py: Template-based document generation
- authority_resolver.py: Department and authority mapping
- document_generator.py: PDF/DOCX/XLSX generation
"""

from .inference_orchestrator import InferenceResult, run_inference, IntentType, DocumentType
from .draft_assembler import DraftAssembler, get_draft_assembler
from .authority_resolver import resolve_authority, Authority, AuthorityMatch, ResolutionResult
from .document_generator import DocumentGenerator, get_document_generator

# Re-export from sub-packages for convenience
from .nlp import (
    extract_entities,
    extract_key_phrases,
    full_analysis as nlp_full_analysis,
    gate_result,
    ConfidenceLevel,
    preload_all_models,
)

from .rule_engine import (
    classify_intent,
    classify_intent_detailed,
    map_issue_to_department,
    detect_legal_triggers,
    analyze_complete as rule_engine_analyze,
)

__all__ = [
    # Main services
    "InferenceResult",
    "run_inference",
    "IntentType",
    "DocumentType",
    "DraftAssembler",
    "get_draft_assembler",
    "resolve_authority",
    "Authority",
    "AuthorityMatch",
    "ResolutionResult",
    "DocumentGenerator",
    "get_document_generator",
    
    # NLP exports
    "extract_entities",
    "extract_key_phrases",
    "nlp_full_analysis",
    "gate_result",
    "ConfidenceLevel",
    "preload_all_models",
    
    # Rule engine exports
    "classify_intent",
    "classify_intent_detailed",
    "map_issue_to_department",
    "detect_legal_triggers",
    "rule_engine_analyze",
]
