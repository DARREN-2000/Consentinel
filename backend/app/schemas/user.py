"""Pydantic schemas for User endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    external_id: str | None = None
    email: str | None = None
    name: str | None = None
    company_name: str | None = None
    company_size: int | None = None
    lifecycle_stage: str = "unknown"
    preferred_channel: str | None = None
    metadata_: dict | None = Field(None, alias="metadata")

    model_config = {"populate_by_name": True}


class UserUpdate(BaseModel):
    email: str | None = None
    name: str | None = None
    company_name: str | None = None
    company_size: int | None = None
    lifecycle_stage: str | None = None
    preferred_channel: str | None = None
    activated: bool | None = None
    metadata_: dict | None = Field(None, alias="metadata")

    model_config = {"populate_by_name": True}


class UserResponse(BaseModel):
    id: str
    external_id: str | None = None
    email: str | None = None
    name: str | None = None
    company_name: str | None = None
    company_size: int | None = None
    lifecycle_stage: str
    intent_score: float
    churn_risk: float
    activation_score: float
    fatigue_score: float
    preferred_channel: str | None = None
    last_meaningful_touchpoint: datetime | None = None
    activated: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserScoresResponse(BaseModel):
    user_id: str
    intent_score: float
    churn_risk: float
    activation_score: float
    fatigue_score: float


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
    page: int
    page_size: int
