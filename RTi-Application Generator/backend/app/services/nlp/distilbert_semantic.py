"""
DistilBERT Semantic Engine
Used ONLY for similarity matching and ranking
NOT for generation or classification decisions

Following MODEL_USAGE_POLICY:
- ONLY used for semantic similarity ranking
- NO text generation
- Called ONLY when rule engine has low confidence
- All decisions logged for audit trail
"""

from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, field
import numpy as np
import logging
from functools import lru_cache
import hashlib

logger = logging.getLogger(__name__)

# Model will be loaded on first use
_model = None
_tokenizer = None
_embedding_cache: Dict[str, np.ndarray] = {}
_cache_max_size = 1000


@dataclass
class SimilarityResult:
    """Similarity result with audit trail"""
    candidate: str
    score: float
    rank: int
    explanation: str
    
    def to_dict(self) -> Dict:
        return {
            "candidate": self.candidate,
            "score": round(self.score, 4),
            "rank": self.rank,
            "explanation": self.explanation
        }


@dataclass
class SemanticAnalysisResult:
    """Complete semantic analysis with audit trail"""
    query: str
    top_matches: List[SimilarityResult]
    processing_time_ms: float
    model_used: str
    cache_hit: bool
    audit_trail: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "query": self.query[:100] + "..." if len(self.query) > 100 else self.query,
            "top_matches": [m.to_dict() for m in self.top_matches],
            "processing_time_ms": round(self.processing_time_ms, 2),
            "model_used": self.model_used,
            "cache_hit": self.cache_hit,
            "audit_trail": self.audit_trail
        }


def get_model():
    """Lazy load DistilBERT model with proper error handling"""
    global _model, _tokenizer
    
    if _model is None:
        try:
            from transformers import DistilBertModel, DistilBertTokenizer
            import torch
            
            logger.info("Loading DistilBERT model...")
            _tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
            _model = DistilBertModel.from_pretrained('distilbert-base-uncased')
            
            # Set to evaluation mode
            _model.eval()
            
            # Move to GPU if available
            if torch.cuda.is_available():
                _model = _model.cuda()
                logger.info("DistilBERT loaded on GPU")
            else:
                logger.info("DistilBERT loaded on CPU")
                
        except Exception as e:
            logger.error(f"Failed to load DistilBERT: {e}")
            raise RuntimeError(f"Failed to load DistilBERT: {e}")
    
    return _model, _tokenizer


def is_model_loaded() -> bool:
    """Check if model is already loaded"""
    return _model is not None


def _get_cache_key(text: str) -> str:
    """Generate cache key for text"""
    return hashlib.md5(text.encode()).hexdigest()


