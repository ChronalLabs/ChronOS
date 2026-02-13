"""
Robustness Test Suite for Resume Section Detection
Tests 50 different resume format variations to ensure reliable parsing.
"""
import re

# Copied from section_detector.py to verify pattern logic in isolation
SECTION_PATTERNS = {
    "education": [
        r"education",
        r"academic\s*(background|history|qualifications|profile)?",
        r"degrees?",
        r"qualifications?",
        r"certifications?\s*(&|and)?\s*education",
        r"educational\s*background",
        r"education\s*(and|&)\s*academic",  # Added for "Education and Academic Qualifications"
    ],
    "experience": [
        r"(work\s*)?experience",
        r"employment(\s*history)?",
        r"professional\s*(experience|background|history)",
        r"work\s*history",
        r"career\s*(history|summary)",
        r"previous\s*(employment|positions?)",
        r"positions\s*held",
        r"recent\s*work",
    ],
    "skills": [
        r"skills?",
        r"technical\s*skills?",
        r"core\s*(competencies|skills?)",
        r"technologies?",
        r"expertise",
        r"proficiencies?",
        r"competencies",
        r"abilities",
    ],
    "projects": [
        r"projects?",
        r"personal\s*projects?",
        r"academic\s*projects?",
        r"portfolio",
        r"key\s*projects?",
    ]
}

def find_section_headers(text):
    """
    Find which section types are present in the text.
    Returns a set of section types found.
    """
    found_sections = set()
    
    for section_type, patterns in SECTION_PATTERNS.items():
        for pattern in patterns:
            # Relaxed pattern matching with many decorator styles:
            # - Leading: ---, ***, ===, ___, >>, •, [, (, unicode dashes, arrows
            # - Numbering: 1., I., (1), 01.
            # - Trailing: ---, :, etc.
            combined_pattern = (
                f"(?:^|\\n)\\s*"  # Start of line/text
                f"(?:[-–—*=_>•►▶→\\[\\(]+\\s*)?"  # Optional leading decoration (inc. arrows)
                f"(?:\\d+[\\.)\\-]?|[IVX]+\\.)?\\s*"  # Optional numbering
                f"{pattern}"  # The actual section pattern
                f"(?:\\s*[:\\-–—._\\]\\)]*)?\\s*"  # Optional trailing decoration
                f"(?:$|\\n|[|,])"  # End of line or separator
            )
            
            if re.search(combined_pattern, text, re.IGNORECASE):
                found_sections.add(section_type)
                break
    
    return found_sections

