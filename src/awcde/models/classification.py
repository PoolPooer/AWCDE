"""Workload classification models."""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ClassificationCategory(str, Enum):
    """Primary workload classification categories."""

    LATENCY_CRITICAL = "latency_critical"
    THROUGHPUT_OPTIMIZED = "throughput_optimized"
    MEMORY_INTENSIVE = "memory_intensive"
    BURST_TOLERANT = "burst_tolerant"
    HARDWARE_SPECIALIZED = "hardware_specialized"
    GENERAL_PURPOSE = "general_purpose"


class WorkloadClassification(BaseModel):
    """Classification result for a workload signature."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    signature_id: str
    classified_at: datetime
    primary_category: ClassificationCategory
    secondary_tags: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    rationale: str
    dimension_summary: dict[str, float]
