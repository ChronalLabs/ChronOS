"""
Policy Intent & Keyword Extraction
Extract semantic understanding of policy documents using DistilBERT
"""

from typing import List, Dict, Any, TYPE_CHECKING
import warnings

if TYPE_CHECKING:
    import numpy as np
    NDArray = np.ndarray
else:
    NDArray = Any

warnings.filterwarnings('ignore')

# Optional dependencies - will show helpful error if not installed
try:
    from transformers import AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    AutoTokenizer = None
    AutoModel = None

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

try:
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    cosine_similarity = None


class PolicyIntentExtractor:
    """Extract policy intent and key concepts using DistilBERT"""
    
    def __init__(self, model_name="distilbert-base-uncased"):
        """
        Initialize DistilBERT model for semantic analysis
        
        Args:
            model_name: HuggingFace model identifier
        """
        if not all([TRANSFORMERS_AVAILABLE, TORCH_AVAILABLE, NUMPY_AVAILABLE, SKLEARN_AVAILABLE]):
            missing = []
            if not TRANSFORMERS_AVAILABLE:
                missing.append("transformers")
            if not TORCH_AVAILABLE:
                missing.append("torch")
            if not NUMPY_AVAILABLE:
                missing.append("numpy")
            if not SKLEARN_AVAILABLE:
                missing.append("scikit-learn")
            
            raise ImportError(
                f"Required packages not installed: {', '.join(missing)}\n"
                "Please install them with:\n"
                "pip install transformers torch numpy scikit-learn\n"
                "See FIX_IMPORTS.md for detailed installation instructions."
            )
        
        print(f"Loading {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        
        # Set to evaluation mode
        self.model.eval()
        
        # Use CPU (hackathon-friendly)
        self.device = torch.device('cpu')
        self.model.to(self.device)
        
        print(f"✓ DistilBERT loaded on {self.device}")
    
    def get_embedding(self, text: str) -> NDArray:
        """
        Get semantic embedding for text
        
        Args:
            text: Input text
            
        Returns:
            numpy array of embeddings
        """
        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            max_length=512,
            padding=True
        )
        
        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use [CLS] token embedding (first token)
            embeddings = outputs.last_hidden_state[:, 0, :]
        
        return embeddings[0].cpu().numpy()
    
    def extract_intent(self, policy_text: str) -> Dict:
        """
        Extract policy intent and key information
        
        Args:
            policy_text: Full policy document text
            
        Returns:
            Dict with intent analysis
        """
        # Split into sentences
        sentences = [s.strip() for s in policy_text.split('.') if len(s.strip()) > 20]
        
        if not sentences:
            return {
                'summary': 'No substantial content found',
                'key_sentences': [],
                'embedding': None
            }
        
        # Get embeddings for all sentences
        sentence_embeddings = []
        for sentence in sentences:
            try:
                emb = self.get_embedding(sentence)
                sentence_embeddings.append(emb)
            except Exception as e:
                print(f"Warning: Could not process sentence: {e}")
                continue
        
        if not sentence_embeddings:
            return {
                'summary': 'Could not process sentences',
                'key_sentences': [],
                'embedding': None
            }
        
        # Calculate importance scores (distance from mean)
        mean_embedding = np.mean(sentence_embeddings, axis=0)
        importance_scores = []
        
        for i, emb in enumerate(sentence_embeddings):
            similarity = cosine_similarity([emb], [mean_embedding])[0][0]
            importance_scores.append({
                'sentence': sentences[i],
                'importance': float(similarity)
            })
        
        # Sort by importance
        importance_scores.sort(key=lambda x: x['importance'], reverse=True)
        
        return {
            'summary': 'Policy intent extracted',
            'key_sentences': importance_scores[:5],  # Top 5 sentences
            'total_sentences': len(sentences),
            'embedding': mean_embedding.tolist()
        }
    
    def find_similar_policies(
        self,
        query_policy: str,
        candidate_policies: List[str]
    ) -> List[Dict]:
        """
        Find policies similar to query
        
        Args:
            query_policy: Policy to compare
            candidate_policies: List of policies to compare against
            
        Returns:
            List of dicts with similarity scores
        """
        # Get query embedding
        query_emb = self.get_embedding(query_policy)
        
        results = []
        for i, candidate in enumerate(candidate_policies):
            try:
                candidate_emb = self.get_embedding(candidate)
                similarity = cosine_similarity([query_emb], [candidate_emb])[0][0]
                
                results.append({
                    'policy_index': i,
                    'policy_text': candidate[:100] + '...',
                    'similarity': float(similarity)
                })
            except Exception as e:
                print(f"Warning: Could not process candidate {i}: {e}")
                continue
        
        return sorted(results, key=lambda x: x['similarity'], reverse=True)
    
    def extract_keywords_semantic(
        self,
        policy_text: str,
        keyword_candidates: List[str]
    ) -> List[Dict]:
        """
        Score keywords by semantic relevance
        
        Args:
            policy_text: Policy document
            keyword_candidates: List of potential keywords
            
        Returns:
            List of keywords with relevance scores
        """
        # Get policy embedding
        policy_emb = self.get_embedding(policy_text)
        
        keyword_scores = []
        for keyword in keyword_candidates:
            try:
                keyword_emb = self.get_embedding(keyword)
                relevance = cosine_similarity([policy_emb], [keyword_emb])[0][0]
                
                keyword_scores.append({
                    'keyword': keyword,
                    'relevance': float(relevance)
                })
            except Exception as e:
                print(f"Warning: Could not process keyword '{keyword}': {e}")
                continue
        
        return sorted(keyword_scores, key=lambda x: x['relevance'], reverse=True)


def main():
    """Example usage"""
    print("🧠 CIVISIM Policy Intent Extractor")
    print("=" * 50)
    
    # Initialize
    extractor = PolicyIntentExtractor()
    
    # Sample policy
    sample_policy = """
    Construction activities are regulated to minimize disruption during peak hours.
    Night construction is permitted only in residential zones where necessary and approved.
    Safety inspections are mandatory weekly. All contractors must maintain proper
    equipment and follow safety protocols. Noise levels must be monitored continuously.
    Emergency procedures must be established for all construction sites.
    """
    
    print("\n📋 Sample Policy:")
    print(sample_policy[:200] + "...")
    
    # Extract intent
    print("\n🔍 Extracting Intent...")
    intent = extractor.extract_intent(sample_policy)
    
    print(f"\n✓ Processed {intent['total_sentences']} sentences")
    print("\n🎯 Key Sentences:")
    for i, sent in enumerate(intent['key_sentences'][:3], 1):
        print(f"\n{i}. {sent['sentence']}")
        print(f"   Importance: {sent['importance']:.3f}")
    
    # Score keywords
    keywords = [
        "night construction",
        "safety inspection",
        "residential zone",
        "noise limits",
        "emergency protocols"
    ]
    
    print("\n\n🔑 Keyword Relevance:")
    scores = extractor.extract_keywords_semantic(sample_policy, keywords)
    for item in scores:
        print(f"  • {item['keyword']:25} {item['relevance']:.3f}")


if __name__ == "__main__":
    main()
