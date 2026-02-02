"""
Unit tests for Issue Rules Engine - Self-contained version
Tests the issue-to-department mapping functionality
"""

import pytest
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any


# ============================================================================
# INLINE DEFINITIONS
# ============================================================================

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
    """Department information"""
    name: str
    level: str
    parent_department: Optional[str] = None
    grievance_portal: Optional[str] = None
    typical_response_days: int = 30


@dataclass
class IssueMatch:
    """Issue match result"""
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


# Issue-department mapping
ISSUE_DEPARTMENT_MAP = {
    IssueCategory.ELECTRICITY: {
        "departments": [
            DepartmentInfo("State Electricity Board", "state"),
            DepartmentInfo("DISCOM", "state"),
        ],
        "keywords": [
            ("electricity", 0.3), ("power", 0.2), ("meter", 0.2),
            ("power cut", 0.25), ("transformer", 0.2), ("voltage", 0.2),
        ],
        "escalation_path": ["Junior Engineer → Executive Engineer → Chief Engineer"]
    },
    IssueCategory.WATER: {
        "departments": [
            DepartmentInfo("Water Supply Department", "state"),
            DepartmentInfo("Jal Board", "state"),
        ],
        "keywords": [
            ("water", 0.3), ("water supply", 0.3), ("pipeline", 0.25),
            ("sewage", 0.2), ("drainage", 0.2), ("jal board", 0.3),
        ],
        "escalation_path": ["AE Water → EE Water → Chief Engineer"]
    },
    IssueCategory.ROADS: {
        "departments": [
            DepartmentInfo("Public Works Department (PWD)", "state"),
            DepartmentInfo("NHAI", "central"),
        ],
        "keywords": [
            ("road", 0.3), ("pothole", 0.3), ("highway", 0.25),
            ("pwd", 0.3), ("nhai", 0.3), ("street light", 0.2),
        ],
        "escalation_path": ["AE PWD → EE PWD → Chief Engineer"]
    },
    IssueCategory.EDUCATION: {
        "departments": [
            DepartmentInfo("Department of Education", "state"),
            DepartmentInfo("District Education Officer", "district"),
        ],
        "keywords": [
            ("school", 0.3), ("college", 0.25), ("education", 0.25),
            ("admission", 0.2), ("fees", 0.15), ("certificate", 0.15),
        ],
        "escalation_path": ["BEO → DEO → Director Education"]
    },
    IssueCategory.HEALTH: {
        "departments": [
            DepartmentInfo("Department of Health", "state"),
            DepartmentInfo("District CMO", "district"),
        ],
        "keywords": [
            ("hospital", 0.3), ("doctor", 0.25), ("health", 0.25),
            ("medicine", 0.2), ("clinic", 0.2), ("treatment", 0.2),
        ],
        "escalation_path": ["CMO → Director Health"]
    },
    IssueCategory.POLICE: {
        "departments": [
            DepartmentInfo("State Police", "state"),
            DepartmentInfo("District SP", "district"),
        ],
        "keywords": [
            ("police", 0.3), ("fir", 0.3), ("theft", 0.2),
            ("crime", 0.2), ("station", 0.1),
        ],
        "escalation_path": ["SHO → DSP → SP → IG"]
    },
    IssueCategory.LAND: {
        "departments": [
            DepartmentInfo("Revenue Department", "state"),
            DepartmentInfo("Tehsildar", "district"),
        ],
        "keywords": [
            ("land", 0.3), ("property", 0.25), ("registration", 0.2),
            ("mutation", 0.25), ("registry", 0.2),
        ],
        "escalation_path": ["Tehsildar → SDM → Collector"]
    },
    IssueCategory.TRANSPORT: {
        "departments": [
            DepartmentInfo("RTO", "district"),
            DepartmentInfo("Transport Department", "state"),
        ],
        "keywords": [
            ("bus", 0.2), ("transport", 0.25), ("rto", 0.3),
            ("license", 0.2), ("driving", 0.15),
        ],
        "escalation_path": ["RTO → Transport Commissioner"]
    },
    IssueCategory.RATION: {
        "departments": [
            DepartmentInfo("Food & Civil Supplies", "state"),
            DepartmentInfo("District Supply Officer", "district"),
        ],
        "keywords": [
            ("ration", 0.3), ("pds", 0.3), ("bpl", 0.25),
            ("food", 0.1), ("kerosene", 0.2),
        ],
        "escalation_path": ["DSO → Director Food"]
    },
    IssueCategory.PENSION: {
        "departments": [
            DepartmentInfo("Pension Department", "state"),
            DepartmentInfo("AG Office", "state"),
        ],
        "keywords": [
            ("pension", 0.3), ("retirement", 0.25), ("gratuity", 0.2),
            ("old age", 0.2), ("epf", 0.25),
        ],
        "escalation_path": ["DTO → Director Pension"]
    },
    IssueCategory.MUNICIPAL: {
        "departments": [
            DepartmentInfo("Municipal Corporation", "local"),
            DepartmentInfo("Nagar Palika", "local"),
        ],
        "keywords": [
            ("garbage", 0.3), ("municipal", 0.3), ("drain", 0.2),
            ("sweeper", 0.2), ("sanitation", 0.25),
        ],
        "escalation_path": ["Ward Officer → Zonal Officer → Commissioner"]
    },
    IssueCategory.TAX: {
        "departments": [
            DepartmentInfo("Income Tax Department", "central"),
            DepartmentInfo("GST Department", "central"),
        ],
        "keywords": [
            ("tax", 0.3), ("income tax", 0.3), ("gst", 0.3),
            ("refund", 0.2), ("assessment", 0.2),
        ],
        "escalation_path": ["ITO → ACIT → CCIT"]
    },
    IssueCategory.BANKING: {
        "departments": [
            DepartmentInfo("RBI", "central"),
            DepartmentInfo("Banking Ombudsman", "central"),
        ],
        "keywords": [
            ("bank", 0.3), ("loan", 0.25), ("account", 0.2),
            ("cheque", 0.2), ("atm", 0.2),
        ],
        "escalation_path": ["Branch Manager → Regional Manager → Ombudsman"]
    },
    IssueCategory.TELECOM: {
        "departments": [
            DepartmentInfo("DOT", "central"),
            DepartmentInfo("TRAI", "central"),
        ],
        "keywords": [
            ("mobile", 0.25), ("network", 0.25), ("telecom", 0.3),
            ("bsnl", 0.3), ("tower", 0.2),
        ],
        "escalation_path": ["Nodal Officer → Appellate → TRAI"]
    },
    IssueCategory.RAILWAY: {
        "departments": [
            DepartmentInfo("Railway Board", "central"),
            DepartmentInfo("Divisional Railway Manager", "zonal"),
        ],
        "keywords": [
            ("railway", 0.3), ("train", 0.25), ("station", 0.15),
            ("ticket", 0.2), ("irctc", 0.3),
        ],
        "escalation_path": ["SM → DRM → GM → Railway Board"]
    },
    IssueCategory.PASSPORT: {
        "departments": [
            DepartmentInfo("Regional Passport Office", "regional"),
            DepartmentInfo("MEA", "central"),
        ],
        "keywords": [
            ("passport", 0.3), ("visa", 0.2), ("psk", 0.25),
            ("renewal", 0.15), ("tatkal", 0.2),
        ],
        "escalation_path": ["RPO → CPV Division → MEA"]
    },
    IssueCategory.EMPLOYMENT: {
        "departments": [
            DepartmentInfo("Labour Department", "state"),
            DepartmentInfo("Employment Exchange", "district"),
        ],
        "keywords": [
            ("employment", 0.3), ("job", 0.2), ("labour", 0.25),
            ("wage", 0.2), ("unemployment", 0.25),
        ],
        "escalation_path": ["Labour Inspector → Labour Commissioner"]
    },
    IssueCategory.SOCIAL_WELFARE: {
        "departments": [
            DepartmentInfo("Social Welfare Department", "state"),
            DepartmentInfo("District Social Welfare Officer", "district"),
        ],
        "keywords": [
            ("welfare", 0.25), ("disability", 0.2), ("widow", 0.2),
            ("scholarship", 0.2), ("caste certificate", 0.25),
        ],
        "escalation_path": ["DSWO → Director Social Welfare"]
    },
    IssueCategory.ENVIRONMENT: {
        "departments": [
            DepartmentInfo("State Pollution Control Board", "state"),
            DepartmentInfo("CPCB", "central"),
        ],
        "keywords": [
            ("pollution", 0.3), ("environment", 0.25), ("noise", 0.2),
            ("factory", 0.15), ("waste", 0.2),
        ],
        "escalation_path": ["Regional Officer → Member Secretary → Chairman"]
    },
}


