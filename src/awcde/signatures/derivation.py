"""Signature derivation from benchmark telemetry.

Aggregates multi-record telemetry into a single representative record,
evaluates all eight workload dimensions using flyweight evaluators,
and produces a deterministic WorkloadSignature.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

from awcde.flyweight.registry import FlyweightRegistry
from awcde.models.signature import DimensionScore, WorkloadSignature
from awcde.models.telemetry import (
    ArrivalPattern,
    BenchmarkRecord,
    BenchmarkTelemetry,
    Modality,
)
from awcde.signatures.identity import compute_signature_id
from awcde.signatures.schema import get_schema_version

# Maps DIMENSION_DEFINITIONS keys to WorkloadSignature field names.
# Most are identical; the exception is modality_profile -> modality.
_DIMENSION_TO_FIELD: dict[str, str] = {
    "latency_sensitivity": "latency_sensitivity",
    "throughput_orientation": "throughput_orientation",
    "memory_intensity": "memory_intensity",
    "burst_behaviour": "burst_behaviour",
    "context_length_profile": "context_length_profile",
    "concurrency_profile": "concurrency_profile",
    "hardware_affinity": "hardware_affinity",
    "modality_profile": "modality",
}


def _mode(values: list[str]) -> str:
    """Return the most common value from a list of strings."""
    counter = Counter(values)
    return counter.most_common(1)[0][0]


def _aggregate_records(records: list[BenchmarkRecord]) -> BenchmarkRecord:
    """Aggregate multiple benchmark records into a single representative record.

    Numeric fields are averaged. Categorical fields use the statistical
    mode (most frequent value).

    Args:
        records: One or more BenchmarkRecord instances.

    Returns:
        A single aggregated BenchmarkRecord.
    """
    if len(records) == 1:
        return records[0]

    n = len(records)

    # Average numeric fields
    latency_p50 = sum(r.latency_p50_ms for r in records) / n
    latency_p99 = sum(r.latency_p99_ms for r in records) / n
    throughput = sum(r.throughput_rps for r in records) / n
    peak_mem = sum(r.peak_memory_gb for r in records) / n
    avg_mem = sum(r.avg_memory_gb for r in records) / n
    ctx_p50 = round(sum(r.context_length_p50 for r in records) / n)
    ctx_p99 = round(sum(r.context_length_p99 for r in records) / n)
    concurrency = max(1, round(sum(r.concurrency_level for r in records) / n))
    gpu_util = sum(r.gpu_utilization_pct for r in records) / n

    # Mode for categorical fields
    arrival = ArrivalPattern(
        _mode([r.request_arrival_pattern.value for r in records])
    )
    accelerator = _mode([r.accelerator_type for r in records])
    modality = Modality(_mode([r.modality.value for r in records]))

    # Ensure p99 >= p50 invariants hold after averaging
    if latency_p99 < latency_p50:
        latency_p99 = latency_p50
    if ctx_p99 < ctx_p50:
        ctx_p99 = ctx_p50

    return BenchmarkRecord(
        latency_p50_ms=latency_p50,
        latency_p99_ms=latency_p99,
        throughput_rps=throughput,
        peak_memory_gb=peak_mem,
        avg_memory_gb=avg_mem,
        request_arrival_pattern=arrival,
        context_length_p50=ctx_p50,
        context_length_p99=ctx_p99,
        concurrency_level=concurrency,
        accelerator_type=accelerator,
        gpu_utilization_pct=gpu_util,
        modality=modality,
    )


class SignatureDerivation:
    """Derives workload signatures from benchmark telemetry.

    Uses flyweight dimension evaluators to score each of the eight
    workload dimensions, then assembles a deterministic WorkloadSignature.
    """

    def __init__(self, flyweight_registry: FlyweightRegistry) -> None:
        self._evaluators = flyweight_registry.get_all_dimension_evaluators()

    def derive(self, telemetry: BenchmarkTelemetry) -> WorkloadSignature:
        """Derive a workload signature from benchmark telemetry.

        For multi-record telemetry, records are first aggregated into a
        single representative record by averaging numeric fields and
        taking the mode of categorical fields.

        Args:
            telemetry: Benchmark telemetry with one or more records.

        Returns:
            A WorkloadSignature with deterministic ID and all eight
            dimension scores populated.
        """
        aggregated = _aggregate_records(telemetry.records)

        # Evaluate each dimension against the aggregated record
        dimension_scores: dict[str, DimensionScore] = {}
        for evaluator in self._evaluators:
            dim_name = evaluator.definition.name
            field_name = _DIMENSION_TO_FIELD[dim_name]
            dimension_scores[field_name] = evaluator.evaluate(aggregated)

        schema_version = get_schema_version()
        signature_id = compute_signature_id(telemetry, schema_version)

        return WorkloadSignature(
            id=signature_id,
            schema_version=schema_version,
            telemetry_id=telemetry.id,
            derived_at=datetime.now(timezone.utc),
            **dimension_scores,
        )
