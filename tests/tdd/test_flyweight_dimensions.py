"""Tier 1 TDD: Flyweight dimension definitions and evaluators."""

from __future__ import annotations

import pytest
from dataclasses import FrozenInstanceError

from awcde.flyweight.dimensions import (
    DimensionDefinition,
    DimensionEvaluator,
    DIMENSION_DEFINITIONS,
)
from awcde.models.telemetry import BenchmarkRecord
from awcde.models.signature import DimensionLevel
from tests.conftest import TestDataFactory


pytestmark = pytest.mark.unit


class TestDimensionDefinitionImmutability:
    def test_all_8_dimensions_defined(self):
        expected = {
            "latency_sensitivity", "throughput_orientation", "memory_intensity",
            "burst_behaviour", "context_length_profile", "concurrency_profile",
            "hardware_affinity", "modality_profile",
        }
        assert set(DIMENSION_DEFINITIONS.keys()) == expected

    def test_definitions_are_frozen(self):
        defn = DIMENSION_DEFINITIONS["latency_sensitivity"]
        with pytest.raises(FrozenInstanceError):
            defn.name = "something_else"

    def test_definitions_have_thresholds(self):
        for name, defn in DIMENSION_DEFINITIONS.items():
            assert 0.0 <= defn.low_threshold < defn.high_threshold <= 1.0, f"{name} thresholds invalid"

    def test_definitions_have_input_fields(self):
        for name, defn in DIMENSION_DEFINITIONS.items():
            assert len(defn.input_fields) > 0, f"{name} has no input fields"


class TestDimensionEvaluator:
    @pytest.fixture
    def evaluator(self):
        return DimensionEvaluator(DIMENSION_DEFINITIONS["latency_sensitivity"])

    def test_evaluate_returns_dimension_score(self, evaluator):
        record = BenchmarkRecord(**TestDataFactory.create_benchmark_record())
        score = evaluator.evaluate(record)
        assert score.level in {DimensionLevel.LOW, DimensionLevel.MEDIUM, DimensionLevel.HIGH}
        assert 0.0 <= score.score <= 1.0
        assert len(score.raw_inputs) > 0

    def test_raw_inputs_contain_input_fields(self, evaluator):
        record = BenchmarkRecord(**TestDataFactory.create_benchmark_record())
        score = evaluator.evaluate(record)
        for field in evaluator.definition.input_fields:
            assert field in score.raw_inputs

    def test_score_always_in_range(self):
        for name, defn in DIMENSION_DEFINITIONS.items():
            evaluator = DimensionEvaluator(defn)
            record = BenchmarkRecord(**TestDataFactory.create_benchmark_record())
            score = evaluator.evaluate(record)
            assert 0.0 <= score.score <= 1.0, f"{name} score {score.score} out of range"


class TestLatencySensitivityScoring:
    @pytest.fixture
    def evaluator(self):
        return DimensionEvaluator(DIMENSION_DEFINITIONS["latency_sensitivity"])

    def test_high_latency_variance_scores_high(self, evaluator):
        record = BenchmarkRecord(**TestDataFactory.create_benchmark_record(
            latency_p50_ms=5.0, latency_p99_ms=500.0
        ))
        score = evaluator.evaluate(record)
        assert score.level == DimensionLevel.HIGH

    def test_low_latency_scores_low(self, evaluator):
        record = BenchmarkRecord(**TestDataFactory.create_benchmark_record(
            latency_p50_ms=5.0, latency_p99_ms=6.0
        ))
        score = evaluator.evaluate(record)
        assert score.level == DimensionLevel.LOW


class TestBurstBehaviourScoring:
    @pytest.fixture
    def evaluator(self):
        return DimensionEvaluator(DIMENSION_DEFINITIONS["burst_behaviour"])

    def test_bursty_pattern_scores_higher(self, evaluator):
        bursty = BenchmarkRecord(**TestDataFactory.create_benchmark_record(
            request_arrival_pattern="bursty", latency_p50_ms=10.0, latency_p99_ms=200.0
        ))
        steady = BenchmarkRecord(**TestDataFactory.create_benchmark_record(
            request_arrival_pattern="steady", latency_p50_ms=10.0, latency_p99_ms=200.0
        ))
        assert evaluator.evaluate(bursty).score > evaluator.evaluate(steady).score


class TestHardwareAffinityScoring:
    @pytest.fixture
    def evaluator(self):
        return DimensionEvaluator(DIMENSION_DEFINITIONS["hardware_affinity"])

    def test_cpu_scores_zero(self, evaluator):
        record = BenchmarkRecord(**TestDataFactory.create_benchmark_record(
            accelerator_type="CPU", gpu_utilization_pct=0.0
        ))
        score = evaluator.evaluate(record)
        assert score.score == 0.0

    def test_gpu_high_util_scores_high(self, evaluator):
        record = BenchmarkRecord(**TestDataFactory.create_benchmark_record(
            accelerator_type="H100", gpu_utilization_pct=95.0
        ))
        score = evaluator.evaluate(record)
        assert score.score > 0.7


class TestModalityScoring:
    @pytest.fixture
    def evaluator(self):
        return DimensionEvaluator(DIMENSION_DEFINITIONS["modality_profile"])

    def test_text_scores_low(self, evaluator):
        record = BenchmarkRecord(**TestDataFactory.create_benchmark_record(modality="text"))
        score = evaluator.evaluate(record)
        assert score.score == 0.2

    def test_multimodal_scores_high(self, evaluator):
        record = BenchmarkRecord(**TestDataFactory.create_benchmark_record(modality="multimodal"))
        score = evaluator.evaluate(record)
        assert score.score == 0.9
