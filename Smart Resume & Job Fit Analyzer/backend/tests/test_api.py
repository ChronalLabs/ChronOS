"""
Comprehensive test script for Smart Resume Analyzer API.
Tests resume parsing, JD analysis, evaluation, and NLP functionality.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("=" * 50)
    print("Testing Health Endpoint...")
    resp = requests.get(f"{BASE_URL}/health")
    data = resp.json()
    print(f"Status: {data['status']}")
    print(f"Service: {data['service']}")
    print(f"spaCy Loaded: {data['spacy_loaded']}")
    assert data['status'] == 'healthy', "Health check failed!"
    assert data['spacy_loaded'] == True, "spaCy not loaded!"
    print("✅ Health check passed!")
    return True

def test_job_description_analysis():
    """Test JD parsing and skill extraction."""
    print("\n" + "=" * 50)
    print("Testing Job Description Analysis...")
    
    jd_text = """
    Senior Software Engineer
    
    We are looking for an experienced Software Engineer to join our team.
    
    Requirements:
    - 5+ years of experience with Python and JavaScript
    - Strong experience with React and Node.js
    - Experience with AWS, Docker, and Kubernetes
    - Familiarity with PostgreSQL and MongoDB
    - Experience with machine learning is a plus
    - Strong problem-solving and communication skills
    
    Nice to have:
    - Experience with TensorFlow or PyTorch
    - Knowledge of GraphQL and microservices
    - Experience with CI/CD pipelines
    """
    
    resp = requests.post(
        f"{BASE_URL}/api/analyze-jd",
        json={"job_description": jd_text}
    )
    
    assert resp.status_code == 200, f"JD analysis failed: {resp.text}"
    
    data = resp.json()
    session_id = data['session_id']
    parsed_jd = data['parsed_jd']
    
    print(f"Session ID: {session_id}")
    print(f"Required Skills: {parsed_jd['required_skills']}")
    print(f"Optional Skills: {parsed_jd['optional_skills']}")
    print(f"Requirements Count: {len(parsed_jd['requirements'])}")
    
    assert len(parsed_jd['required_skills']) > 0, "No required skills extracted!"
    print("✅ JD analysis passed!")
    
    return session_id, parsed_jd

def test_skill_extraction():
    """Test that skill extraction from text works."""
    print("\n" + "=" * 50)
    print("Testing Skill Extraction Logic...")
    
    # Import the skill extraction function directly
    import sys
    sys.path.insert(0, '.')
    from parsers.section_detector import _extract_skills_from_text
    
    test_text = """
    I have experience with Python, JavaScript, and TypeScript.
    Used React and Node.js for frontend and backend development.
    Deployed applications on AWS using Docker and Kubernetes.
    Worked with PostgreSQL, MongoDB, and Redis databases.
    Applied machine learning with TensorFlow and PyTorch.
    Familiar with Agile and Scrum methodologies.
    """
    
    skills = _extract_skills_from_text(test_text)
    skill_names = [s.canonical_name for s in skills]
    
    print(f"Extracted {len(skills)} skills:")
    for skill in skills:
        print(f"  - {skill.canonical_name} ({skill.category})")
    
    expected_skills = ["Python", "JavaScript", "TypeScript", "React", "Node.js", 
                       "AWS", "Docker", "Kubernetes", "PostgreSQL", "MongoDB", "Redis",
                       "TensorFlow", "PyTorch", "Agile", "Scrum"]
    
    found = [s for s in expected_skills if s in skill_names]
    print(f"\nFound {len(found)}/{len(expected_skills)} expected skills")
    
    assert len(found) >= 10, f"Too few skills extracted! Expected at least 10, got {len(found)}"
    print("✅ Skill extraction passed!")
    
    return True

def test_spacy_nlp():
    """Test spaCy NLP functionality."""
    print("\n" + "=" * 50)
    print("Testing spaCy NLP Functionality...")
    
    import sys
    sys.path.insert(0, '.')
    from ai_assist.semantic_analyzer import analyze_text
    
    test_text = """
    Led a team of 10 engineers to build a scalable microservices platform.
    Improved system performance by 40% through code optimization.
    Developed machine learning models for real-time fraud detection.
    """
    
    result = analyze_text(test_text)
    
    print(f"Entities found: {len(result.get('entities', []))}")
    print(f"Verb phrases: {result.get('verb_phrases', [])[:5]}")
    print(f"Technical terms: {result.get('technical_terms', [])[:5]}")
    print(f"Experience indicators: {result.get('experience_indicators', [])}")
    
    print("✅ spaCy NLP test passed!")
    return True

def test_evaluation_engine():
    """Test the rule engine directly."""
    print("\n" + "=" * 50)
    print("Testing Evaluation Engine...")
    
    import sys
    sys.path.insert(0, '.')
    from api.schemas import (
        ParsedResume, ParsedJobDescription, ExtractedSkill,
        JDRequirement, SkillCategory, ConfidenceLevel
    )
    from rules import evaluate
    
    # Create mock resume
    resume = ParsedResume(
        raw_text="Test resume with Python and React experience",
        education=[],
        experience=[],
        projects=[],
        skills=[
            ExtractedSkill(name="python", canonical_name="Python", 
                          category=SkillCategory.PROGRAMMING_LANGUAGES,
                          confidence=ConfidenceLevel.HIGH, source_text="python"),
            ExtractedSkill(name="react", canonical_name="React",
                          category=SkillCategory.FRAMEWORKS,
                          confidence=ConfidenceLevel.HIGH, source_text="react"),
            ExtractedSkill(name="aws", canonical_name="AWS",
                          category=SkillCategory.CLOUD,
                          confidence=ConfidenceLevel.HIGH, source_text="aws"),
        ],
        contact_info={},
        parsing_warnings=[],
    )
    
    # Create mock JD
    jd = ParsedJobDescription(
        raw_text="Looking for Python and React developer",
        requirements=[
            JDRequirement(text="Python required", skills=["Python"], priority="required"),
            JDRequirement(text="React experience", skills=["React"], priority="required"),
            JDRequirement(text="AWS preferred", skills=["AWS"], priority="optional"),
            JDRequirement(text="Docker preferred", skills=["Docker"], priority="optional"),
        ],
        required_skills=["Python", "React"],
        optional_skills=["AWS", "Docker"],
    )
    
    result = evaluate(resume, jd)
    
    print(f"Job Fit Score: {result.job_fit_score}/100")
    print(f"Matched Skills: {result.matched_count}")
    print(f"Missing Skills: {result.missing_count}")
    print(f"Score Breakdown:")
    print(f"  - Required Skills: {result.score_breakdown.required_skills_score:.1f}%")
    print(f"  - Optional Skills: {result.score_breakdown.optional_skills_score:.1f}%")
    print(f"Suggestions: {len(result.improvement_suggestions)}")
    
    assert result.job_fit_score > 0, "Score should be > 0"
    assert result.matched_count >= 2, "Should match at least Python and React"
    print("✅ Evaluation engine passed!")
    
    return result

def main():
    print("🔍 Smart Resume Analyzer - Comprehensive Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Test 1: Health check
    try:
        test_health()
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        all_passed = False
    
    # Test 2: JD Analysis
    try:
        session_id, parsed_jd = test_job_description_analysis()
    except Exception as e:
        print(f"❌ JD analysis failed: {e}")
        all_passed = False
    
    # Test 3: Skill extraction
    try:
        test_skill_extraction()
    except Exception as e:
        print(f"❌ Skill extraction failed: {e}")
        all_passed = False
    
    # Test 4: spaCy NLP
    try:
        test_spacy_nlp()
    except Exception as e:
        print(f"❌ spaCy NLP test failed: {e}")
        all_passed = False
    
    # Test 5: Evaluation engine
    try:
        test_evaluation_engine()
    except Exception as e:
        print(f"❌ Evaluation engine failed: {e}")
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  Some tests failed - see above for details")
    
    return all_passed

if __name__ == "__main__":
    main()
