"""Pydantic schemas for Experiment endpoints."""

from datetime import datetime

from pydantic import BaseModel


class ExperimentCreate(BaseModel):
    name: str
    description: str | None = None
    experiment_type: str
    journey_id: str | None = None
    variants: list[dict]
    traffic_split: dict | None = None
    status: str = "draft"
    start_date: datetime | None = None
    end_date: datetime | None = None


class ExperimentResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    experiment_type: str
    journey_id: str | None = None
    variants: list[dict] | dict
    traffic_split: dict | None = None
    status: str
    start_date: datetime | None = None
    end_date: datetime | None = None
    winner_variant: str | None = None
    statistical_confidence: float | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ExperimentSuggestionRequest(BaseModel):
    journey_name: str
    open_rate: float = 0.0
    click_rate: float = 0.0
    conversion_rate: float = 0.0
