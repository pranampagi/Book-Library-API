"""Authentication API tests."""

from fastapi.testclient import TestClient


def test_register_and_login(client: TestClient):
    """Verify user registration, login, and profile retrieval."""
    register_response = client.post(
        "/auth/register",
        json={"username": "alice", "password": "secret123"},
    )
    assert register_response.status_code == 201
    assert register_response.json()["username"] == "alice"

    login_response = client.post(
        "/auth/token",
        data={"username": "alice", "password": "secret123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert token

    me_response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "alice"
