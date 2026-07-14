"""Tier 5 Fuzz: Property-based tests for schema validation edge cases."""

from __future__ import annotations

import json
import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st
from pydantic import ValidationError

from awcde.models.telemetry import BenchmarkRecord


pytestmark = pytest.mark.fuzz


class TestSchemaValidationFuzz:
    @given(
        concurrency=st.integers(max_value=0),
    )
    @settings(max_examples=50)
    def test_zero_or_negative_concurrency_rejected(self, concurrency):
        from tests.conftest import TestDataFactory
        data = TestDataFactory.create_benchmark_record(concurrency_level=concurrency)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)

    @given(
        gpu=st.floats(min_value=-1000.0, max_value=-0.01),
    )
    @settings(max_examples=50)
    def test_negative_gpu_rejected(self, gpu):
        from tests.conftest import TestDataFactory
        data = TestDataFactory.create_benchmark_record(gpu_utilization_pct=gpu)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)

    @given(
        throughput=st.floats(min_value=-1000.0, max_value=-0.01),
    )
    @settings(max_examples=50)
    def test_negative_throughput_rejected(self, throughput):
        from tests.conftest import TestDataFactory
        data = TestDataFactory.create_benchmark_record(throughput_rps=throughput)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)

    @given(
        memory=st.floats(min_value=-1000.0, max_value=-0.01),
    )
    @settings(max_examples=50)
    def test_negative_memory_rejected(self, memory):
        from tests.conftest import TestDataFactory
        data = TestDataFactory.create_benchmark_record(peak_memory_gb=memory)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)
