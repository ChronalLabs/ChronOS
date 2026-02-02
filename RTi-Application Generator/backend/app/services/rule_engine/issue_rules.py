"""
Issue Rules - Maps issues to departments and authorities
Deterministic mapping for common issue categories

Following MODEL_USAGE_POLICY:
- All structural decisions go through rule engine first
- Deterministic mappings with confidence scores
- Supports all Indian states and major departments
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import re
import logging

logger = logging.getLogger(__name__)


class IssueCategory(Enum):
    """Supported issue categories"""
    ELECTRICITY = "electricity"
    WATER = "water"
    ROADS = "roads"
    EDUCATION = "education"
    HEALTH = "health"
    POLICE = "police"
    LAND = "land"
    TRANSPORT = "transport"
    RATION = "ration"
    PENSION = "pension"
    MUNICIPAL = "municipal"
    TAX = "tax"
    BANKING = "banking"
    TELECOM = "telecom"
    RAILWAY = "railway"
    PASSPORT = "passport"
    EMPLOYMENT = "employment"
    SOCIAL_WELFARE = "social_welfare"
    ENVIRONMENT = "environment"
    GENERAL = "general"


@dataclass
class DepartmentInfo:
    """Department information with contact details"""
    name: str
    level: str  # central, state, district, local
    parent_department: Optional[str] = None
    grievance_portal: Optional[str] = None
    typical_response_days: int = 30


@dataclass
class IssueMatch:
    """Detailed issue match result"""
    category: IssueCategory
    confidence: float
    keywords_matched: List[str]
    departments: List[DepartmentInfo]
    suggested_authority: str
    escalation_path: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category.value,
            "confidence": round(self.confidence, 4),
            "keywords_matched": self.keywords_matched,
            "departments": [
                {"name": d.name, "level": d.level, "response_days": d.typical_response_days}
                for d in self.departments
            ],
            "suggested_authority": self.suggested_authority,
            "escalation_path": self.escalation_path
        }


# ============================================================================
# COMPREHENSIVE ISSUE-DEPARTMENT MAPPING
# ============================================================================

ISSUE_DEPARTMENT_MAP = {
    IssueCategory.ELECTRICITY: {
        "departments": [
            DepartmentInfo("State Electricity Board", "state", grievance_portal="https://www.pgportal.gov.in"),
            DepartmentInfo("DISCOM (Distribution Company)", "state"),
            DepartmentInfo("Power Department", "state"),
            DepartmentInfo("Electrical Inspector", "district"),
        ],
        "keywords": [
            ("electricity", 0.3), ("power", 0.2), ("electric", 0.2),
            ("meter", 0.2), ("billing", 0.15), ("load shedding", 0.25),
            ("transformer", 0.2), ("voltage", 0.2), ("power cut", 0.25),
            ("blackout", 0.25), ("current", 0.1), ("wire", 0.1),
            ("connection", 0.15), ("unit", 0.1), ("tariff", 0.15),
            ("discom", 0.3), ("electricity board", 0.3)
        ],
        "escalation_path": [
            "Junior Engineer → Executive Engineer → Superintending Engineer → Chief Engineer → CMD"
        ]
    },
    
    IssueCategory.WATER: {
        "departments": [
            DepartmentInfo("Water Supply Department", "state"),
            DepartmentInfo("Jal Board", "state"),
            DepartmentInfo("Municipal Corporation Water Works", "local"),
            DepartmentInfo("Public Health Engineering Department (PHED)", "state"),
        ],
        "keywords": [
            ("water", 0.3), ("water supply", 0.3), ("pipeline", 0.25),
            ("sewage", 0.2), ("drainage", 0.2), ("tap", 0.15),
            ("borewell", 0.2), ("tank", 0.1), ("contaminated", 0.2),
            ("dirty water", 0.25), ("no water", 0.25), ("water tanker", 0.2),
            ("jal board", 0.3), ("phed", 0.3), ("water meter", 0.2)
        ],
        "escalation_path": [
            "AE Water → EE Water → SE Water → Chief Engineer → Secretary"
        ]
    },
    
    IssueCategory.ROADS: {
        "departments": [
            DepartmentInfo("Public Works Department (PWD)", "state"),
            DepartmentInfo("Municipal Corporation Roads", "local"),
            DepartmentInfo("National Highway Authority of India (NHAI)", "central"),
            DepartmentInfo("State Highway Department", "state"),
        ],
        "keywords": [
            ("road", 0.3), ("pothole", 0.3), ("highway", 0.25),
            ("street", 0.2), ("footpath", 0.2), ("bridge", 0.2),
            ("flyover", 0.2), ("construction", 0.15), ("repair", 0.1),
            ("damaged road", 0.25), ("broken road", 0.25), ("street light", 0.2),
            ("pwd", 0.3), ("nhai", 0.3), ("pavement", 0.15)
        ],
        "escalation_path": [
            "AE PWD → EE PWD → SE PWD → Chief Engineer → Secretary PWD"
        ]
    },
    
    IssueCategory.EDUCATION: {
        "departments": [
            DepartmentInfo("Department of School Education", "state"),
            DepartmentInfo("District Education Officer", "district"),
            DepartmentInfo("Block Education Officer", "block"),
            DepartmentInfo("University Grants Commission (UGC)", "central"),
        ],
        "keywords": [
            ("school", 0.3), ("college", 0.25), ("education", 0.25),
            ("admission", 0.2), ("fees", 0.15), ("certificate", 0.15),
            ("teacher", 0.2), ("student", 0.1), ("exam", 0.15),
            ("result", 0.15), ("scholarship", 0.2), ("hostel", 0.15),
            ("university", 0.25), ("board exam", 0.25), ("marksheet", 0.2),
            ("transfer certificate", 0.25), ("tc", 0.2)
        ],
        "escalation_path": [
            "Principal → BEO → DEO → Director Education → Secretary Education"
        ]
    },
    
    IssueCategory.HEALTH: {
        "departments": [
            DepartmentInfo("Department of Health", "state"),
            DepartmentInfo("District Health Officer", "district"),
            DepartmentInfo("Chief Medical Officer (CMO)", "district"),
            DepartmentInfo("Hospital Administration", "local"),
        ],
        "keywords": [
            ("hospital", 0.3), ("health", 0.25), ("medical", 0.25),
            ("doctor", 0.2), ("medicine", 0.2), ("treatment", 0.2),
            ("clinic", 0.2), ("phc", 0.25), ("primary health center", 0.25),
            ("ambulance", 0.2), ("emergency", 0.15), ("patient", 0.1),
            ("nurse", 0.15), ("surgery", 0.2), ("blood", 0.1),
            ("vaccination", 0.2), ("ayushman", 0.25)
        ],
        "escalation_path": [
            "Medical Officer → CMO → Director Health → Secretary Health"
        ]
    },
    
    IssueCategory.POLICE: {
        "departments": [
            DepartmentInfo("Police Station", "local"),
            DepartmentInfo("SP/SSP Office", "district"),
            DepartmentInfo("Police Commissioner Office", "city"),
            DepartmentInfo("DGP Office", "state"),
        ],
        "keywords": [
            ("police", 0.3), ("fir", 0.3), ("crime", 0.25),
            ("theft", 0.25), ("harassment", 0.2), ("safety", 0.15),
            ("robbery", 0.25), ("assault", 0.25), ("cybercrime", 0.25),
            ("missing", 0.2), ("violence", 0.2), ("threat", 0.2),
            ("investigation", 0.2), ("constable", 0.15), ("station", 0.1),
            ("chargesheet", 0.2), ("bail", 0.15)
        ],
        "escalation_path": [
            "SHO → Circle Officer → SP → IG → DGP"
        ]
    },
    
    IssueCategory.LAND: {
        "departments": [
            DepartmentInfo("Revenue Department", "state"),
            DepartmentInfo("Tehsildar Office", "tehsil"),
            DepartmentInfo("Sub-Registrar Office", "district"),
            DepartmentInfo("Collector Office", "district"),
        ],
        "keywords": [
            ("land", 0.3), ("property", 0.25), ("registry", 0.25),
            ("mutation", 0.25), ("encroachment", 0.25), ("survey", 0.2),
            ("khasra", 0.25), ("khatauni", 0.25), ("jamabandi", 0.25),
            ("tehsil", 0.2), ("patwari", 0.2), ("circle rate", 0.2),
            ("stamp duty", 0.2), ("deed", 0.2), ("plot", 0.15),
            ("possession", 0.2), ("fard", 0.2)
        ],
        "escalation_path": [
            "Patwari → Tehsildar → SDM → Collector → Revenue Secretary"
        ]
    },
    
    IssueCategory.TRANSPORT: {
        "departments": [
            DepartmentInfo("Regional Transport Office (RTO)", "district"),
            DepartmentInfo("Transport Department", "state"),
            DepartmentInfo("Traffic Police", "local"),
            DepartmentInfo("Motor Vehicle Department", "state"),
        ],
        "keywords": [
            ("vehicle", 0.25), ("license", 0.25), ("driving license", 0.3),
            ("registration", 0.2), ("traffic", 0.2), ("bus", 0.15),
            ("transport", 0.2), ("rto", 0.3), ("fitness", 0.2),
            ("permit", 0.2), ("challan", 0.25), ("rc", 0.25),
            ("pollution certificate", 0.25), ("puc", 0.25), ("insurance", 0.15),
            ("number plate", 0.2), ("transfer", 0.15)
        ],
        "escalation_path": [
            "RTO → DTO → Transport Commissioner → Secretary Transport"
        ]
    },
    
    IssueCategory.RATION: {
        "departments": [
            DepartmentInfo("Food & Civil Supplies Department", "state"),
            DepartmentInfo("PDS Office", "district"),
            DepartmentInfo("Fair Price Shop", "local"),
            DepartmentInfo("District Supply Officer", "district"),
        ],
        "keywords": [
            ("ration", 0.3), ("pds", 0.3), ("food", 0.15),
            ("fair price", 0.25), ("ration card", 0.3), ("aadhar", 0.1),
            ("kerosene", 0.2), ("sugar", 0.1), ("wheat", 0.1),
            ("rice", 0.1), ("bpl", 0.25), ("apl", 0.2),
            ("antyodaya", 0.25), ("fps", 0.25)
        ],
        "escalation_path": [
            "FPS Dealer → Inspector → DSO → Director Food → Secretary"
        ]
    },
    
    IssueCategory.PENSION: {
        "departments": [
            DepartmentInfo("Pension Department", "state"),
            DepartmentInfo("Treasury Office", "district"),
            DepartmentInfo("AG Office", "state"),
            DepartmentInfo("Social Welfare (for social pensions)", "state"),
        ],
        "keywords": [
            ("pension", 0.3), ("retirement", 0.25), ("epf", 0.25),
            ("gratuity", 0.25), ("ppo", 0.25), ("old age pension", 0.3),
            ("widow pension", 0.3), ("disability pension", 0.3),
            ("family pension", 0.25), ("commutation", 0.2),
            ("treasury", 0.2), ("arrears", 0.2)
        ],
        "escalation_path": [
            "Treasury Officer → Director Pension → AG → Secretary Finance"
        ]
    },
    
    IssueCategory.MUNICIPAL: {
        "departments": [
            DepartmentInfo("Municipal Corporation", "city"),
            DepartmentInfo("Nagar Palika", "town"),
            DepartmentInfo("Nagar Panchayat", "town"),
            DepartmentInfo("Town Planning", "local"),
        ],
        "keywords": [
            ("municipal", 0.3), ("corporation", 0.2), ("garbage", 0.25),
            ("sanitation", 0.25), ("building", 0.15), ("house tax", 0.25),
            ("property tax", 0.25), ("noc", 0.2), ("building plan", 0.2),
            ("encroachment", 0.2), ("demolition", 0.2), ("birth certificate", 0.25),
            ("death certificate", 0.25), ("trade license", 0.2),
            ("advertisement", 0.15), ("parking", 0.15)
        ],
        "escalation_path": [
            "Ward Officer → Zonal Officer → Commissioner → Mayor"
        ]
    },
    
    IssueCategory.TAX: {
        "departments": [
            DepartmentInfo("Income Tax Department", "central"),
            DepartmentInfo("GST Department", "central"),
            DepartmentInfo("Commercial Tax", "state"),
            DepartmentInfo("Stamp & Registration", "state"),
        ],
        "keywords": [
            ("tax", 0.25), ("income tax", 0.3), ("gst", 0.3),
            ("refund", 0.2), ("pan", 0.2), ("tan", 0.2),
            ("return", 0.15), ("itr", 0.25), ("assessment", 0.2),
            ("notice", 0.15), ("demand", 0.15), ("tds", 0.25)
        ],
        "escalation_path": [
            "Assessing Officer → CIT → CCIT → CBDT"
        ]
    },
    
    IssueCategory.BANKING: {
        "departments": [
            DepartmentInfo("Bank Branch", "local"),
            DepartmentInfo("Regional Manager", "regional"),
            DepartmentInfo("Banking Ombudsman", "regional"),
            DepartmentInfo("RBI", "central"),
        ],
        "keywords": [
            ("bank", 0.3), ("account", 0.2), ("loan", 0.25),
            ("atm", 0.25), ("cheque", 0.2), ("interest", 0.15),
            ("deposit", 0.15), ("withdrawal", 0.15), ("fraud", 0.2),
            ("netbanking", 0.2), ("upi", 0.2), ("transaction", 0.15)
        ],
        "escalation_path": [
            "Branch Manager → Regional Manager → CMD → Banking Ombudsman → RBI"
        ]
    },
    
    IssueCategory.TELECOM: {
        "departments": [
            DepartmentInfo("Telecom Service Provider", "private"),
            DepartmentInfo("TRAI", "central"),
            DepartmentInfo("DoT", "central"),
        ],
        "keywords": [
            ("mobile", 0.2), ("phone", 0.2), ("sim", 0.25),
            ("network", 0.2), ("internet", 0.2), ("broadband", 0.25),
            ("recharge", 0.15), ("bill", 0.1), ("trai", 0.3),
            ("portability", 0.2), ("dnd", 0.2), ("otp", 0.15)
        ],
        "escalation_path": [
            "Customer Care → Nodal Officer → Appellate Authority → TRAI"
        ]
    },
    
    IssueCategory.RAILWAY: {
        "departments": [
            DepartmentInfo("Railway Station", "local"),
            DepartmentInfo("Division Railway Manager", "division"),
            DepartmentInfo("Railway Board", "central"),
        ],
        "keywords": [
            ("railway", 0.3), ("train", 0.25), ("ticket", 0.2),
            ("reservation", 0.2), ("irctc", 0.3), ("tatkal", 0.25),
            ("coach", 0.15), ("station", 0.1), ("platform", 0.15),
            ("refund", 0.15), ("pnr", 0.25), ("delay", 0.1)
        ],
        "escalation_path": [
            "Station Master → DRM → GM → Railway Board"
        ]
    },
    
    IssueCategory.PASSPORT: {
        "departments": [
            DepartmentInfo("Passport Seva Kendra", "district"),
            DepartmentInfo("Regional Passport Office", "regional"),
            DepartmentInfo("Ministry of External Affairs", "central"),
        ],
        "keywords": [
            ("passport", 0.3), ("visa", 0.25), ("psk", 0.25),
            ("tatkaal passport", 0.3), ("ecr", 0.2), ("emigration", 0.2),
            ("renewal", 0.15), ("police verification", 0.2)
        ],
        "escalation_path": [
            "PSK → RPO → CPV Division → MEA"
        ]
    },
    
    IssueCategory.EMPLOYMENT: {
        "departments": [
            DepartmentInfo("Employment Exchange", "district"),
            DepartmentInfo("Labour Department", "state"),
            DepartmentInfo("EPFO", "central"),
        ],
        "keywords": [
            ("employment", 0.25), ("job", 0.2), ("recruitment", 0.2),
            ("labour", 0.2), ("epfo", 0.3), ("provident fund", 0.25),
            ("esic", 0.25), ("minimum wage", 0.25), ("factory", 0.15)
        ],
        "escalation_path": [
            "District Employment Officer → Labour Commissioner → Secretary"
        ]
    },
    
    IssueCategory.SOCIAL_WELFARE: {
        "departments": [
            DepartmentInfo("Social Welfare Department", "state"),
            DepartmentInfo("Women & Child Development", "state"),
            DepartmentInfo("Disability Commissioner", "state"),
        ],
        "keywords": [
            ("disability", 0.25), ("handicapped", 0.2), ("scholarship", 0.2),
            ("widow", 0.2), ("orphan", 0.2), ("senior citizen", 0.25),
            ("women", 0.1), ("child", 0.1), ("caste certificate", 0.25),
            ("income certificate", 0.25), ("domicile", 0.2)
        ],
        "escalation_path": [
            "Welfare Officer → District Officer → Director → Secretary"
        ]
    },
    
    IssueCategory.ENVIRONMENT: {
        "departments": [
            DepartmentInfo("Pollution Control Board", "state"),
            DepartmentInfo("Environment Department", "state"),
            DepartmentInfo("Forest Department", "state"),
            DepartmentInfo("NGT", "central"),
        ],
        "keywords": [
            ("pollution", 0.3), ("environment", 0.25), ("forest", 0.25),
            ("air quality", 0.25), ("noise", 0.2), ("waste", 0.2),
            ("industrial", 0.15), ("effluent", 0.2), ("tree", 0.1),
            ("wildlife", 0.2), ("ngt", 0.3)
        ],
        "escalation_path": [
            "District Officer → Regional Officer → Chairman PCB → NGT"
        ]
    },
}


def map_issue_to_department(text: str) -> Dict:
    """
    Map user's issue description to relevant departments.
    Returns matched departments with confidence.
    
    This is the PRIMARY decision function for issue categorization.
    """
    result = map_issue_detailed(text)
    
    return {
        "matches": [m.to_dict() for m in result[:3]],
        "primary_category": result[0].category.value if result else None,
        "primary_departments": [d.name for d in result[0].departments] if result else []
    }


def map_issue_detailed(text: str) -> List[IssueMatch]:
    """
    Detailed issue mapping with full audit trail.
    Returns list of IssueMatch objects sorted by confidence.
    """
    text_lower = text.lower()
    matches = []
    
    for category, data in ISSUE_DEPARTMENT_MAP.items():
        keywords_found = []
        total_weight = 0.0
        
        for keyword, weight in data["keywords"]:
            if keyword in text_lower:
                keywords_found.append(keyword)
                total_weight += weight
        
        if keywords_found:
            # Calculate confidence (base + weights, capped at 0.95)
            confidence = min(0.95, 0.3 + total_weight + len(keywords_found) * 0.02)
            
            matches.append(IssueMatch(
                category=category,
                confidence=confidence,
                keywords_matched=keywords_found,
                departments=data["departments"],
                suggested_authority=data["departments"][0].name,
                escalation_path=data["escalation_path"]
            ))
    
    # Sort by confidence
    matches.sort(key=lambda x: x.confidence, reverse=True)
    
    # If no matches, return general category
    if not matches:
        general_data = ISSUE_DEPARTMENT_MAP.get(IssueCategory.GENERAL, {
            "departments": [DepartmentInfo("Grievance Cell", "state")],
            "escalation_path": ["District Officer → State Level"]
        })
        matches.append(IssueMatch(
            category=IssueCategory.GENERAL,
            confidence=0.3,
            keywords_matched=[],
            departments=general_data.get("departments", []),
            suggested_authority="District Grievance Cell",
            escalation_path=general_data.get("escalation_path", [])
        ))
    
    return matches


def get_department_by_category(category: str) -> List[Dict[str, Any]]:
    """Get departments for a specific category"""
    try:
        cat = IssueCategory(category.lower())
    except ValueError:
        return []
    
    data = ISSUE_DEPARTMENT_MAP.get(cat)
    if not data:
        return []
    
    return [
        {
            "name": d.name,
            "level": d.level,
            "grievance_portal": d.grievance_portal,
            "response_days": d.typical_response_days
        }
        for d in data["departments"]
    ]


def get_escalation_path(category: str) -> List[str]:
    """Get escalation path for a category"""
    try:
        cat = IssueCategory(category.lower())
    except ValueError:
        return []
    
    data = ISSUE_DEPARTMENT_MAP.get(cat)
    return data.get("escalation_path", []) if data else []


def get_all_categories() -> List[Dict[str, str]]:
    """Get list of all supported issue categories"""
    return [
        {
            "value": cat.value,
            "label": cat.value.replace("_", " ").title(),
            "department_count": len(ISSUE_DEPARTMENT_MAP.get(cat, {}).get("departments", []))
        }
        for cat in IssueCategory
        if cat in ISSUE_DEPARTMENT_MAP
    ]


def suggest_categories(text: str, top_n: int = 3) -> List[Dict[str, Any]]:
    """
    Suggest categories for user selection.
    Useful when confidence is low.
    """
    matches = map_issue_detailed(text)
    
    suggestions = []
    for match in matches[:top_n]:
        suggestions.append({
            "category": match.category.value,
            "confidence": round(match.confidence, 2),
            "keywords_found": match.keywords_matched[:5],
            "primary_department": match.suggested_authority
        })
    
    return suggestions
