"""
ML Models Package
All models handle missing dependencies gracefully with helpful error messages
"""

# This allows imports like: from models import DocumentParser, PolicyIntentExtractor
try:
    from .document_parser import DocumentParser
except ImportError:
    DocumentParser = None

try:
    from .intent_extractor import PolicyIntentExtractor
except ImportError:
    PolicyIntentExtractor = None

__all__ = ['DocumentParser', 'PolicyIntentExtractor']
