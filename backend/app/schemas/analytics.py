"""Pydantic schemas for Analytics endpoints."""

from pydantic import BaseModel


class ChannelMetrics(BaseModel):
    channel: str
    total_decisions: int
    suppressed: int
    delivered: int
    opened: int
    clicked: int
    converted: int
    suppression_rate: float
    open_rate: float
    click_rate: float


class FatigueDistribution(BaseModel):
    bucket: str
    count: int
    percentage: float


class SuppressionStats(BaseModel):
    reason: str
    count: int
    percentage: float


class AnalyticsSummary(BaseModel):
    total_users: int
    total_decisions: int
    total_events: int
    suppression_rate: float
    avg_intent_score: float
    avg_churn_risk: float
    avg_fatigue_score: float
    activated_users: int
    activation_rate: float
