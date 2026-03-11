"""Pydantic schemas for Journey endpoints."""

from datetime import datetime

from pydantic import BaseModel


class JourneyTemplateCreate(BaseModel):
    name: str
    description: str | None = None
    goal: str | None = None
    audience_id: str | None = None
    steps: list[dict]
    entry_conditions: dict | None = None
    exit_conditions: dict | None = None
    suppression_rules: dict | None = None
    created_by: str | None = None


class JourneyTemplateResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    goal: str | None = None
    audience_id: str | None = None
    steps: list[dict]
    entry_conditions: dict | None = None
    exit_conditions: dict | None = None
    suppression_rules: dict | None = None
    is_active: bool
    created_by: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class JourneyRunResponse(BaseModel):
    id: str
    template_id: str
    user_id: str
    current_step: int
    status: str
    entered_at: datetime
    exited_at: datetime | None = None
    exit_reason: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class JourneyDesignRequest(BaseModel):
    goal: str
    audience: dict | None = None
