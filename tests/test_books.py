"""Book CRUD API tests."""

from fastapi.testclient import TestClient


def _register_and_login(client: TestClient, username: str, password: str) -> str:
    """Create a user and return a valid bearer token."""
    register_response = client.post(
        "/auth/register",
        json={"username": username, "password": password},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/token",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


def test_books_crud_flow(client: TestClient):
    """Verify create, list, read, update, and delete flow for books."""
    token = _register_and_login(client, "bob", "secret123")
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/books",
        json={
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "isbn": "9780132350884",
            "published_year": 2008,
            "genre": "Software",
            "description": "A handbook of agile software craftsmanship.",
        },
        headers=headers,
    )
    assert create_response.status_code == 201
    created = create_response.json()
    book_id = created["id"]
    assert created["title"] == "Clean Code"

    list_response = client.get("/books", headers=headers)
    assert list_response.status_code == 200
    listed = list_response.json()
    assert len(listed) == 1
    assert listed[0]["id"] == book_id

    get_response = client.get(f"/books/{book_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["author"] == "Robert C. Martin"

    update_response = client.put(
        f"/books/{book_id}",
        json={"genre": "Programming"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["genre"] == "Programming"

    delete_response = client.delete(f"/books/{book_id}", headers=headers)
    assert delete_response.status_code == 204

    missing_response = client.get(f"/books/{book_id}", headers=headers)
    assert missing_response.status_code == 404
