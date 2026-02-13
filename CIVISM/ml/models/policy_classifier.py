"""
Policy Classification (Task 5)
Classify policy as Speed-focused, Safety-focused, or Balanced using Zero-Shot BART
"""

from transformers import pipeline
from typing import Dict, List


class PolicyClassifier:
    """Classify policies using zero-shot classification"""
    
    def __init__(self, model="facebook/bart-large-mnli"):
        """
        Initialize zero-shot classifier
        
        Args:
            model (str): HuggingFace model identifier
        """
        self.classifier = pipeline(
            "zero-shot-classification",
            model=model,
            device=-1  # -1 = CPU, 0+ = GPU
        )
        print(f"✓ Zero-shot classifier loaded: {model}")
    
    def classify_policy_focus(self, text: str) -> Dict:
        """
        Classify policy as speed-focused, safety-focused, or balanced
        
        Args:
            text (str): Policy text (use first 512 tokens)
            
        Returns:
            dict: Classification results with confidence scores
        """
        # Limit to first 512 tokens for efficiency
        tokens = text.split()[:512]
        text = ' '.join(tokens)
        
        labels = [
            "speed-focused policy that prioritizes fast project completion",
            "safety-focused policy that prioritizes worker and public safety",
            "balanced policy that considers both speed and safety equally"
        ]
        
        result = self.classifier(text, labels, multi_label=False)
        
        return {
            'primary_classification': result['labels'][0],
            'confidence': float(result['scores'][0]),
            'all_scores': {
                labels[i]: float(result['scores'][i])
                for i in range(len(labels))
            },
            'recommendation': self._generate_recommendation(result['labels'][0])
        }
    
    def classify_policy_type(self, text: str) -> Dict:
        """
        Classify policy by domain (construction, environmental, etc)
        
        Args:
            text (str): Policy text
            
        Returns:
            dict: Domain classification
        """
        labels = [
            "construction and building policy",
            "environmental and ecological policy",
            "traffic and transportation policy",
            "safety and risk management policy",
            "labor and worker protection policy"
        ]
        
        result = self.classifier(text, labels, multi_label=False)
        
        return {
            'domain': result['labels'][0],
            'confidence': float(result['scores'][0]),
            'domain_scores': {
                labels[i]: float(result['scores'][i])
                for i in range(len(labels))
            }
        }
    
    def classify_multi_aspect(self, text: str) -> Dict:
        """
        Classify policy across multiple aspects simultaneously
        
        Args:
            text (str): Policy text
            
        Returns:
            dict: Multi-aspect classification
        """
        # Truncate for efficiency
        tokens = text.split()[:512]
        text = ' '.join(tokens)
        
        classifications = {}
        
        # Speed vs Safety
        speed_safety = self.classify_policy_focus(text)
        classifications['speed_safety_focus'] = speed_safety
        
        # Policy domain
        domain = self.classify_policy_type(text)
        classifications['domain'] = domain
        
        # Strictness level
        strictness_labels = [
            "permissive policy with minimal restrictions",
            "moderate policy with balanced restrictions",
            "strict policy with comprehensive regulations"
        ]
        
        strictness = self.classifier(text, strictness_labels, multi_label=False)
        classifications['strictness'] = {
            'level': strictness['labels'][0],
            'confidence': float(strictness['scores'][0]),
            'scores': {
                strictness_labels[i]: float(strictness['scores'][i])
                for i in range(len(strictness_labels))
            }
        }
        
        return classifications
    
    def _generate_recommendation(self, classification: str) -> str:
        """Generate simulation parameter recommendation"""
        if "speed-focused" in classification:
            return "Recommend: SPEED_PRIORITY=0.7, SAFETY_PRIORITY=0.3"
        elif "safety-focused" in classification:
            return "Recommend: SAFETY_PRIORITY=0.8, SPEED_PRIORITY=0.2"
        else:
            return "Recommend: SPEED_PRIORITY=0.5, SAFETY_PRIORITY=0.5"
    
    def batch_classify(
        self,
        policies: List[str],
        aspect: str = "focus"
    ) -> List[Dict]:
        """
        Classify multiple policies efficiently
        
        Args:
            policies (List[str]): List of policy texts
            aspect (str): 'focus', 'domain', or 'multi'
            
        Returns:
            List[Dict]: Classification results
        """
        results = []
        
        for i, policy in enumerate(policies):
            print(f"  Processing policy {i+1}/{len(policies)}...", end='\r')
            
            if aspect == "focus":
                result = self.classify_policy_focus(policy)
            elif aspect == "domain":
                result = self.classify_policy_type(policy)
            else:  # multi
                result = self.classify_multi_aspect(policy)
            
            results.append(result)
        
        print(f"✓ Classified {len(policies)} policies")
        return results


# Quick test
if __name__ == "__main__":
    classifier = PolicyClassifier()
    
    policy = """
    Construction limited to 7 AM - 6 PM. Weekly safety audits mandatory.
    All equipment inspected daily. Worker breaks required every 4 hours.
    """
    
    result = classifier.classify_policy_focus(policy)
    print(f"\n📋 Classification: {result['primary_classification']}")
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Recommendation: {result['recommendation']}")
