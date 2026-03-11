"""Tests for health and readiness endpoints."""


def test_health_check(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["service"] == "relevance-engine"
    assert data["version"] == "1.0.0"


def test_readiness_check(client):
    resp = client.get("/api/ready")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ready"
    assert data["database"] == "connected"
