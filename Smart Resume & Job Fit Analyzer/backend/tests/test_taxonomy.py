"""
Test the Skill Taxonomy Loading and Matching
Validates that all domain categories are properly loaded and can match skills
"""

import sys
sys.path.insert(0, ".")

from taxonomy.normalizer import SkillNormalizer, get_normalizer

def test_taxonomy_loading():
    """Test that the taxonomy loads all categories"""
    print("=" * 60)
    print("TAXONOMY LOADING TEST")
    print("=" * 60)
    
    normalizer = SkillNormalizer()
    taxonomy = normalizer.taxonomy
    categories = list(taxonomy.get("categories", {}).keys())
    
    print(f"\n[OK] Loaded {len(categories)} categories:")
    for cat in categories:
        skills_count = len(taxonomy["categories"][cat].get("canonical", []))
        print(f"  - {cat}: {skills_count} skills")
    
    # Expected new categories
    expected_categories = [
        "programming_languages", "frontend_frameworks", "backend_frameworks",
        "databases", "cloud_platforms", "devops_tools", "data_ml",
        "development_tools", "methodologies",
        # New domains
        "healthcare", "finance", "marketing", "design", "legal",
        "education", "sales", "human_resources", "engineering",
        "data_analytics", "soft_skills", "project_management"
    ]
    
    missing = [c for c in expected_categories if c not in categories]
    if missing:
        print(f"\n[WARN] Missing categories: {missing}")
    else:
        print(f"\n[OK] All {len(expected_categories)} expected categories present!")
    
    # Total skills count
    total_skills = len(normalizer.canonical_skills)
    print(f"\n[OK] Total canonical skills: {total_skills}")
    
    return taxonomy, normalizer


def test_skill_normalization(normalizer):
    """Test that aliases are properly normalized"""
    print("\n" + "=" * 60)
    print("SKILL NORMALIZATION TEST")
    print("=" * 60)
    
    test_cases = [
        # Tech
        ("py", "Python"),
        ("reactjs", "React"),
        ("k8s", "Kubernetes"),
        ("ml", "Machine Learning"),
        # Healthcare
        ("emr", "Electronic Medical Records"),
        ("cpr certified", "CPR Certified"),
        # Finance
        ("cfa", "CFA"),
        ("cpa", "CPA"),
        ("gaap", "GAAP"),
        # Marketing
        ("seo", "SEO"),
        ("ppc", "PPC"),
        # Design
        ("ux", "UX Design"),
        ("ui", "UI Design"),
        # Legal
        ("ip", "Intellectual Property"),
        ("gdpr", "GDPR"),
        # Education
        ("lms", "Learning Management Systems"),
        ("esl", "ESL"),
        # HR
        ("hris", "HRIS"),
        # Engineering
        ("cad", "CAD"),
        # Project Management
        ("pmp", "PMP"),
    ]
    
    passed = 0
    failed = 0
    
    for alias, expected in test_cases:
        result = normalizer.normalize(alias)
        canonical = result[0]
        confidence = result[1]
        if canonical.lower() == expected.lower():
            print(f"  [OK] '{alias}' -> '{canonical}' ({confidence})")
            passed += 1
        else:
            print(f"  [FAIL] '{alias}' -> '{canonical}' (expected: '{expected}')")
            failed += 1
    
    print(f"\n[RESULT] Passed: {passed}/{len(test_cases)}, Failed: {failed}")
    return passed, failed


def test_domain_skill_detection(normalizer):
    """Test that skills from different domains can be detected"""
    print("\n" + "=" * 60)
    print("DOMAIN SKILL DETECTION TEST")
    print("=" * 60)
    
    domain_samples = {
        "healthcare": ["Patient Care", "HIPAA Compliance", "Epic Systems", "Nursing"],
        "finance": ["Financial Analysis", "Bloomberg Terminal", "GAAP", "Auditing"],
        "marketing": ["SEO", "Google Analytics", "Content Marketing", "HubSpot"],
        "design": ["Figma", "Adobe Photoshop", "UX Design", "Wireframing"],
        "legal": ["Legal Research", "Contract Law", "Westlaw", "Compliance"],
        "education": ["Curriculum Development", "Lesson Planning", "Canvas"],
        "sales": ["Salesforce", "CRM", "Lead Generation", "B2B Sales"],
        "human_resources": ["Recruiting", "Onboarding", "Workday", "HRIS"],
        "engineering": ["SolidWorks", "AutoCAD", "Six Sigma"],
        "soft_skills": ["Leadership", "Communication", "Problem Solving"],
    }
    
    results = {}
    
    for domain, skills in domain_samples.items():
        detected = 0
        for skill in skills:
            category = normalizer.get_category(skill)
            if category:
                detected += 1
        
        pct = (detected / len(skills)) * 100
        results[domain] = pct
        status = "[OK]" if pct >= 60 else "[WARN]"
        print(f"  {status} {domain}: {detected}/{len(skills)} ({pct:.0f}%)")
    
    avg_detection = sum(results.values()) / len(results)
    print(f"\n[RESULT] Average detection rate: {avg_detection:.1f}%")
    
    return results


def test_sample_resume_skills(normalizer):
    """Test normalizing sample skills from different resume types"""
    print("\n" + "=" * 60)
    print("SAMPLE RESUME SKILLS TEST")
    print("=" * 60)
    
    # Sample skills from different domain resumes
    sample_skills = [
        # Tech
        "Python", "React", "AWS", "Docker", "Kubernetes",
        # Healthcare
        "Patient Care", "HIPAA", "Epic Systems",
        # Finance
        "Financial Analysis", "Excel", "Bloomberg",
        # Marketing
        "SEO", "Google Analytics", "Social Media Marketing",
        # Design
        "Figma", "UX Design", "Adobe Photoshop",
        # Legal
        "Contract Law", "Compliance", "Legal Research",
        # Soft Skills
        "Leadership", "Communication", "Project Management"
    ]
    
    results = normalizer.normalize_batch(sample_skills)
    
    high_conf = [r for r in results if r["confidence"] == "high"]
    med_conf = [r for r in results if r["confidence"] == "medium"]
    low_conf = [r for r in results if r["confidence"] == "low"]
    no_match = [r for r in results if r["confidence"] == "no_match"]
    
    print(f"  Total skills tested: {len(sample_skills)}")
    print(f"  [OK] High confidence: {len(high_conf)}")
    print(f"  [OK] Medium confidence: {len(med_conf)}")
    print(f"  [WARN] Low confidence: {len(low_conf)}")
    print(f"  [FAIL] No match: {len(no_match)}")
    
    if no_match:
        print(f"\n  Unmatched skills: {[r['original'] for r in no_match]}")
    
    return results


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("MULTI-DOMAIN SKILL TAXONOMY VALIDATION")
    print("=" * 60)
    
    # Run tests
    taxonomy, normalizer = test_taxonomy_loading()
    passed, failed = test_skill_normalization(normalizer)
    domain_results = test_domain_skill_detection(normalizer)
    skill_results = test_sample_resume_skills(normalizer)
    
    # Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"\n  Categories Loaded: {len(taxonomy.get('categories', {}))}")
    print(f"  Total Canonical Skills: {len(normalizer.canonical_skills)}")
    print(f"  Normalization Tests: {passed} passed, {failed} failed")
    print(f"  Avg Domain Detection: {sum(domain_results.values()) / len(domain_results):.1f}%")
    
    high_conf = len([r for r in skill_results if r["confidence"] == "high"])
    print(f"  Sample Skills High Confidence: {high_conf}/{len(skill_results)}")
    
    print("\n[DONE] Validation complete")
