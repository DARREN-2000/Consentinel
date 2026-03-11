"""Tests for user API endpoints."""


def test_create_user(client):
    resp = client.post(
        "/api/users",
        json={
            "external_id": "ext-1",
            "name": "Bob",
            "lifecycle_stage": "lead",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Bob"
    assert data["lifecycle_stage"] == "lead"
    assert "id" in data


def test_create_user_with_email(client):
    resp = client.post(
        "/api/users",
        json={"email": "carol@example.com", "name": "Carol"},
    )
    assert resp.status_code == 201
    assert resp.json()["email"] == "carol@example.com"


def test_get_user(client):
    create = client.post("/api/users", json={"name": "Dave"})
    user_id = create.json()["id"]

    resp = client.get(f"/api/users/{user_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == user_id
    assert resp.json()["name"] == "Dave"


def test_get_user_not_found(client):
    resp = client.get("/api/users/nonexistent-id")
    assert resp.status_code == 404


def test_list_users(client):
    client.post("/api/users", json={"name": "User1"})
    client.post("/api/users", json={"name": "User2"})

    resp = client.get("/api/users")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 2
    assert len(data["users"]) >= 2


def test_update_user(client):
    create = client.post("/api/users", json={"name": "Eve"})
    user_id = create.json()["id"]

    resp = client.put(
        f"/api/users/{user_id}",
        json={"name": "Eve Updated", "activated": True},
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Eve Updated"
    assert resp.json()["activated"] is True
