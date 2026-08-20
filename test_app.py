import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads successfully (HTTP 200)."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Automated Docker Deployment" in response.data

def test_health_endpoint(client):
    """Test that the healthcheck endpoint returns status 200 and healthy JSON."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "uptime_seconds" in data

def test_api_info_endpoint(client):
    """Test that the API info endpoint returns application metadata."""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.get_json()
    assert data["app_name"] == "Automated Docker Deployment App"
    assert "hostname" in data
