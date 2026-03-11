"""Pydantic schemas for Consent and ChannelPreference endpoints."""

from datetime import datetime

from pydantic import BaseModel


class ConsentCreate(BaseModel):
    user_id: str
    channel: str
    status: str  # granted | denied
    source: str | None = None
    region: str | None = None
    granted_at: datetime | None = None
    expires_at: datetime | None = None


class ConsentUpdate(BaseModel):
    status: str | None = None
    source: str | None = None
    withdrawn_at: datetime | None = None


class ConsentResponse(BaseModel):
    id: str
    user_id: str
    channel: str
    status: str
    source: str | None = None
    region: str | None = None
    granted_at: datetime | None = None
    withdrawn_at: datetime | None = None
    expires_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConsentSummary(BaseModel):
    user_id: str
    channels: dict[str, dict]


class ChannelPreferenceCreate(BaseModel):
    user_id: str
    channel: str
    frequency_cap_daily: int = 1
    frequency_cap_weekly: int = 3
    quiet_hours_start: str | None = None
    quiet_hours_end: str | None = None
    topics: list[str] | None = None


class ChannelPreferenceResponse(BaseModel):
    id: str
    user_id: str
    channel: str
    frequency_cap_daily: int
    frequency_cap_weekly: int
    quiet_hours_start: str | None = None
    quiet_hours_end: str | None = None
    topics: dict | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
