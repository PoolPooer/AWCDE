"""Tier 5 Fuzz: Property-based tests for dimension scoring invariants."""

from __future__ import annotations

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from awcde.flyweight.dimensions import DimensionEvaluator, DIMENSION_DEFINITIONS
from awcde.models.telemetry import BenchmarkRecord
from awcde.models.signature import DimensionLevel


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
    "accelerator_type": st.sampled_from(["CPU", "A100", "H100", "RTX5090"]),
    "gpu_utilization_pct": st.floats(min_value=0.0, max_value=100.0),
    "modality": st.sampled_from(["text", "vision", "multimodal"]),
})


class TestDimensionScoringInvariants:
    @given(data=valid_record_strategy)
    @settings(max_examples=200)
    def test_all_scores_in_unit_interval(self, data):
        data["latency_p99_ms"] = max(data["latency_p99_ms"], data["latency_p50_ms"])
        data["context_length_p99"] = max(data["context_length_p99"], data["context_length_p50"])
        record = BenchmarkRecord(**data)

        for name, defn in DIMENSION_DEFINITIONS.items():
            evaluator = DimensionEvaluator(defn)
            score = evaluator.evaluate(record)
            assert 0.0 <= score.score <= 1.0, f"{name} score {score.score} out of [0,1]"

    @given(data=valid_record_strategy)
    @settings(max_examples=200)
    def test_all_levels_are_valid(self, data):
        data["latency_p99_ms"] = max(data["latency_p99_ms"], data["latency_p50_ms"])
        data["context_length_p99"] = max(data["context_length_p99"], data["context_length_p50"])
        record = BenchmarkRecord(**data)

        valid_levels = {DimensionLevel.LOW, DimensionLevel.MEDIUM, DimensionLevel.HIGH}
        for name, defn in DIMENSION_DEFINITIONS.items():
            evaluator = DimensionEvaluator(defn)
            score = evaluator.evaluate(record)
            assert score.level in valid_levels, f"{name} level {score.level} not valid"

    @given(data=valid_record_strategy)
    @settings(max_examples=200)
    def test_level_consistent_with_score(self, data):
        data["latency_p99_ms"] = max(data["latency_p99_ms"], data["latency_p50_ms"])
        data["context_length_p99"] = max(data["context_length_p99"], data["context_length_p50"])
        record = BenchmarkRecord(**data)

        for name, defn in DIMENSION_DEFINITIONS.items():
            evaluator = DimensionEvaluator(defn)
            result = evaluator.evaluate(record)
            if result.score < defn.low_threshold:
                assert result.level == DimensionLevel.LOW
            elif result.score >= defn.high_threshold:
                assert result.level == DimensionLevel.HIGH
            else:
                assert result.level == DimensionLevel.MEDIUM

    @given(data=valid_record_strategy)
    @settings(max_examples=100)
    def test_raw_inputs_contain_definition_fields(self, data):
        data["latency_p99_ms"] = max(data["latency_p99_ms"], data["latency_p50_ms"])
        data["context_length_p99"] = max(data["context_length_p99"], data["context_length_p50"])
        record = BenchmarkRecord(**data)

        for name, defn in DIMENSION_DEFINITIONS.items():
            evaluator = DimensionEvaluator(defn)
            result = evaluator.evaluate(record)
            for field in defn.input_fields:
                assert field in result.raw_inputs, f"{name} missing {field} in raw_inputs"
