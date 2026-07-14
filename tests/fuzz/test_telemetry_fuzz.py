"""Tier 5 Fuzz: Property-based tests for BenchmarkRecord validation."""

from __future__ import annotations

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st
from pydantic import ValidationError

from awcde.models.telemetry import BenchmarkRecord, ArrivalPattern, Modality


pytestmark = pytest.mark.fuzz


valid_record_strategy = st.fixed_dictionaries({
    "latency_p50_ms": st.floats(min_value=0.0, max_value=10000.0),
    "latency_p99_ms": st.floats(min_value=0.0, max_value=50000.0),
    "throughput_rps": st.floats(min_value=0.0, max_value=100000.0),
    "peak_memory_gb": st.floats(min_value=0.0, max_value=1000.0),
    "avg_memory_gb": st.floats(min_value=0.0, max_value=1000.0),
    "request_arrival_pattern": st.sampled_from(["steady", "bursty"]),
    "context_length_p50": st.integers(min_value=0, max_value=200000),
    "context_length_p99": st.integers(min_value=0, max_value=200000),
    "concurrency_level": st.integers(min_value=1, max_value=10000),
    "accelerator_type": st.sampled_from(["CPU", "A100", "H100", "RTX5090", "V100"]),
    "gpu_utilization_pct": st.floats(min_value=0.0, max_value=100.0),
    "modality": st.sampled_from(["text", "vision", "multimodal"]),
})


class TestBenchmarkRecordFuzz:
    @given(data=valid_record_strategy)
    @settings(max_examples=200)
    def test_valid_records_with_correct_ordering_always_parse(self, data):
        data["latency_p99_ms"] = max(data["latency_p99_ms"], data["latency_p50_ms"])
        data["context_length_p99"] = max(data["context_length_p99"], data["context_length_p50"])
        record = BenchmarkRecord(**data)
        assert record.latency_p99_ms >= record.latency_p50_ms
        assert record.context_length_p99 >= record.context_length_p50

    @given(
        p50=st.floats(min_value=0.0, max_value=1000.0),
        p99=st.floats(min_value=0.0, max_value=1000.0),
    )
    @settings(max_examples=100)
    def test_p99_lt_p50_always_rejected(self, p50, p99):
        assume(p99 < p50)
        from tests.conftest import TestDataFactory
        data = TestDataFactory.create_benchmark_record(latency_p50_ms=p50, latency_p99_ms=p99)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)

    @given(gpu_pct=st.floats(min_value=100.01, max_value=1000.0))
    @settings(max_examples=50)
    def test_gpu_over_100_always_rejected(self, gpu_pct):
        from tests.conftest import TestDataFactory
        data = TestDataFactory.create_benchmark_record(gpu_utilization_pct=gpu_pct)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)

    @given(latency=st.floats(max_value=-0.01))
    @settings(max_examples=50)
    def test_negative_values_always_rejected(self, latency):
        assume(latency < 0)
        from tests.conftest import TestDataFactory
        data = TestDataFactory.create_benchmark_record(latency_p50_ms=latency)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)
