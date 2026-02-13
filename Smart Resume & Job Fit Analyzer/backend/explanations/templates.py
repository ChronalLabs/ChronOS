"""
Explanation templates for rule-based generation.
No LLM usage - pure Python template assembly.
"""

# Main score explanation template
SCORE_EXPLANATION = """Your job-fit score is {score}/100.

This score reflects:
• {matched_count} skills fully matched ({matched_percentage:.0f}%)
• {partial_count} skills partially matched
• {missing_count} required skills not found

{score_breakdown}"""

# Score breakdown template
SCORE_BREAKDOWN = """Score Breakdown:
─────────────────────────────
Required Skills:    {required_score:>6.1f}% × {required_weight:.0%} = {required_contribution:>5.1f}
Preferred Skills:   {optional_score:>6.1f}% × {optional_weight:.0%} = {optional_contribution:>5.1f}
Experience Depth:   {experience_score:>6.1f}% × {experience_weight:.0%} = {experience_contribution:>5.1f}
Education Match:    {education_score:>6.1f}% × {education_weight:.0%} = {education_contribution:>5.1f}
─────────────────────────────
Subtotal:                              {subtotal:>5.1f}
Penalties Applied:                     {penalties:>5.1f}
─────────────────────────────
Final Score:                           {final_score:>5.0f}"""

# Skill match explanation
SKILL_MATCHED = "✓ {skill_name}: Found in your resume ({evidence})"
SKILL_PARTIAL = "◐ {skill_name}: Partially matched ({confidence} confidence)"
SKILL_MISSING = "✗ {skill_name}: Not found in your resume"

# Category headers
REQUIRED_SKILLS_HEADER = "\n🎯 Required Skills ({matched}/{total} matched)"
OPTIONAL_SKILLS_HEADER = "\n📌 Preferred Skills ({matched}/{total} matched)"

# Evidence snippet template
EVIDENCE_SNIPPET = '"{snippet}" (from {section})'

# Improvement suggestion templates
SUGGESTION_MISSING_SKILL = """Add "{skill}" to your resume
   → Include specific examples showing how you've used this skill
   → Mention projects or work where {skill} was essential"""

SUGGESTION_STRENGTHEN = """Strengthen your "{skill}" evidence
   → Your resume mentions this, but lacks specific examples
   → Add metrics or project details demonstrating expertise"""

SUGGESTION_ADD_METRICS = """Quantify your achievements
   → Use numbers to show impact (e.g., "reduced load time by 40%")
   → Include team sizes, user counts, or performance improvements"""

SUGGESTION_EXPERIENCE = """Expand your experience section
   → Add more detail about your responsibilities
   → Include technologies used and outcomes achieved"""

# Advisory notice (required on all results)
ADVISORY_NOTICE = """
───────────────────────────────────────────────────────────────────
⚠️ ADVISORY NOTICE
This analysis is for informational purposes only and should not be
used as the sole basis for hiring decisions. Actual job fit depends
on many factors not captured in this automated assessment.
───────────────────────────────────────────────────────────────────"""

# Score label explanations
SCORE_LABELS = {
    (85, 100): ("Excellent Match", "Your resume strongly aligns with this position."),
    (70, 85): ("Good Match", "Your resume shows good alignment with key requirements."),
    (55, 70): ("Fair Match", "Your resume covers some requirements but has gaps."),
    (0, 55): ("Needs Work", "Significant improvements needed to match this position."),
}


def get_score_label(score: int) -> tuple[str, str]:
    """Get the label and description for a score."""
    for (min_score, max_score), (label, desc) in SCORE_LABELS.items():
        if min_score <= score <= max_score:
            return label, desc
    return "Unknown", ""