def classify_issue(text: str) -> Tuple[IssueCategory, float]:
    """Classify text into issue category"""
    if not text or not text.strip():
        return IssueCategory.GENERAL, 0.0
    
    text_lower = text.lower()
    scores = {cat: 0.0 for cat in IssueCategory}
    
    for category, mapping in ISSUE_DEPARTMENT_MAP.items():
        for keyword, weight in mapping.get("keywords", []):
            if keyword in text_lower:
                scores[category] += weight
    
    best_match = max(scores.items(), key=lambda x: x[1])
    if best_match[1] == 0:
        return IssueCategory.GENERAL, 0.0
    
    return best_match[0], min(best_match[1], 1.0)


def classify_issue_detailed(text: str) -> IssueMatch:
    """Detailed issue classification"""
    category, confidence = classify_issue(text)
    text_lower = text.lower()
    
    keywords_matched = []
    if category in ISSUE_DEPARTMENT_MAP:
        mapping = ISSUE_DEPARTMENT_MAP[category]
        for keyword, weight in mapping.get("keywords", []):
            if keyword in text_lower:
                keywords_matched.append(keyword)
    
    departments = []
    escalation = []
    suggested = "General Grievance Cell"
    
    if category in ISSUE_DEPARTMENT_MAP:
        mapping = ISSUE_DEPARTMENT_MAP[category]
        departments = mapping.get("departments", [])
        escalation = mapping.get("escalation_path", [])
        if departments:
            suggested = departments[0].name
    
    return IssueMatch(
        category=category,
        confidence=confidence,
        keywords_matched=keywords_matched,
        departments=departments,
        suggested_authority=suggested,
        escalation_path=escalation
    )


