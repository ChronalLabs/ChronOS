"""
Skill matching logic.
Compares normalized skills from resume vs JD with evidence tracking.
"""
from typing import Optional
from taxonomy.normalizer import get_normalizer


def match_skills(
    resume_skills: list[dict],
    jd_required_skills: list[str],
    jd_optional_skills: list[str],
    full_match_threshold: float = 90.0,
    partial_match_threshold: float = 70.0,
) -> dict:
    """
    Match resume skills against job description requirements.
    
    Args:
        resume_skills: List of skills extracted from resume (with source_text)
        jd_required_skills: List of required skill names from JD
        jd_optional_skills: List of optional skill names from JD
        full_match_threshold: Score threshold for full match
        partial_match_threshold: Score threshold for partial match
    
    Returns:
        Dictionary with matched, partial, and missing skills with evidence
    """
    from api.schemas import SkillMatch, MatchType, ConfidenceLevel, SkillPriority
    
    normalizer = get_normalizer()
    results = {
        "matches": [],           # List of SkillMatch objects
        "matched_required": [],  # Required skills that were matched
        "matched_optional": [],  # Optional skills that were matched
        "partial_required": [],  # Required skills with partial matches
        "partial_optional": [],  # Optional skills with partial matches
        "missing_required": [],  # Required skills not found
        "missing_optional": [],  # Optional skills not found
        "stats": {
            "matched_count": 0,
            "partial_count": 0,
            "missing_count": 0,
            "required_matched": 0,
            "required_total": len(jd_required_skills),
            "optional_matched": 0,
            "optional_total": len(jd_optional_skills),
        },
    }
    
    # Normalize resume skills for lookup
    resume_skill_map = {}
    for skill in resume_skills:
        # Get canonical name
        name = skill.get("name") or skill.get("canonical_name", "")
        canonical, _, _ = normalizer.normalize(name)
        resume_skill_map[canonical.lower()] = skill
    
    # Match required skills
    for jd_skill in jd_required_skills:
        jd_canonical, _, _ = normalizer.normalize(jd_skill)
        match_result = _find_skill_match(
            jd_canonical,
            resume_skill_map,
            normalizer,
            full_match_threshold,
            partial_match_threshold,
        )
        
        if match_result["match_type"] == "full":
            skill_match = SkillMatch(
                skill_name=jd_skill,
                canonical_name=jd_canonical,
                match_type=MatchType.MATCHED,
                confidence=_score_to_confidence(match_result["score"]),
                jd_priority=SkillPriority.REQUIRED,
                evidence=match_result.get("evidence"),
                line_number=match_result.get("line_number"),
                match_score=match_result["score"] / 100.0,
            )
            results["matches"].append(skill_match)
            results["matched_required"].append(jd_skill)
            results["stats"]["matched_count"] += 1
            results["stats"]["required_matched"] += 1
            
        elif match_result["match_type"] == "partial":
            skill_match = SkillMatch(
                skill_name=jd_skill,
                canonical_name=jd_canonical,
                match_type=MatchType.PARTIAL,
                confidence=_score_to_confidence(match_result["score"]),
                jd_priority=SkillPriority.REQUIRED,
                evidence=match_result.get("evidence"),
                line_number=match_result.get("line_number"),
                match_score=match_result["score"] / 100.0,
            )
            results["matches"].append(skill_match)
            results["partial_required"].append(jd_skill)
            results["stats"]["partial_count"] += 1
            
        else:
            skill_match = SkillMatch(
                skill_name=jd_skill,
                canonical_name=jd_canonical,
                match_type=MatchType.MISSING,
                confidence=ConfidenceLevel.LOW,
                jd_priority=SkillPriority.REQUIRED,
                match_score=0.0,
            )
            results["matches"].append(skill_match)
            results["missing_required"].append(jd_skill)
            results["stats"]["missing_count"] += 1
    
    # Match optional skills
    for jd_skill in jd_optional_skills:
        jd_canonical, _, _ = normalizer.normalize(jd_skill)
        match_result = _find_skill_match(
            jd_canonical,
            resume_skill_map,
            normalizer,
            full_match_threshold,
            partial_match_threshold,
        )
        
        if match_result["match_type"] == "full":
            skill_match = SkillMatch(
                skill_name=jd_skill,
                canonical_name=jd_canonical,
                match_type=MatchType.MATCHED,
                confidence=_score_to_confidence(match_result["score"]),
                jd_priority=SkillPriority.OPTIONAL,
                evidence=match_result.get("evidence"),
                line_number=match_result.get("line_number"),
                match_score=match_result["score"] / 100.0,
            )
            results["matches"].append(skill_match)
            results["matched_optional"].append(jd_skill)
            results["stats"]["matched_count"] += 1
            results["stats"]["optional_matched"] += 1
            
        elif match_result["match_type"] == "partial":
            skill_match = SkillMatch(
                skill_name=jd_skill,
                canonical_name=jd_canonical,
                match_type=MatchType.PARTIAL,
                confidence=_score_to_confidence(match_result["score"]),
                jd_priority=SkillPriority.OPTIONAL,
                evidence=match_result.get("evidence"),
                line_number=match_result.get("line_number"),
                match_score=match_result["score"] / 100.0,
            )
            results["matches"].append(skill_match)
            results["partial_optional"].append(jd_skill)
            results["stats"]["partial_count"] += 1
            
        else:
            skill_match = SkillMatch(
                skill_name=jd_skill,
                canonical_name=jd_canonical,
                match_type=MatchType.MISSING,
                confidence=ConfidenceLevel.LOW,
                jd_priority=SkillPriority.OPTIONAL,
                match_score=0.0,
            )
            results["matches"].append(skill_match)
            results["missing_optional"].append(jd_skill)
            results["stats"]["missing_count"] += 1
    
    return results


def _find_skill_match(
    jd_canonical: str,
    resume_skill_map: dict,
    normalizer,
    full_threshold: float,
    partial_threshold: float,
) -> dict:
    """
    Find the best match for a JD skill in resume skills.
    """
    from rapidfuzz import fuzz
    
    jd_lower = jd_canonical.lower()
    
    # Check for exact match first
    if jd_lower in resume_skill_map:
        skill_data = resume_skill_map[jd_lower]
        return {
            "match_type": "full",
            "score": 100.0,
            "evidence": skill_data.get("source_text"),
            "line_number": skill_data.get("line_number"),
        }
    
    # Fuzzy match against all resume skills
    best_match = {"match_type": "none", "score": 0.0}
    
    for resume_canonical, skill_data in resume_skill_map.items():
        score = fuzz.ratio(jd_lower, resume_canonical)
        
        if score > best_match["score"]:
            best_match = {
                "score": score,
                "evidence": skill_data.get("source_text"),
                "line_number": skill_data.get("line_number"),
            }
            
            if score >= full_threshold:
                best_match["match_type"] = "full"
            elif score >= partial_threshold:
                best_match["match_type"] = "partial"
            else:
                best_match["match_type"] = "none"
    
    return best_match


def _score_to_confidence(score: float) -> "ConfidenceLevel":
    """Convert match score to confidence level."""
    from api.schemas import ConfidenceLevel
    
    if score >= 90:
        return ConfidenceLevel.HIGH
    elif score >= 70:
        return ConfidenceLevel.MEDIUM
    else:
        return ConfidenceLevel.LOW
