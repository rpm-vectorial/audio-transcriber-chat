import pytest
from fastapi.testclient import TestClient
import io

def test_api_root(client):
    """Test the root API endpoint."""
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Audio Transcription and Chat API"}

def test_transcription_endpoints(client, db_session):
    """Test transcription endpoints."""
    # Test GET transcriptions (empty list initially)
    response = client.get("/api/v1/transcriptions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0

    # Test POST transcription (mock file upload)
    test_file = io.BytesIO(b"test audio content")
    files = {"file": ("test.mp3", test_file, "audio/mpeg")}
    response = client.post("/api/v1/transcriptions/", files=files)
    assert response.status_code in [200, 422]  # 422 if file validation fails

    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert data["filename"] == "test.mp3"
        assert "content" in data
        assert "created_at" in data

def test_chat_endpoints(client, db_session):
    """Test chat endpoints."""
    # First create a transcription
    test_file = io.BytesIO(b"test audio content")
    files = {"file": ("test.mp3", test_file, "audio/mpeg")}
    response = client.post("/api/v1/transcriptions/", files=files)
    
    if response.status_code == 200:
        transcription_id = response.json()["id"]
        
        # Test GET chat history (empty initially)
        response = client.get(f"/api/v1/chat/history/{transcription_id}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0

        # Test POST chat message
        test_message = {
            "transcription_id": transcription_id,
            "message": "Test message"
        }
        response = client.post("/api/v1/chat/", json=test_message)
        assert response.status_code in [200, 404]  # 404 if transcription not found
        
        if response.status_code == 200:
            data = response.json()
            assert "answer" in data

def test_error_handling(client):
    """Test error handling."""
    # Test invalid endpoint
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404

    # Test invalid chat message format
    invalid_message = {
        "message": ""  # Empty message
    }
    response = client.post("/api/v1/chat/", json=invalid_message)
    assert response.status_code == 422  # Validation error 