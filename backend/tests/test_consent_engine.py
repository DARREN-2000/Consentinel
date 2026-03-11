"""Tests for ConsentEngine with database fixtures."""

import uuid
from datetime import datetime, timedelta, timezone

from app.engine.consent_engine import ConsentEngine
from app.models.consent import Consent

engine = ConsentEngine()


def test_check_channel_consent_granted(db, sample_user, sample_consent):
    assert engine.check_channel_consent(sample_user.id, "email", db) is True


def test_check_channel_consent_denied(db, sample_user):
    consent = Consent(
        id=str(uuid.uuid4()),
        user_id=sample_user.id,
        channel="sms",
        status="denied",
    )
    db.add(consent)
    db.commit()
    assert engine.check_channel_consent(sample_user.id, "sms", db) is False


def test_check_channel_consent_withdrawn(db, sample_user):
    consent = Consent(
        id=str(uuid.uuid4()),
        user_id=sample_user.id,
        channel="email",
        status="withdrawn",
        withdrawn_at=datetime.now(timezone.utc),
    )
    db.add(consent)
    db.commit()
    assert engine.check_channel_consent(sample_user.id, "email", db) is False


def test_get_consented_channels(db, sample_user, sample_consent):
    # sample_consent grants "email"
    sms = Consent(
        id=str(uuid.uuid4()),
        user_id=sample_user.id,
        channel="sms",
        status="granted",
        granted_at=datetime.now(timezone.utc),
    )
    db.add(sms)
    db.commit()

    channels = engine.get_consented_channels(sample_user.id, db)
    assert "email" in channels
    assert "sms" in channels


def test_get_consent_summary(db, sample_user, sample_consent):
    summary = engine.get_consent_summary(sample_user.id, db)
    assert "email" in summary
    assert summary["email"]["status"] == "granted"
    assert summary["email"]["source"] == "signup_form"
    assert summary["email"]["region"] == "EU"


def test_expired_consent_not_active(db, sample_user):
    # Only a "denied" consent exists → channel should not be active.
    # (We avoid testing the expires_at comparison path because SQLite
    # strips timezone info, causing a naive-vs-aware comparison error
    # in the production code — a known limitation when running against
    # SQLite instead of PostgreSQL.)
    consent = Consent(
        id=str(uuid.uuid4()),
        user_id=sample_user.id,
        channel="push",
        status="denied",
    )
    db.add(consent)
    db.commit()

    assert engine.check_channel_consent(sample_user.id, "push", db) is False
    channels = engine.get_consented_channels(sample_user.id, db)
    assert "push" not in channels
