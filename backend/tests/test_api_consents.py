"""Tests for consent API endpoints."""


def _create_user(client, name="TestUser"):
    resp = client.post("/api/users", json={"name": name})
    return resp.json()["id"]


def test_record_consent(client):
    user_id = _create_user(client)
    resp = client.post(
        "/api/consents",
        json={
            "user_id": user_id,
            "channel": "email",
            "status": "granted",
            "source": "web_form",
            "region": "US",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["channel"] == "email"
    assert data["status"] == "granted"
    assert data["user_id"] == user_id
    assert data["granted_at"] is not None


def test_get_user_consents(client):
    user_id = _create_user(client)
    client.post(
        "/api/consents",
        json={"user_id": user_id, "channel": "email", "status": "granted"},
    )
    client.post(
        "/api/consents",
        json={"user_id": user_id, "channel": "sms", "status": "granted"},
    )

    resp = client.get(f"/api/consents/{user_id}")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_withdraw_consent(client):
    user_id = _create_user(client)
    create_resp = client.post(
        "/api/consents",
        json={"user_id": user_id, "channel": "email", "status": "granted"},
    )
    consent_id = create_resp.json()["id"]

    resp = client.put(f"/api/consents/{consent_id}/withdraw")
    assert resp.status_code == 200
    assert resp.json()["status"] == "withdrawn"
    assert resp.json()["withdrawn_at"] is not None


def test_consent_summary(client):
    user_id = _create_user(client)
    client.post(
        "/api/consents",
        json={
            "user_id": user_id,
            "channel": "email",
            "status": "granted",
            "source": "form",
        },
    )

    resp = client.get(f"/api/consents/{user_id}/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["user_id"] == user_id
    assert "email" in data["channels"]
    assert data["channels"]["email"]["status"] == "granted"
