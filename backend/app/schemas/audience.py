"""Pydantic schemas for Audience endpoints."""

from datetime import datetime

from pydantic import BaseModel


class AudienceCreate(BaseModel):
    name: str
    description: str | None = None
    definition: dict
    sql_preview: str | None = None
    estimated_size: int | None = None
    created_by: str | None = None


class AudienceResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    definition: dict
    sql_preview: str | None = None
    estimated_size: int | None = None
    created_by: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AudienceGenerateRequest(BaseModel):
    goal: str
    event_schema: dict | None = None
