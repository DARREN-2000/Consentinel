"""Tests for decision API endpoints."""


def _setup_user_with_consent(client, intent=0.5, churn=0.3):
    """Create a user and grant email consent; return user_id."""
    create = client.post(
        "/api/users",
        json={
            "name": "DecisionUser",
            "company_size": 5,
        },
    )
    user_id = create.json()["id"]

    # Grant email consent
    client.post(
        "/api/consents",
        json={"user_id": user_id, "channel": "email", "status": "granted"},
    )
    return user_id


def test_next_best_action_for_user(client):
    user_id = _setup_user_with_consent(client)
    resp = client.post(
        "/api/decisions/next-best-action",
        json={"user_id": user_id},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "channel" in data
    assert "action" in data
    assert "reason" in data
    assert data["user_id"] == user_id


def test_next_best_action_batch(client):
    uid1 = _setup_user_with_consent(client)
    uid2 = _setup_user_with_consent(client)

    resp = client.post(
        "/api/decisions/next-best-action/batch",
        json=[{"user_id": uid1}, {"user_id": uid2}],
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_decision_explain(client):
    user_id = _setup_user_with_consent(client)

    # Make a decision first
    nba_resp = client.post(
        "/api/decisions/next-best-action",
        json={"user_id": user_id},
    )
    decision_id = nba_resp.json()["id"]

    resp = client.get(f"/api/decisions/{decision_id}/explain")
    assert resp.status_code == 200
    data = resp.json()
    assert data["decision_id"] == decision_id
    assert data["user_id"] == user_id
    assert "factors" in data
    assert "consent_state" in data
    assert "suppression_checks" in data


def test_next_best_action_user_not_found(client):
    resp = client.post(
        "/api/decisions/next-best-action",
        json={"user_id": "nonexistent"},
    )
    assert resp.status_code == 404
