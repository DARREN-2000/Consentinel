"""Tests for event API endpoints."""


def _create_user(client):
    resp = client.post("/api/users", json={"name": "EventUser"})
    return resp.json()["id"]


def test_ingest_event(client):
    user_id = _create_user(client)
    resp = client.post(
        "/api/events",
        json={
            "user_id": user_id,
            "event_type": "page_view",
            "event_name": "pricing_view",
            "source": "web",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["event_type"] == "page_view"
    assert data["event_name"] == "pricing_view"
    assert data["user_id"] == user_id


def test_batch_ingest_events(client):
    user_id = _create_user(client)
    events = [
        {
            "user_id": user_id,
            "event_type": "page_view",
            "event_name": "home",
        },
        {
            "user_id": user_id,
            "event_type": "click",
            "event_name": "cta_button",
        },
    ]
    resp = client.post("/api/events/batch", json=events)
    assert resp.status_code == 201
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_user_events(client):
    user_id = _create_user(client)
    client.post(
        "/api/events",
        json={
            "user_id": user_id,
            "event_type": "page_view",
            "event_name": "docs",
        },
    )
    client.post(
        "/api/events",
        json={
            "user_id": user_id,
            "event_type": "click",
            "event_name": "signup_btn",
        },
    )

    resp = client.get(f"/api/events/{user_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["events"]) == 2
