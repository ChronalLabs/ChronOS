"""
Ambiguity Detection (Task 4)
Flag uncertain language that affects simulation trustworthiness
"""

import re
from typing import List, Dict
from enum import Enum


class AmbiguityLevel(Enum):
    """Severity levels for ambiguous phrases"""
    CRITICAL = "critical"      # Policy very unclear
    HIGH = "high"              # Significant ambiguity
    MEDIUM = "medium"          # Somewhat unclear
    LOW = "low"                # Slightly ambiguous


class AmbiguityDetector:
    """Detect ambiguous language in policies"""
    
    # Define ambiguous phrase patterns
    AMBIGUOUS_PHRASES = {
        AmbiguityLevel.CRITICAL: [
            r"\bmay\b",                    # "may be" - optional
            r"\bmight\b",                  # "might" - uncertain
            r"\bif\sfeasible\b",           # "if feasible" - vague condition
            r"\bas\srequired\b",           # "as required" - undefined
            r"\bwhere\snecessary\b",       # "where necessary" - subjective
            r"\bwhere\sapplicable\b",      # "where applicable" - vague
        ],
        AmbiguityLevel.HIGH: [
            r"\bshould\b",                 # "should" - recommendation
            r"\bor\s(?:equivalent|similar)",  # "or equivalent" - subjective
            r"\breasona(?:ble|bly)\b",     # "reasonable" - undefined
            r"\bappropriate(?:ly)?\b",     # "appropriate" - vague
            r"\bexcept\s(?:as|where)",     # "except as/where" - conditional
        ],
        AmbiguityLevel.MEDIUM: [
            r"\bconsider\b",               # "consider" - optional action
            r"\bencourage\b",              # "encourage" - optional
            r"\battempt\b",                # "attempt" - effort-based
            r"\bto\sthe\s(?:extent|degree)",  # "to the extent" - qualified
        ],
        AmbiguityLevel.LOW: [
            r"\bcontingent\s(?:on|upon)",  # "contingent on" - conditional
            r"\bprovided\sthat\b",         # "provided that" - condition
        ]
    }
    
    def __init__(self):
        """Compile regex patterns"""
        self.compiled_patterns = {}
        for level, phrases in self.AMBIGUOUS_PHRASES.items():
            self.compiled_patterns[level] = [
                re.compile(phrase, re.IGNORECASE)
                for phrase in phrases
            ]
    
    def find_ambiguities(self, text: str) -> List[Dict]:
        """
        Find all ambiguous phrases in text
        
        Args:
            text (str): Policy text
            
        Returns:
            List[Dict]: Ambiguous phrases with context
        """
        findings = []
        
        for level in AmbiguityLevel:
            patterns = self.compiled_patterns[level]
            
            for pattern in patterns:
                matches = pattern.finditer(text)
                
                for match in matches:
                    # Get context (50 chars before and after)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].strip()
                    
                    findings.append({
                        'phrase': match.group(),
                        'severity': level.value,
                        'context': context,
                        'position': match.start(),
                        'pattern': pattern.pattern
                    })
        
        # Sort by position
        return sorted(findings, key=lambda x: x['position'])
    
    def ambiguity_score(self, text: str) -> Dict:
        """
        Calculate overall ambiguity score (0-100)
        
        Args:
            text (str): Policy text
            
        Returns:
            dict: Ambiguity metrics
        """
        findings = self.find_ambiguities(text)
        
        # Weight by severity
        weights = {
            'critical': 5,
            'high': 3,
            'medium': 2,
            'low': 1
        }
        
        total_score = sum(weights[f['severity']] for f in findings)
        
        # Normalize to 0-100
        # Rough: 20 critical phrases = 100
        normalized_score = min(100, (total_score / 100) * 100)
        
        # Count by severity
        severity_counts = {}
        for level in AmbiguityLevel:
            count = sum(1 for f in findings if f['severity'] == level.value)
            severity_counts[level.value] = count
        
        return {
            'overall_score': float(normalized_score),
            'total_ambiguous_phrases': len(findings),
            'by_severity': severity_counts,
            'findings': findings,
            'trust_level': self._classify_trust(normalized_score)
        }
    
    def _classify_trust(self, score: float) -> str:
        """Classify trustworthiness based on ambiguity score"""
        if score < 20:
            return "HIGH - Policy is clear"
        elif score < 40:
            return "MEDIUM - Some unclear language"
        elif score < 60:
            return "LOW - Significant ambiguity"
        else:
            return "VERY LOW - Policy is vague"
    
    def flag_ambiguous_sections(self, text: str) -> List[Dict]:
        """
        Flag sections of policy with highest ambiguity
        
        Args:
            text (str): Policy text
            
        Returns:
            List[Dict]: Sections ranked by ambiguity
        """
        sentences = text.split('. ')
        
        sentence_ambiguity = []
        
        for i, sentence in enumerate(sentences):
            findings = self.find_ambiguities(sentence)
            score = sum(
                {'critical': 5, 'high': 3, 'medium': 2, 'low': 1}[f['severity']]
                for f in findings
            )
            
            if findings:  # Only include sentences with ambiguity
                sentence_ambiguity.append({
                    'sentence_num': i + 1,
                    'text': sentence.strip(),
                    'ambiguity_score': score,
                    'phrases': [f['phrase'] for f in findings]
                })
        
        return sorted(
            sentence_ambiguity,
            key=lambda x: x['ambiguity_score'],
            reverse=True
        )
    
    def generate_report(self, text: str) -> str:
        """
        Generate human-readable ambiguity report
        
        Args:
            text (str): Policy text
            
        Returns:
            str: Formatted report
        """
        score_data = self.ambiguity_score(text)
        
        report = f"""
╔═══════════════════════════════════════════════╗
║     POLICY AMBIGUITY ANALYSIS REPORT          ║
╚═══════════════════════════════════════════════╝

📊 OVERALL SCORE: {score_data['overall_score']:.1f}/100
🔒 TRUST LEVEL: {score_data['trust_level']}

📈 BREAKDOWN:
  • Critical Ambiguities: {score_data['by_severity']['critical']}
  • High: {score_data['by_severity']['high']}
  • Medium: {score_data['by_severity']['medium']}
  • Low: {score_data['by_severity']['low']}
  • TOTAL: {score_data['total_ambiguous_phrases']}

⚠️ TOP FLAGGED PHRASES:
"""
        for finding in score_data['findings'][:5]:
            report += f"\n  [{finding['severity'].upper()}] {finding['phrase']}"
            report += f"\n    Context: ...{finding['context'][:60]}...\n"
        
        report += f"""
✅ RECOMMENDATION:
"""
        if score_data['overall_score'] > 60:
            report += "  ⚠️  This policy needs SIGNIFICANT clarification before simulation."
        elif score_data['overall_score'] > 40:
            report += "  ⚠️  Address flagged ambiguities for reliable simulation."
        else:
            report += "  ✓ Policy is sufficiently clear for simulation."
        
        return report


# Quick test
if __name__ == "__main__":
    detector = AmbiguityDetector()
    
    policy = """
    Night construction may be permitted in residential zones where feasible.
    Safety inspections should be conducted as required. Contractors must make
    reasonable attempts to minimize noise where applicable.
    """
    
    score_data = detector.ambiguity_score(policy)
    print(f"📊 Ambiguity Score: {score_data['overall_score']:.1f}/100")
    print(f"🔒 Trust Level: {score_data['trust_level']}")
    print(detector.generate_report(policy))
