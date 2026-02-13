"""
OpenAI Service - Core LLM Integration
=====================================

DESIGN PRINCIPLE:
    "Rules decide what is allowed. LLMs improve how it is expressed."
    
This service provides controlled access to OpenAI's API with:
1. Strict system prompts that enforce legal/civic language
2. Guardrails preventing hallucination of legal facts
3. Audit logging of all LLM interactions
4. Fallback to rule-based output if LLM fails

The LLM is NEVER the authority - it assists within controlled boundaries.
"""

import os
from enum import Enum
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI package not installed. LLM features disabled.")

from app.config import get_settings


class LLMMode(str, Enum):
    """Modes of LLM assistance - each has strict boundaries"""
    POLISH = "polish"           # Improve clarity without changing meaning
    TRANSLATE = "translate"     # Translate to Hindi/regional language
    CLARIFY = "clarify"         # Make user's issue description clearer
    SUMMARIZE = "summarize"     # Create summary for preview
    TONE_ADJUST = "tone_adjust" # Adjust formality level


@dataclass
class LLMResponse:
    """Response from LLM with audit trail"""
    original_text: str
    enhanced_text: str
    mode: LLMMode
    model_used: str
    tokens_used: int
    processing_time_ms: float
    changes_made: List[str] = field(default_factory=list)
    confidence: float = 1.0
    fallback_used: bool = False
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


# =============================================================================
# SYSTEM PROMPTS - The guardrails that control LLM behavior
# =============================================================================

SYSTEM_PROMPTS = {
    LLMMode.POLISH: """You are a legal document assistant for Indian RTI applications and public complaints.

YOUR ROLE: Improve clarity and readability of EXISTING text. You do NOT create new content.

STRICT RULES:
1. NEVER add legal claims, rights, or sections that weren't in the original
2. NEVER change dates, names, addresses, or factual claims
3. NEVER add emotional language or threats
4. PRESERVE all legal terminology exactly (RTI Act 2005, Section numbers, etc.)
5. Maintain formal, respectful tone appropriate for government correspondence
6. Fix grammar and improve sentence structure only
7. Keep the same paragraph structure

OUTPUT: Return ONLY the improved text, nothing else.""",

    LLMMode.TRANSLATE: """You are a Hindi translator for official Indian government documents.

YOUR ROLE: Translate English text to formal Hindi (Shuddh Hindi) suitable for government offices.

STRICT RULES:
1. Use formal Hindi (शुद्ध हिन्दी) - not colloquial
2. PRESERVE all proper nouns, names, dates, and numbers in original form
3. Use standard government terminology (आवेदन पत्र, सूचना का अधिकार, etc.)
4. Keep legal references like "RTI Act 2005" or translate to "सूचना का अधिकार अधिनियम 2005"
5. Maintain the formal, respectful tone
6. Do NOT add or remove any information

OUTPUT: Return ONLY the Hindi translation, nothing else.""",

    LLMMode.CLARIFY: """You are assisting an Indian citizen in writing their grievance or information request.

YOUR ROLE: Make their description clearer and more specific WITHOUT changing what they want to say.

STRICT RULES:
1. NEVER add facts, dates, or claims the user didn't provide
2. NEVER assume details - if something is vague, keep it vague
3. Organize the text logically (background → problem → impact)
4. Use clear, simple language
5. Remove redundancy but keep all unique points
6. Maintain the citizen's voice - don't make it sound artificial

OUTPUT: Return ONLY the clarified text, nothing else.""",

    LLMMode.TONE_ADJUST: """You are adjusting the tone of an official Indian government application.

YOUR ROLE: Adjust formality level while keeping the exact same meaning.

TONE LEVELS:
- "neutral": Professional, factual, matter-of-fact
- "formal": Highly formal, uses "Respected Sir/Madam", traditional structure
- "assertive": Firm but respectful, emphasizes rights and timelines

STRICT RULES:
1. NEVER change facts, dates, names, or claims
2. NEVER add threats or disrespectful language
3. Keep legal references exactly as they are
4. Adjust ONLY the style of expression

OUTPUT: Return ONLY the adjusted text, nothing else.""",

    LLMMode.SUMMARIZE: """You are creating a preview summary of an RTI/complaint document.

YOUR ROLE: Create a 2-3 line summary for the user to quickly verify the document.

STRICT RULES:
1. Include: document type, target department, main request
2. Keep it under 50 words
3. Use simple language
4. Don't add anything not in the original

OUTPUT: Return ONLY the summary, nothing else."""
}


