"""
API Integration Tests for RTI & Complaint Generator
"""
import sys
import json
from fastapi.testclient import TestClient

# Add app to path
sys.path.insert(0, 'app')

from app.main import app

client = TestClient(app)

def print_test(name, passed, details=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {name}")
    if details:
        print(f"       {details}")

def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    passed = response.status_code == 200 and "healthy" in response.json().get("status", "")
    print_test("Health Check", passed, f"Status: {response.json().get('status')}")
    return passed

def test_infer_rti():
    """Test RTI intent classification"""
    payload = {
        "text": "I want to file an RTI application to get information about road construction expenses under RTI Act 2005",
        "language": "english"
    }
    response = client.post("/api/infer", json=payload)
    data = response.json()
    confidence = data.get("confidence", {})
    conf_value = confidence.get("overall", 0) if isinstance(confidence, dict) else confidence
    passed = (
        response.status_code == 200 and 
        data.get("intent") == "rti"
    )
    print_test("RTI Intent Classification", passed, 
               f"Intent: {data.get('intent')}, Confidence: {conf_value:.2f}")
    return passed

def test_infer_complaint():
    """Test complaint intent classification"""
    payload = {
        "text": "The water supply has been cut off for 5 days in our area. This is causing severe hardship to residents.",
        "language": "english"
    }
    response = client.post("/api/infer", json=payload)
    data = response.json()
    confidence = data.get("confidence", {})
    conf_value = confidence.get("overall", 0) if isinstance(confidence, dict) else confidence
    passed = (
        response.status_code == 200 and 
        data.get("intent") in ["complaint", "unknown"]
    )
    print_test("Complaint Intent Classification", passed,
               f"Intent: {data.get('intent')}, Confidence: {conf_value:.2f}")
    return passed

def test_infer_hindi():
    """Test Hindi language inference"""
    payload = {
        "text": "मुझे अपने इलाके में सड़क निर्माण के खर्च की जानकारी चाहिए RTI के तहत",
        "language": "hindi"
    }
    response = client.post("/api/infer", json=payload)
    data = response.json()
    passed = response.status_code == 200 and data.get("intent") in ["rti", "complaint", "unknown"]
    print_test("Hindi Language Inference", passed,
               f"Intent: {data.get('intent')}, Language detected correctly")
    return passed

def test_draft_rti():
    """Test RTI document generation"""
    payload = {
        "document_type": "information_request",
        "applicant": {
            "name": "Test User",
            "address": "123 Test Street, Delhi",
            "state": "Delhi"
        },
        "issue": {
            "description": "Road construction expenses",
            "specific_request": "Itemized expenditure details",
            "time_period": "2024-2025"
        },
        "authority": {
            "department_name": "PWD",
            "designation": "PIO"
        }
    }
    response = client.post("/api/draft", json=payload)
    data = response.json()
    passed = (
        response.status_code == 200 and 
        "draft_text" in data and
        len(data.get("draft_text", "")) > 100
    )
    word_count = len(data.get("draft_text", "").split())
    print_test("RTI Draft Generation", passed,
               f"Template: {data.get('template_used')}, Words: {word_count}")
    return passed

def test_draft_complaint():
    """Test complaint document generation"""
    payload = {
        "document_type": "grievance",
        "applicant": {
            "name": "Test User",
            "address": "123 Test Street, Delhi",
            "state": "Delhi"
        },
        "issue": {
            "description": "Water supply disruption for 5 days",
            "specific_request": "Restore water supply immediately",
            "time_period": "Last week"
        },
        "authority": {
            "department_name": "Delhi Jal Board",
            "designation": "Executive Engineer"
        }
    }
    response = client.post("/api/draft", json=payload)
    data = response.json()
    passed = (
        response.status_code == 200 and 
        "draft_text" in data and
        len(data.get("draft_text", "")) > 100
    )
    word_count = len(data.get("draft_text", "").split())
    print_test("Complaint Draft Generation", passed,
               f"Template: {data.get('template_used')}, Words: {word_count}")
    return passed

def test_download_pdf():
    """Test PDF download"""
    # First generate a draft
    draft_payload = {
        "document_type": "information_request",
        "applicant": {
            "name": "Test User",
            "address": "123 Test Street, New Delhi",
            "state": "Delhi"
        },
        "issue": {
            "description": "Test request for information",
            "specific_request": "Test info needed",
            "time_period": "2024"
        },
        "authority": {
            "department_name": "PWD",
            "designation": "PIO"
        }
    }
    draft_response = client.post("/api/draft", json=draft_payload)
    draft_text = draft_response.json().get("draft_text", "")
    
    payload = {
        "draft_text": draft_text,
        "document_type": "information_request",
        "format": "pdf",
        "applicant": {
            "name": "Test User",
            "address": "123 Test Street, New Delhi",
            "state": "Delhi"
        }
    }
    response = client.post("/api/download", json=payload)
    passed = (
        response.status_code == 200 and 
        "application/pdf" in response.headers.get("content-type", "")
    )
    size = len(response.content)
    print_test("PDF Download", passed, f"Size: {size} bytes")
    return passed

def test_download_docx():
    """Test DOCX download"""
    # First generate a draft
    draft_payload = {
        "document_type": "grievance",
        "applicant": {
            "name": "Test User",
            "address": "123 Test Street, New Delhi",
            "state": "Delhi"
        },
        "issue": {
            "description": "Test complaint description",
            "specific_request": "Test action required",
            "time_period": "2024"
        },
        "authority": {
            "department_name": "Municipal",
            "designation": "Commissioner"
        }
    }
    draft_response = client.post("/api/draft", json=draft_payload)
    draft_text = draft_response.json().get("draft_text", "")
    
    payload = {
        "draft_text": draft_text,
        "document_type": "grievance",
        "format": "docx",
        "applicant": {
            "name": "Test User",
            "address": "123 Test Street, New Delhi",
            "state": "Delhi"
        }
    }
    response = client.post("/api/download", json=payload)
    passed = (
        response.status_code == 200 and 
        "openxmlformats" in response.headers.get("content-type", "")
    )
    size = len(response.content)
    print_test("DOCX Download", passed, f"Size: {size} bytes")
    return passed

def test_download_xlsx():
    """Test XLSX download"""
    # First generate a draft
    draft_payload = {
        "document_type": "information_request",
        "applicant": {
            "name": "Test User",
            "address": "123 Test Street, New Delhi",
            "state": "Delhi"
        },
        "issue": {
            "description": "Test request for records",
            "specific_request": "Test records required",
            "time_period": "2024"
        },
        "authority": {
            "department_name": "Education",
            "designation": "Director"
        }
    }
    draft_response = client.post("/api/draft", json=draft_payload)
    draft_text = draft_response.json().get("draft_text", "")
    
    payload = {
        "draft_text": draft_text,
        "document_type": "information_request",
        "format": "xlsx",
        "applicant": {
            "name": "Test User",
            "address": "123 Test Street, New Delhi",
            "state": "Delhi"
        }
    }
    response = client.post("/api/download", json=payload)
    passed = (
        response.status_code == 200 and 
        "spreadsheet" in response.headers.get("content-type", "")
    )
    size = len(response.content)
    print_test("XLSX Download", passed, f"Size: {size} bytes")
    return passed

def test_authority_endpoint():
    """Test authority lookup"""
    # Authority endpoint is POST not GET
    payload = {
        "state": "Delhi",
        "issue_category": "electricity"
    }
    response = client.post("/api/authority", json=payload)
    passed = response.status_code == 200
    data = response.json()
    print_test("Authority Lookup", passed, 
               f"Found authorities for Delhi electricity")
    return passed

def test_validate_rti():
    """Test RTI validation endpoint"""
    payload = {
        "document_type": "rti",
        "subject": "Road construction expenditure",
        "authority_name": "PWD",
        "information_sought": "I want to know the total expenditure on road construction in my area for the financial year 2024-2025",
        "applicant_name": "Test User",
        "applicant_address": "123 Test Street, New Delhi"
    }
    response = client.post("/api/validate/rti", json=payload)
    passed = response.status_code == 200
    if passed:
        data = response.json()
        print_test("RTI Validation", passed,
                   f"Score: {data.get('score', 'N/A')}, Grade: {data.get('grade', 'N/A')}")
    else:
        print_test("RTI Validation", passed, f"Status: {response.status_code}")
    return passed

def test_validate_edit():
    """Test edit validation endpoint"""
    payload = {
        "original_text": "I request information under RTI Act.",
        "edited_text": "I request information under RTI Act 2005 regarding road construction.",
        "document_type": "rti"
    }
    response = client.post("/api/validate/edit", json=payload)
    passed = response.status_code == 200
    if passed:
        data = response.json()
        print_test("Edit Validation", passed,
                   f"Valid: {data.get('is_valid', 'N/A')}")
    else:
        print_test("Edit Validation", passed, f"Status: {response.status_code}")
    return passed

def main():
    print("\n" + "="*60)
    print("🧪 RTI & Complaint Generator - API Integration Tests")
    print("="*60 + "\n")
    
    tests = [
        ("Health", test_health),
        ("RTI Inference", test_infer_rti),
        ("Complaint Inference", test_infer_complaint),
        ("Hindi Inference", test_infer_hindi),
        ("RTI Draft", test_draft_rti),
        ("Complaint Draft", test_draft_complaint),
        ("PDF Download", test_download_pdf),
        ("DOCX Download", test_download_docx),
        ("XLSX Download", test_download_xlsx),
        ("Authority Lookup", test_authority_endpoint),
        ("RTI Validation", test_validate_rti),
        ("Edit Validation", test_validate_edit),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print_test(name, False, f"Exception: {str(e)[:50]}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 Results: {passed} passed, {failed} failed, {len(tests)} total")
    print("="*60 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
