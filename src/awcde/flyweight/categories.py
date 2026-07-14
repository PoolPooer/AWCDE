"""Flyweight category definitions and evaluators.

Each CategoryDefinition maps a classification category to the dominant
dimension and the minimum score threshold for matching.
"""

from __future__ import annotations

from dataclasses import dataclass

from awcde.models.classification import ClassificationCategory
from awcde.models.signature import WorkloadSignature


@dataclass(frozen=True)
class CategoryDefinition:
    """Immutable flyweight definition for a workload category."""

    name: str
    dominant_dimension: str
    min_score: float
    description: str


CATEGORY_DEFINITIONS: dict[str, CategoryDefinition] = {
    "latency_critical": CategoryDefinition(
        name="latency_critical",
        dominant_dimension="latency_sensitivity",
        min_score=0.7,
        description="Workloads where response latency is the primary concern.",
    ),
    "throughput_optimized": CategoryDefinition(
        name="throughput_optimized",
        dominant_dimension="throughput_orientation",
        min_score=0.7,
        description="Workloads optimized for maximum request throughput.",
    ),
    "memory_intensive": CategoryDefinition(
        name="memory_intensive",
        dominant_dimension="memory_intensity",
        min_score=0.7,
        description="Workloads with high memory requirements.",
    ),
    "burst_tolerant": CategoryDefinition(
        name="burst_tolerant",
        dominant_dimension="burst_behaviour",
        min_score=0.7,
        description="Workloads that experience bursty traffic patterns.",
    ),
    "hardware_specialized": CategoryDefinition(
        name="hardware_specialized",
        dominant_dimension="hardware_affinity",
        min_score=0.7,
        description="Workloads that benefit from specialized hardware accelerators.",
    ),
    "general_purpose": CategoryDefinition(
        name="general_purpose",
        dominant_dimension="throughput_orientation",
        min_score=0.0,
        description="Workloads without a single dominant characteristic.",
    ),
}

# Map category definition names to ClassificationCategory enum values.
_CATEGORY_ENUM_MAP: dict[str, ClassificationCategory] = {
    "latency_critical": ClassificationCategory.LATENCY_CRITICAL,
    "throughput_optimized": ClassificationCategory.THROUGHPUT_OPTIMIZED,
    "memory_intensive": ClassificationCategory.MEMORY_INTENSIVE,
    "burst_tolerant": ClassificationCategory.BURST_TOLERANT,
    "hardware_specialized": ClassificationCategory.HARDWARE_SPECIALIZED,
    "general_purpose": ClassificationCategory.GENERAL_PURPOSE,
}


def _get_dimension_score(signature: WorkloadSignature, dimension_name: str) -> float:
    """Extract the numeric score for a named dimension from a signature."""
    dimension_field_map: dict[str, str] = {
        "latency_sensitivity": "latency_sensitivity",
        "throughput_orientation": "throughput_orientation",
        "memory_intensity": "memory_intensity",
        "burst_behaviour": "burst_behaviour",
        "context_length_profile": "context_length_profile",
        "concurrency_profile": "concurrency_profile",
        "hardware_affinity": "hardware_affinity",
        "modality_profile": "modality",
    }
    field_name = dimension_field_map.get(dimension_name, dimension_name)
    dimension_score = getattr(signature, field_name, None)
    if dimension_score is None:
        return 0.0
    return dimension_score.score


class CategoryEvaluator:
    """Evaluates whether a workload signature matches a category.

    Each evaluator is bound to a CategoryDefinition and checks whether the
    dominant dimension score meets the minimum threshold.
    """

    def __init__(self, definition: CategoryDefinition) -> None:
        self._definition = definition

    @property
    def definition(self) -> CategoryDefinition:
        """Return the underlying flyweight definition."""
        return self._definition

    @property
    def category(self) -> ClassificationCategory:
        """Return the ClassificationCategory enum value for this category."""
        return _CATEGORY_ENUM_MAP[self._definition.name]

    def matches(self, signature: WorkloadSignature) -> tuple[bool, float]:
        """Check if a signature matches this category.

        Returns:
            A tuple of (is_match, confidence) where confidence is the
            dominant dimension's score, and is_match is True when the
            score meets or exceeds the minimum threshold.
        """
        score = _get_dimension_score(signature, self._definition.dominant_dimension)
        is_match = score >= self._definition.min_score
        return is_match, score