# ============================================================================
# 50 Test Cases covering various resume formats
# ============================================================================
TEST_CASES = [
    # --- Standard Formats (1-10) ---
    {"name": "1. Standard ALL CAPS", "text": "EDUCATION\nB.Tech\nEXPERIENCE\nGoogle\nSKILLS\nPython", "expected": {"education", "experience", "skills"}},
    {"name": "2. Title Case", "text": "Education\nMIT\nExperience\nMicrosoft\nSkills\nJava", "expected": {"education", "experience", "skills"}},
    {"name": "3. lowercase", "text": "education\nHarvard\nexperience\nAmazon\nskills\nC++", "expected": {"education", "experience", "skills"}},
    {"name": "4. With Colons", "text": "Education:\nStanford\nExperience:\nApple\nSkills:\nSwift", "expected": {"education", "experience", "skills"}},
    {"name": "5. Mixed Case", "text": "EDUCATION\nCaltech\nExperience\nTesla\nSKILLS\nMatlab", "expected": {"education", "experience", "skills"}},
    
    # --- Numbered Headers (6-15) ---
    {"name": "6. Arabic Numerals", "text": "1. Education\nPhD\n2. Experience\nNASA\n3. Skills\nPython", "expected": {"education", "experience", "skills"}},
    {"name": "7. Roman Numerals", "text": "I. Education\nBA\nII. Experience\nIBM\nIII. Skills\nSQL", "expected": {"education", "experience", "skills"}},
    {"name": "8. Parenthetical Numbers", "text": "(1) Education\nBS\n(2) Experience\nOracle", "expected": {"education", "experience"}},
    {"name": "9. Number with Dash", "text": "1- Education\nMS\n2- Work Experience\nSAP", "expected": {"education", "experience"}},
    {"name": "10. Double Digit Numbers", "text": "01. Education\n02. Professional Experience", "expected": {"education", "experience"}},
    
    # --- Decorated Headers (11-20) ---
    {"name": "11. Dash Decorated", "text": "--- Education ---\nMBA\n--- Experience ---\nDeloitte", "expected": {"education", "experience"}},
    {"name": "12. Asterisk Decorated", "text": "*** Education ***\nCPA\n*** Experience ***\nPwC", "expected": {"education", "experience"}},
    {"name": "13. Equal Sign Decorated", "text": "=== Education ===\nJD\n=== Experience ===\nLaw Firm", "expected": {"education", "experience"}},
    {"name": "14. Underscore Decorated", "text": "___ Education ___\nPhD\n___ Experience ___\nResearch", "expected": {"education", "experience"}},
    {"name": "15. Trailing Dashes Only", "text": "Education ------\nMD\nExperience ------\nHospital", "expected": {"education", "experience"}},
    {"name": "16. Leading Dashes Only", "text": "---- Education\nDDS\n---- Experience\nClinic", "expected": {"education", "experience"}},
    {"name": "17. Arrow Style", "text": ">> Education\nBS\n>> Experience\nStartup", "expected": {"education", "experience"}},
    {"name": "18. Bullet Points", "text": "• Education\nBA\n• Experience\nAgency", "expected": {"education", "experience"}},
    {"name": "19. Square Brackets", "text": "[Education]\nMS\n[Experience]\nLab", "expected": {"education", "experience"}},
    {"name": "20. Mixed Decoration", "text": "--- EDUCATION ---\nPhD\n*** EXPERIENCE ***\nUniversity", "expected": {"education", "experience"}},
    
    # --- Alternative Phrasing (21-35) ---
    {"name": "21. Academic Background", "text": "Academic Background\nHarvard MBA", "expected": {"education"}},
    {"name": "22. Academic Profile", "text": "Academic Profile\nOxford DPhil", "expected": {"education"}},
    {"name": "23. Educational Background", "text": "Educational Background\nStanford MS", "expected": {"education"}},
    {"name": "24. Qualifications", "text": "Qualifications\nCFA, CPA", "expected": {"education"}},
    {"name": "25. Work Experience", "text": "Work Experience\nGoogle Engineer", "expected": {"experience"}},
    {"name": "26. Professional Experience", "text": "Professional Experience\nMcKinsey Consultant", "expected": {"experience"}},
    {"name": "27. Employment History", "text": "Employment History\n5 years at Amazon", "expected": {"experience"}},
    {"name": "28. Work History", "text": "Work History\nFacebook PM", "expected": {"experience"}},
    {"name": "29. Career Summary", "text": "Career Summary\n10 years in tech", "expected": {"experience"}},
    {"name": "30. Positions Held", "text": "Positions Held\nCEO, CTO, VP", "expected": {"experience"}},
    {"name": "31. Technical Skills", "text": "Technical Skills\nPython, Java, C++", "expected": {"skills"}},
    {"name": "32. Core Competencies", "text": "Core Competencies\nLeadership, Strategy", "expected": {"skills"}},
    {"name": "33. Technologies", "text": "Technologies\nReact, Node, AWS", "expected": {"skills"}},
    {"name": "34. Expertise", "text": "Expertise\nMachine Learning, NLP", "expected": {"skills"}},
    {"name": "35. Proficiencies", "text": "Proficiencies\nExcel, PowerPoint", "expected": {"skills"}},
    
    # --- Messy Formatting (36-45) ---
    {"name": "36. Extra Whitespace", "text": "   EDUCATION   \n   MIT   \n   EXPERIENCE   \n   Google   ", "expected": {"education", "experience"}},
    {"name": "37. Multiple Newlines", "text": "\n\n\nEducation\n\n\nMIT\n\n\nExperience\n\n\nGoogle", "expected": {"education", "experience"}},
    {"name": "38. Tab Characters", "text": "\tEducation\t\n\tMIT\t\n\tExperience\t\n\tGoogle\t", "expected": {"education", "experience"}},
    {"name": "39. Mixed Whitespace", "text": " \t Education \t \nMIT\n \t Experience \t \nGoogle", "expected": {"education", "experience"}},
    {"name": "40. Inconsistent Casing", "text": "eDuCaTiOn\nMIT\neXpErIeNcE\nGoogle", "expected": {"education", "experience"}},
    {"name": "41. Leading Spaces Each Line", "text": "    Education\n    MIT\n    Experience\n    Google", "expected": {"education", "experience"}},
    {"name": "42. Unicode Dashes", "text": "– Education –\nMIT\n— Experience —\nGoogle", "expected": {"education", "experience"}},
    {"name": "43. Carriage Returns", "text": "Education\r\nMIT\r\nExperience\r\nGoogle", "expected": {"education", "experience"}},
    {"name": "44. Multiple Sections Same Line", "text": "Education: MIT | Experience: Google", "expected": {"education", "experience"}},
    {"name": "45. Very Long Header", "text": "Education and Academic Qualifications\nPhD from MIT", "expected": {"education"}},
    
    # --- Edge Cases (46-50) ---
    {"name": "46. Projects Section", "text": "Projects\nOpen Source Contributions\nPersonal Projects\nAI Chatbot", "expected": {"projects"}},
    {"name": "47. All Sections Present", "text": "Education\nMIT\nExperience\nGoogle\nSkills\nPython\nProjects\nAI Bot", "expected": {"education", "experience", "skills", "projects"}},
    {"name": "48. Minimal Resume", "text": "Skills: Python, Java", "expected": {"skills"}},
    {"name": "49. No Recognized Sections", "text": "John Doe\nSoftware Developer\njohn@email.com", "expected": set()},
    {"name": "50. Section in Sentence", "text": "I have 5 years of experience in software development.", "expected": set()},  # Should NOT match "experience" in sentence
]

