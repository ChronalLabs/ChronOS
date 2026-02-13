"""
Multi-Domain Resume Testing Script
Tests skill extraction across different professional domains
"""

import requests
import json
from typing import Dict, List

BASE_URL = "http://localhost:8000"

# Sample resumes from different domains
DOMAIN_RESUMES = {
    "software_engineer": """
JOHN SMITH
Software Engineer | john.smith@email.com | (555) 123-4567

EXPERIENCE
Senior Software Engineer | TechCorp Inc. | 2020 - Present
- Developed microservices using Python, FastAPI, and Docker
- Built React frontend with TypeScript and Next.js
- Managed PostgreSQL database and Redis caching layer
- Deployed to AWS using Kubernetes and Terraform
- Implemented CI/CD pipelines with GitHub Actions

Software Developer | StartupXYZ | 2018 - 2020
- Built REST APIs with Django and Flask
- Worked with MongoDB and Elasticsearch
- Applied machine learning using PyTorch and scikit-learn

EDUCATION
B.S. Computer Science | Stanford University | 2018

SKILLS
Python, JavaScript, TypeScript, React, Node.js, Docker, Kubernetes, AWS, PostgreSQL, MongoDB
""",

    "healthcare_nurse": """
SARAH JOHNSON, RN, BSN
Registered Nurse | sarah.johnson@email.com | (555) 234-5678

EXPERIENCE
Registered Nurse | City Hospital | 2019 - Present
- Provided patient care to 15+ patients daily in critical care unit
- Maintained HIPAA compliance in all patient interactions
- Used Epic Systems for electronic medical records documentation
- Administered medications and performed vital signs monitoring
- Collaborated with physicians on care coordination
- BLS and ACLS certified, maintained CPR certification

Nurse Assistant | Community Clinic | 2017 - 2019
- Assisted with phlebotomy and patient assessments
- Ensured OSHA compliance and infection control protocols

EDUCATION
Bachelor of Science in Nursing | UCLA | 2019
CPR Certified | BLS Certified | ACLS Certified

SKILLS
Patient Care, HIPAA, EMR, Epic Systems, Medication Administration, Vital Signs, Clinical Research
""",

    "financial_analyst": """
MICHAEL CHEN, CFA
Financial Analyst | michael.chen@email.com | (555) 345-6789

EXPERIENCE
Senior Financial Analyst | Goldman Sachs | 2020 - Present
- Built financial models for M&A transactions using Excel and Bloomberg Terminal
- Performed equity research and investment analysis
- Conducted risk assessment and portfolio management
- Prepared financial reports following GAAP standards
- Developed DCF models and valuation analyses

Financial Analyst | Morgan Stanley | 2018 - 2020
- Performed credit analysis and due diligence
- Created forecasting models and budget analysis
- Used SAP and Oracle Financials for reporting

EDUCATION
MBA Finance | Harvard Business School | 2018
CFA Level III | BS Economics | NYU

SKILLS
Financial Modeling, Bloomberg Terminal, Excel, Risk Assessment, GAAP, Investment Analysis, Portfolio Management
""",

    "marketing_manager": """
JESSICA WILLIAMS
Digital Marketing Manager | jessica.williams@email.com | (555) 456-7890

EXPERIENCE
Digital Marketing Manager | Nike | 2019 - Present
- Led SEO and SEM campaigns increasing organic traffic by 150%
- Managed Google Ads and Facebook Ads with $2M annual budget
- Used Google Analytics to track KPIs and conversion optimization
- Developed content marketing strategy and brand positioning
- Implemented marketing automation using HubSpot
- Ran A/B tests improving email marketing conversion by 35%

Marketing Specialist | Coca-Cola | 2017 - 2019
- Managed social media marketing across all platforms
- Created copywriting for campaigns and PR materials
- Used Marketo for email campaigns and lead nurturing

EDUCATION
MBA Marketing | Northwestern Kellogg | 2017

SKILLS
SEO, SEM, Google Analytics, Google Ads, Facebook Ads, HubSpot, Content Marketing, Email Marketing, A/B Testing
""",

    "ux_designer": """
EMILY RODRIGUEZ
UX/UI Designer | emily.rodriguez@email.com | (555) 567-8901

EXPERIENCE
Senior UX Designer | Apple | 2020 - Present
- Led user research and created wireframes in Figma
- Developed design systems and component libraries
- Conducted usability testing and created prototypes
- Applied typography and color theory principles
- Designed responsive layouts for iOS and web applications

Product Designer | Airbnb | 2018 - 2020
- Created UI designs using Adobe XD and Sketch
- Built interactive prototypes with InVision
- Collaborated on motion design using After Effects
- Conducted user interviews and A/B testing

EDUCATION
BFA Graphic Design | Rhode Island School of Design | 2018

SKILLS
Figma, Adobe XD, Sketch, User Research, Wireframing, Prototyping, Design Systems, Typography, UI Design, UX Design
""",

    "lawyer": """
DAVID WILSON, JD
Corporate Attorney | david.wilson@email.com | (555) 678-9012

EXPERIENCE
Associate Attorney | Skadden Arps | 2019 - Present
- Conducted legal research using Westlaw and LexisNexis
- Drafted contracts and managed corporate transactions
- Handled intellectual property and trademark matters
- Ensured GDPR compliance for international clients
- Managed e-discovery process for litigation cases

Legal Intern | Sullivan & Cromwell | 2018 - 2019
- Performed due diligence for M&A transactions
- Assisted with regulatory compliance matters
- Drafted legal memoranda and briefs

EDUCATION
JD | Yale Law School | 2019
Bar Admission: New York, California

SKILLS
Legal Research, Contract Law, Corporate Law, Intellectual Property, GDPR, Westlaw, LexisNexis, Litigation, Compliance
""",

    "teacher": """
AMANDA BROWN
High School English Teacher | amanda.brown@email.com | (555) 789-0123

EXPERIENCE
English Teacher | Lincoln High School | 2018 - Present
- Developed curriculum for AP English Literature
- Created lesson plans aligned with state standards
- Managed classroom of 30+ students with differentiated instruction
- Used Google Classroom and Canvas for online teaching
- Implemented student assessments and IEP accommodations
- Mentored new teachers and led professional development

ESL Teacher | International Academy | 2016 - 2018
- Taught English as Second Language to diverse students
- Developed TESOL-certified curriculum
- Used educational technology for interactive learning

EDUCATION
M.Ed Education | Columbia Teachers College | 2016
TESOL Certification

SKILLS
Curriculum Development, Lesson Planning, Classroom Management, Google Classroom, Canvas, Student Assessment, IEP, ESL
""",

    "sales_manager": """
ROBERT MARTINEZ
Sales Manager | robert.martinez@email.com | (555) 890-1234

EXPERIENCE
Regional Sales Manager | Oracle | 2019 - Present
- Managed territory of $15M annual quota with 120% achievement
- Built and managed team of 10 account executives
- Used Salesforce CRM for pipeline management
- Led enterprise sales negotiations and contract discussions
- Implemented B2B sales strategies and lead generation
- Developed customer retention and upselling programs

Sales Representative | Microsoft | 2016 - 2019
- Exceeded sales forecasting targets by 25%
- Managed account relationships and cold calling
- Used HubSpot CRM for customer relationship management

EDUCATION
BBA Business | University of Michigan | 2016

SKILLS
Sales Strategy, Salesforce, CRM, Account Management, B2B Sales, Negotiation, Lead Generation, Pipeline Management
""",

    "hr_manager": """
LISA THOMPSON
HR Manager | lisa.thompson@email.com | (555) 901-2345

EXPERIENCE
HR Manager | Google | 2019 - Present
- Led recruiting and talent acquisition for engineering teams
- Managed onboarding programs for 200+ new hires annually
- Administered benefits using Workday HRIS
- Developed training and development programs
- Handled employee relations and performance management
- Ensured labor law compliance and diversity inclusion initiatives

HR Coordinator | Amazon | 2017 - 2019
- Processed payroll using ADP
- Managed HRIS data and employee records
- Coordinated succession planning initiatives

EDUCATION
M.S. Human Resources | Cornell ILR | 2017
SHRM-CP Certified

SKILLS
Recruiting, Talent Acquisition, Onboarding, Workday, HRIS, Benefits Administration, Training, Employee Relations, SHRM
""",

    "mechanical_engineer": """
KEVIN NGUYEN
Mechanical Engineer | kevin.nguyen@email.com | (555) 012-3456

EXPERIENCE
Senior Mechanical Engineer | Boeing | 2019 - Present
- Designed aircraft components using SolidWorks and CATIA
- Performed FEA analysis with Ansys and MATLAB simulations
- Implemented Six Sigma and lean manufacturing improvements
- Managed quality control and safety compliance protocols
- Led project management for $5M component development

Mechanical Engineer | General Electric | 2016 - 2019
- Created AutoCAD drawings for turbine systems
- Developed process engineering improvements
- Used PLC programming for automation systems

EDUCATION
M.S. Mechanical Engineering | MIT | 2016
Six Sigma Green Belt Certified

SKILLS
SolidWorks, CATIA, AutoCAD, Ansys, MATLAB, Six Sigma, Quality Control, Lean Manufacturing, Project Management
"""
}

