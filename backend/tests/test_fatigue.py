"""Tests for FatigueEngine."""

import uuid
from datetime import datetime, timedelta, timezone

from app.engine.fatigue import FatigueEngine
from app.models.decision import MessageDecision

engine = FatigueEngine()


def test_no_decisions_not_fatigued(db, sample_user):
    assert engine.is_fatigued(sample_user.id, db) is False


def test_many_decisions_fatigued(db, sample_user):
    """Inserting 10+ unseen messages with no engagement -> fatigue >= 0.80."""
    now = datetime.now(timezone.utc)
    for i in range(12):
        db.add(
            MessageDecision(
                id=str(uuid.uuid4()),
                user_id=sample_user.id,
                channel="email",
                action="educate",
                reason="test",
                suppressed=False,
                created_at=now - timedelta(days=1, hours=i),
            )
        )
    db.commit()

    assert engine.is_fatigued(sample_user.id, db) is True


def test_fatigue_score_calculation(db, sample_user):
    """No messages → score 0.0."""
    score = engine.calculate_fatigue_score(sample_user.id, db)
    assert score == 0.0


def test_fatigue_score_with_engagement(db, sample_user):
    """Messages with full engagement should keep fatigue low."""
    now = datetime.now(timezone.utc)
    for i in range(5):
        db.add(
            MessageDecision(
                id=str(uuid.uuid4()),
                user_id=sample_user.id,
                channel="email",
                action="educate",
                reason="test",
                suppressed=False,
                result="clicked",
                created_at=now - timedelta(hours=i),
            )
        )
    db.commit()

    score = engine.calculate_fatigue_score(sample_user.id, db)
    # All messages engaged => fatigue should be 0.0
    assert score == 0.0
