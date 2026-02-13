"""
Section detection for resume parsing.
Identifies Education, Experience, Projects, and Skills sections.
"""
import re
from typing import Any


# Section header patterns
SECTION_PATTERNS = {
    "education": [
        r"education",
        r"academic\s*(background|history|qualifications|profile)?",
        r"degrees?",
        r"qualifications?",
        r"certifications?\s*(&|and)?\s*education",
        r"educational\s*background",
        r"education\s*(and|&)\s*academic",  # "Education and Academic Qualifications"
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
    "projects": [
        r"projects?",
        r"personal\s*projects?",
        r"academic\s*projects?",
        r"portfolio",
        r"key\s*projects?",
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
    "certifications": [
        r"certifications?",
        r"certificates?",
        r"licenses?\s*(and|&)?\s*certifications?",
        r"professional\s*certifications?",
        r"credentials?",
        r"accreditations?",
    ],
    "contact": [
        r"contact(\s*info(rmation)?)?",
        r"personal\s*(info(rmation)?|details?)",
    ],
    "summary": [
        r"(professional\s*)?summary",
        r"(career\s*)?objective",
        r"profile",
        r"about\s*me",
    ],
}


def detect_sections(raw_text: str, text_blocks: list[dict]) -> dict[str, Any]:
    """
    Detect and extract resume sections.
    
    Args:
        raw_text: Full resume text
        text_blocks: Text blocks with positioning
    
    Returns:
        Dictionary with parsed sections
    """
    # Find section boundaries
    section_boundaries = _find_section_boundaries(text_blocks)
    
    # Extract content for each section
    sections = {
        "education": [],
        "experience": [],
        "projects": [],
        "skills": [],
        "certifications": [],
        "contact_info": {},
        "warnings": [],
    }
    
    # Process each detected section
    for section_type, (start_idx, end_idx) in section_boundaries.items():
        section_blocks = text_blocks[start_idx:end_idx]
        section_text = "\n".join(block["text"] for block in section_blocks)
        
        if section_type == "education":
            sections["education"] = _parse_education(section_text, section_blocks)
        elif section_type == "experience":
            sections["experience"] = _parse_experience(section_text, section_blocks)
        elif section_type == "projects":
            sections["projects"] = _parse_projects(section_text, section_blocks)
        elif section_type == "skills":
            sections["skills"] = _parse_skills(section_text, section_blocks)
        elif section_type == "certifications":
            sections["certifications"] = _parse_certifications(section_text, section_blocks)
        elif section_type == "contact":
            sections["contact_info"] = _parse_contact(section_text)
    
    # FALLBACK: If Experience or Education are empty, try extracting from raw_text directly
    # This handles two-column layouts where block boundaries are interleaved
    if not sections["experience"]:
        exp_text = _extract_section_from_raw_text(raw_text, "experience")
        if exp_text:
            sections["experience"] = _parse_experience(exp_text, [])
    
    if not sections["education"]:
        edu_text = _extract_section_from_raw_text(raw_text, "education")
        if edu_text:
            sections["education"] = _parse_education(edu_text, [])
    
    # ALWAYS extract skills from entire document (not just skills section)
    # This ensures we catch skills mentioned anywhere in the resume
    all_skills = _extract_skills_from_text(raw_text)
    
    # Merge with section-based skills (avoid duplicates)
    existing_skill_names = {s.canonical_name for s in sections["skills"]}
    for skill in all_skills:
        if skill.canonical_name not in existing_skill_names:
            sections["skills"].append(skill)
            existing_skill_names.add(skill.canonical_name)
    
    return sections


def _find_section_boundaries(text_blocks: list[dict]) -> dict[str, tuple[int, int]]:
    """
    Find the start and end indices of each section.
    Handles two-column layouts by detecting column structure.
    """
    if not text_blocks:
        return {}
    
    # Detect if this is a two-column layout
    left_positions = [block.get("left", 0) for block in text_blocks]
    if left_positions:
        avg_left = sum(left_positions) / len(left_positions)
        page_width_estimate = max(left_positions) + 100  # rough estimate
        
        # Check if blocks are distributed across two distinct columns
        left_column_blocks = [b for b in text_blocks if b.get("left", 0) < page_width_estimate * 0.4]
        right_column_blocks = [b for b in text_blocks if b.get("left", 0) >= page_width_estimate * 0.4]
        
        # If significant blocks in both columns, handle as two-column
        is_two_column = len(left_column_blocks) > 5 and len(right_column_blocks) > 5
    else:
        is_two_column = False
    
    section_starts = []
    
    for idx, block in enumerate(text_blocks):
        text = block["text"].lower().strip()
        
        # Check if this line is a section header
        for section_type, patterns in SECTION_PATTERNS.items():
            for pattern in patterns:
                # Relaxed pattern matching to handle:
                # 1. Numbering: "2. Experience" or "II. Experience"
                # 2. Decoration: "--- Experience ---" or "*** Work History ***"
                # 3. Colons: "Experience:"
                # 4. Unicode dashes (en-dash, em-dash)
                # 5. Square brackets, parentheses
                
                # Check for start of line with optional decoration, numbering, and trailing decoration
                combined_pattern = (
                    f"(?:^|\\n)\\s*"
                    f"(?:[-–—*=_<>►▶→•\\[\\(#]+\\s*)?"  # Include arrows, bullets, hash, and brackets
                    f"(?:\\d+[\\.)\\-]?|[IVX]+\\.)?\\s*"
                    f"{pattern}"
                    f"(?:\\s*[:\\-–—._\\]\\)*=_<>►▶→•#]*)?\\s*"
                    f"(?:$|\\n|[|,])"
                )
                
                # If exact match or very close match
                if re.search(combined_pattern, text, re.IGNORECASE):
                    # Guard against false positives in long text blocks (headers should be short)
                    if len(text) < 80:
                        # Store block index, section type, and column position
                        left_pos = block.get("left", 0)
                        section_starts.append((idx, section_type, left_pos))
                        break
    
    if not section_starts:
        return {}
    
    # Sort by index (which is already sorted by top, then left in PDF parser)
    section_starts.sort(key=lambda x: x[0])
    
    # For two-column layouts, calculate boundaries within same column
    boundaries = {}
    
    if is_two_column:
        # Group sections by column
        column_threshold = page_width_estimate * 0.4
        left_sections = [(idx, stype) for idx, stype, left in section_starts if left < column_threshold]
        right_sections = [(idx, stype) for idx, stype, left in section_starts if left >= column_threshold]
        
        # Process each column separately
        for column_sections in [left_sections, right_sections]:
            for i, (start_idx, section_type) in enumerate(column_sections):
                # Find the next section header in the SAME column
                if i + 1 < len(column_sections):
                    next_idx = column_sections[i + 1][0]
                else:
                    # End of column - find all blocks in same column after this section
                    start_left = text_blocks[start_idx].get("left", 0)
                    is_left_col = start_left < column_threshold
                    
                    # Find the last block in this column
                    next_idx = start_idx + 1
                    for j in range(start_idx + 1, len(text_blocks)):
                        block_left = text_blocks[j].get("left", 0)
                        block_in_same_col = (block_left < column_threshold) == is_left_col
                        if block_in_same_col:
                            next_idx = j + 1
                
                # Skip the header line itself
                if section_type not in boundaries:
                    boundaries[section_type] = (start_idx + 1, next_idx)
    else:
        # Standard single-column processing
        for i, (start_idx, section_type, _) in enumerate(section_starts):
            if i + 1 < len(section_starts):
                end_idx = section_starts[i + 1][0]
            else:
                end_idx = len(text_blocks)
            
            # Skip the header line itself
            boundaries[section_type] = (start_idx + 1, end_idx)
    
    return boundaries


def _extract_section_from_raw_text(raw_text: str, section_type: str) -> str:
    """
    Extract section content directly from raw text using regex.
    Fallback for when block-based detection fails (e.g., two-column layouts).
    
    Args:
        raw_text: Full resume text
        section_type: 'experience' or 'education'
    
    Returns:
        Extracted section text or empty string
    """
    # Section header patterns
    if section_type == "experience":
        header_patterns = [
            r"(?:^|\n)\s*(?:EXPERIENCE|WORK\s*EXPERIENCE|PROFESSIONAL\s*EXPERIENCE|EMPLOYMENT(?:\s*HISTORY)?|WORK\s*HISTORY|CAREER\s*HISTORY)",
        ]
        # Next section markers (end of experience section)
        next_section = r"(?:EDUCATION|SKILLS|PROJECTS|CERTIFICATIONS|AWARDS|REFERENCES|VOLUNTEER)"
    else:  # education
        header_patterns = [
            r"(?:^|\n)\s*(?:EDUCATION|ACADEMIC\s*(?:BACKGROUND|PROFILE)|QUALIFICATIONS|DEGREES?)",
        ]
        # Next section markers (end of education section) 
        next_section = r"(?:EXPERIENCE|SKILLS|PROJECTS|AWARDS|CERTIFICATIONS)"
    
    # Try to find section header
    for pattern in header_patterns:
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            start_pos = match.end()
            
            # Find the next section header
            next_match = re.search(rf"(?:^|\n)\s*{next_section}", raw_text[start_pos:], re.IGNORECASE)
            
            if next_match:
                end_pos = start_pos + next_match.start()
            else:
                # Take up to 2000 chars or end of text
                end_pos = min(start_pos + 2000, len(raw_text))
            
            section_text = raw_text[start_pos:end_pos].strip()
            
            # Only return if we got substantial content
            if len(section_text) > 50:
                return section_text
    
    return ""



def _parse_education(text: str, blocks: list[dict]) -> list:
    """Parse education entries."""
    from api.schemas import EducationEntry
    
    entries = []
    current_entry = None
    
    # Common patterns
    degree_patterns = [
        r"(bachelor|master|phd|doctorate|associate|b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?|b\.?tech|m\.?tech)",
    ]
    
    # If no blocks provided, create them from text lines
    if not blocks and text:
        blocks = [{"text": line.strip(), "is_bold": False} 
                  for line in text.split('\n') if line.strip()]
    
    for block in blocks:
        text = block["text"]
        
        # Check if this is a new entry (institution line)
        has_degree = any(re.search(p, text, re.IGNORECASE) for p in degree_patterns)
        
        if has_degree or _looks_like_institution(text):
            if current_entry:
                entries.append(current_entry)
            
            current_entry = EducationEntry(
                institution=_extract_institution(text),
                degree=_extract_degree(text),
                source_text=text,
            )
        elif current_entry:
            # Additional info for current entry
            if _looks_like_date(text):
                dates = _extract_dates(text)
                if dates:
                    current_entry.start_date = dates[0]
                    current_entry.end_date = dates[1] if len(dates) > 1 else None
            elif _looks_like_gpa(text):
                current_entry.gpa = _extract_gpa(text)
    
    if current_entry:
        entries.append(current_entry)
    
    return entries


def _parse_experience(text: str, blocks: list[dict]) -> list:
    """Parse work experience entries."""
    from api.schemas import ExperienceEntry
    
    entries = []
    current_entry = None
    
    # If no blocks provided, create them from text lines
    if not blocks and text:
        blocks = [{"text": line.strip(), "is_bold": False} 
                  for line in text.split('\n') if line.strip()]
    
    for block in blocks:
        text = block["text"]
        
        # Check if this is a new entry (company/title line)
        # Fix: Ensure bullet points don't trigger new entries even if they contain keywords
        is_bullet = text.strip().startswith(("-", "•", "▪", "○", "*"))
        is_likely_title = _looks_like_job_title(text) and not is_bullet
        
        # Additional safe-guard: Job titles are usually short or bold
        # If we already have an entry, be stricter about starting a new one
        if is_likely_title and (not current_entry or block.get("is_bold") or len(text) < 80):
            if current_entry:
                entries.append(current_entry)
            
            current_entry = ExperienceEntry(
                company=_extract_company(text),
                title=_extract_job_title(text),
                description="",
                source_text=text,
            )
        elif current_entry:
            # Additional content
            if _looks_like_date(text):
                dates = _extract_dates(text)
                if dates:
                    current_entry.start_date = dates[0]
                    current_entry.end_date = dates[1] if len(dates) > 1 else None
            elif text.strip().startswith(("-", "•", "▪", "○")):
                # Bullet point - responsibility
                clean_text = text.lstrip("-•▪○ ").strip()
                current_entry.responsibilities.append(clean_text)
                current_entry.description += f" {clean_text}"
    
    if current_entry:
        entries.append(current_entry)
    
    return entries


def _parse_projects(text: str, blocks: list[dict]) -> list:
    """Parse project entries."""
    from api.schemas import ProjectEntry
    
    entries = []
    current_entry = None
    
    for block in blocks:
        text = block["text"]
        is_bold = block.get("is_bold", False)
        
        # Project titles are often bold or followed by description
        if is_bold or (len(text) < 100 and not text.startswith(("-", "•"))):
            if current_entry:
                entries.append(current_entry)
            
            current_entry = ProjectEntry(
                name=text.strip(),
                description="",
                source_text=text,
            )
        elif current_entry:
            if text.strip().startswith(("-", "•", "▪")):
                clean_text = text.lstrip("-•▪ ").strip()
                current_entry.description += f" {clean_text}"
                # Extract technologies mentioned
                techs = _extract_technologies(clean_text)
                current_entry.technologies.extend(techs)
            else:
                current_entry.description += f" {text}"
    
    if current_entry:
        entries.append(current_entry)
    
    return entries


def _parse_certifications(text: str, blocks: list[dict]) -> list:
    """Parse certification entries."""
    from api.schemas import CertificationEntry
    
    entries = []
    
    # If no blocks provided, create them from text lines
    if not blocks and text:
        blocks = [{"text": line.strip(), "is_bold": False} 
                  for line in text.split('\n') if line.strip()]
    
    for block in blocks:
        text_line = block["text"]
        
        # Skip empty lines and header lines
        if not text_line.strip() or len(text_line.strip()) < 5:
            continue
        
        # Check for certification keywords
        cert_keywords = ["certification", "certificate", "certified", "by ", "from ", "coursera", "udemy", "linkedin learning", "aws", "google", "microsoft", "meta", "forage"]
        
        is_cert_line = any(kw in text_line.lower() for kw in cert_keywords)
        
        if is_cert_line or len(text_line) < 150:  # Certification lines are usually short
            # Extract certification name and issuer
            entry = CertificationEntry(
                name=_extract_cert_name(text_line),
                issuer=_extract_cert_issuer(text_line),
                source_text=text_line,
            )
            
            # Extract date if present
            dates = _extract_dates(text_line)
            if dates:
                entry.date = dates[0]
            
            entries.append(entry)
    
    return entries


def _extract_cert_name(text: str) -> str:
    """Extract certification name from text."""
    # Remove common issuer phrases
    issuer_phrases = [
        r"\s*by\s+\w+.*$",
        r"\s*from\s+\w+.*$",
        r"\s*-\s*\w+.*$",
        r"\s*\|\s*\w+.*$",
    ]
    
    name = text
    for pattern in issuer_phrases:
        name = re.sub(pattern, "", name, flags=re.IGNORECASE)
    
    return name.strip()


def _extract_cert_issuer(text: str) -> str:
    """Extract certification issuer from text."""
    # Common issuers
    issuers = ["AWS", "Google", "Microsoft", "Meta", "Coursera", "Udemy", "LinkedIn Learning", "Forage", "IBM", "Oracle", "Cisco"]
    
    text_lower = text.lower()
    for issuer in issuers:
        if issuer.lower() in text_lower:
            return issuer
    
    # Check for "by X" or "from X" pattern
    match = re.search(r"(?:by|from)\s+([A-Za-z\s]+?)(?:\s*[\|\-]|\s*$)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    return ""


def _parse_skills(text: str, blocks: list[dict]) -> list:
    """Parse skills from a dedicated skills section."""
    return _extract_skills_from_text(text)


def _extract_skills_from_text(text: str) -> list:
    """Extract skills from any text using pattern matching."""
    from api.schemas import ExtractedSkill, SkillCategory, ConfidenceLevel
    
    skills = []
    
    # Common technology keywords - expanded list
    tech_patterns = [
        # Programming Languages
        (r"\bpython\b", "Python", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bjavascript\b|\bjs\b", "JavaScript", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\btypescript\b|\bts\b", "TypeScript", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bjava\b", "Java", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bc\+\+\b|cpp\b", "C++", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bc#\b|csharp\b", "C#", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\b(?<!en)go\b|\bgolang\b", "Go", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\brust\b", "Rust", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bruby\b", "Ruby", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bphp\b", "PHP", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bswift\b", "Swift", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bkotlin\b", "Kotlin", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bscala\b", "Scala", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\br\b(?=\s|,|\.)", "R", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bmatlab\b", "MATLAB", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bsql\b", "SQL", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bhtml\b", "HTML", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bcss\b", "CSS", SkillCategory.PROGRAMMING_LANGUAGES),
        (r"\bshell\b|\bbash\b", "Bash", SkillCategory.PROGRAMMING_LANGUAGES),
        
        # Frameworks - Web
        (r"\breact\b|\breactjs\b|react\.js\b", "React", SkillCategory.FRAMEWORKS),
        (r"\bangular\b", "Angular", SkillCategory.FRAMEWORKS),
        (r"\bvue\b|\bvuejs\b|vue\.js\b", "Vue.js", SkillCategory.FRAMEWORKS),
        (r"\bnode\b|\bnodejs\b|node\.js\b", "Node.js", SkillCategory.FRAMEWORKS),
        (r"\bexpress\b|express\.js\b", "Express.js", SkillCategory.FRAMEWORKS),
        (r"\bdjango\b", "Django", SkillCategory.FRAMEWORKS),
        (r"\bflask\b", "Flask", SkillCategory.FRAMEWORKS),
        (r"\bfastapi\b", "FastAPI", SkillCategory.FRAMEWORKS),
        (r"\bspring\s?boot\b|\bspring\b", "Spring Boot", SkillCategory.FRAMEWORKS),
        (r"\bnext\.?js\b", "Next.js", SkillCategory.FRAMEWORKS),
        (r"\btailwind\b", "Tailwind CSS", SkillCategory.FRAMEWORKS),
        (r"\bbootstrap\b", "Bootstrap", SkillCategory.FRAMEWORKS),
        (r"\bjquery\b", "jQuery", SkillCategory.FRAMEWORKS),
        (r"\brails\b|ruby on rails\b", "Ruby on Rails", SkillCategory.FRAMEWORKS),
        (r"\blasp\.?net\b|\.net\b", ".NET", SkillCategory.FRAMEWORKS),
        
        # ML/AI Frameworks
        (r"\btensorflow\b", "TensorFlow", SkillCategory.FRAMEWORKS),
        (r"\bpytorch\b", "PyTorch", SkillCategory.FRAMEWORKS),
        (r"\bkeras\b", "Keras", SkillCategory.FRAMEWORKS),
        (r"\bscikit-?learn\b|sklearn\b", "Scikit-learn", SkillCategory.FRAMEWORKS),
        (r"\bpandas\b", "Pandas", SkillCategory.FRAMEWORKS),
        (r"\bnumpy\b", "NumPy", SkillCategory.FRAMEWORKS),
        (r"\bopencv\b", "OpenCV", SkillCategory.FRAMEWORKS),
        (r"\bhugging\s?face\b", "Hugging Face", SkillCategory.FRAMEWORKS),
        
        # Databases
        (r"\bpostgres(?:ql)?\b", "PostgreSQL", SkillCategory.DATABASES),
        (r"\bmysql\b", "MySQL", SkillCategory.DATABASES),
        (r"\bmongodb\b|\bmongo\b", "MongoDB", SkillCategory.DATABASES),
        (r"\bredis\b", "Redis", SkillCategory.DATABASES),
        (r"\bsqlite\b", "SQLite", SkillCategory.DATABASES),
        (r"\boracle\b", "Oracle", SkillCategory.DATABASES),
        (r"\bsql server\b|mssql\b", "SQL Server", SkillCategory.DATABASES),
        (r"\bdynamodb\b", "DynamoDB", SkillCategory.DATABASES),
        (r"\bcassandra\b", "Cassandra", SkillCategory.DATABASES),
        (r"\belasticsearch\b", "Elasticsearch", SkillCategory.DATABASES),
        (r"\bfirebase\b", "Firebase", SkillCategory.DATABASES),
        
        # Cloud & DevOps
        (r"\baws\b|amazon web services\b", "AWS", SkillCategory.CLOUD),
        (r"\bgcp\b|google cloud\b", "Google Cloud", SkillCategory.CLOUD),
        (r"\bazure\b|microsoft azure\b", "Azure", SkillCategory.CLOUD),
        (r"\bdocker\b", "Docker", SkillCategory.TOOLS),
        (r"\bkubernetes\b|\bk8s\b", "Kubernetes", SkillCategory.TOOLS),
        (r"\bgit\b(?!hub)", "Git", SkillCategory.TOOLS),
        (r"\bgithub\b", "GitHub", SkillCategory.TOOLS),
        (r"\bgitlab\b", "GitLab", SkillCategory.TOOLS),
        (r"\bjenkins\b", "Jenkins", SkillCategory.TOOLS),
        (r"\bci/?cd\b", "CI/CD", SkillCategory.TOOLS),
        (r"\bterraform\b", "Terraform", SkillCategory.TOOLS),
        (r"\bansible\b", "Ansible", SkillCategory.TOOLS),
        (r"\blinux\b", "Linux", SkillCategory.TOOLS),
        (r"\bnginx\b", "Nginx", SkillCategory.TOOLS),
        (r"\bapache\b", "Apache", SkillCategory.TOOLS),
        (r"\bjira\b", "Jira", SkillCategory.TOOLS),
        (r"\bconfluence\b", "Confluence", SkillCategory.TOOLS),
        (r"\bfigma\b", "Figma", SkillCategory.TOOLS),
        (r"\bpostman\b", "Postman", SkillCategory.TOOLS),
        
        # Soft Skills
        (r"\bcommunication\b", "Communication", SkillCategory.SOFT_SKILLS),
        (r"\bleadership\b", "Leadership", SkillCategory.SOFT_SKILLS),
        (r"\bteamwork\b|team\s*work\b", "Teamwork", SkillCategory.SOFT_SKILLS),
        (r"\bproblem[- ]?solving\b", "Problem Solving", SkillCategory.SOFT_SKILLS),
        (r"\bagile\b", "Agile", SkillCategory.SOFT_SKILLS),
        (r"\bscrum\b", "Scrum", SkillCategory.SOFT_SKILLS),
        (r"\badaptability\b", "Adaptability", SkillCategory.SOFT_SKILLS),
        (r"\bcollaboration\b", "Collaboration", SkillCategory.SOFT_SKILLS),
        (r"\btime[- ]?management\b", "Time Management", SkillCategory.SOFT_SKILLS),
        (r"\bcritical[- ]?thinking\b", "Critical Thinking", SkillCategory.SOFT_SKILLS),
        (r"\bwork[- ]?ethic\b|strong work ethic\b", "Strong Work Ethic", SkillCategory.SOFT_SKILLS),
        (r"\battention[- ]?to[- ]?detail\b", "Attention to Detail", SkillCategory.SOFT_SKILLS),
        (r"\bproject[- ]?management\b", "Project Management", SkillCategory.SOFT_SKILLS),
        (r"\bcustomer[- ]?service\b", "Customer Service", SkillCategory.SOFT_SKILLS),
        (r"\borganization\b|organizational\b", "Organization", SkillCategory.SOFT_SKILLS),
        (r"\bpresentation\b", "Presentation", SkillCategory.SOFT_SKILLS),
        (r"\bmultitasking\b|multi-tasking\b", "Multitasking", SkillCategory.SOFT_SKILLS),
        (r"\bhandling[- ]?pressure\b", "Handling Pressure", SkillCategory.SOFT_SKILLS),
        (r"\binterpersonal\b", "Interpersonal Skills", SkillCategory.SOFT_SKILLS),
        (r"\bconflict[- ]?resolution\b", "Conflict Resolution", SkillCategory.SOFT_SKILLS),
        (r"\bnegotiation\b", "Negotiation", SkillCategory.SOFT_SKILLS),
        (r"\bcoaching\b|mentoring\b", "Coaching/Mentoring", SkillCategory.SOFT_SKILLS),
        
        # Business Tools (common in administrative roles)
        (r"\bmicrosoft\s*excel\b|\bexcel\b", "Microsoft Excel", SkillCategory.TOOLS),
        (r"\bmicrosoft\s*word\b|\bword\b", "Microsoft Word", SkillCategory.TOOLS),
        (r"\bmicrosoft\s*powerpoint\b|\bpowerpoint\b", "Microsoft PowerPoint", SkillCategory.TOOLS),
        (r"\bmicrosoft\s*office\b|\bms\s*office\b", "Microsoft Office", SkillCategory.TOOLS),
        (r"\boutlook\b", "Outlook", SkillCategory.TOOLS),
        (r"\bsalesforce\b", "Salesforce", SkillCategory.TOOLS),
        (r"\bsap\b", "SAP", SkillCategory.TOOLS),
        (r"\btableau\b", "Tableau", SkillCategory.TOOLS),
        (r"\bpower\s*bi\b", "Power BI", SkillCategory.TOOLS),
        
        # Other
        (r"\brest\s*api\b|\brestful\b", "REST API", SkillCategory.OTHER),
        (r"\bgraphql\b", "GraphQL", SkillCategory.OTHER),
        (r"\bmicroservices\b", "Microservices", SkillCategory.OTHER),
        (r"\bmachine\s*learning\b|\bml\b", "Machine Learning", SkillCategory.OTHER),
        (r"\bdeep\s*learning\b|\bdl\b", "Deep Learning", SkillCategory.OTHER),
        (r"\bdata\s*science\b", "Data Science", SkillCategory.OTHER),
        (r"\bnlp\b|natural language processing\b", "NLP", SkillCategory.OTHER),
        (r"\bcomputer vision\b", "Computer Vision", SkillCategory.OTHER),
        
        # Full Stack & Development Roles
        (r"\bfull\s*stack\b|fullstack\b", "Full Stack Development", SkillCategory.OTHER),
        (r"\bfront\s*end\b|frontend\b", "Frontend Development", SkillCategory.OTHER),
        (r"\bback\s*end\b|backend\b", "Backend Development", SkillCategory.OTHER),
        (r"\bweb\s*development\b|web\s*dev\b", "Web Development", SkillCategory.OTHER),
        (r"\bmobile\s*development\b|mobile\s*dev\b|app\s*development\b", "Mobile Development", SkillCategory.OTHER),
        (r"\bsoftware\s*development\b|software\s*dev\b", "Software Development", SkillCategory.OTHER),
        
        # Data Structures & Algorithms  
        (r"\bdsa\b|data\s*structures?\s*(and|&)?\s*algorithms?\b", "Data Structures & Algorithms", SkillCategory.OTHER),
        (r"\balgorithms?\b", "Algorithms", SkillCategory.OTHER),
        (r"\bdata\s*structures?\b", "Data Structures", SkillCategory.OTHER),
        (r"\boops?\b|object\s*oriented\s*programming\b", "Object-Oriented Programming", SkillCategory.OTHER),
        (r"\boop\s*concepts?\b", "OOP Concepts", SkillCategory.OTHER),
        
        # Design Skills
        (r"\bgraphic\s*design(er|ing)?\b", "Graphic Design", SkillCategory.TOOLS),
        (r"\bui\s*/?ux\b|ux\s*/?ui\b", "UI/UX Design", SkillCategory.TOOLS),
        (r"\buser\s*experience\b", "User Experience", SkillCategory.TOOLS),
        (r"\buser\s*interface\b", "User Interface", SkillCategory.TOOLS),
        (r"\bvisual\s*design\b", "Visual Design", SkillCategory.TOOLS),
        (r"\bweb\s*design\b", "Web Design", SkillCategory.TOOLS),
        (r"\badobe\s*photoshop\b|photoshop\b", "Adobe Photoshop", SkillCategory.TOOLS),
        (r"\badobe\s*illustrator\b|illustrator\b", "Adobe Illustrator", SkillCategory.TOOLS),
        (r"\badobe\s*xd\b", "Adobe XD", SkillCategory.TOOLS),
        (r"\bcanva\b", "Canva", SkillCategory.TOOLS),
        (r"\bsketch\b", "Sketch", SkillCategory.TOOLS),
        (r"\binvision\b", "InVision", SkillCategory.TOOLS),
        
        # IoT & Embedded Systems
        (r"\biot\b|internet\s*of\s*things\b", "IoT", SkillCategory.OTHER),
        (r"\bembedded\s*systems?\b", "Embedded Systems", SkillCategory.OTHER),
        (r"\barduino\b", "Arduino", SkillCategory.TOOLS),
        (r"\braspberry\s*pi\b", "Raspberry Pi", SkillCategory.TOOLS),
        (r"\bmicrocontrollers?\b", "Microcontrollers", SkillCategory.OTHER),
        (r"\bhardware\b", "Hardware", SkillCategory.OTHER),
        (r"\bfirmware\b", "Firmware", SkillCategory.OTHER),
        (r"\bpcb\s*design\b", "PCB Design", SkillCategory.TOOLS),
        
        # Social Media & Content
        (r"\bsocial\s*media\b", "Social Media", SkillCategory.TOOLS),
        (r"\bcontent\s*creation\b|content\s*creator\b", "Content Creation", SkillCategory.OTHER),
        (r"\bvideo\s*editing\b", "Video Editing", SkillCategory.TOOLS),
        (r"\bpremiere\s*pro\b", "Adobe Premiere Pro", SkillCategory.TOOLS),
        (r"\bafter\s*effects\b", "Adobe After Effects", SkillCategory.TOOLS),
        (r"\bfinal\s*cut\b", "Final Cut Pro", SkillCategory.TOOLS),
        
        # Certifications/Platforms (for detection purposes)
        (r"\bcoursera\b", "Coursera", SkillCategory.OTHER),
        (r"\budemy\b", "Udemy", SkillCategory.OTHER),
        (r"\bedx\b", "edX", SkillCategory.OTHER),
        (r"\bforage\b", "Forage", SkillCategory.OTHER),
        (r"\blinkedin\s*learning\b", "LinkedIn Learning", SkillCategory.OTHER),
        
        # Healthcare & Medical
        (r"\bpatient\s*care\b", "Patient Care", SkillCategory.HEALTHCARE),
        (r"\bvital\s*signs\b", "Vital Signs", SkillCategory.HEALTHCARE),
        (r"\bphlebotomy\b", "Phlebotomy", SkillCategory.HEALTHCARE),
        (r"\bemr\b|electronic\s*medical\s*records?\b", "EMR", SkillCategory.TOOLS),
        (r"\behr\b|electronic\s*health\s*records?\b", "EHR", SkillCategory.TOOLS),
        (r"\bhipaa\b", "HIPAA", SkillCategory.HEALTHCARE),
        (r"\bbls\b|basic\s*life\s*support\b", "BLS", SkillCategory.CERTIFICATIONS),
        (r"\bacls\b|advanced\s*cardiac\s*life\s*support\b", "ACLS", SkillCategory.CERTIFICATIONS),
        (r"\bcpr\b", "CPR", SkillCategory.CERTIFICATIONS),
        (r"\btriage\b", "Triage", SkillCategory.HEALTHCARE),
        (r"\bmedication\s*administration\b", "Medication Administration", SkillCategory.HEALTHCARE),
        (r"\bclinical\s*documentation\b", "Clinical Documentation", SkillCategory.HEALTHCARE),
        (r"\bmedical\s*billing\b", "Medical Billing", SkillCategory.HEALTHCARE),
        (r"\bicd[- ]?10\b", "ICD-10", SkillCategory.HEALTHCARE),
        (r"\bepic\b", "Epic", SkillCategory.TOOLS),
        (r"\bcerner\b", "Cerner", SkillCategory.TOOLS),
        (r"\bmeditech\b", "Meditech", SkillCategory.TOOLS),
        (r"\bnursing\b", "Nursing", SkillCategory.HEALTHCARE),
        (r"\banatomy\b", "Anatomy", SkillCategory.HEALTHCARE),
        (r"\bphysiology\b", "Physiology", SkillCategory.HEALTHCARE),
    ]
    
    text_lower = text.lower()
    seen = set()
    
    for pattern, canonical, category in tech_patterns:
        matches = re.finditer(pattern, text_lower)
        for match in matches:
            if canonical not in seen:
                seen.add(canonical)
                # Find the original text context
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                skills.append(ExtractedSkill(
                    name=match.group(),
                    canonical_name=canonical,
                    category=category,
                    confidence=ConfidenceLevel.HIGH,
                    source_text=context,
                ))
    
    return skills


def _parse_contact(text: str) -> dict:
    """Extract contact information."""
    contact = {}
    
    # Email pattern
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    if email_match:
        contact["email"] = email_match.group()
    
    # Phone pattern
    phone_match = re.search(r"[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}", text)
    if phone_match:
        contact["phone"] = phone_match.group()
    
    # LinkedIn
    linkedin_match = re.search(r"linkedin\.com/in/[\w-]+", text, re.IGNORECASE)
    if linkedin_match:
        contact["linkedin"] = linkedin_match.group()
    
    # GitHub
    github_match = re.search(r"github\.com/[\w-]+", text, re.IGNORECASE)
    if github_match:
        contact["github"] = github_match.group()
    
    return contact


# Helper functions
def _looks_like_institution(text: str) -> bool:
    """Check if text looks like an institution name."""
    keywords = ["university", "college", "institute", "school"]
    return any(k in text.lower() for k in keywords)


def _looks_like_date(text: str) -> bool:
    """Check if text contains date patterns."""
    date_patterns = [
        r"\d{4}",  # Year
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)",
        r"(present|current)",
    ]
    return any(re.search(p, text.lower()) for p in date_patterns)


def _looks_like_gpa(text: str) -> bool:
    """Check if text contains GPA."""
    return bool(re.search(r"(gpa|cgpa|grade)", text.lower()))


def _looks_like_job_title(text: str) -> bool:
    """Check if text looks like a job title."""
    title_keywords = [
        "engineer", "developer", "manager", "analyst", "designer",
        "architect", "lead", "senior", "junior", "intern", "director",
        "consultant", "specialist", "administrator", "coordinator", "officer",
        "executive", "assistant", "associate", "founder", "ceo", "cto",
        "scientist", "researcher", "student", "representative", "agent",
        "technician", "supervisor", "head", "vp", "president", "principal", 
        "freelancer", "contractor"
    ]
    return any(k in text.lower() for k in title_keywords)


def _extract_institution(text: str) -> str:
    """Extract institution name from text."""
    # Simple extraction - take the main portion
    parts = re.split(r"[,|–-]", text)
    for part in parts:
        if _looks_like_institution(part):
            return part.strip()
    return parts[0].strip() if parts else text


def _extract_degree(text: str) -> str:
    """Extract degree from text."""
    degree_map = {
        r"bachelor": "Bachelor's",
        r"master": "Master's",
        r"phd|doctorate": "PhD",
        r"b\.?s\.?": "B.S.",
        r"m\.?s\.?": "M.S.",
        r"b\.?a\.?": "B.A.",
        r"m\.?a\.?": "M.A.",
        r"b\.?tech": "B.Tech",
        r"m\.?tech": "M.Tech",
    }
    
    for pattern, degree in degree_map.items():
        if re.search(pattern, text, re.IGNORECASE):
            return degree
    return "Degree"


def _extract_dates(text: str) -> list[str]:
    """Extract dates from text."""
    dates = []
    
    # Year patterns
    years = re.findall(r"(20\d{2}|19\d{2})", text)
    dates.extend(years)
    
    # Check for "Present" or "Current"
    if re.search(r"(present|current)", text, re.IGNORECASE):
        dates.append("Present")
    
    return dates[:2]  # Return at most start and end


def _extract_gpa(text: str) -> str:
    """Extract GPA value."""
    gpa_match = re.search(r"(\d+\.?\d*)\s*/?\s*(\d+\.?\d*)?", text)
    if gpa_match:
        return gpa_match.group(0)
    return ""


def _extract_company(text: str) -> str:
    """Extract company name from text."""
    parts = re.split(r"[,|–-]", text)
    return parts[0].strip()


def _extract_job_title(text: str) -> str:
    """Extract job title from text."""
    parts = re.split(r"[,|–-]", text)
    if len(parts) > 1:
        return parts[1].strip()
    return parts[0].strip()


def _extract_technologies(text: str) -> list[str]:
    """Extract technology names from text."""
    techs = []
    # Look for common tech patterns
    tech_pattern = r"\b(Python|JavaScript|React|Node|AWS|Docker|Kubernetes|PostgreSQL|MongoDB|Redis|Git)\b"
    matches = re.findall(tech_pattern, text, re.IGNORECASE)
    return list(set(matches))
