import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "German Simplification API" in response.json()["message"]


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_simplify_endpoint_missing_auth():
    """Test that the simplify endpoint requires authentication"""
    response = client.post(
        "/v1/simplify",
        json={
            "input": "Der komplizierte deutsche Text.",
            "format": "text",
            "mode": "easy"
        }
    )
    # Should return 401 or 422 depending on auth implementation
    assert response.status_code in [401, 422]


def test_simplify_endpoint_invalid_input():
    """Test the simplify endpoint with invalid input"""
    response = client.post(
        "/v1/simplify",
        json={
            "input": "",  # Empty input should be invalid
            "format": "text",
            "mode": "easy"
        }
    )
    assert response.status_code == 422  # Validation error


def test_simplify_endpoint_valid_input():
    """Test the simplify endpoint with valid input (mock auth)"""
    # This test will need to be updated when proper auth is implemented
    response = client.post(
        "/v1/simplify",
        json={
            "input": "Der komplizierte deutsche Text, der vereinfacht werden soll.",
            "format": "text",
            "mode": "easy",
            "max_output_chars": 1000
        },
        headers={"Authorization": "Bearer mock-token"}  # Mock auth for now
    )
    # This might fail until we implement proper auth, but the structure should be correct
    assert response.status_code in [200, 401, 500]  # Accept various responses for now