# Sample job descriptions for each domain
DOMAIN_JDS = {
    "software_engineer": """
Senior Software Engineer - Full Stack
Requirements:
- 5+ years experience with Python or JavaScript
- Experience with React, Node.js, or similar frontend frameworks
- Database experience (PostgreSQL, MongoDB)
- Cloud deployment (AWS, GCP, or Azure)
- Docker and Kubernetes knowledge
- Agile/Scrum experience
""",

    "healthcare_nurse": """
Registered Nurse - ICU
Requirements:
- Active RN license with BSN preferred
- BLS and ACLS certification required
- Experience with Epic or Cerner EMR
- Strong patient care and assessment skills
- HIPAA compliance knowledge
- Critical care experience preferred
""",

    "financial_analyst": """
Senior Financial Analyst
Requirements:
- CFA or CPA preferred
- Advanced Excel and financial modeling skills
- Bloomberg Terminal experience
- Knowledge of GAAP/IFRS accounting standards
- Risk assessment and portfolio analysis experience
- Strong analytical and forecasting abilities
""",

    "marketing_manager": """
Digital Marketing Manager
Requirements:
- 5+ years digital marketing experience
- SEO/SEM expertise with Google Analytics certification
- Experience with Google Ads and Facebook Ads
- Marketing automation (HubSpot, Marketo)
- Content marketing and email marketing experience
- A/B testing and conversion optimization skills
""",

    "ux_designer": """
Senior UX/UI Designer
Requirements:
- 5+ years UX/UI design experience
- Proficiency in Figma, Sketch, or Adobe XD
- Strong user research and wireframing skills
- Experience with design systems
- Prototyping and usability testing experience
- Understanding of typography and visual design
""",

    "lawyer": """
Corporate Associate Attorney
Requirements:
- JD from accredited law school
- Bar admission required
- Contract drafting and negotiation experience
- Corporate law and M&A transaction experience
- Legal research using Westlaw or LexisNexis
- Intellectual property knowledge preferred
""",

    "teacher": """
High School English Teacher
Requirements:
- Teaching certification required
- Experience with curriculum development
- Classroom management skills
- Familiarity with LMS (Canvas, Google Classroom)
- Experience with differentiated instruction
- IEP/special education experience preferred
""",

    "sales_manager": """
Regional Sales Manager
Requirements:
- 5+ years B2B sales experience
- Salesforce or CRM proficiency
- Territory and pipeline management experience
- Strong negotiation and closing skills
- Team leadership and coaching abilities
- Track record of quota achievement
""",

    "hr_manager": """
HR Manager
Requirements:
- 5+ years HR experience
- SHRM certification preferred
- HRIS experience (Workday, ADP)
- Recruiting and talent acquisition expertise
- Benefits administration knowledge
- Employee relations and compliance experience
""",

    "mechanical_engineer": """
Senior Mechanical Engineer
Requirements:
- 5+ years mechanical engineering experience
- CAD proficiency (SolidWorks, CATIA, AutoCAD)
- FEA/simulation experience (Ansys, MATLAB)
- Six Sigma or Lean certification preferred
- Quality control and project management skills
- Manufacturing process knowledge
"""
}


