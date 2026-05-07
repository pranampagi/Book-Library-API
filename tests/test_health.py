from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Book Library API is running"
    assert payload["docs"] == "/docs"


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["mongo"] in {"ok", "unavailable"}
