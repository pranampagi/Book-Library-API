"""Health and root endpoint tests."""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Ensure root endpoint responds with service metadata."""
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Book Library API is running"
    assert payload["docs"] == "/docs"


def test_health_endpoint(client: TestClient):
    """Ensure health endpoint reports API status."""
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["mongo"] in {"ok", "unavailable"}