def get_escalation_path(category: IssueCategory) -> List[str]:
    """Get escalation path for category"""
    if category in ISSUE_DEPARTMENT_MAP:
        return ISSUE_DEPARTMENT_MAP[category].get("escalation_path", [])
    return ["Contact General Grievance Cell"]


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_water_issue():
    return "There is no water supply in our colony. Pipeline is broken."


# ============================================================================
# TESTS
# ============================================================================

class TestIssueCategory:
    """Tests for IssueCategory enum"""
    
    def test_all_categories_defined(self):
        expected = ["electricity", "water", "roads", "education", "health",
                   "police", "land", "transport", "ration", "pension",
                   "municipal", "tax", "banking", "telecom", "railway",
                   "passport", "employment", "social_welfare", "environment", "general"]
        for cat in expected:
            assert any(c.value == cat for c in IssueCategory)
    
    def test_category_count(self):
        assert len(IssueCategory) == 20


class TestDepartmentInfo:
    """Tests for DepartmentInfo dataclass"""
    
    def test_department_creation(self):
        dept = DepartmentInfo(name="Test", level="state", typical_response_days=30)
        assert dept.name == "Test"
        assert dept.level == "state"
        assert dept.typical_response_days == 30


class TestClassifyIssue:
    """Tests for classify_issue function"""
    
    def test_electricity_issue(self):
        text = "There is no electricity in my area. Power cut for 3 days."
        category, confidence = classify_issue(text)
        assert category == IssueCategory.ELECTRICITY
        assert confidence > 0
    
    def test_water_issue(self, sample_water_issue):
        category, confidence = classify_issue(sample_water_issue)
        assert category == IssueCategory.WATER
        assert confidence > 0
    
    def test_road_issue(self):
        text = "There are multiple potholes on the highway. Road is damaged."
        category, confidence = classify_issue(text)
        assert category == IssueCategory.ROADS
        assert confidence > 0
    
    def test_education_issue(self):
        text = "School is not issuing certificate. College admission problem."
        category, confidence = classify_issue(text)
        assert category == IssueCategory.EDUCATION
        assert confidence > 0
    
    def test_health_issue(self):
        text = "Hospital refused treatment. Doctor not available in clinic."
        category, confidence = classify_issue(text)
        assert category == IssueCategory.HEALTH
        assert confidence > 0
    
    def test_police_issue(self):
        text = "Police refused to file FIR for theft."
        category, confidence = classify_issue(text)
        assert category == IssueCategory.POLICE
        assert confidence > 0
    
    def test_empty_text_returns_general(self):
        category, confidence = classify_issue("")
        assert category == IssueCategory.GENERAL
        assert confidence == 0.0
    
    def test_case_insensitivity(self):
        text1 = "ELECTRICITY POWER CUT"
        text2 = "electricity power cut"
        cat1, _ = classify_issue(text1)
        cat2, _ = classify_issue(text2)
        assert cat1 == cat2


class TestClassifyIssueDetailed:
    """Tests for classify_issue_detailed function"""
    
    def test_returns_issue_match(self):
        text = "Power cut in my area"
        result = classify_issue_detailed(text)
        assert isinstance(result, IssueMatch)
    
    def test_issue_match_fields(self):
        text = "No water supply"
        result = classify_issue_detailed(text)
        assert hasattr(result, 'category')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'keywords_matched')
        assert hasattr(result, 'departments')
    
    def test_to_dict_works(self):
        text = "School fee problem"
        result = classify_issue_detailed(text)
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert "category" in result_dict


class TestGetEscalationPath:
    """Tests for get_escalation_path function"""
    
    def test_electricity_escalation(self):
        path = get_escalation_path(IssueCategory.ELECTRICITY)
        assert isinstance(path, list)
        assert len(path) >= 1
    
    def test_general_has_path(self):
        path = get_escalation_path(IssueCategory.GENERAL)
        assert isinstance(path, list)


class TestSpecialCases:
    """Tests for special cases"""
    
    def test_abbreviations(self):
        text = "PWD not maintaining roads. NHAI should act."
        category, _ = classify_issue(text)
        assert category == IssueCategory.ROADS
    
    def test_railway_issues(self):
        text = "Train always late. Railway station not clean."
        category, _ = classify_issue(text)
        assert category == IssueCategory.RAILWAY
    
    def test_passport_issues(self):
        text = "Passport renewal delayed."
        category, _ = classify_issue(text)
        assert category == IssueCategory.PASSPORT


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
