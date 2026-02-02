"""
Authority Resolver
Deterministic mapping: Issue → Department → Authority

This module uses RULES ONLY to resolve authorities.
AI is NOT used for guessing authorities - only for entity hints from spaCy.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger


class AuthorityLevel(str, Enum):
    """Hierarchy levels for authorities"""
    LOCAL = "local"           # Block/Ward level
    DISTRICT = "district"     # District level
    STATE = "state"           # State level
    CENTRAL = "central"       # Central government


@dataclass
class Authority:
    """Represents a government authority"""
    name: str
    designation: str
    department: str
    level: AuthorityLevel
    address_template: str
    rti_fee: int = 10  # Default RTI fee in INR
    email_pattern: Optional[str] = None
    phone_pattern: Optional[str] = None
    website: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class AuthorityMatch:
    """Result of authority resolution"""
    authority: Authority
    confidence: float
    match_reason: str
    is_primary: bool = False


@dataclass
class ResolutionResult:
    """Complete resolution result"""
    matches: List[AuthorityMatch]
    primary: Optional[AuthorityMatch]
    category: str
    department: str
    suggestions: List[str] = field(default_factory=list)
    requires_state_selection: bool = False


# =============================================================================
# AUTHORITY DATABASE
# This is the deterministic mapping - NO AI DECISIONS
# =============================================================================

DEPARTMENT_AUTHORITIES: Dict[str, Dict[str, Authority]] = {
    # -------------------------------------------------------------------------
    # ELECTRICITY
    # -------------------------------------------------------------------------
    "electricity": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO, Electricity Department",
            department="State Electricity Board / DISCOM",
            level=AuthorityLevel.STATE,
            address_template="{state} State Electricity Board, {district}",
            notes="For RTI applications related to electricity"
        ),
        "ae": Authority(
            name="Assistant Engineer",
            designation="Assistant Engineer (Electrical)",
            department="State Electricity Board",
            level=AuthorityLevel.LOCAL,
            address_template="Assistant Engineer Office, {area}, {district}",
            notes="For local electrical complaints"
        ),
        "se": Authority(
            name="Superintending Engineer",
            designation="Superintending Engineer",
            department="State Electricity Board",
            level=AuthorityLevel.DISTRICT,
            address_template="SE Office, {district} Circle",
            notes="For escalated complaints"
        ),
        "grievance": Authority(
            name="Consumer Grievance Redressal Forum",
            designation="Chairman, CGRF",
            department="State Electricity Regulatory Commission",
            level=AuthorityLevel.STATE,
            address_template="CGRF, {state} Electricity Regulatory Commission",
            notes="For unresolved consumer complaints"
        ),
    },
    
    # -------------------------------------------------------------------------
    # WATER SUPPLY
    # -------------------------------------------------------------------------
    "water": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO, Water Supply Department",
            department="Jal Board / Municipal Corporation",
            level=AuthorityLevel.DISTRICT,
            address_template="{state} Jal Board, {district}",
        ),
        "je": Authority(
            name="Junior Engineer",
            designation="Junior Engineer (Water Supply)",
            department="Municipal Corporation / Jal Board",
            level=AuthorityLevel.LOCAL,
            address_template="JE Office, Water Supply Division, {area}",
            notes="For local water supply issues"
        ),
        "ee": Authority(
            name="Executive Engineer",
            designation="Executive Engineer (Water)",
            department="Jal Board",
            level=AuthorityLevel.DISTRICT,
            address_template="EE Office, {district} Division",
            notes="For district-level water issues"
        ),
    },
    
    # -------------------------------------------------------------------------
    # ROADS & PWD
    # -------------------------------------------------------------------------
    "roads": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO, PWD",
            department="Public Works Department",
            level=AuthorityLevel.STATE,
            address_template="PWD Secretariat, {state}",
        ),
        "je": Authority(
            name="Junior Engineer",
            designation="Junior Engineer (Roads)",
            department="PWD / Municipal Corporation",
            level=AuthorityLevel.LOCAL,
            address_template="PWD Sub-Division, {area}, {district}",
            notes="For local road repair complaints"
        ),
        "ee": Authority(
            name="Executive Engineer",
            designation="Executive Engineer (Roads)",
            department="PWD",
            level=AuthorityLevel.DISTRICT,
            address_template="PWD Division Office, {district}",
        ),
        "nhai": Authority(
            name="Project Director",
            designation="Project Director, NHAI",
            department="National Highways Authority of India",
            level=AuthorityLevel.CENTRAL,
            address_template="NHAI Project Office, {state}",
            notes="For national highway issues"
        ),
    },
    
    # -------------------------------------------------------------------------
    # EDUCATION
    # -------------------------------------------------------------------------
    "education": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO, Education Department",
            department="Directorate of Education",
            level=AuthorityLevel.STATE,
            address_template="Directorate of Education, {state}",
        ),
        "deo": Authority(
            name="District Education Officer",
            designation="DEO",
            department="Education Department",
            level=AuthorityLevel.DISTRICT,
            address_template="DEO Office, {district}",
            notes="For school-related issues"
        ),
        "principal": Authority(
            name="Principal",
            designation="Principal / Headmaster",
            department="Government School",
            level=AuthorityLevel.LOCAL,
            address_template="Government School, {area}, {district}",
        ),
    },
    
    # -------------------------------------------------------------------------
    # HEALTH
    # -------------------------------------------------------------------------
    "health": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO, Health Department",
            department="Directorate of Health Services",
            level=AuthorityLevel.STATE,
            address_template="Directorate of Health Services, {state}",
        ),
        "cmo": Authority(
            name="Chief Medical Officer",
            designation="CMO",
            department="District Health Department",
            level=AuthorityLevel.DISTRICT,
            address_template="CMO Office, {district}",
            notes="For district health complaints"
        ),
        "medical_superintendent": Authority(
            name="Medical Superintendent",
            designation="Medical Superintendent",
            department="District / Government Hospital",
            level=AuthorityLevel.DISTRICT,
            address_template="Government Hospital, {district}",
        ),
    },
    
    # -------------------------------------------------------------------------
    # POLICE
    # -------------------------------------------------------------------------
    "police": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO, Police Department",
            department="Police Headquarters",
            level=AuthorityLevel.STATE,
            address_template="Police Headquarters, {state}",
        ),
        "sho": Authority(
            name="Station House Officer",
            designation="SHO",
            department="Police Station",
            level=AuthorityLevel.LOCAL,
            address_template="Police Station, {area}, {district}",
            notes="For FIR and local law enforcement"
        ),
        "sp": Authority(
            name="Superintendent of Police",
            designation="SP",
            department="District Police",
            level=AuthorityLevel.DISTRICT,
            address_template="SP Office, {district}",
            notes="For escalated police complaints"
        ),
        "ig": Authority(
            name="Inspector General of Police",
            designation="IG",
            department="Police Range",
            level=AuthorityLevel.STATE,
            address_template="IG Office, {state}",
        ),
    },
    
    # -------------------------------------------------------------------------
    # LAND & REVENUE
    # -------------------------------------------------------------------------
    "land": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO, Revenue Department",
            department="Revenue Department",
            level=AuthorityLevel.STATE,
            address_template="Revenue Secretariat, {state}",
        ),
        "tehsildar": Authority(
            name="Tehsildar",
            designation="Tehsildar / Naib Tehsildar",
            department="Revenue Department",
            level=AuthorityLevel.LOCAL,
            address_template="Tehsil Office, {area}, {district}",
            notes="For land records, mutations, revenue issues"
        ),
        "sdo": Authority(
            name="Sub-Divisional Officer",
            designation="SDO (Revenue)",
            department="Revenue Department",
            level=AuthorityLevel.DISTRICT,
            address_template="SDO Office, {district}",
        ),
        "collector": Authority(
            name="District Collector",
            designation="Collector & District Magistrate",
            department="District Administration",
            level=AuthorityLevel.DISTRICT,
            address_template="Collectorate, {district}",
            notes="For major land disputes and escalations"
        ),
    },
    
    # -------------------------------------------------------------------------
    # TRANSPORT / RTO
    # -------------------------------------------------------------------------
    "transport": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO, Transport Department",
            department="Transport Department",
            level=AuthorityLevel.STATE,
            address_template="Transport Commissioner Office, {state}",
        ),
        "rto": Authority(
            name="Regional Transport Officer",
            designation="RTO",
            department="Regional Transport Office",
            level=AuthorityLevel.DISTRICT,
            address_template="RTO Office, {district}",
            notes="For license, registration, permits"
        ),
        "arto": Authority(
            name="Assistant Regional Transport Officer",
            designation="ARTO",
            department="Regional Transport Office",
            level=AuthorityLevel.DISTRICT,
            address_template="RTO Office, {district}",
        ),
    },
    
    # -------------------------------------------------------------------------
    # RATION / PDS
    # -------------------------------------------------------------------------
    "ration": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO, Food & Civil Supplies",
            department="Food & Civil Supplies Department",
            level=AuthorityLevel.STATE,
            address_template="Food & Civil Supplies Directorate, {state}",
        ),
        "fso": Authority(
            name="Food & Supply Officer",
            designation="FSO / DFSO",
            department="Food & Civil Supplies",
            level=AuthorityLevel.DISTRICT,
            address_template="FSO Office, {district}",
            notes="For ration card, PDS shop issues"
        ),
        "inspector": Authority(
            name="Food Inspector",
            designation="Food Inspector",
            department="Food & Civil Supplies",
            level=AuthorityLevel.LOCAL,
            address_template="FSO Office, {area}, {district}",
        ),
    },
    
    # -------------------------------------------------------------------------
    # PENSION
    # -------------------------------------------------------------------------
    "pension": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO, Pension Department",
            department="Pension & Pensioners Welfare",
            level=AuthorityLevel.STATE,
            address_template="Pension Directorate, {state}",
        ),
        "treasury": Authority(
            name="Treasury Officer",
            designation="District Treasury Officer",
            department="Treasury Department",
            level=AuthorityLevel.DISTRICT,
            address_template="District Treasury, {district}",
            notes="For pension disbursement issues"
        ),
    },
    
    # -------------------------------------------------------------------------
    # MUNICIPAL / CIVIC
    # -------------------------------------------------------------------------
    "municipal": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO, Municipal Corporation",
            department="Municipal Corporation / Nagar Palika",
            level=AuthorityLevel.DISTRICT,
            address_template="Municipal Corporation, {district}",
        ),
        "commissioner": Authority(
            name="Municipal Commissioner",
            designation="Commissioner",
            department="Municipal Corporation",
            level=AuthorityLevel.DISTRICT,
            address_template="Municipal Corporation, {district}",
            notes="For major civic issues"
        ),
        "health_officer": Authority(
            name="Municipal Health Officer",
            designation="MHO",
            department="Municipal Corporation",
            level=AuthorityLevel.DISTRICT,
            address_template="Municipal Corporation, {district}",
            notes="For sanitation, health hazards"
        ),
    },
    
    # -------------------------------------------------------------------------
    # GENERAL / FALLBACK
    # -------------------------------------------------------------------------
    "general": {
        "pio": Authority(
            name="Public Information Officer",
            designation="PIO",
            department="Concerned Department",
            level=AuthorityLevel.STATE,
            address_template="Secretariat, {state}",
        ),
        "collector": Authority(
            name="District Collector",
            designation="Collector & District Magistrate",
            department="District Administration",
            level=AuthorityLevel.DISTRICT,
            address_template="Collectorate, {district}",
            notes="For general grievances"
        ),
        "grievance": Authority(
            name="Grievance Cell",
            designation="Officer In-Charge, Grievance Cell",
            department="Chief Minister's Office / District Administration",
            level=AuthorityLevel.STATE,
            address_template="CM Grievance Cell, {state}",
        ),
    },
}


# =============================================================================
# STATE-SPECIFIC INFORMATION
# =============================================================================

STATE_INFO: Dict[str, Dict[str, str]] = {
    "andhra_pradesh": {"capital": "Amaravati", "code": "AP"},
    "arunachal_pradesh": {"capital": "Itanagar", "code": "AR"},
    "assam": {"capital": "Dispur", "code": "AS"},
    "bihar": {"capital": "Patna", "code": "BR"},
    "chhattisgarh": {"capital": "Raipur", "code": "CG"},
    "goa": {"capital": "Panaji", "code": "GA"},
    "gujarat": {"capital": "Gandhinagar", "code": "GJ"},
    "haryana": {"capital": "Chandigarh", "code": "HR"},
    "himachal_pradesh": {"capital": "Shimla", "code": "HP"},
    "jharkhand": {"capital": "Ranchi", "code": "JH"},
    "karnataka": {"capital": "Bengaluru", "code": "KA"},
    "kerala": {"capital": "Thiruvananthapuram", "code": "KL"},
    "madhya_pradesh": {"capital": "Bhopal", "code": "MP"},
    "maharashtra": {"capital": "Mumbai", "code": "MH"},
    "manipur": {"capital": "Imphal", "code": "MN"},
    "meghalaya": {"capital": "Shillong", "code": "ML"},
    "mizoram": {"capital": "Aizawl", "code": "MZ"},
    "nagaland": {"capital": "Kohima", "code": "NL"},
    "odisha": {"capital": "Bhubaneswar", "code": "OD"},
    "punjab": {"capital": "Chandigarh", "code": "PB"},
    "rajasthan": {"capital": "Jaipur", "code": "RJ"},
    "sikkim": {"capital": "Gangtok", "code": "SK"},
    "tamil_nadu": {"capital": "Chennai", "code": "TN"},
    "telangana": {"capital": "Hyderabad", "code": "TG"},
    "tripura": {"capital": "Agartala", "code": "TR"},
    "uttar_pradesh": {"capital": "Lucknow", "code": "UP"},
    "uttarakhand": {"capital": "Dehradun", "code": "UK"},
    "west_bengal": {"capital": "Kolkata", "code": "WB"},
    "delhi": {"capital": "New Delhi", "code": "DL"},
}


def _normalize_state(state: str) -> str:
    """Normalize state name for lookup"""
    return state.lower().replace(" ", "_").replace("-", "_")


def _format_address(template: str, state: str, district: Optional[str], area: Optional[str]) -> str:
    """Format address template with location details"""
    address = template
    
    # Format state name
    state_display = state.replace("_", " ").title()
    address = address.replace("{state}", state_display)
    
    # Format district
    district_display = district.title() if district else "[District]"
    address = address.replace("{district}", district_display)
    
    # Format area
    area_display = area.title() if area else "[Area/Locality]"
    address = address.replace("{area}", area_display)
    
    return address


def resolve_authority(
    category: str,
    state: str,
    district: Optional[str] = None,
    area: Optional[str] = None,
    is_rti: bool = True,
    extracted_entities: Optional[Dict] = None
) -> ResolutionResult:
    """
    Resolve appropriate authority for an issue.
    
    This is DETERMINISTIC - no AI guessing.
    
    Args:
        category: Issue category (electricity, water, etc.)
        state: State name
        district: District name (optional)
        area: Local area (optional)
        is_rti: True for RTI, False for Complaint
        extracted_entities: Entities extracted by spaCy (hints only)
    
    Returns:
        ResolutionResult with matched authorities
    """
    logger.info(f"Resolving authority for category={category}, state={state}, is_rti={is_rti}")
    
    # Normalize inputs
    category = category.lower().strip()
    state_normalized = _normalize_state(state)
    
    # Get department authorities
    dept_authorities = DEPARTMENT_AUTHORITIES.get(category, DEPARTMENT_AUTHORITIES["general"])
    
    matches: List[AuthorityMatch] = []
    suggestions: List[str] = []
    
    # For RTI - always recommend PIO first
    if is_rti and "pio" in dept_authorities:
        pio = dept_authorities["pio"]
        formatted_address = _format_address(pio.address_template, state, district, area)
        
        matches.append(AuthorityMatch(
            authority=Authority(
                name=pio.name,
                designation=pio.designation,
                department=pio.department,
                level=pio.level,
                address_template=formatted_address,
                rti_fee=pio.rti_fee,
                notes=pio.notes
            ),
            confidence=0.95,
            match_reason="PIO is the designated officer for RTI applications",
            is_primary=True
        ))
        
        suggestions.append("RTI applications should be addressed to the Public Information Officer (PIO)")
        suggestions.append(f"RTI fee: Rs. {pio.rti_fee}/- via IPO/DD/Online")
    
    # For Complaints - recommend appropriate level based on context
    else:
        # Start with local level for complaints
        local_keys = ["je", "sho", "inspector", "tehsildar", "ae"]
        district_keys = ["ee", "sp", "cmo", "rto", "sdo", "fso", "deo"]
        
        # Check if this seems like an escalation
        is_escalation = False
        if extracted_entities:
            text_hints = str(extracted_entities).lower()
            escalation_words = ["no response", "ignored", "months", "escalate", "higher"]
            is_escalation = any(word in text_hints for word in escalation_words)
        
        if is_escalation:
            # For escalations, go to district level directly
            for key in district_keys:
                if key in dept_authorities:
                    auth = dept_authorities[key]
                    formatted_address = _format_address(auth.address_template, state, district, area)
                    matches.append(AuthorityMatch(
                        authority=Authority(
                            name=auth.name,
                            designation=auth.designation,
                            department=auth.department,
                            level=auth.level,
                            address_template=formatted_address,
                            notes=auth.notes
                        ),
                        confidence=0.85,
                        match_reason="District-level authority for escalated complaints",
                        is_primary=len(matches) == 0
                    ))
                    break
            
            suggestions.append("For escalated complaints, consider mentioning previous complaint details")
        else:
            # For new complaints, start at local level
            for key in local_keys:
                if key in dept_authorities:
                    auth = dept_authorities[key]
                    formatted_address = _format_address(auth.address_template, state, district, area)
                    matches.append(AuthorityMatch(
                        authority=Authority(
                            name=auth.name,
                            designation=auth.designation,
                            department=auth.department,
                            level=auth.level,
                            address_template=formatted_address,
                            notes=auth.notes
                        ),
                        confidence=0.85,
                        match_reason="Local-level authority for new complaints",
                        is_primary=True
                    ))
                    break
    
    # Add fallback options
    if "grievance" in dept_authorities and len(matches) < 3:
        grievance = dept_authorities["grievance"]
        formatted_address = _format_address(grievance.address_template, state, district, area)
        matches.append(AuthorityMatch(
            authority=Authority(
                name=grievance.name,
                designation=grievance.designation,
                department=grievance.department,
                level=grievance.level,
                address_template=formatted_address,
                notes=grievance.notes
            ),
            confidence=0.7,
            match_reason="Grievance redressal forum as alternative",
            is_primary=False
        ))
    
    # Add collector as final fallback
    if category != "general" and len(matches) < 3:
        collector = DEPARTMENT_AUTHORITIES["general"]["collector"]
        formatted_address = _format_address(collector.address_template, state, district, area)
        matches.append(AuthorityMatch(
            authority=Authority(
                name=collector.name,
                designation=collector.designation,
                department=collector.department,
                level=collector.level,
                address_template=formatted_address,
                notes=collector.notes
            ),
            confidence=0.6,
            match_reason="District Collector as general authority",
            is_primary=False
        ))
    
    # Determine primary
    primary = next((m for m in matches if m.is_primary), matches[0] if matches else None)
    
    # Check if state selection needed
    requires_state = state_normalized not in STATE_INFO
    if requires_state:
        suggestions.append("Please verify your state name for accurate authority details")
    
    return ResolutionResult(
        matches=matches,
        primary=primary,
        category=category,
        department=dept_authorities.get("pio", dept_authorities.get("grievance", Authority(
            name="", designation="", department="General", level=AuthorityLevel.STATE, address_template=""
        ))).department,
        suggestions=suggestions,
        requires_state_selection=requires_state
    )


def get_all_categories() -> List[str]:
    """Get list of all supported issue categories"""
    return list(DEPARTMENT_AUTHORITIES.keys())


def get_all_states() -> List[Dict[str, str]]:
    """Get list of all supported states"""
    return [
        {"name": state.replace("_", " ").title(), "code": info["code"]}
        for state, info in STATE_INFO.items()
    ]