def test_domain(domain: str) -> Dict:
    """Test resume parsing and matching for a specific domain"""
    resume_text = DOMAIN_RESUMES[domain]
    jd_text = DOMAIN_JDS[domain]
    
    # Step 1: Parse resume
    parse_response = requests.post(
        f"{BASE_URL}/api/parse",
        json={"resume_text": resume_text, "job_description": jd_text}
    )
    
    if parse_response.status_code != 200:
        return {"domain": domain, "error": f"Parse failed: {parse_response.text}", "success": False}
    
    session_id = parse_response.json()["session_id"]
    parsed_data = parse_response.json()["parsed_resume"]
    
    # Step 2: Evaluate
    eval_response = requests.post(
        f"{BASE_URL}/api/evaluate/{session_id}"
    )
    
    if eval_response.status_code != 200:
        return {"domain": domain, "error": f"Evaluate failed: {eval_response.text}", "success": False}
    
    evaluation = eval_response.json()
    
    return {
        "domain": domain,
        "success": True,
        "session_id": session_id,
        "skills_extracted": len(parsed_data.get("skills", [])),
        "skills_list": [s.get("name", s) if isinstance(s, dict) else s for s in parsed_data.get("skills", [])[:10]],
        "experience_count": len(parsed_data.get("experience", [])),
        "education_count": len(parsed_data.get("education", [])),
        "job_fit_score": evaluation.get("job_fit_score", 0),
        "confidence": evaluation.get("confidence_level", "unknown"),
        "matched_skills": len([s for s in evaluation.get("skill_matches", []) if s.get("match_type") == "matched"]),
        "partial_skills": len([s for s in evaluation.get("skill_matches", []) if s.get("match_type") == "partial"]),
        "missing_skills": len([s for s in evaluation.get("skill_matches", []) if s.get("match_type") == "missing"]),
    }


