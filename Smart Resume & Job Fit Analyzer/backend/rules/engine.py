"""
Rule-based evaluation engine.
Computes deterministic scores using configurable weights.
Rules always override AI signals.
"""
import os
import re
import yaml
from typing import Optional

from api.schemas import (
    ParsedResume,
    ParsedJobDescription,
    EvaluationResult,
    ScoreBreakdown,
    ImprovementSuggestion,
    SkillMatch,
)
from .matchers import match_skills


class RuleEngine:
    """Deterministic rule-based evaluation engine."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the engine with scoring configuration.
        
        Args:
            config_path: Path to config.yaml, defaults to same directory
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        
        self.config = self._load_config(config_path)
        self.weights = self.config["scoring"]["weights"]
        self.thresholds = self.config["scoring"]["match_thresholds"]
        self.penalties = self.config["scoring"]["penalties"]
        self.bounds = self.config["scoring"]["score_bounds"]
        self.enforcement = self.config["scoring"]["required_skill_enforcement"]
    
    def _load_config(self, path: str) -> dict:
        """Load configuration from YAML."""
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    def evaluate(
        self,
        resume: ParsedResume,
        job_description: ParsedJobDescription,
    ) -> EvaluationResult:
        """
        Evaluate resume against job description.
        
        Args:
            resume: Parsed resume data
            job_description: Parsed job description data
        
        Returns:
            EvaluationResult with score, breakdown, and suggestions
        """
        # Step 1: Match skills
        skill_results = match_skills(
            resume_skills=[s.dict() for s in resume.skills],
            jd_required_skills=job_description.required_skills,
            jd_optional_skills=job_description.optional_skills,
            full_match_threshold=self.thresholds["full_match"],
            partial_match_threshold=self.thresholds["partial_match"],
        )
        
        # Step 2: Calculate component scores
        required_score = self._calculate_required_skills_score(skill_results)
        optional_score = self._calculate_optional_skills_score(skill_results)
        experience_score = self._calculate_experience_score(resume)
        education_score = self._calculate_education_score(resume, job_description)
        
        # Step 3: Apply weights
        weighted_score = (
            required_score * self.weights["required_skills"] +
            optional_score * self.weights["optional_skills"] +
            experience_score * self.weights["experience_depth"] +
            education_score * self.weights["education_match"]
        )
        
        # Step 4: Apply penalties
        penalties_applied = []
        penalty_total = 0
        
        missing_required_count = len(skill_results["missing_required"])
        if missing_required_count > 0:
            skill_penalty = missing_required_count * self.penalties["missing_required_skill"]
            skill_penalty = max(skill_penalty, self.penalties["max_penalty"])
            penalty_total += skill_penalty
            penalties_applied.append(
                f"{missing_required_count} missing required skill(s): {skill_penalty} points"
            )
        
        weighted_score += penalty_total
        
        # Step 5: Enforce required skill minimum
        if skill_results["stats"]["required_total"] > 0:
            required_ratio = (
                skill_results["stats"]["required_matched"] /
                skill_results["stats"]["required_total"]
            )
            if required_ratio < self.enforcement["minimum_required_matched"]:
                cap = self.enforcement["below_minimum_cap"]
                if weighted_score > cap:
                    weighted_score = cap
                    penalties_applied.append(
                        f"Score capped at {cap}: below {self.enforcement['minimum_required_matched']*100}% required skills matched"
                    )
        
        # Step 6: Bound final score
        final_score = self._bound_score(weighted_score)
        
        # Step 7: Generate explanation
        explanation = self._generate_explanation(
            final_score,
            skill_results,
            required_score,
            optional_score,
            experience_score,
            education_score,
        )
        
        # Step 8: Generate improvement suggestions
        suggestions = self._generate_suggestions(skill_results, resume, job_description)
        
        # Step 9: Analyze experience signals
        from api.schemas import ExperienceSignals, ConfidenceLevel
        
        ownership_verbs = ["led", "managed", "architected", "designed", "created", "spearheaded", "built", "developed"]
        leadership_verbs = ["led", "mentored", "managed", "supervised", "directed"]
        
        leadership_signals = []
        ownership_count = 0
        relevant_years = 0.0 # simplified placeholder
        
        if resume.experience:
             # Basic heuristic for years - simplistic for now
            relevant_years = len(resume.experience) * 1.5 
            
            for exp in resume.experience:
                text_lower = (exp.title + " " + exp.description + " " + " ".join(exp.responsibilities)).lower()
                if any(v in text_lower for v in leadership_verbs):
                    leadership_signals.append(f"Leadership detected in {exp.company}")
                
                # Check for ownership in title or action verbs
                if any(v in text_lower for v in ownership_verbs):
                    ownership_count += 1
        
        ownership_strength = "High" if ownership_count >= 2 else "Medium" if ownership_count > 0 else "Low"
        
        exp_signals = ExperienceSignals(
            relevant_years=relevant_years,
            ownership_strength=ownership_strength,
            leadership_signals=leadership_signals,
            responsibility_alignment=f"Found {ownership_count} roles with strong ownership signals."
        )
        
        # Determine overall confidence
        # High if we have good resume content and good JD coverage
        confidence = ConfidenceLevel.MEDIUM
        if len(resume.experience) > 0 and len(resume.skills) > 5 and len(job_description.required_skills) > 0:
            confidence = ConfidenceLevel.HIGH
        elif len(resume.skills) < 3:
            confidence = ConfidenceLevel.LOW
        
        # Build score breakdown
        breakdown = ScoreBreakdown(
            required_skills_score=required_score,
            optional_skills_score=optional_score,
            experience_depth_score=experience_score,
            education_match_score=education_score,
            weights_applied=self.weights,
            penalties_applied=penalties_applied,
        )
        
        return EvaluationResult(
            job_fit_score=final_score,
            confidence_level=confidence,
            score_breakdown=breakdown,
            skill_matches=skill_results["matches"],
            matched_count=skill_results["stats"]["matched_count"],
            partial_count=skill_results["stats"]["partial_count"],
            missing_count=skill_results["stats"]["missing_count"],
            explanation=explanation,
            experience_signals=exp_signals,
            improvement_suggestions=suggestions,
        )
    
    def _calculate_required_skills_score(self, skill_results: dict) -> float:
        """Calculate score for required skills (0-100)."""
        stats = skill_results["stats"]
        if stats["required_total"] == 0:
            return 100.0  # No requirements = full score
        
        matched = stats["required_matched"]
        partial = len(skill_results["partial_required"])
        total = stats["required_total"]
        
        # Full matches count as 100%, partial as 50%
        score = ((matched * 100) + (partial * 50)) / total
        return min(100.0, score)
    
    def _calculate_optional_skills_score(self, skill_results: dict) -> float:
        """Calculate score for optional skills (0-100)."""
        stats = skill_results["stats"]
        if stats["optional_total"] == 0:
            return 100.0  # No optional skills = full score
        
        matched = stats["optional_matched"]
        partial = len(skill_results["partial_optional"])
        total = stats["optional_total"]
        
        score = ((matched * 100) + (partial * 50)) / total
        return min(100.0, score)
    
    def _calculate_experience_score(self, resume: ParsedResume) -> float:
        """Calculate experience depth score (0-100)."""
        if not resume.experience:
            return 50.0  # Neutral if no experience section
        
        score = 50.0  # Base score
        signals = self.config.get("experience_signals", {})
        
        # Analyze experience descriptions
        for exp in resume.experience:
            text = exp.description.lower() + " ".join(exp.responsibilities).lower()
            
            # Check for leadership signals
            if "leadership" in signals:
                for pattern in signals["leadership"]["patterns"]:
                    if re.search(pattern, text, re.IGNORECASE):
                        score += 10 * signals["leadership"]["weight"]
                        break
            
            # Check for scale signals
            if "scale" in signals:
                for pattern in signals["scale"]["patterns"]:
                    if re.search(pattern, text, re.IGNORECASE):
                        score += 10 * signals["scale"]["weight"]
                        break
            
            # Check for technical depth
            if "technical_depth" in signals:
                for pattern in signals["technical_depth"]["patterns"]:
                    if re.search(pattern, text, re.IGNORECASE):
                        score += 8 * signals["technical_depth"]["weight"]
                        break
        
        return min(100.0, score)
    
    def _calculate_education_score(
        self,
        resume: ParsedResume,
        job_description: ParsedJobDescription,
    ) -> float:
        """Calculate education match score (0-100)."""
        if not resume.education:
            return 50.0  # Neutral if no education section
        
        education_config = self.config.get("education", {})
        degree_levels = education_config.get("degree_levels", {})
        
        # Find highest degree level
        max_score = 50.0
        for edu in resume.education:
            degree_lower = edu.degree.lower()
            for degree_type, score in degree_levels.items():
                if degree_type in degree_lower:
                    max_score = max(max_score, score)
                    break
        
        # Check field match if JD has education requirements
        if job_description.education_requirements:
            jd_edu = job_description.education_requirements.lower()
            for edu in resume.education:
                if edu.field_of_study:
                    # Simple keyword matching for field
                    if any(word in jd_edu for word in edu.field_of_study.lower().split()):
                        max_score += education_config.get("field_match_bonus", 10)
                        break
        
        return min(100.0, max_score)
    
    def _bound_score(self, score: float) -> int:
        """Bound score to configured min/max."""
        bounded = max(self.bounds["min"], min(self.bounds["max"], score))
        return round(bounded)
    
    def _generate_explanation(
        self,
        score: int,
        skill_results: dict,
        required_score: float,
        optional_score: float,
        experience_score: float,
        education_score: float,
    ) -> str:
        """Generate human-readable explanation."""
        stats = skill_results["stats"]
        
        explanation = f"""Your job-fit score is {score}/100.

