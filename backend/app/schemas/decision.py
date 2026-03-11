"""Pydantic schemas for Decision endpoints."""

from datetime import datetime

from pydantic import BaseModel


class DecisionRequest(BaseModel):
    user_id: str


class DecisionResponse(BaseModel):
    id: str | None = None
    user_id: str
    channel: str
    action: str
    reason: str
    consent_checked: bool = True
    fatigue_checked: bool = True
    suppressed: bool = False
    suppression_reason: str | None = None
    model_confidence: float | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class DecisionListResponse(BaseModel):
    decisions: list[DecisionResponse]
    total: int


class ExplainabilityResponse(BaseModel):
    decision_id: str
    user_id: str
    channel: str
    action: str
    reason: str
    factors: dict
    consent_state: dict
    suppression_checks: list[dict]
