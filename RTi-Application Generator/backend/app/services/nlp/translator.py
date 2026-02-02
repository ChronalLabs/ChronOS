"""
Translator Service
Handles translation between supported languages using Hugging Face Transformers.
Specifically designed for English <-> Hindi translation.

Note: Requires transformers package. Falls back to original text if unavailable.
"""

from loguru import logger
import functools
import os

# Try to import transformers, but don't fail if it's not available
try:
    from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("transformers package not available. Translation features disabled.")

# Global cache for pipeline
_translator_pipeline = None
_model_name = "Helsinki-NLP/opus-mt-en-hi"

def get_translator():
    """
    Get or load the translation pipeline.
    Uses Singleton pattern to avoid reloading model.
    Returns None if transformers not available.
    """
    global _translator_pipeline
    
    if not TRANSFORMERS_AVAILABLE:
        return None
    
    if _translator_pipeline is not None:
        return _translator_pipeline
        
    try:
        logger.info(f"Loading translation model: {_model_name}")
        # Use a local cache directory if possible to be nice to the filesystem
        tokenizer = AutoTokenizer.from_pretrained(_model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(_model_name)
        _translator_pipeline = pipeline("translation", model=model, tokenizer=tokenizer)  # type: ignore[call-overload]
        logger.info("Translation model loaded successfully")
        return _translator_pipeline
    except Exception as e:
        logger.error(f"Failed to load translation model {_model_name}: {e}")
        return None

def translate_to_hindi(text: str) -> str:
    """
    Translate English text to Hindi.
    Returns original text if translation fails or model unavailable.
    """
    if not text or not text.strip():
        return text
    
    # If text contains very few alphabetic characters, return as is (e.g. numbers, separators)
    if sum(c.isalpha() for c in text) < 2:
        return text

    pipeline_instance = get_translator()
    if not pipeline_instance:
        return text
    
    try:
        # Handle long text by splitting if necessary, 
        # but for now we rely on the pipeline's truncation or simple usage headers.
        # Check text length - opus-mt usually handles ~512 tokens.
        # If text is very long, we might just translate the first chunk or need a splitter.
        # For typical description (5000 chars), we might need chunking.
        
        # Simple chunking by newlines or crude length
        import textwrap
        chunks = textwrap.wrap(text, width=1000, break_long_words=False, replace_whitespace=False)
        
        translated_chunks = []
        for chunk in chunks:
            # Pipeline is typically [ {'translation_text': '...'} ]
            result = pipeline_instance(chunk)
            if result and isinstance(result, list) and 'translation_text' in result[0]:
                # Clean up the output slightly
                trans = result[0]['translation_text']
                translated_chunks.append(trans)
            else:
                translated_chunks.append(chunk) # Fallback for chunk
        
        return " ".join(translated_chunks)
        
    except Exception as e:
        logger.error(f"Translation error during processing: {e}")
        return text
