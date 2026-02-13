"""
Job Description parser.
Extracts skills, requirements, and classifications from JD text.
"""
import re

from typing import Optional


def parse_job_description(jd_text: str) -> "ParsedJobDescription":
    """
    Parse a job description and extract structured information.
    
    Args:
        jd_text: Raw job description text
    
    Returns:
        ParsedJobDescription with skills and requirements
    """
    from api.schemas import ParsedJobDescription, JDRequirement, SkillPriority
    import spacy
    
    # Extract job title (usually first line or after "Title:")
    title = _extract_title(jd_text)
    title = _extract_title(jd_text)
    
    # Extract company name
    company = _extract_company(jd_text)
    
    # Extract requirements and skills
    requirements = []
    required_skills = []
    optional_skills = []
    
    # Split into sections
    sections = _split_jd_sections(jd_text)
    
    # Process requirements section
    for section_name, section_text in sections.items():
        if any(k in section_name.lower() for k in ["requirement", "qualif", "must", "essential", "responsibilit", "duties"]):
            # Required skills section (including responsibilities where skills are often listed)
            skills, reqs = _extract_skills_and_requirements(section_text, SkillPriority.REQUIRED)
            required_skills.extend(skills)
            requirements.extend(reqs)
        elif any(k in section_name.lower() for k in ["prefer", "nice", "bonus", "plus", "optional"]):
            # Optional skills section
            skills, reqs = _extract_skills_and_requirements(section_text, SkillPriority.OPTIONAL)
            optional_skills.extend(skills)
            requirements.extend(reqs)
    
    # If no sections found, extract from full text
    if not required_skills:
        required_skills = _extract_skills_from_text(jd_text)
    
    # Extract experience requirements
    experience_req = _extract_experience_requirement(jd_text)
    
    # Extract education requirements
    education_req = _extract_education_requirement(jd_text)
    
    return ParsedJobDescription(
        raw_text=jd_text,
        title=title,
        company=company,
        requirements=requirements,
        required_skills=list(set(required_skills)),
        optional_skills=list(set(optional_skills)),
        experience_requirements=experience_req,
        education_requirements=education_req,
    )


def _extract_title(text: str) -> Optional[str]:
    """Extract job title from JD."""
    lines = text.strip().split("\n")
    
    # Check first few lines
    for line in lines[:5]:
        line = line.strip()
        
        # Look for explicit title markers
        title_match = re.match(r"(job\s*)?title\s*:\s*(.+)", line, re.IGNORECASE)
        if title_match:
            return title_match.group(2).strip()
        
        # Look for position markers
        pos_match = re.match(r"position\s*:\s*(.+)", line, re.IGNORECASE)
        if pos_match:
            return pos_match.group(1).strip()
        
        # First short line might be the title
        if len(line) < 80 and not any(k in line.lower() for k in ["company", "location", "about"]):
            if any(k in line.lower() for k in ["engineer", "developer", "manager", "analyst", "designer", "architect"]):
                return line
    
    return None


