"""Infrastructure recommendation models."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class RecommendationEvidence(BaseModel):
    """Evidence supporting a specific recommendation."""

    rule_id: str
    source_type: str  # "signature", "classification", "telemetry"
    attribute: str
    attribute_value: float | int | str
    condition_matched: str


class RecommendationBlock(BaseModel):
    """A single recommendation with reasoning and evidence."""

    recommendation: str
    reasoning: str
    evidence: list[RecommendationEvidence]


class InfrastructureRecommendation(BaseModel):
    """Complete infrastructure recommendation for a classified workload."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    classification_id: str
    signature_id: str
    generated_at: datetime
    model_family: RecommendationBlock
    runtime: RecommendationBlock
    hardware_suitability: RecommendationBlock
    deployment_topology: RecommendationBlock
    scheduling_policy: RecommendationBlock
