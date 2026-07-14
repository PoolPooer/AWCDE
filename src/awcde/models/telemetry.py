"""Telemetry data models for benchmark ingestion."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class ArrivalPattern(str, Enum):
    """Request arrival pattern classification."""

    STEADY = "steady"
    BURSTY = "bursty"


class Modality(str, Enum):
    """Model input modality."""

    TEXT = "text"
    VISION = "vision"
    MULTIMODAL = "multimodal"


class BenchmarkRecord(BaseModel):
    """A single benchmark measurement record."""

    latency_p50_ms: float = Field(ge=0)
    latency_p99_ms: float = Field(ge=0)
    throughput_rps: float = Field(ge=0)
    peak_memory_gb: float = Field(ge=0)
    avg_memory_gb: float = Field(ge=0)
    request_arrival_pattern: ArrivalPattern
    context_length_p50: int = Field(ge=0)
    context_length_p99: int = Field(ge=0)
    concurrency_level: int = Field(ge=1)
    accelerator_type: str
    gpu_utilization_pct: float = Field(ge=0, le=100)
    modality: Modality

    @model_validator(mode="after")
    def validate_percentile_ordering(self) -> BenchmarkRecord:
        """Ensure p99 values are >= p50 values."""
        if self.latency_p99_ms < self.latency_p50_ms:
            msg = (
                f"latency_p99_ms ({self.latency_p99_ms}) must be >= "
                f"latency_p50_ms ({self.latency_p50_ms})"
            )
            raise ValueError(msg)
        if self.context_length_p99 < self.context_length_p50:
            msg = (
                f"context_length_p99 ({self.context_length_p99}) must be >= "
                f"context_length_p50 ({self.context_length_p50})"
            )
            raise ValueError(msg)
        return self


class BenchmarkTelemetry(BaseModel):
    """Collection of benchmark records from a single ingestion."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider_id: str
    source_ref: str
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    records: list[BenchmarkRecord]