This score reflects:
• {stats['required_matched']} of {stats['required_total']} required skills matched ({required_score:.0f}% score)
• {stats['optional_matched']} of {stats['optional_total']} preferred skills matched ({optional_score:.0f}% score)
• Experience depth score: {experience_score:.0f}%
• Education alignment score: {education_score:.0f}%

"""
        
        if skill_results["missing_required"]:
            explanation += f"Missing required skills: {', '.join(skill_results['missing_required'][:5])}\n"
        
        if skill_results["partial_required"]:
            explanation += f"Partially matched skills: {', '.join(skill_results['partial_required'][:5])}\n"
        
        return explanation.strip()
    
    def _generate_suggestions(
        self,
        skill_results: dict,
        resume: ParsedResume,
        job_description: ParsedJobDescription,
    ) -> list[ImprovementSuggestion]:
        """Generate actionable improvement suggestions."""
        suggestions = []
        max_suggestions = self.config.get("output", {}).get("max_suggestions", 5)
        
        
        # Determine domain for specific checks
        domain = self._detect_domain(job_description)
        
        # Priority 1: Formatting & Structure Gaps (Immediate fix)
        # Check contact info
        contact_gaps = []
        if not resume.contact_info.get("email"):
            contact_gaps.append("email")
        if not resume.contact_info.get("phone"):
            contact_gaps.append("phone number")
        
        # Check for LinkedIn/GitHub for tech roles
        is_tech_role = domain in ["software_engineering", "data_science"] or \
                      any(s in job_description.raw_text.lower() for s in ["software", "developer", "engineer", "data", "full stack"])
                      
        if is_tech_role:
            if not resume.contact_info.get("linkedin"):
                contact_gaps.append("LinkedIn profile")
            if not resume.contact_info.get("github") and "github" not in str(resume.contact_info).lower():
                 # Only suggest GitHub if it's a coding role
                contact_gaps.append("GitHub profile")
                
        if contact_gaps:
            suggestions.append(ImprovementSuggestion(
                category="Formatting",
                priority=1,
                suggestion=f"Add missing contact information: {', '.join(contact_gaps)}",
            ))

        # Priority 2: Missing required skills
        for skill in skill_results["missing_required"][:3]:
            suggestions.append(ImprovementSuggestion(
                category="Missing Skill",
                priority=1,
                suggestion=f"Add '{skill}' to your resume with specific examples of usage",
                affected_skills=[skill],
            ))
        
        # Priority 3: Experience Quality Gaps
        if not resume.experience:
             suggestions.append(ImprovementSuggestion(
                category="Experience",
                priority=1,
                suggestion="Add a detailed work experience section with responsibilities and achievements",
            ))
        else:
            # Domain-Specific Checks
            if domain == "finance":
                # Stricter checks: require currency symbols or specific metric keywords with numbers
                # e.g. "$50k", "15% margin", "budget of 50k"
                finance_metrics = [
                    r"[\$€£]\s*\d+",           # Currency + number
                    r"\d+\s*%",                # Percentage
                    r"\d+\s*(?:k|m|b)\+?",     # Short numbers (50k, 10m)
                    r"budget\s*(?:of)?\s*[\$€£]?\d+", # Budget + number
                    r"saved\s*[\$€£]?\d+",     # Saved + number
                    r"revenue",                # specific enough? maybe 
                    r"profit\s*margin" 
                ]
                
                has_finance_metrics = any(
                    any(re.search(pat, " ".join(exp.responsibilities), re.IGNORECASE) for pat in finance_metrics)
                    for exp in resume.experience
                )
                
                if not has_finance_metrics:
                     suggestions.append(ImprovementSuggestion(
                        category="Domain Gap",
                        priority=1,
                        suggestion="Finance roles require quantifiable results. Highlight budgets managed, cost savings, or revenue growth ($/%) in your bullet points.",
                    ))
            
            elif domain == "healthcare":
                # Healthcare: Check for patient volume or specific clinical terms
                # "patient" is too generic if just "saw patients". 
                # Look for "caseload", "acuity", "triage", "compliance" or numbers + patient
                health_context = [
                    r"caseload",
                    r"acuity",
                    r"triage",
                    r"vital\s*signs",
                    r"compliance",
                    r"hipaa",
                    r"\d+\s*patients", # "20 patients"
                    r"administer(?:ed)?\s*med" # "administered medication" - clearer action
                ]
                
                has_health_context = any(
                    any(re.search(pat, " ".join(exp.responsibilities), re.IGNORECASE) for pat in health_context)
                    for exp in resume.experience
                )
                
                if not has_health_context:
                    suggestions.append(ImprovementSuggestion(
                        category="Domain Gap",
                        priority=1,
                        suggestion="Emphasize patient outcomes, clinical volume (e.g., 'managed 20+ patients'), and specific care procedures.",
                    ))

            # General Weak Verbs Check
            strong_verbs = {"led", "developed", "created", "managed", "designed", "implemented", "architected", "improved", "increased", "decreased", "saved", "launched", "engineered", "optimized", "spearheaded", "forecasted", "audited", "diagnosed", "treated", "administered"}
            weak_starts = 0
            total_bullets = 0
            
            for exp in resume.experience:
                for bullet in exp.responsibilities:
                    total_bullets += 1
                    first_word = bullet.strip().split()[0].lower() if bullet.strip() else ""
                    if first_word not in strong_verbs and not first_word.endswith("ed"): # Simple heuristic
                         weak_starts += 1
            
            if total_bullets > 0 and (weak_starts / total_bullets) > 0.5:
                 suggestions.append(ImprovementSuggestion(
                    category="Impact",
                    priority=2,
                    suggestion="Start bullet points with strong action verbs (e.g., 'Led', 'Developed', 'Optimized') instead of passive language.",
                ))

            # General Metrics Check (skip if specific domain check failed already to avoid double dipping)
            has_metrics = any(
                re.search(r'\d+%|\d+ (users|customers|requests|\$)|[\$€£]\d+', 
                         " ".join(exp.responsibilities))
                for exp in resume.experience
            )
            if not has_metrics and domain != "finance": # Finance already checked specifically
                suggestions.append(ImprovementSuggestion(
                    category="Quantify Impact",
                    priority=2,
                    suggestion="Add quantifiable metrics to your experience (e.g., 'Improved performance by 40%', 'Managed team of 10')",
                ))
            
            # Check for short bullets
            short_bullets = sum(1 for exp in resume.experience for b in exp.responsibilities if len(b.split()) < 5)
            if short_bullets > 2:
                suggestions.append(ImprovementSuggestion(
                    category="Detail",
                    priority=3,
                    suggestion="Expand on short bullet points to provide more context about your contributions.",
                ))
                
        # Priority 4: Partially matched skills need more evidence
        for skill in skill_results["partial_required"][:2]:
            suggestions.append(ImprovementSuggestion(
                category="Strengthen Evidence",
                priority=3,
                suggestion=f"Provide more concrete examples for '{skill}' in your experience section",
                affected_skills=[skill],
            ))
        
        # Priority 5: Missing optional skills
        for skill in skill_results["missing_optional"][:2]:
            suggestions.append(ImprovementSuggestion(
                category="Nice to Have",
                priority=4,
                suggestion=f"Consider adding '{skill}' if you have experience with it",
                affected_skills=[skill],
            ))
            
        return suggestions[:max_suggestions]
    
    def _detect_domain(self, jd: ParsedJobDescription) -> str:
        """Detect job domain from JD text/title."""
        # Handle potential None title
        title_text = jd.title if jd.title else ""
        text = (title_text + " " + jd.raw_text).lower()
        
        if any(w in text for w in ["nurse", "medical", "patient", "clinical", "healthcare", "doctor"]):
            return "healthcare"
        if any(w in text for w in ["financial", "finance", "accounting", "audit", "analyst", "investment"]):
            return "finance"
        if any(w in text for w in ["software", "developer", "engineer", "data", "full stack", "backend", "frontend"]):
            return "software_engineering"
        if any(w in text for w in ["marketing", "brand", "social media", "content", "campaign"]):
            return "marketing"
            
        return "general"


# Module-level convenience function
_engine_instance = None


def get_engine() -> RuleEngine:
    """Get singleton engine instance."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = RuleEngine()
    return _engine_instance


def evaluate(resume: ParsedResume, job_description: ParsedJobDescription) -> EvaluationResult:
    """Convenience function to evaluate resume."""
    return get_engine().evaluate(resume, job_description)
