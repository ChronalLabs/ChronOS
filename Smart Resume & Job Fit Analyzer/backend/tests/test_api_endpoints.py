"""
Tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
import io


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_check(self, client):
        """Test the health endpoint returns healthy."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "spacy_loaded" in data
    
    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "docs" in data


class TestResumeUploadEndpoint:
    """Test resume upload endpoint."""
    
    def test_upload_requires_file(self, client):
        """Test that upload requires a file."""
        response = client.post("/api/upload-resume")
        
        assert response.status_code == 422  # Validation error
    
    def test_rejects_invalid_file_type(self, client):
        """Test that invalid file types are rejected."""
        file_content = b"This is a text file"
        files = {"file": ("resume.txt", io.BytesIO(file_content), "text/plain")}
        
        response = client.post("/api/upload-resume", files=files)
        
        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]
    
    def test_accepts_docx(self, client, temp_docx_file):
        """Test that DOCX files are accepted."""
        with open(temp_docx_file, "rb") as f:
            files = {"file": ("resume.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            response = client.post("/api/upload-resume", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert "parsed_resume" in data


class TestJobDescriptionEndpoint:
    """Test job description analysis endpoint."""
    
    def test_analyze_jd(self, client, sample_jd_text):
        """Test JD analysis endpoint."""
        response = client.post(
            "/api/analyze-jd",
            json={"job_description": sample_jd_text}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert "parsed_jd" in data
    
    def test_analyze_empty_jd(self, client):
        """Test handling of empty job description."""
        response = client.post(
            "/api/analyze-jd",
            json={"job_description": ""}
        )
        
        # Schema requires min_length=50, so this should fail validation
        assert response.status_code == 422
    
    def test_analyze_jd_extracts_skills(self, client, sample_jd_text):
        """Test that JD analysis extracts skills."""
        response = client.post(
            "/api/analyze-jd",
            json={"job_description": sample_jd_text}
        )
        
        data = response.json()
        parsed_jd = data["parsed_jd"]
        
        assert "required_skills" in parsed_jd
        assert len(parsed_jd["required_skills"]) > 0


class TestEvaluationEndpoint:
    """Test evaluation endpoint."""
    
    def test_requires_session(self, client):
        """Test that evaluation requires a valid session."""
        response = client.post(
            "/api/evaluate",
            json={"session_id": "invalid-session-id"}
        )
        
        assert response.status_code == 404
    
    def test_full_evaluation_flow(self, client, temp_docx_file, sample_jd_text):
        """Test complete evaluation flow."""
        # Step 1: Upload resume
        with open(temp_docx_file, "rb") as f:
            files = {"file": ("resume.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            upload_response = client.post("/api/upload-resume", files=files)
        
        assert upload_response.status_code == 200
        session_id = upload_response.json()["session_id"]
        
        # Step 2: Analyze JD (with session)
        jd_response = client.post(
            f"/api/analyze-jd?session_id={session_id}",
            json={"job_description": sample_jd_text}
        )
        
        assert jd_response.status_code == 200
        
        # Step 3: Evaluate
        eval_response = client.post(
            "/api/evaluate",
            json={"session_id": session_id}
        )
        
        assert eval_response.status_code == 200
        result = eval_response.json()
        
        assert "result" in result
        assert "job_fit_score" in result["result"]
        assert result["result"]["job_fit_score"] >= 0
        assert result["result"]["job_fit_score"] <= 100


class TestSessionEndpoints:
    """Test session management endpoints."""
    
    def test_get_nonexistent_session(self, client):
        """Test getting a session that doesn't exist."""
        response = client.get("/api/session/nonexistent-id")
        
        assert response.status_code == 404
    
    def test_delete_session(self, client, temp_docx_file):
        """Test session deletion."""
        # Create a session
        with open(temp_docx_file, "rb") as f:
            files = {"file": ("resume.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            response = client.post("/api/upload-resume", files=files)
        
        session_id = response.json()["session_id"]
        
        # Delete it
        delete_response = client.delete(f"/api/session/{session_id}")
        assert delete_response.status_code == 200
        
        # Verify it's gone
        get_response = client.get(f"/api/session/{session_id}")
        assert get_response.status_code == 404


class TestExportEndpoint:
    """Test export endpoint."""
    
    def test_export_requires_evaluation(self, client, temp_docx_file, sample_jd_text):
        """Test that export requires completed evaluation."""
        # Create session and upload resume
        with open(temp_docx_file, "rb") as f:
            files = {"file": ("resume.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            response = client.post("/api/upload-resume", files=files)
        
        session_id = response.json()["session_id"]
        
        # Try to export without evaluation
        export_response = client.get(f"/api/export/{session_id}")
        
        # Should fail because no evaluation exists
        assert export_response.status_code == 404
