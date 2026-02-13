from exports.pdf_export import generate_pdf_report
from api.schemas import SessionData, EvaluationResult, ScoreBreakdown, SkillMatch, MatchType, ConfidenceLevel, SkillPriority, ImprovementSuggestion, SkillCategory
from datetime import datetime
import os

def test_pdf_generation():
    print("Testing PDF Generation...")
    
    # Mock data
    score_breakdown = ScoreBreakdown(
        required_skills_score=80.0,
        optional_skills_score=60.0,
        experience_depth_score=75.0,
        education_match_score=100.0,
    )
    
    skill_match = SkillMatch(
        skill_name="Python",
        canonical_name="Python",
        match_type=MatchType.MATCHED,
        confidence=ConfidenceLevel.HIGH,
        jd_priority=SkillPriority.REQUIRED,
        evidence="Used Python for 5 years",
        match_score=1.0,
    )
    
    missing_skill = SkillMatch(
        skill_name="Kubernetes",
        canonical_name="Kubernetes",
        match_type=MatchType.MISSING,
        confidence=ConfidenceLevel.LOW,
        jd_priority=SkillPriority.REQUIRED,
        match_score=0.0,
    )
    
    suggestion = ImprovementSuggestion(
        category="Skills",
        priority=1,
        suggestion="Learn Kubernetes",
        action_items=["Take a course", "Build a cluster"],
    )
    
    eval_result = EvaluationResult(
        job_fit_score=78,
        confidence_level=ConfidenceLevel.MEDIUM,
        score_breakdown=score_breakdown,
        skill_matches=[skill_match, missing_skill],
        explanation="Good fit but missing K8s",
        improvement_suggestions=[suggestion],
    )
    
    session = SessionData(
        session_id="test-session",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        evaluation=eval_result,
    )
    
    output_path = "test_report.pdf"
    generate_pdf_report(session, output_path)
    
    if os.path.exists(output_path):
        print(f"SUCCESS: PDF created at {output_path}")
    else:
        print("FAILURE: PDF not found")

if __name__ == "__main__":
    test_pdf_generation()