def run_tests():
    """
    Run all robustness tests and report results.
    """
    print("=" * 80)
    print("ROBUSTNESS TEST SUITE - Resume Section Detection")
    print("=" * 80)
    print(f"{'#':<4} {'TEST CASE':<50} {'STATUS':<8} DETAILS")
    print("-" * 80)
    
    passed = 0
    failed = 0
    failed_cases = []
    
    for case in TEST_CASES:
        found = find_section_headers(case["text"])
        expected = case["expected"]
        
        # Check if found sections match expected
        missing = expected - found
        extra = found - expected
        
        if not missing and not extra:
            status = "PASS"
            passed += 1
            details = ""
        else:
            status = "FAIL"
            failed += 1
            details = ""
            if missing:
                details += f"Missing: {missing}"
            if extra:
                details += f" Extra: {extra}"
            failed_cases.append((case["name"], details))
        
        print(f"{case['name']:<54} {status:<8} {details}")
    
    print("-" * 80)
    print(f"\nSUMMARY: {passed}/{len(TEST_CASES)} tests passed ({passed/len(TEST_CASES)*100:.1f}%)")
    
    if failed_cases:
        print(f"\nFAILED CASES ({failed}):")
        for name, details in failed_cases:
            print(f"  - {name}: {details}")
    else:
        print("\n✅ All tests passed!")
    
    return passed, len(TEST_CASES)

if __name__ == "__main__":
    run_tests()