def _extract_company(text: str) -> Optional[str]:
    """Extract company name from JD."""
    patterns = [
        r"company\s*:\s*(.+)",
        r"about\s+(\w+(?:\s+\w+)?(?:\s+inc\.?|\s+llc\.?|\s+corp\.?)?)",
        r"at\s+(\w+(?:\s+\w+)?(?:\s+inc\.?|\s+llc\.?|\s+corp\.?)?)\s",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None


def _split_jd_sections(text: str) -> dict[str, str]:
    """Split JD into sections based on headers."""
    sections = {}
    current_section = "general"
    current_content = []
    
    # Common section headers
    header_patterns = [
        r"^(requirements?|qualifications?|what we('re)? look(ing)? for)\s*:?\s*$",
        r"^(responsibilities?|what you('ll)? do|duties)\s*:?\s*$",
        r"^(preferred|nice to have|bonus|optional)\s*:?\s*$",
        r"^(about|company|who we are)\s*:?\s*$",
        r"^(benefits?|perks?|what we offer)\s*:?\s*$",
    ]
    
    for line in text.split("\n"):
        line_stripped = line.strip()
        
        # Check if this is a section header
        is_header = False
        for pattern in header_patterns:
            if re.match(pattern, line_stripped, re.IGNORECASE):
                # Save previous section
                if current_content:
                    sections[current_section] = "\n".join(current_content)
                
                current_section = line_stripped.lower()
                current_content = []
                is_header = True
                break
        
        if not is_header and line_stripped:
            current_content.append(line)
    
    # Save last section
    if current_content:
        sections[current_section] = "\n".join(current_content)
    
    return sections


def _extract_skills_and_requirements(text: str, priority: "SkillPriority") -> tuple[list[str], list]:
    """Extract skills and requirements from section text."""
    from api.schemas import JDRequirement
    
    skills = []
    requirements = []
    
    # Extract skills using patterns
    skills.extend(_extract_skills_from_text(text))
    
    # Extract individual requirements (bullet points)
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith(("-", "•", "▪", "○", "*")) or re.match(r"^\d+\.", line):
            clean_line = re.sub(r"^[-•▪○*\d.]+\s*", "", line).strip()
            if clean_line:
                # Extract skills from this requirement
                line_skills = _extract_skills_from_text(clean_line)
                requirements.append(JDRequirement(
                    text=clean_line,
                    skills=line_skills,
                    priority=priority,
                ))
                skills.extend(line_skills)
    
    return skills, requirements


def _extract_skills_from_text(text: str) -> list[str]:
    """Extract skill names from text using pattern matching."""
    skills = []
    
    # Technology patterns
    tech_patterns = [
        # Programming Languages
        (r"\bpython\b", "Python"),
        (r"\bjavascript\b|\bjs\b", "JavaScript"),
        (r"\btypescript\b|\bts\b", "TypeScript"),
        (r"\bjava\b", "Java"),
        (r"\bc\+\+\b|cpp\b", "C++"),
        (r"\bc#\b|csharp\b", "C#"),
        (r"\b(?<!en)go\b|\bgolang\b", "Go"),
        (r"\brust\b", "Rust"),
        (r"\bruby\b", "Ruby"),
        (r"\bphp\b", "PHP"),
        (r"\bswift\b", "Swift"),
        (r"\bkotlin\b", "Kotlin"),
        (r"\bscala\b", "Scala"),
        (r"\br\b(?=\s|,|\.)", "R"),
        (r"\bsql\b", "SQL"),
        (r"\bhtml\b", "HTML"),
        (r"\bcss\b", "CSS"),
        (r"\bshell\b|\bbash\b", "Bash"),
        
        # Frameworks
        (r"\breact\b|\breactjs\b", "React"),
        (r"\bangular\b", "Angular"),
        (r"\bvue\b|\bvuejs\b", "Vue.js"),
        (r"\bnode\b|\bnodejs\b", "Node.js"),
        (r"\bexpress\b", "Express.js"),
        (r"\bdjango\b", "Django"),
        (r"\bflask\b", "Flask"),
        (r"\bfastapi\b", "FastAPI"),
        (r"\bspring\b", "Spring Boot"),
        (r"\bnext\.?js\b", "Next.js"),
        (r"\btailwind\b", "Tailwind CSS"),
        (r"\bbootstrap\b", "Bootstrap"),
        
        # ML/AI
        (r"\btensorflow\b", "TensorFlow"),
        (r"\bpytorch\b", "PyTorch"),
        (r"\bscikit-?learn\b", "Scikit-learn"),
        (r"\bpandas\b", "Pandas"),
        (r"\bnumpy\b", "NumPy"),
        (r"\bopencv\b", "OpenCV"),
        
        # Databases
        (r"\bpostgres(?:ql)?\b", "PostgreSQL"),
        (r"\bmysql\b", "MySQL"),
        (r"\bmongodb\b", "MongoDB"),
        (r"\bredis\b", "Redis"),
        (r"\belasticsearch\b", "Elasticsearch"),
        (r"\bdynamodb\b", "DynamoDB"),
        
        # Cloud & DevOps
        (r"\baws\b", "AWS"),
        (r"\bgcp\b|google cloud\b", "Google Cloud"),
        (r"\bazure\b", "Azure"),
        (r"\bdocker\b", "Docker"),
        (r"\bkubernetes\b|\bk8s\b", "Kubernetes"),
        (r"\bgit\b", "Git"),
        (r"\bjenkins\b", "Jenkins"),
        (r"\bterraform\b", "Terraform"),
        (r"\bansible\b", "Ansible"),
        (r"\blinux\b", "Linux"),
        (r"\bjira\b", "Jira"),
        
        # Soft Skills & Business
        (r"\bcommunication\b", "Communication"),
        (r"\bleadership\b", "Leadership"),
        (r"\bteamwork\b", "Teamwork"),
        (r"\bproblem[- ]?solving\b", "Problem Solving"),
        (r"\bagile\b", "Agile"),
        (r"\bscrum\b", "Scrum"),
        (r"\bproject[- ]?management\b", "Project Management"),
        (r"\btime[- ]?management\b", "Time Management"),
        (r"\bcustomer[- ]?service\b", "Customer Service"),
        (r"\bpresentation\b", "Presentation"),
        (r"\banalysis\b|\banalytical\b", "Analytical Skills"),
        (r"\bmarketing\b", "Marketing"),
        (r"\bsales\b", "Sales"),
        (r"\bexcel\b", "Excel"),
        (r"\bpower\s?bi\b", "Power BI"),
        (r"\btableau\b", "Tableau"),
        
        # Finance & Accounting
        (r"\bgaap\b", "GAAP"),
        (r"\bifrs\b", "IFRS"),
        (r"\bsox\b", "SOX"),
        (r"\bcpa\b", "CPA"),
        (r"\bcfa\b", "CFA"),
        (r"\btax\b|\btaxation\b", "Taxation"),
        (r"\baudit\b|\bauditing\b", "Auditing"),
        (r"\baccounting\b", "Accounting"),
        (r"\bfinancial\s+analysis\b", "Financial Analysis"),
        (r"\bfinancial\s+modeling\b", "Financial Modeling"),
        (r"\bbudgeting\b", "Budgeting"),
        (r"\bforecasting\b", "Forecasting"),
        (r"\bvariance\s+analysis\b", "Variance Analysis"),
        (r"\bpayroll\b", "Payroll"),
        
        # Healthcare
        (r"\bhcfa\b", "HCFA"),
        (r"\bhipaa\b", "HIPAA"),
        (r"\bemr\b|\behr\b", "EMR/EHR"),
        (r"\bepic\b", "Epic"),
        (r"\bcerner\b", "Cerner"),
        (r"\bmeditech\b", "Meditech"),
        (r"\bpatient\s+care\b", "Patient Care"),
        (r"\btriag(?:e|ing)\b", "Triage"),
        (r"\bclinical\b", "Clinical Skills"),
        (r"\bphlebotomy\b", "Phlebotomy"),
        (r"\bbls\b", "BLS"),
        (r"\bacls\b", "ACLS"),
        (r"\bcnor\b", "CNOR"),
        (r"\brn\b|\bregistered\s+nurse\b", "Registered Nurse"),
        
         # General Business
        (r"\bstrategic\s+planning\b", "Strategic Planning"),
        (r"\bnegotiation\b", "Negotiation"),
        (r"\boperations\b", "Operations Management"),
        (r"\bcompliance\b", "Compliance"),
        (r"\brisk\s+management\b", "Risk Management"),
        (r"\bdata\s+entry\b", "Data Entry"),
    ]
    
    text_lower = text.lower()
    seen = set()
    
    for pattern, skill_name in tech_patterns:
        if re.search(pattern, text_lower) and skill_name not in seen:
            skills.append(skill_name)
            seen.add(skill_name)
    
    return skills


def _extract_experience_requirement(text: str) -> Optional[str]:
    """Extract experience requirements from JD."""
    patterns = [
        r"(\d+\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)?)",
        r"(experience\s*:\s*\d+\+?\s*(?:years?|yrs?))",
        r"(minimum\s+\d+\s*(?:years?|yrs?)\s*(?:of\s*)?experience)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None


def _extract_education_requirement(text: str) -> Optional[str]:
    """Extract education requirements from JD."""
    patterns = [
        r"(bachelor'?s?|master'?s?|phd|doctorate)\s*(?:degree)?\s*(?:in\s+[\w\s]+)?",
        r"(bs|ms|ba|ma|b\.s\.|m\.s\.)\s*(?:in\s+[\w\s]+)?",
        r"(degree\s+in\s+[\w\s]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    
    return None