class OpenAIService:
    """
    Controlled OpenAI service with safety guardrails.
    
    The LLM is treated as an assistant that works WITHIN the rule-based system,
    not as a replacement for it.
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.client: Optional[OpenAI] = None
        self._initialized = False
        self._audit_log: List[Dict[str, Any]] = []
        
    def _initialize(self) -> bool:
        """Lazy initialization of OpenAI client"""
        if self._initialized:
            return self.client is not None
            
        if not OPENAI_AVAILABLE:
            logger.warning("OpenAI package not available")
            self._initialized = True
            return False
            
        api_key = self.settings.OPENAI_API_KEY
        if not api_key:
            logger.warning("OPENAI_API_KEY not set. LLM features disabled.")
            self._initialized = True
            return False
            
        try:
            self.client = OpenAI(api_key=api_key)
            self._initialized = True
            logger.info("OpenAI service initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI: {e}")
            self._initialized = True
            return False
    
    def is_available(self) -> bool:
        """Check if LLM service is available"""
        if not self._initialized:
            self._initialize()
        return self.client is not None and self.settings.ENABLE_LLM_ENHANCEMENT
    
    async def enhance_text(
        self,
        text: str,
        mode: LLMMode,
        context: Optional[Dict[str, Any]] = None
    ) -> LLMResponse:
        """
        Enhance text using LLM within controlled boundaries.
        
        Args:
            text: Original text to enhance
            mode: Type of enhancement (polish, translate, etc.)
            context: Additional context (language, tone, etc.)
            
        Returns:
            LLMResponse with enhanced text and audit trail
        """
        import time
        start_time = time.time()
        
        # Ensure initialized
        if not self.is_available():
            return LLMResponse(
                original_text=text,
                enhanced_text=text,  # Return original as fallback
                mode=mode,
                model_used="none",
                tokens_used=0,
                processing_time_ms=0,
                fallback_used=True,
                error="LLM service not available"
            )
        
        # Get appropriate system prompt
        system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS[LLMMode.POLISH])
        
        # Add context to prompt if provided
        user_message = text
        if context:
            if mode == LLMMode.TONE_ADJUST and "tone" in context:
                user_message = f"TARGET TONE: {context['tone']}\n\nTEXT:\n{text}"
            elif mode == LLMMode.TRANSLATE and "target_language" in context:
                user_message = f"Translate to: {context.get('target_language', 'Hindi')}\n\nTEXT:\n{text}"
        
        try:
            if self.client is None:
                raise ValueError("OpenAI client not initialized")
            
            response = self.client.chat.completions.create(
                model=self.settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=self.settings.OPENAI_MAX_TOKENS,
                temperature=self.settings.OPENAI_TEMPERATURE,
            )
            
            content = response.choices[0].message.content
            enhanced_text = content.strip() if content else text
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            processing_time = (time.time() - start_time) * 1000
            
            # Create response with audit trail
            result = LLMResponse(
                original_text=text,
                enhanced_text=enhanced_text,
                mode=mode,
                model_used=self.settings.OPENAI_MODEL,
                tokens_used=tokens_used,
                processing_time_ms=processing_time,
                changes_made=self._detect_changes(text, enhanced_text),
                confidence=0.95,  # High confidence for controlled prompts
                fallback_used=False
            )
            
            # Log for audit
            self._log_interaction(result, context)
            
            return result
            
        except Exception as e:
            logger.error(f"LLM enhancement failed: {e}")
            processing_time = (time.time() - start_time) * 1000
            
            return LLMResponse(
                original_text=text,
                enhanced_text=text,  # Return original as fallback
                mode=mode,
                model_used=self.settings.OPENAI_MODEL,
                tokens_used=0,
                processing_time_ms=processing_time,
                fallback_used=True,
                error=str(e)
            )
    
    def _detect_changes(self, original: str, enhanced: str) -> List[str]:
        """Detect what changes were made (for transparency)"""
        changes = []
        
        if len(enhanced) != len(original):
            diff = len(enhanced) - len(original)
            if diff > 0:
                changes.append(f"Text expanded by {diff} characters")
            else:
                changes.append(f"Text condensed by {abs(diff)} characters")
        
        # Check for structural changes
        orig_paras = original.count('\n\n')
        new_paras = enhanced.count('\n\n')
        if orig_paras != new_paras:
            changes.append(f"Paragraph structure adjusted")
        
        return changes
    
    def _log_interaction(self, response: LLMResponse, context: Optional[Dict] = None):
        """Log LLM interaction for audit purposes"""
        log_entry = {
            "timestamp": response.timestamp.isoformat(),
            "mode": response.mode.value,
            "model": response.model_used,
            "tokens": response.tokens_used,
            "processing_ms": response.processing_time_ms,
            "changes": response.changes_made,
            "fallback": response.fallback_used,
            "context": context,
            # Don't log full text for privacy, just lengths
            "original_length": len(response.original_text),
            "enhanced_length": len(response.enhanced_text),
        }
        self._audit_log.append(log_entry)
        
        # Keep only last 100 entries in memory
        if len(self._audit_log) > 100:
            self._audit_log = self._audit_log[-100:]
        
        logger.debug(f"LLM interaction logged: {response.mode.value}, {response.tokens_used} tokens")
    
    def get_audit_log(self) -> List[Dict[str, Any]]:
        """Get recent LLM interactions for audit"""
        return self._audit_log.copy()


# =============================================================================
# Module-level singleton and helpers
# =============================================================================

_service_instance: Optional[OpenAIService] = None


def get_openai_service() -> OpenAIService:
    """Get or create the OpenAI service singleton"""
    global _service_instance
    if _service_instance is None:
        _service_instance = OpenAIService()
    return _service_instance


def is_llm_available() -> bool:
    """Quick check if LLM features are available"""
    return get_openai_service().is_available()
