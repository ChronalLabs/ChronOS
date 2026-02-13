import requests
import os
import sys

BASE_URL = "http://localhost:8000"

def test_flow():
    print(f"Testing API at {BASE_URL}...")
    
    # 1. Health Check
    try:
        r = requests.get(f"{BASE_URL}/docs")
        if r.status_code == 200:
            print("âœ… Backend is UP")
        else:
            print(f"â Œ Backend returned {r.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("â Œ FAILED to connect to backend. Is it running on port 8000?")
        return

    # 2. Upload Resume
    print("\n[1/4] Uploading Resume...")
    files = {'file': open('test_resume.pdf', 'rb')}
    session_id = None
    try:
        r = requests.post(f"{BASE_URL}/api/upload-resume", files=files)
        if r.status_code != 200:
            print(f"â Œ Upload failed: {r.text}")
            return
        data = r.json()
        session_id = data.get('session_id')
        print(f"âœ… Upload success. Session ID: {session_id}")
    except Exception as e:
        print(f"â Œ Upload error: {e}")
        return

    # 3. Analyze JD
    print("\n[2/4] Analyzing Job Description...")
    jd_text = "We are looking for a Senior Software Engineer with Python, FastAPI, and AWS experience. React is a plus."
    
    try:
        r = requests.post(f"{BASE_URL}/api/analyze-jd", json={"job_description": jd_text}, params={"session_id": session_id})
        if r.status_code != 200:
            print(f"â Œ JD Analysis failed: {r.text}")
            return
        print(f"âœ… JD Analysis success.")
    except Exception as e:
        print(f"â Œ JD Analysis error: {e}")
        return

    # 4. Evaluate
    print("\n[3/4] Evaluating Match...")
    try:
        r = requests.post(f"{BASE_URL}/api/evaluate", json={"session_id": session_id})
        if r.status_code != 200:
            print(f"â Œ Evaluation failed: {r.text}")
            return
        
        result = r.json().get('result', {})
        print(f"âœ… Evaluation success. Job Fit Score: {result.get('job_fit_score')}")
    except Exception as e:
        print(f"â Œ Evaluation error: {e}")
        return

    # 5. Export PDF
    print("\n[4/4] Exporting PDF...")
    try:
        r = requests.get(f"{BASE_URL}/api/export/{session_id}", params={"format": "pdf"})
        if r.status_code == 200:
            with open("e2e_report.pdf", "wb") as f:
                f.write(r.content)
            print("âœ… PDF Export success. Saved to 'e2e_report.pdf'")
        else:
            print(f"â Œ PDF Export failed: {r.text}")
            return
    except Exception as e:
        print(f"â Œ Export error: {e}")
        return

    print("\nâœ¨ E2E Test Passed Successfully!")

if __name__ == "__main__":
    test_flow()
