"""
LLM Services Package
OpenAI integration following the principle:
    "Rules decide what is allowed. LLMs improve how it is expressed."

CRITICAL DESIGN PRINCIPLES:
1. LLM is NEVER the authority - it is an assistant
2. All legal content comes from pre-approved templates
3. LLM only POLISHES, CLARIFIES, or TRANSLATES existing rule-based output
4. Original rule-based content is always preserved for audit
5. User can always see what LLM changed

Components:
- openai_service: Core OpenAI API wrapper with safety guardrails
- text_enhancer: Polishes draft text while preserving legal accuracy
- smart_translator: Better translation than rule-based models
"""

from .openai_service import (
    OpenAIService,
    get_openai_service,
    is_llm_available,
    LLMResponse,
    LLMMode,
)

from .text_enhancer import (
    enhance_draft_text,
    clarify_issue_description,
    improve_formal_tone,
    translate_to_hindi_llm,
    EnhancementResult,
)

__all__ = [
    # OpenAI Service
    "OpenAIService",
    "get_openai_service",
    "is_llm_available",
    "LLMResponse",
    "LLMMode",
    
    # Text Enhancer
    "enhance_draft_text",
    "clarify_issue_description",
    "improve_formal_tone",
    "translate_to_hindi_llm",
    "EnhancementResult",
]
