"""
Text Enhancer - LLM-Powered Text Improvement
=============================================

This module provides text enhancement functions that use LLM to IMPROVE
existing rule-based output, not replace it.

DESIGN PRINCIPLE:
    Rules create the document → LLM polishes the language
    
The original rule-based text is ALWAYS preserved and can be shown to user.
LLM enhancement is optional and transparent.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger

from .openai_service import (
    get_openai_service,
    is_llm_available,
    LLMMode,
    LLMResponse
)


@dataclass
class EnhancementResult:
    """Result of text enhancement with full transparency"""
    
    # The texts
    original_text: str          # What the rule-based system created
    enhanced_text: str          # What LLM improved (or original if failed)
    
    # Status
    was_enhanced: bool          # True if LLM actually modified the text
    enhancement_mode: str       # What kind of enhancement was applied
    
    # Transparency
    changes_summary: str        # Human-readable summary of changes
    tokens_used: int            # For cost awareness
    model_used: str             # Which model was used
    
    # Audit
    timestamp: datetime = field(default_factory=datetime.utcnow)
    error: Optional[str] = None


async def enhance_draft_text(
    draft_text: str,
    language: str = "english",
    tone: str = "neutral",
    preserve_placeholders: bool = True
) -> EnhancementResult:
    """
    Enhance a generated draft document for better readability.
    
    This is called AFTER the rule-based template has been filled.
    The LLM only improves language, never changes legal content.
    
    Args:
        draft_text: The rule-based generated draft
        language: Target language (english/hindi)
        tone: Desired tone (neutral/formal/assertive)
        preserve_placeholders: Keep [PLACEHOLDER] markers intact
        
    Returns:
        EnhancementResult with both original and enhanced versions
    """
    
    if not is_llm_available():
        return EnhancementResult(
            original_text=draft_text,
            enhanced_text=draft_text,
            was_enhanced=False,
            enhancement_mode="none",
            changes_summary="LLM enhancement not available",
            tokens_used=0,
            model_used="none"
        )
    
    service = get_openai_service()
    
    # Determine the enhancement mode
    if language == "hindi":
        mode = LLMMode.TRANSLATE
        context = {"target_language": "Hindi"}
    elif tone != "neutral":
        mode = LLMMode.TONE_ADJUST
        context = {"tone": tone}
    else:
        mode = LLMMode.POLISH
        context = {}
    
    # Extract placeholders to preserve them
    placeholders = []
    if preserve_placeholders:
        import re
        placeholders = re.findall(r'\[([A-Z_]+)\]', draft_text)
    
    try:
        response: LLMResponse = await service.enhance_text(
            text=draft_text,
            mode=mode,
            context=context
        )
        
        enhanced = response.enhanced_text
        
        # Verify placeholders are preserved (safety check)
        if preserve_placeholders and placeholders:
            for ph in placeholders:
                if f"[{ph}]" not in enhanced:
                    logger.warning(f"LLM removed placeholder [{ph}], reverting to original")
                    return EnhancementResult(
                        original_text=draft_text,
                        enhanced_text=draft_text,
                        was_enhanced=False,
                        enhancement_mode=mode.value,
                        changes_summary="Enhancement reverted: placeholders were modified",
                        tokens_used=response.tokens_used,
                        model_used=response.model_used,
                        error="Placeholder integrity check failed"
                    )
        
        # Build changes summary
        if response.changes_made:
            changes_summary = "; ".join(response.changes_made)
        elif response.fallback_used:
            changes_summary = "No changes (fallback to original)"
        else:
            changes_summary = "Text polished for clarity"
        
        return EnhancementResult(
            original_text=draft_text,
            enhanced_text=enhanced,
            was_enhanced=not response.fallback_used,
            enhancement_mode=mode.value,
            changes_summary=changes_summary,
            tokens_used=response.tokens_used,
            model_used=response.model_used
        )
        
    except Exception as e:
        logger.error(f"Draft enhancement failed: {e}")
        return EnhancementResult(
            original_text=draft_text,
            enhanced_text=draft_text,
            was_enhanced=False,
            enhancement_mode="error",
            changes_summary="Enhancement failed, using original",
            tokens_used=0,
            model_used="none",
            error=str(e)
        )


async def clarify_issue_description(
    user_description: str,
    category: Optional[str] = None
) -> EnhancementResult:
    """
    Help clarify a user's issue description without changing facts.
    
    Called BEFORE template filling to help user express their issue better.
    The LLM organizes and clarifies but NEVER adds facts.
    
    Args:
        user_description: Raw user input describing their issue
        category: Issue category for context (electricity, water, etc.)
        
    Returns:
        EnhancementResult with clarified description
    """
    
    if not is_llm_available():
        return EnhancementResult(
            original_text=user_description,
            enhanced_text=user_description,
            was_enhanced=False,
            enhancement_mode="clarify",
            changes_summary="Clarification not available",
            tokens_used=0,
            model_used="none"
        )
    
    # Don't clarify very short descriptions
    if len(user_description.strip()) < 50:
        return EnhancementResult(
            original_text=user_description,
            enhanced_text=user_description,
            was_enhanced=False,
            enhancement_mode="clarify",
            changes_summary="Description too short for clarification",
            tokens_used=0,
            model_used="none"
        )
    
    service = get_openai_service()
    
    context = {}
    if category:
        context["category"] = category
    
    try:
        response = await service.enhance_text(
            text=user_description,
            mode=LLMMode.CLARIFY,
            context=context
        )
        
        return EnhancementResult(
            original_text=user_description,
            enhanced_text=response.enhanced_text,
            was_enhanced=not response.fallback_used,
            enhancement_mode="clarify",
            changes_summary="Issue description organized and clarified" if not response.fallback_used else "Using original description",
            tokens_used=response.tokens_used,
            model_used=response.model_used
        )
        
    except Exception as e:
        logger.error(f"Clarification failed: {e}")
        return EnhancementResult(
            original_text=user_description,
            enhanced_text=user_description,
            was_enhanced=False,
            enhancement_mode="clarify",
            changes_summary="Clarification failed",
            tokens_used=0,
            model_used="none",
            error=str(e)
        )


async def improve_formal_tone(
    text: str,
    target_tone: str = "formal"
) -> EnhancementResult:
    """
    Adjust the tone of text to be more formal/assertive.
    
    Args:
        text: Text to adjust
        target_tone: "formal" or "assertive"
        
    Returns:
        EnhancementResult with tone-adjusted text
    """
    
    if not is_llm_available():
        return EnhancementResult(
            original_text=text,
            enhanced_text=text,
            was_enhanced=False,
            enhancement_mode="tone_adjust",
            changes_summary="Tone adjustment not available",
            tokens_used=0,
            model_used="none"
        )
    
    service = get_openai_service()
    
    try:
        response = await service.enhance_text(
            text=text,
            mode=LLMMode.TONE_ADJUST,
            context={"tone": target_tone}
        )
        
        return EnhancementResult(
            original_text=text,
            enhanced_text=response.enhanced_text,
            was_enhanced=not response.fallback_used,
            enhancement_mode="tone_adjust",
            changes_summary=f"Tone adjusted to {target_tone}" if not response.fallback_used else "Using original tone",
            tokens_used=response.tokens_used,
            model_used=response.model_used
        )
        
    except Exception as e:
        logger.error(f"Tone adjustment failed: {e}")
        return EnhancementResult(
            original_text=text,
            enhanced_text=text,
            was_enhanced=False,
            enhancement_mode="tone_adjust",
            changes_summary="Tone adjustment failed",
            tokens_used=0,
            model_used="none",
            error=str(e)
        )


async def translate_to_hindi_llm(text: str) -> EnhancementResult:
    """
    Translate text to Hindi using LLM for better quality.
    
    Falls back to rule-based translation if LLM unavailable.
    """
    
    if not is_llm_available():
        # Fallback to existing translator
        from app.services.nlp import translate_to_hindi
        translated = translate_to_hindi(text)
        
        return EnhancementResult(
            original_text=text,
            enhanced_text=translated,
            was_enhanced=translated != text,
            enhancement_mode="translate_fallback",
            changes_summary="Translated using rule-based model",
            tokens_used=0,
            model_used="Helsinki-NLP/opus-mt-en-hi"
        )
    
    service = get_openai_service()
    
    try:
        response = await service.enhance_text(
            text=text,
            mode=LLMMode.TRANSLATE,
            context={"target_language": "Hindi"}
        )
        
        return EnhancementResult(
            original_text=text,
            enhanced_text=response.enhanced_text,
            was_enhanced=True,
            enhancement_mode="translate",
            changes_summary="Translated to formal Hindi",
            tokens_used=response.tokens_used,
            model_used=response.model_used
        )
        
    except Exception as e:
        logger.error(f"LLM translation failed, using fallback: {e}")
        from app.services.nlp import translate_to_hindi
        translated = translate_to_hindi(text)
        
        return EnhancementResult(
            original_text=text,
            enhanced_text=translated,
            was_enhanced=translated != text,
            enhancement_mode="translate_fallback",
            changes_summary="Translated using fallback model",
            tokens_used=0,
            model_used="Helsinki-NLP/opus-mt-en-hi",
            error=str(e)
        )
