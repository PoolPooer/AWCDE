"""Workload signature models derived from telemetry analysis."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DimensionLevel(str, Enum):
    """Discrete level for a workload dimension."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DimensionScore(BaseModel):
    """Score for a single workload dimension."""

    level: DimensionLevel
    score: float = Field(ge=0, le=1)
    raw_inputs: dict[str, float | int | str]


class WorkloadSignature(BaseModel):
    """Eight-dimensional workload characterization derived from telemetry.

    The id is a SHA-256 hash computed deterministically from the dimension scores
    and telemetry_id, ensuring identical inputs produce the same signature id.
    """

    id: str
    schema_version: str = "1.0.0"
    telemetry_id: str
    derived_at: datetime
    latency_sensitivity: DimensionScore
    throughput_orientation: DimensionScore
    memory_intensity: DimensionScore
    burst_behaviour: DimensionScore
    context_length_profile: DimensionScore
    concurrency_profile: DimensionScore
    hardware_affinity: DimensionScore
    modality: DimensionScore
