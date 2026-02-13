"""
Improvement suggestion generator.
Creates actionable guidance based on evaluation gaps.
"""
from typing import list as List
from .templates import (
    SUGGESTION_MISSING_SKILL,
    SUGGESTION_STRENGTHEN,
    SUGGESTION_ADD_METRICS,
    SUGGESTION_EXPERIENCE,
)


def generate_suggestions(
    skill_matches: list,
    resume_analysis: dict = None,
    max_suggestions: int = 5,
) -> list[dict]:
    """
    Generate prioritized improvement suggestions.
    
    Args:
        skill_matches: List of SkillMatch objects from evaluation
        resume_analysis: Optional analysis of resume quality
        max_suggestions: Maximum number of suggestions to return
    
    Returns:
        List of suggestion dictionaries with priority, category, and text
    """
    suggestions = []
    
    # Priority 1: Missing required skills (highest priority)
    missing_required = [
        m for m in skill_matches 
        if m.match_type.value == "missing" and m.jd_priority.value == "required"
    ]
    
    for match in missing_required[:2]:  # Top 2 missing required skills
        suggestions.append({
            "priority": 1,
            "category": "Missing Required Skill",
            "skill": match.skill_name,
            "suggestion": SUGGESTION_MISSING_SKILL.format(skill=match.skill_name),
            "impact": "high",
        })
    
    # Priority 2: Partial matches that need strengthening
    partial_required = [
        m for m in skill_matches
        if m.match_type.value == "partial" and m.jd_priority.value == "required"
    ]
    
    for match in partial_required[:2]:
        suggestions.append({
            "priority": 2,
            "category": "Strengthen Evidence",
            "skill": match.skill_name,
            "suggestion": SUGGESTION_STRENGTHEN.format(skill=match.skill_name),
            "impact": "medium",
        })
    
    # Priority 3: General improvements based on resume analysis
    if resume_analysis:
        # Check if experience section needs work
        if not resume_analysis.get("has_experience", True):
            suggestions.append({
                "priority": 3,
                "category": "Experience Section",
                "suggestion": SUGGESTION_EXPERIENCE,
                "impact": "high",
            })
        
        # Check for lack of metrics
        if not resume_analysis.get("has_metrics", True):
            suggestions.append({
                "priority": 3,
                "category": "Quantify Impact",
                "suggestion": SUGGESTION_ADD_METRICS,
                "impact": "medium",
            })
    
    # Priority 4: Missing optional skills (nice to have)
    missing_optional = [
        m for m in skill_matches
        if m.match_type.value == "missing" and m.jd_priority.value == "optional"
    ]
    
    for match in missing_optional[:2]:
        suggestions.append({
            "priority": 4,
            "category": "Nice to Have",
            "skill": match.skill_name,
            "suggestion": f'Consider adding "{match.skill_name}" if you have experience with it.',
            "impact": "low",
        })
    
    # Sort by priority and limit
    suggestions.sort(key=lambda x: x["priority"])
    return suggestions[:max_suggestions]


def format_suggestions_text(suggestions: list[dict]) -> str:
    """
    Format suggestions into a readable text block.
    
    Args:
        suggestions: List of suggestion dictionaries
    
    Returns:
        Formatted text string
    """
    if not suggestions:
        return "No specific improvements suggested. Your resume aligns well with this position!"
    
    output = ["💡 Improvement Suggestions\n"]
    output.append("───────────────────────────────────────")
    
    for i, suggestion in enumerate(suggestions, 1):
        priority_icon = _get_priority_icon(suggestion["priority"])
        output.append(f"\n{i}. {priority_icon} {suggestion['category']}")
        output.append(f"   Impact: {suggestion.get('impact', 'medium').upper()}")
        output.append(f"\n   {suggestion['suggestion']}")
    
    output.append("\n───────────────────────────────────────")
    return "\n".join(output)


def _get_priority_icon(priority: int) -> str:
    """Get icon for priority level."""
    icons = {
        1: "🔴",  # Critical
        2: "🟠",  # High
        3: "🟡",  # Medium
        4: "🟢",  # Low/Nice to have
        5: "⚪",  # Optional
    }
    return icons.get(priority, "⚪")


def analyze_resume_quality(resume) -> dict:
    """
    Analyze resume for common quality issues.
    
    Args:
        resume: ParsedResume object
    
    Returns:
        Dictionary with quality metrics
    """
    import re
    
    analysis = {
        "has_experience": bool(resume.experience),
        "has_education": bool(resume.education),
        "has_skills": bool(resume.skills),
        "has_projects": bool(resume.projects),
        "has_metrics": False,
        "has_action_verbs": False,
        "experience_count": len(resume.experience),
        "skill_count": len(resume.skills),
    }
    
    # Check for metrics in experience descriptions
    metrics_pattern = r'\d+%|\d+x|\$\d+|\d+ (users|customers|requests|team)'
    
    for exp in resume.experience:
        all_text = exp.description + " ".join(exp.responsibilities)
        
        if re.search(metrics_pattern, all_text, re.IGNORECASE):
            analysis["has_metrics"] = True
        
        # Check for action verbs
        action_verbs = ["led", "developed", "built", "created", "managed", 
                       "implemented", "designed", "improved", "optimized"]
        if any(verb in all_text.lower() for verb in action_verbs):
            analysis["has_action_verbs"] = True
    
    return analysis
