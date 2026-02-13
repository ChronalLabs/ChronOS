"""
Quick test for resume parsing improvements
Tests skill extraction for the user's resume content
"""

import sys
sys.path.insert(0, ".")

# Test resume text - simulating Anurag's resume
TEST_RESUME = """
Anurag Mishra
Software Developer

CONTACT
Phone: +91 7000597872
Email: anuragmishra8835@gmail.com
Address: Gwalior, Madhya Pradesh, India
Linkedin: Anurag Mishra
Github: Anurag Mishra

PROFESSIONAL EXPERIENCE
IETE Students' Forum (On-Campus) | 2025-2026
Graphic Designer

- Designed posters and social media creatives for technical events, workshops, and hackathons, improving event visibility and student engagement.
- Collaborated with core team members to maintain a consistent visual identity across digital platforms and offline promotional materials.
- Supported branding and communication efforts for student-led technical initiatives, contributing to improved outreach and participation within the campus community.

EDUCATION
Madhav Institute of Technology and Science, Gwalior | 2024-2028
Bachelor of Technology - B.Tech, Computer Science & Design
- GPA: 8.09
- Working Member of the Graphic Team, IETE Students' FORUM (On Campus)
- Recognition for having successfully built a IoT Embedded Systems Kit.

Maharaja Public School, Bela Satna(M.P) | 2022-2023
Senior Secondary

SKILLS
Full Stack development
DSA in C++
Graphic Designer

CERTIFICATES
AWS APAC - Solutions Architecture Job Simulation
By Forage and AWS

Meta Frontend Development Course Certification
By Coursera
"""

def test_skill_extraction():
    """Test that skills are properly extracted"""
    from parsers.section_detector import _extract_skills_from_text
    
    print("=" * 60)
    print("SKILL EXTRACTION TEST")
    print("=" * 60)
    
    skills = _extract_skills_from_text(TEST_RESUME)
    
    print(f"\n[OK] Extracted {len(skills)} skills:")
    for skill in skills:
        print(f"  - {skill.canonical_name} ({skill.category.value})")
    
    # Check for expected skills
    expected = ["Full Stack Development", "C++", "Graphic Design", "IoT", "Embedded Systems", "AWS", "Coursera", "Forage"]
    found = [s.canonical_name for s in skills]
    
    print(f"\nExpected skills check:")
    for exp in expected:
        if exp in found:
            print(f"  [OK] {exp}")
        else:
            print(f"  [MISS] {exp} not found")
    
    return skills


def test_section_detection():
    """Test section detection"""
    from parsers.section_detector import detect_sections
    
    print("\n" + "=" * 60)
    print("SECTION DETECTION TEST")
    print("=" * 60)
    
    # Create mock blocks
    lines = TEST_RESUME.strip().split("\n")
    blocks = [{"text": line, "is_bold": False, "left": 0, "top": i*20} for i, line in enumerate(lines)]
    
    sections = detect_sections(TEST_RESUME, blocks)
    
    print(f"\n[>] Education entries: {len(sections.get('education', []))}")
    print(f"[>] Experience entries: {len(sections.get('experience', []))}")
    print(f"[>] Skills extracted: {len(sections.get('skills', []))}")
    print(f"[>] Certifications: {len(sections.get('certifications', []))}")
    
    # Show certifications if any
    if sections.get('certifications'):
        print("\nCertifications found:")
        for cert in sections['certifications']:
            print(f"  - {cert.name} ({cert.issuer})")
    
    return sections


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RESUME PARSING IMPROVEMENTS TEST")
    print("=" * 60)
    
    skills = test_skill_extraction()
    
    # Test ProjectEntry specifically
    try:
        from api.schemas import ProjectEntry
        print("Testing ProjectEntry...")
        p = ProjectEntry(name="Test", description="Desc", source_text="Src")
        print("ProjectEntry OK")
    except Exception as e:
        print(f"ProjectEntry FAILED: {e}")
        import traceback
        traceback.print_exc()

    sections = test_section_detection()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"[>] Total skills extracted: {len(skills)}")
    print(f"[>] Education: {len(sections.get('education', []))}")
    print(f"[>] Experience: {len(sections.get('experience', []))}")
    print(f"[>] Certifications: {len(sections.get('certifications', []))}")
    print("\n[DONE] Test complete")
