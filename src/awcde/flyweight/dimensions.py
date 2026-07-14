"""Flyweight dimension definitions and evaluators.

Each DimensionDefinition is a frozen dataclass shared across all evaluations.
DimensionEvaluator instances are created per-definition and cached by the registry.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from awcde.models.signature import DimensionLevel, DimensionScore
from awcde.models.telemetry import ArrivalPattern, BenchmarkRecord, Modality


@dataclass(frozen=True)
class DimensionDefinition:
    """Immutable flyweight definition for a workload dimension."""

    name: str
    input_fields: tuple[str, ...]
    low_threshold: float
    high_threshold: float


DIMENSION_DEFINITIONS: dict[str, DimensionDefinition] = {
    "latency_sensitivity": DimensionDefinition(
        name="latency_sensitivity",
        input_fields=("latency_p50_ms", "latency_p99_ms"),
        low_threshold=0.3,
        high_threshold=0.7,
    ),
    "throughput_orientation": DimensionDefinition(
        name="throughput_orientation",
        input_fields=("throughput_rps", "concurrency_level"),
        low_threshold=0.3,
        high_threshold=0.7,
    ),
    "memory_intensity": DimensionDefinition(
        name="memory_intensity",
        input_fields=("peak_memory_gb", "avg_memory_gb"),
        low_threshold=0.3,
        high_threshold=0.7,
    ),
    "burst_behaviour": DimensionDefinition(
        name="burst_behaviour",
        input_fields=("request_arrival_pattern", "latency_p99_ms", "latency_p50_ms"),
        low_threshold=0.3,
        high_threshold=0.7,
    ),
    "context_length_profile": DimensionDefinition(
        name="context_length_profile",
        input_fields=("context_length_p50", "context_length_p99"),
        low_threshold=0.3,
        high_threshold=0.7,
    ),
    "concurrency_profile": DimensionDefinition(
        name="concurrency_profile",
        input_fields=("concurrency_level", "throughput_rps"),
        low_threshold=0.3,
        high_threshold=0.7,
    ),
    "hardware_affinity": DimensionDefinition(
        name="hardware_affinity",
        input_fields=("accelerator_type", "gpu_utilization_pct"),
        low_threshold=0.3,
        high_threshold=0.7,
    ),
    "modality_profile": DimensionDefinition(
        name="modality_profile",
        input_fields=("modality",),
        low_threshold=0.3,
        high_threshold=0.7,
    ),
}


def _score_to_level(score: float, definition: DimensionDefinition) -> DimensionLevel:
    """Map a numeric score to a discrete level using the definition thresholds."""
    if score < definition.low_threshold:
        return DimensionLevel.LOW
    if score >= definition.high_threshold:
        return DimensionLevel.HIGH
    return DimensionLevel.MEDIUM


class DimensionEvaluator:
    """Evaluates a single dimension against a benchmark record.

    Each evaluator is bound to a DimensionDefinition and implements the
    scoring logic for that specific dimension.
    """

    def __init__(self, definition: DimensionDefinition) -> None:
        self._definition = definition

    @property
    def definition(self) -> DimensionDefinition:
        """Return the underlying flyweight definition."""
        return self._definition

    def evaluate(self, record: BenchmarkRecord) -> DimensionScore:
        """Evaluate a benchmark record and produce a dimension score."""
        raw_inputs: dict[str, float | int | str] = {}
        for field_name in self._definition.input_fields:
            value = getattr(record, field_name)
            if isinstance(value, Enum):
                raw_inputs[field_name] = value.value
            else:
                raw_inputs[field_name] = value

        score = self._compute_score(raw_inputs)
        score = max(0.0, min(1.0, score))
        level = _score_to_level(score, self._definition)

        return DimensionScore(level=level, score=score, raw_inputs=raw_inputs)

    def _compute_score(self, raw_inputs: dict[str, float | int | str]) -> float:
        """Compute the numeric score for this dimension.

        Each dimension has its own scoring heuristic based on the raw input values.
        """
        name = self._definition.name

        if name == "latency_sensitivity":
            return self._score_latency_sensitivity(raw_inputs)
        if name == "throughput_orientation":
            return self._score_throughput_orientation(raw_inputs)
        if name == "memory_intensity":
            return self._score_memory_intensity(raw_inputs)
        if name == "burst_behaviour":
            return self._score_burst_behaviour(raw_inputs)
        if name == "context_length_profile":
            return self._score_context_length_profile(raw_inputs)
        if name == "concurrency_profile":
            return self._score_concurrency_profile(raw_inputs)
        if name == "hardware_affinity":
            return self._score_hardware_affinity(raw_inputs)
        if name == "modality_profile":
            return self._score_modality_profile(raw_inputs)

        return 0.0

    @staticmethod
    def _score_latency_sensitivity(raw: dict[str, float | int | str]) -> float:
        """Higher p99/p50 ratio and absolute p99 level indicate latency sensitivity."""
        p50 = float(raw["latency_p50_ms"])
        p99 = float(raw["latency_p99_ms"])
        ratio_component = min(1.0, (p99 / max(p50, 0.01) - 1) / 10)
        absolute_component = min(1.0, p99 / 1000)
        return 0.6 * ratio_component + 0.4 * absolute_component

    @staticmethod
    def _score_throughput_orientation(raw: dict[str, float | int | str]) -> float:
        """Higher RPS and concurrency indicate throughput orientation."""
        rps = float(raw["throughput_rps"])
        concurrency = int(raw["concurrency_level"])
        rps_component = min(1.0, rps / 5000)
        concurrency_weight = min(1.0, concurrency / 64)
        return 0.7 * rps_component + 0.3 * concurrency_weight

    @staticmethod
    def _score_memory_intensity(raw: dict[str, float | int | str]) -> float:
        """Higher peak memory and peak/avg ratio indicate memory intensity."""
        peak = float(raw["peak_memory_gb"])
        avg = float(raw["avg_memory_gb"])
        peak_component = min(1.0, peak / 80)
        ratio = avg / max(peak, 0.01)
        ratio_component = 1.0 - ratio  # higher difference = more spiky memory usage
        return 0.7 * peak_component + 0.3 * ratio_component

    @staticmethod
    def _score_burst_behaviour(raw: dict[str, float | int | str]) -> float:
        """Bursty arrival patterns and high latency jitter indicate burst behaviour."""
        pattern = str(raw["request_arrival_pattern"])
        p50 = float(raw["latency_p50_ms"])
        p99 = float(raw["latency_p99_ms"])

        base = 0.5 if pattern == ArrivalPattern.BURSTY.value else 0.1
        jitter_ratio = min(0.5, (p99 / max(p50, 0.01) - 1) / 20)
        return base + jitter_ratio

    @staticmethod
    def _score_context_length_profile(raw: dict[str, float | int | str]) -> float:
        """Higher context lengths indicate heavier context usage."""
        p99 = int(raw["context_length_p99"])
        return min(1.0, p99 / 8192)

    @staticmethod
    def _score_concurrency_profile(raw: dict[str, float | int | str]) -> float:
        """Higher concurrency levels indicate concurrent workload profiles."""
        concurrency = int(raw["concurrency_level"])
        return min(1.0, concurrency / 128)

    @staticmethod
    def _score_hardware_affinity(raw: dict[str, float | int | str]) -> float:
        """Non-CPU accelerators with high GPU utilization indicate hardware affinity."""
        accelerator = str(raw["accelerator_type"])
        gpu_util = float(raw["gpu_utilization_pct"])
        if accelerator.upper() == "CPU":
            return 0.0
        return gpu_util / 100.0

    @staticmethod
    def _score_modality_profile(raw: dict[str, float | int | str]) -> float:
        """Map modality to a complexity score."""
        modality = str(raw["modality"])
        modality_scores = {
            Modality.TEXT.value: 0.2,
            Modality.VISION.value: 0.6,
            Modality.MULTIMODAL.value: 0.9,
        }
        return modality_scores.get(modality, 0.2)
