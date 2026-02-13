"""
Explanation generator using templates.
Assembles human-readable explanations from evaluation data.
No LLM usage - pure Python template assembly.
"""
from typing import Optional
from .templates import (
    SCORE_EXPLANATION,
    SCORE_BREAKDOWN,
    SKILL_MATCHED,
    SKILL_PARTIAL,
    SKILL_MISSING,
    REQUIRED_SKILLS_HEADER,
    OPTIONAL_SKILLS_HEADER,
    EVIDENCE_SNIPPET,
    ADVISORY_NOTICE,
    get_score_label,
)


def generate_explanation(
    score: int,
    skill_matches: list,
    score_breakdown: dict,
    weights: dict,
) -> str:
    """
    Generate a complete explanation for evaluation results.
    
    Args:
        score: Final job-fit score (0-100)
        skill_matches: List of SkillMatch objects
        score_breakdown: Dictionary with component scores
        weights: Dictionary with score weights
    
    Returns:
        Formatted explanation string
    """
    # Count skills by category
    matched_required = sum(1 for m in skill_matches 
                          if m.match_type.value == "matched" and m.jd_priority.value == "required")
    matched_optional = sum(1 for m in skill_matches 
                          if m.match_type.value == "matched" and m.jd_priority.value == "optional")
    partial_count = sum(1 for m in skill_matches if m.match_type.value == "partial")
    missing_count = sum(1 for m in skill_matches if m.match_type.value == "missing")
    matched_count = matched_required + matched_optional
    
    # Calculate totals
    total_required = sum(1 for m in skill_matches if m.jd_priority.value == "required")
    total_optional = sum(1 for m in skill_matches if m.jd_priority.value == "optional")
    total_skills = total_required + total_optional
    
    matched_percentage = (matched_count / max(total_skills, 1)) * 100
    
    # Generate score breakdown
    breakdown_text = generate_score_breakdown(score, score_breakdown, weights)
    
    # Assemble main explanation
    explanation = SCORE_EXPLANATION.format(
        score=score,
        matched_count=matched_count,
        matched_percentage=matched_percentage,
        partial_count=partial_count,
        missing_count=missing_count,
        score_breakdown=breakdown_text,
    )
    
    # Add score label
    label, description = get_score_label(score)
    explanation += f"\n\n📊 Result: {label}\n{description}"
    
    # Add skill details
    explanation += generate_skill_details(skill_matches)
    
    # Add advisory notice
    explanation += ADVISORY_NOTICE
    
    return explanation


def generate_score_breakdown(score: int, breakdown: dict, weights: dict) -> str:
    """Generate the detailed score breakdown section."""
    required_score = breakdown.get("required_skills_score", 0)
    optional_score = breakdown.get("optional_skills_score", 0)
    experience_score = breakdown.get("experience_depth_score", 0)
    education_score = breakdown.get("education_match_score", 0)
    
    # Calculate contributions
    required_contribution = required_score * weights.get("required_skills", 0.4)
    optional_contribution = optional_score * weights.get("optional_skills", 0.2)
    experience_contribution = experience_score * weights.get("experience_depth", 0.25)
    education_contribution = education_score * weights.get("education_match", 0.15)
    
    subtotal = (required_contribution + optional_contribution + 
                experience_contribution + education_contribution)
    
    penalties = sum(
        float(p.split(":")[1].strip().split()[0])
        for p in breakdown.get("penalties_applied", [])
        if ":" in p
    ) if breakdown.get("penalties_applied") else 0
    
    return SCORE_BREAKDOWN.format(
        required_score=required_score,
        required_weight=weights.get("required_skills", 0.4),
        required_contribution=required_contribution,
        optional_score=optional_score,
        optional_weight=weights.get("optional_skills", 0.2),
        optional_contribution=optional_contribution,
        experience_score=experience_score,
        experience_weight=weights.get("experience_depth", 0.25),
        experience_contribution=experience_contribution,
        education_score=education_score,
        education_weight=weights.get("education_match", 0.15),
        education_contribution=education_contribution,
        subtotal=subtotal,
        penalties=penalties,
        final_score=score,
    )


def generate_skill_details(skill_matches: list) -> str:
    """Generate detailed skill matching section."""
    output = []
    
    # Separate by priority
    required = [m for m in skill_matches if m.jd_priority.value == "required"]
    optional = [m for m in skill_matches if m.jd_priority.value == "optional"]
    
    # Required skills section
    if required:
        matched = sum(1 for m in required if m.match_type.value == "matched")
        output.append(REQUIRED_SKILLS_HEADER.format(matched=matched, total=len(required)))
        
        for match in required:
            output.append(_format_skill_match(match))
    
    # Optional skills section
    if optional:
        matched = sum(1 for m in optional if m.match_type.value == "matched")
        output.append(OPTIONAL_SKILLS_HEADER.format(matched=matched, total=len(optional)))
        
        for match in optional:
            output.append(_format_skill_match(match))
    
    return "\n".join(output)


def _format_skill_match(match) -> str:
    """Format a single skill match for display."""
    if match.match_type.value == "matched":
        evidence = match.evidence[:50] + "..." if match.evidence and len(match.evidence) > 50 else match.evidence
        return SKILL_MATCHED.format(
            skill_name=match.skill_name,
            evidence=evidence or "found in resume",
        )
    elif match.match_type.value == "partial":
        return SKILL_PARTIAL.format(
            skill_name=match.skill_name,
            confidence=match.confidence.value,
        )
    else:
        return SKILL_MISSING.format(skill_name=match.skill_name)


def generate_evidence_section(matches: list) -> str:
    """Generate detailed evidence section for matched skills."""
    output = ["\n📝 Evidence from Your Resume\n"]
    
    matched_skills = [m for m in matches if m.match_type.value == "matched" and m.evidence]
    
    for match in matched_skills:
        output.append(f"\n{match.skill_name}:")
        output.append(EVIDENCE_SNIPPET.format(
            snippet=match.evidence[:100],
            section="your resume",
        ))
    
    if not matched_skills:
        output.append("No specific evidence snippets available.")
    
    return "\n".join(output)