def run_all_tests():
    """Run tests for all domains and print results"""
    print("=" * 80)
    print("MULTI-DOMAIN RESUME TESTING")
    print("=" * 80)
    
    results = []
    
    for domain in DOMAIN_RESUMES.keys():
        print(f"\n[TEST] Testing: {domain.replace('_', ' ').title()}")
        print("-" * 40)
        
        try:
            result = test_domain(domain)
            results.append(result)
            
            if result["success"]:
                print(f"  [OK] Skills extracted: {result['skills_extracted']}")
                print(f"  [>] Top skills: {', '.join(result['skills_list'][:5])}")
                print(f"  [>] Experience entries: {result['experience_count']}")
                print(f"  [>] Education entries: {result['education_count']}")
                print(f"  [>] Job Fit Score: {result['job_fit_score']}/100")
                print(f"  [>] Matched: {result['matched_skills']} | Partial: {result['partial_skills']} | Missing: {result['missing_skills']}")
            else:
                print(f"  [FAIL] Error: {result['error']}")
                
        except Exception as e:
            print(f"  [FAIL] Exception: {str(e)}")
            results.append({"domain": domain, "success": False, "error": str(e)})
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    print(f"\n[OK] Successful: {len(successful)}/{len(results)}")
    print(f"[FAIL] Failed: {len(failed)}/{len(results)}")
    
    if successful:
        avg_score = sum(r["job_fit_score"] for r in successful) / len(successful)
        avg_skills = sum(r["skills_extracted"] for r in successful) / len(successful)
        print(f"\n[>] Average Job Fit Score: {avg_score:.1f}")
        print(f"[>] Average Skills Extracted: {avg_skills:.1f}")
    
    if failed:
        print("\n[FAIL] Failed domains:")
        for r in failed:
            print(f"  - {r['domain']}: {r.get('error', 'Unknown error')}")
    
    return results


if __name__ == "__main__":
    run_all_tests()
