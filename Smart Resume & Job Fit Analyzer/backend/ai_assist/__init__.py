"""AI assistance package. AI assists only - never decides."""
from .semantic_analyzer import analyze_text
from .experience_signals import extract_signals

__all__ = ["analyze_text", "extract_signals"]
