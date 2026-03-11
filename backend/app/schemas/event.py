"""Pydantic schemas for Event endpoints."""

from datetime import datetime

from pydantic import BaseModel


class EventCreate(BaseModel):
    user_id: str
    event_type: str
    event_name: str
    properties: dict | None = None
    source: str | None = None
    timestamp: datetime | None = None


class EventResponse(BaseModel):
    id: str
    user_id: str
    event_type: str
    event_name: str
    properties: dict | None = None
    source: str | None = None
    timestamp: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class EventListResponse(BaseModel):
    events: list[EventResponse]
    total: int
