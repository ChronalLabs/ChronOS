"""
Skill normalizer using rapidfuzz for fuzzy matching.
Maps skill variations to canonical forms with confidence scoring.
"""
import os
from typing import Optional, Tuple
from rapidfuzz import fuzz, process
import yaml


class SkillNormalizer:
    """Normalizes skill mentions to canonical forms using fuzzy matching."""
    
    def __init__(self, taxonomy_path: Optional[str] = None):
        """
        Initialize the normalizer with a skill taxonomy.
        
        Args:
            taxonomy_path: Path to skills.yaml, defaults to same directory
        """
        if taxonomy_path is None:
            taxonomy_path = os.path.join(os.path.dirname(__file__), "skills.yaml")
        
        self.taxonomy = self._load_taxonomy(taxonomy_path)
        self.canonical_skills = self._build_canonical_list()
        self.alias_map = self._build_alias_map()
        self.thresholds = self.taxonomy.get("thresholds", {
            "exact_match": 100,
            "high_confidence": 90,
            "medium_confidence": 75,
            "low_confidence": 60,
        })
    
    def _load_taxonomy(self, path: str) -> dict:
        """Load taxonomy from YAML file."""
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    def _build_canonical_list(self) -> list[str]:
        """Build flat list of all canonical skill names."""
        skills = []
        categories = self.taxonomy.get("categories", {})
        for category, data in categories.items():
            if isinstance(data, dict) and "canonical" in data:
                skills.extend(data["canonical"])
        return skills
    
    def _build_alias_map(self) -> dict[str, str]:
        """Build mapping from aliases to canonical names."""
        alias_map = {}
        categories = self.taxonomy.get("categories", {})
        
        for category, data in categories.items():
            if not isinstance(data, dict):
                continue
            
            canonical_list = data.get("canonical", [])
            aliases = data.get("aliases", {})
            
            # Map each alias to its canonical form
            for key, alias_list in aliases.items():
                # Find the canonical name that matches this key
                canonical_name = None
                key_lower = key.lower().replace("_", " ")
                
                for c in canonical_list:
                    if c.lower() == key_lower or key.lower() in c.lower().replace(".", ""):
                        canonical_name = c
                        break
                
                if canonical_name and isinstance(alias_list, list):
                    for alias in alias_list:
                        alias_map[alias.lower()] = canonical_name
        
        return alias_map
    
    def normalize(self, skill: str) -> Tuple[str, str, float]:
        """
        Normalize a skill mention to its canonical form.
        
        Args:
            skill: Raw skill text from resume/JD
        
        Returns:
            Tuple of (canonical_name, confidence_level, match_score)
            - canonical_name: Normalized skill name
            - confidence_level: 'high', 'medium', 'low', or 'no_match'
            - match_score: Numeric score 0-100
        """
        skill_lower = skill.lower().strip()
        
        # Check exact alias match first
        if skill_lower in self.alias_map:
            return (self.alias_map[skill_lower], "high", 100.0)
        
        # Check if it's already a canonical name (case-insensitive)
        for canonical in self.canonical_skills:
            if canonical.lower() == skill_lower:
                return (canonical, "high", 100.0)
        
        # Fuzzy match against canonical skills
        if self.canonical_skills:
            result = process.extractOne(
                skill_lower,
                [c.lower() for c in self.canonical_skills],
                scorer=fuzz.ratio
            )
            
            if result:
                match_text, score, idx = result
                # If high score, return immediately
                if score >= self.thresholds["high_confidence"]:
                    canonical = self.canonical_skills[idx]
                    return (canonical, "high", score)
        
        # Fuzzy match against ALIASES
        # This handles cases like "Amazn Web Services" (typo) -> "amazon web services" (alias) -> "AWS" (canonical)
        if self.alias_map:
            alias_result = process.extractOne(
                skill_lower,
                list(self.alias_map.keys()),
                scorer=fuzz.ratio
            )
            
            if alias_result:
                alias_match, alias_score, _ = alias_result
                
                # Check if this alias score is better than the canonical score
                # or if we didn't have a canonical score
                canonical_score = result[1] if result else 0
                
                if alias_score > canonical_score and alias_score >= self.thresholds["medium_confidence"]:
                    start_canonical = self.alias_map[alias_match]
                    return (start_canonical, self._score_to_confidence(alias_score), alias_score)

        # Return best canonical match if it exists and wasn't returned above
        if result:
            match_text, score, idx = result
            canonical = self.canonical_skills[idx]
            confidence = self._score_to_confidence(score)
            
            if confidence != "no_match":
                return (canonical, confidence, score)
        
        # No good match found
        return (skill, "no_match", 0.0)
    
    def normalize_batch(self, skills: list[str]) -> list[dict]:
        """
        Normalize a batch of skills.
        
        Args:
            skills: List of raw skill texts
        
        Returns:
            List of normalization results with original, canonical, and confidence
        """
        results = []
        for skill in skills:
            canonical, confidence, score = self.normalize(skill)
            results.append({
                "original": skill,
                "canonical": canonical,
                "confidence": confidence,
                "score": score,
            })
        return results
    
    def _score_to_confidence(self, score: float) -> str:
        """Convert numeric score to confidence level."""
        if score >= self.thresholds["high_confidence"]:
            return "high"
        elif score >= self.thresholds["medium_confidence"]:
            return "medium"
        elif score >= self.thresholds["low_confidence"]:
            return "low"
        else:
            return "no_match"
    
    def get_category(self, skill: str) -> Optional[str]:
        """
        Get the category of a skill.
        
        Args:
            skill: Canonical or raw skill name
        
        Returns:
            Category name or None if not found
        """
        # Normalize first
        canonical, _, _ = self.normalize(skill)
        
        # Find in categories
        categories = self.taxonomy.get("categories", {})
        for category, data in categories.items():
            if isinstance(data, dict) and "canonical" in data:
                if canonical in data["canonical"]:
                    return category
        
        return None
    
    def get_related_skills(self, skill: str) -> list[str]:
        """
        Get skills in the same category.
        
        Args:
            skill: Skill name to find relatives for
        
        Returns:
            List of related skill names
        """
        category = self.get_category(skill)
        if not category:
            return []
        
        categories = self.taxonomy.get("categories", {})
        if category in categories:
            return categories[category].get("canonical", [])
        
        return []


# Singleton instance for convenience
_normalizer_instance = None


def get_normalizer() -> SkillNormalizer:
    """Get the singleton normalizer instance."""
    global _normalizer_instance
    if _normalizer_instance is None:
        _normalizer_instance = SkillNormalizer()
    return _normalizer_instance


def normalize_skill(skill: str) -> Tuple[str, str, float]:
    """Convenience function to normalize a single skill."""
    return get_normalizer().normalize(skill)