def _manage_cache():
    """Manage cache size"""
    global _embedding_cache
    if len(_embedding_cache) > _cache_max_size:
        # Remove oldest entries (first half)
        keys = list(_embedding_cache.keys())
        for key in keys[:len(keys)//2]:
            del _embedding_cache[key]
        logger.debug(f"Cache trimmed to {len(_embedding_cache)} entries")


def get_embedding(text: str, use_cache: bool = True) -> Tuple[np.ndarray, bool]:
    """
    Get sentence embedding using DistilBERT.
    Uses mean pooling of last hidden states.
    
    Returns: (embedding, cache_hit)
    """
    import torch
    
    cache_key = _get_cache_key(text)
    
    # Check cache
    if use_cache and cache_key in _embedding_cache:
        return _embedding_cache[cache_key], True
    
    model, tokenizer = get_model()
    
    # Tokenize with truncation
    inputs = tokenizer(
        text, 
        return_tensors="pt", 
        truncation=True, 
        max_length=512,
        padding=True
    )
    
    # Move to GPU if available
    if torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    # Get embeddings without gradient computation
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Mean pooling with attention mask
    attention_mask = inputs['attention_mask']
    token_embeddings = outputs.last_hidden_state
    
    # Expand attention mask for broadcasting
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    
    # Sum embeddings where mask is 1, then divide by count
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    embedding = (sum_embeddings / sum_mask).squeeze().cpu().numpy()
    
    # Cache result
    if use_cache:
        _manage_cache()
        _embedding_cache[cache_key] = embedding
    
    return embedding, False


def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute cosine similarity between two texts.
    Returns value between 0 and 1.
    """
    emb1, _ = get_embedding(text1)
    emb2, _ = get_embedding(text2)
    
    # Cosine similarity
    dot_product = np.dot(emb1, emb2)
    norm1 = np.linalg.norm(emb1)
    norm2 = np.linalg.norm(emb2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    similarity = dot_product / (norm1 * norm2)
    
    # Clamp to [0, 1] to handle floating point errors
    return float(max(0.0, min(1.0, similarity)))


def rank_by_similarity(
    query: str, 
    candidates: List[str],
    top_k: Optional[int] = None
) -> List[Tuple[str, float]]:
    """
    Rank candidate texts by similarity to query.
    Returns list of (candidate, score) tuples, sorted by score descending.
    
    USE CASE: Authority matching, template selection
    NOT FOR: Classification decisions (use rule engine)
    """
    import time
    start_time = time.time()
    
    query_emb, query_cached = get_embedding(query)
    
    results = []
    for candidate in candidates:
        cand_emb, _ = get_embedding(candidate)
        
        # Cosine similarity
        dot_product = np.dot(query_emb, cand_emb)
        norm1 = np.linalg.norm(query_emb)
        norm2 = np.linalg.norm(cand_emb)
        
        if norm1 == 0 or norm2 == 0:
            score = 0.0
        else:
            score = float(dot_product / (norm1 * norm2))
            score = max(0.0, min(1.0, score))
        
        results.append((candidate, score))
    
    # Sort by score descending
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Return top_k if specified
    if top_k:
        results = results[:top_k]
    
    logger.debug(f"Ranked {len(candidates)} candidates in {(time.time()-start_time)*1000:.2f}ms")
    
    return results


def rank_by_similarity_detailed(
    query: str,
    candidates: List[str],
    candidate_labels: Optional[List[str]] = None,
    top_k: int = 5
) -> SemanticAnalysisResult:
    """
    Enhanced ranking with detailed audit trail.
    
    Args:
        query: The search query
        candidates: List of candidate texts to rank
        candidate_labels: Optional labels for candidates (for display)
        top_k: Number of top results to return
    
    Returns:
        SemanticAnalysisResult with full audit trail
    """
    import time
    start_time = time.time()
    
    audit_trail = []
    
    # Get query embedding
    query_emb, query_cached = get_embedding(query)
    audit_trail.append({
        "step": "query_embedding",
        "cache_hit": query_cached,
        "embedding_dim": len(query_emb)
    })
    
    # Get candidate embeddings
    results = []
    cache_hits = 0
    
    for i, candidate in enumerate(candidates):
        cand_emb, cached = get_embedding(candidate)
        if cached:
            cache_hits += 1
        
        # Compute similarity
        score = compute_similarity(query, candidate)
        
        label = candidate_labels[i] if candidate_labels else candidate
        results.append({
            "candidate": label,
            "original": candidate,
            "score": score,
            "cached": cached
        })
    
    audit_trail.append({
        "step": "candidate_embeddings",
        "total_candidates": len(candidates),
        "cache_hits": cache_hits
    })
    
    # Sort and rank
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Build top matches with explanations
    top_matches = []
    for i, r in enumerate(results[:top_k]):
        explanation = _generate_explanation(r["score"], i + 1)
        top_matches.append(SimilarityResult(
            candidate=r["candidate"],
            score=r["score"],
            rank=i + 1,
            explanation=explanation
        ))
    
    processing_time = (time.time() - start_time) * 1000
    
    audit_trail.append({
        "step": "ranking_complete",
        "processing_time_ms": round(processing_time, 2),
        "top_score": results[0]["score"] if results else 0
    })
    
    return SemanticAnalysisResult(
        query=query,
        top_matches=top_matches,
        processing_time_ms=processing_time,
        model_used="distilbert-base-uncased",
        cache_hit=query_cached,
        audit_trail=audit_trail
    )


def _generate_explanation(score: float, rank: int) -> str:
    """Generate human-readable explanation for similarity score"""
    if score >= 0.9:
        return f"Rank #{rank}: Very high match ({score:.0%}) - Strong semantic similarity"
    elif score >= 0.75:
        return f"Rank #{rank}: Good match ({score:.0%}) - Related content"
    elif score >= 0.6:
        return f"Rank #{rank}: Moderate match ({score:.0%}) - Some relevance"
    elif score >= 0.4:
        return f"Rank #{rank}: Weak match ({score:.0%}) - Limited relevance"
    else:
        return f"Rank #{rank}: Poor match ({score:.0%}) - Consider other options"


def batch_compute_similarities(
    query: str,
    candidates: List[str],
    batch_size: int = 32
) -> List[float]:
    """
    Compute similarities in batches for efficiency.
    Useful for large candidate sets.
    """
    import torch
    
    model, tokenizer = get_model()
    
    # Get query embedding
    query_emb, _ = get_embedding(query)
    
    scores = []
    
    # Process candidates in batches
    for i in range(0, len(candidates), batch_size):
        batch = candidates[i:i + batch_size]
        
        # Tokenize batch
        inputs = tokenizer(
            batch,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Mean pooling
        attention_mask = inputs['attention_mask']
        token_embeddings = outputs.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        batch_embeddings = (sum_embeddings / sum_mask).cpu().numpy()
        
        # Compute cosine similarities
        for emb in batch_embeddings:
            dot = np.dot(query_emb, emb)
            norm1 = np.linalg.norm(query_emb)
            norm2 = np.linalg.norm(emb)
            
            if norm1 == 0 or norm2 == 0:
                scores.append(0.0)
            else:
                scores.append(float(dot / (norm1 * norm2)))
    
    return scores


# Pre-defined templates for common civic queries
CIVIC_TEMPLATES = {
    "rti_information": [
        "request for information under RTI Act",
        "seeking records from public authority",
        "obtaining government documents",
        "public information disclosure"
    ],
    "rti_inspection": [
        "inspection of official records",
        "access to government files",
        "examine public documents",
        "view official papers"
    ],
    "complaint_service": [
        "complaint about poor service quality",
        "grievance regarding government department",
        "service delivery issue",
        "unsatisfactory public service"
    ],
    "complaint_corruption": [
        "complaint about corruption",
        "bribe demand by official",
        "illegal payment request",
        "extortion by government employee"
    ],
    "complaint_delay": [
        "complaint about delay in service",
        "pending application for months",
        "no action taken on request",
        "bureaucratic delay"
    ]
}


def classify_query_type(query: str) -> Dict[str, float]:
    """
    Classify query into civic document types using semantic similarity.
    
    NOTE: This is used ONLY when rule engine has low confidence.
    The rule engine remains the primary decision maker.
    
    Returns dict of template_type -> similarity_score
    """
    results = {}
    
    for template_type, templates in CIVIC_TEMPLATES.items():
        # Average similarity across templates
        scores = [compute_similarity(query, t) for t in templates]
        results[template_type] = sum(scores) / len(scores)
    
    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


def preload_model():
    """Pre-load model for faster inference"""
    logger.info("Pre-loading DistilBERT model...")
    get_model()
    
    # Warm up with a test embedding
    _ = get_embedding("test query for model warmup")
    
    logger.info("DistilBERT model loaded and ready")


def clear_cache():
    """Clear embedding cache"""
    global _embedding_cache
    _embedding_cache = {}
    logger.info("Embedding cache cleared")


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics"""
    return {
        "cache_size": len(_embedding_cache),
        "max_size": _cache_max_size,
        "model_loaded": is_model_loaded()
    }
