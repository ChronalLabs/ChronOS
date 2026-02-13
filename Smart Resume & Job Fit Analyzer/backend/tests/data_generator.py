import random
import faker

fake = faker.Faker()

# Domains and associated keywords/skills
DOMAINS = {
    "Software Engineering": {
        "titles": ["Software Engineer", "Backend Developer", "Frontend Developer", "Full Stack Engineer", "DevOps Engineer"],
        "skills": ["Python", "Java", "C++", "JavaScript", "React", "Node.js", "Docker", "Kubernetes", "AWS", "SQL", "Git"],
        "degrees": ["Computer Science", "Software Engineering", "Information Technology"]
    },
    "Data Science": {
        "titles": ["Data Scientist", "Data Analyst", "Machine Learning Engineer", "BI Analyst"],
        "skills": ["Python", "R", "SQL", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Tableau", "Power BI"],
        "degrees": ["Data Science", "Statistics", "Mathematics", "Computer Science"]
    },
    "Product Management": {
        "titles": ["Product Manager", "Associate Product Manager", "Product Owner"],
        "skills": ["Product Strategy", "User Research", "Agile", "Scrum", "Jira", "Roadmapping", "A/B Testing", "Data Analysis"],
        "degrees": ["Business Administration", "Management", "Computer Science", "Economics"] 
    },
    "Marketing": {
        "titles": ["Marketing Manager", "Digital Marketing Specialist", "Content Strategist", "SEO Specialist"],
        "skills": ["SEO", "SEM", "Google Analytics", "Social Media Marketing", "Content Marketing", "Email Marketing", "Copywriting"],
        "degrees": ["Marketing", "Communications", "Business Administration", "English"]
    },
    "Finance": {
        "titles": ["Financial Analyst", "Investment Banker", "Accountant", "Auditor"],
        "skills": ["Financial Modeling", "Excel", "Accounting", "Financial Analysis", "Valuation", "QuickBooks", "SAP"],
        "degrees": ["Finance", "Accounting", "Economics", "Business Administration"]
    },
     "Healthcare": {
        "titles": ["Registered Nurse", "Medical Assistant", "Healthcare Administrator", "Clinical Research Coordinator"],
        "skills": ["Patient Care", "EMR", "HIPAA", "Medical Terminology", "Clinical Research", "Healthcare Management"],
        "degrees": ["Nursing", "Health Administration", "Public Health", "Biology"]
    },
    "Design": {
        "titles": ["Graphic Designer", "UX/UI Designer", "Product Designer", "Art Director"],
        "skills": ["Adobe Creative Suite", "Photoshop", "Illustrator", "Figma", "Sketch", "InVision", "User Research", "Prototyping"],
        "degrees": ["Graphic Design", "Interaction Design", "Fine Arts", "Visual Communication"]
    }
}

LAYOUTS = ["standard", "compact", "messy"]

def generate_resume_data(domain=None, layout="standard"):
    """
    Generates a synthetic resume as a dictionary of sections and raw text.
    """
    if not domain:
        domain = random.choice(list(DOMAINS.keys()))
    
    domain_data = DOMAINS[domain]
    
    # Personal Info
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    linkedin = f"linkedin.com/in/{name.lower().replace(' ', '-')}"
    github = f"github.com/{name.lower().replace(' ', '')}" if domain in ["Software Engineering", "Data Science"] else ""
    
    # Education
    education = []
    for _ in range(random.randint(1, 2)):
        degree = random.choice(domain_data["degrees"])
        level = random.choice(["B.S.", "B.A.", "M.S.", "M.A.", "Ph.D.", "B.Tech"])
        edu = {
            "institution": f"{fake.company()} University",
            "degree": f"{level} in {degree}",
            "date": f"{random.randint(2015, 2023)} - {random.randint(2019, 2025)}",
            "gpa": f"GPA: {round(random.uniform(3.0, 4.0), 2)}"
        }
        education.append(edu)

    # Experience
    experience = []
    for _ in range(random.randint(1, 3)):
        start_month = fake.month_name()
        end_month = fake.month_name()
        exp = {
            "company": fake.company(),
            "title": random.choice(domain_data["titles"]),
            "date": f"{start_month} {random.randint(2018, 2022)} - {random.choice(['Present', f'{end_month} {random.randint(2023, 2025)}'])}",
            "bullets": [fake.sentence() for _ in range(random.randint(2, 4))]
        }
        experience.append(exp)

    # Skills
    skills = random.sample(domain_data["skills"], k=min(len(domain_data["skills"]), random.randint(5, 10)))
    
    # Projects (mostly for tech roles)
    projects = []
    if domain in ["Software Engineering", "Data Science", "Design", "Product Management"]:
        for _ in range(random.randint(1, 2)):
            proj = {
                "name": fake.bs().title(),
                "description": fake.paragraph(nb_sentences=2),
                "tech": ", ".join(random.sample(domain_data["skills"], k=random.randint(2, 4)))
            }
            projects.append(proj)
            
    # Certifications
    certifications = []
    if random.random() > 0.5:
        for _ in range(random.randint(1, 2)):
            cert = {
                "name": f"Certified {random.choice(domain_data['skills'])} Specialist",
                "issuer": fake.company(),
                "date": str(random.randint(2020, 2024))
            }
            certifications.append(cert)

    # Construct Raw Text based on Layout
    raw_text = construct_resume_text(name, email, phone, linkedin, github, education, experience, skills, projects, certifications, layout)
    
    return {
        "metadata": {
            "domain": domain,
            "layout": layout,
            "name": name,
            "email_expected": email,
            "phone_expected": phone,
            "skills_expected": skills
        },
        "raw_text": raw_text
    }

def construct_resume_text(name, email, phone, linkedin, github, education, experience, skills, projects, certifications, layout):
    lines = []
    
    # Header
    lines.append(name.upper())
    contact_info = [email, phone, linkedin]
    if github:
        contact_info.append(github)
    
    if layout == "compact":
        lines.append(" | ".join(contact_info))
    else:
        for item in contact_info:
            lines.append(item)
    
    lines.append("")

    # Sections Wrapper
    def add_section_header(title):
        if layout == "messy":
            # Messy headers: inconsistent casing, weird symbols
            symbols = ["", "-", "*", "#", "=>"]
            deco = random.choice(symbols)
            casing = random.choice(["upper", "title", "lower"])
            text = title.upper() if casing == "upper" else (title.title() if casing == "title" else title.lower())
            lines.append(f"{deco} {text} {deco}".strip())
        else:
            lines.append(title.upper())
            lines.append("-" * 20) # Standard underline

    # Experience
    add_section_header("Experience")
    for exp in experience:
        if layout == "compact":
            lines.append(f"{exp['title']} at {exp['company']} ({exp['date']})")
        else:
            lines.append(f"{exp['title']}")
            lines.append(f"{exp['company']} | {exp['date']}")
        
        for bullet in exp['bullets']:
            lines.append(f"- {bullet}")
        lines.append("")
    
    # Education
    add_section_header("Education")
    for edu in education:
        lines.append(f"{edu['institution']}")
        lines.append(f"{edu['degree']}")
        lines.append(f"{edu['date']} | {edu['gpa']}")
        lines.append("")
        
    # Projects
    if projects:
        add_section_header("Projects")
        for proj in projects:
            lines.append(f"{proj['name']}")
            lines.append(proj['description'])
            lines.append(f"Tech: {proj['tech']}")
            lines.append("")

    # Skills
    add_section_header("Skills")
    if layout == "compact":
        lines.append(", ".join(skills))
    else: 
        # listing/bullet style
        for skill in skills:
            lines.append(f"* {skill}")
            
    # Certifications
    if certifications:
        add_section_header("Certifications")
        for cert in certifications:
            lines.append(f"{cert['name']} - {cert['issuer']} ({cert['date']})")

    # Add random noise for messy resumes
    if layout == "messy":
        # Add random newlines or whitespace
        final_lines = []
        for line in lines:
            final_lines.append(line)
            if random.random() < 0.1:
                final_lines.append("")
        lines = final_lines

    return "\n".join(lines)

if __name__ == "__main__":
    # Test generation
    data = generate_resume_data()
    print(f"Generated Domain: {data['metadata']['domain']}")
    print("-" * 50)
    print(data['raw_text'][:500] + "...\n[TRUNCATED]")
