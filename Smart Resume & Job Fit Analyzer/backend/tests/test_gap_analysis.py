import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from api.schemas import ParsedResume, ParsedJobDescription, ExperienceEntry, ExtractedSkill, SkillCategory, ConfidenceLevel
from rules.engine import get_engine, evaluate

def create_resume_for_finance(strong=False):
    resume = ParsedResume(
        raw_text="Finance Resume",
        contact_info={"email": "finance@example.com", "phone": "555-0101"},
        skills=[
            ExtractedSkill(name="Excel", canonical_name="Excel", category=SkillCategory.TOOLS, confidence=ConfidenceLevel.HIGH, source_text="Excel"),
        ],
        experience=[
            ExperienceEntry(
                company="Finance Corp",
                title="Financial Analyst",
                description="Analyst role.",
                responsibilities=[
                    "Forecasted quarterly budgets and audited financial statements." if strong else "Did some budgeting and checked numbers.",
                    "Improved profit margins by 15% through cost reduction." if strong else "Worked on profit margins.",
                ],
                source_text="..."
            )
        ]
    )
    return resume

def create_resume_for_healthcare(strong=False):
    resume = ParsedResume(
        raw_text="Healthcare Resume",
        contact_info={"email": "nurse@example.com", "phone": "555-0102"},
        skills=[
            ExtractedSkill(name="Patient Care", canonical_name="Patient Care", category=SkillCategory.HEALTHCARE, confidence=ConfidenceLevel.HIGH, source_text="Patient Care"),
        ],
        experience=[
            ExperienceEntry(
                company="General Hospital",
                title="Registered Nurse",
                description="Nursing role.",
                responsibilities=[
                    "Administered medication to 20+ patients daily and monitored vital signs." if strong else "gave medicine to patients.",
                    "Ensured HIPAA compliance in all patient documentation." if strong else "Followed rules.",
                ],
                source_text="..."
            )
        ]
    )
    return resume

def test_domain_specific_gaps():
    engine = get_engine()
    
    # JD for Finance
    jd_finance = ParsedJobDescription(
        raw_text="We need a Financial Analyst with budgeting experience.",
        required_skills=["Excel", "Financial Analysis"],
        title="Financial Analyst"
    )

    print("--- Test 3: Finance Domain Analysis ---")
    print("Weak Finance Resume:")
    res_weak_fin = create_resume_for_finance(strong=False)
    result_fin = engine.evaluate(res_weak_fin, jd_finance)
    for i, s in enumerate(result_fin.improvement_suggestions, 1):
        if s.category in ["Domain Gap", "Impact", "Quantify Impact"]:
            print(f"{i}. [{s.category}] {s.suggestion}")

    # JD for Healthcare
    jd_health = ParsedJobDescription(
        raw_text="Registered Nurse needed for patient care.",
        required_skills=["Patient Care", "BLS"],
        title="Registered Nurse"
    )

    print("\n--- Test 4: Healthcare Domain Analysis ---")
    print("Weak Healthcare Resume:")
    res_weak_health = create_resume_for_healthcare(strong=False)
    result_health = engine.evaluate(res_weak_health, jd_health)
    for i, s in enumerate(result_health.improvement_suggestions, 1):
        if s.category in ["Domain Gap", "Impact", "Quantify Impact"]:
            print(f"{i}. [{s.category}] {s.suggestion}")

if __name__ == "__main__":
    test_domain_specific_gaps()
