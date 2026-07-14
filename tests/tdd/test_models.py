"""Tier 1 TDD: Pydantic model validation, constraints, serialization."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from awcde.models.telemetry import BenchmarkRecord, BenchmarkTelemetry, ArrivalPattern, Modality
from awcde.models.signature import DimensionScore, DimensionLevel, WorkloadSignature
from awcde.models.classification import WorkloadClassification, ClassificationCategory
from awcde.models.recommendation import (
    RecommendationBlock,
    RecommendationEvidence,
    InfrastructureRecommendation,
)
from tests.conftest import TestDataFactory


pytestmark = pytest.mark.unit


class TestBenchmarkRecord:
    def test_valid_record(self, factory):
        data = factory.create_benchmark_record()
        record = BenchmarkRecord(**data)
        assert record.latency_p50_ms == 15.0
        assert record.modality == Modality.TEXT

    def test_negative_latency_rejected(self):
        data = TestDataFactory.create_benchmark_record(latency_p50_ms=-1.0)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)

    def test_gpu_over_100_rejected(self):
        data = TestDataFactory.create_benchmark_record(gpu_utilization_pct=101.0)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)

    def test_p99_lt_p50_rejected(self):
        data = TestDataFactory.create_benchmark_record(latency_p50_ms=100.0, latency_p99_ms=50.0)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)

    def test_context_p99_lt_p50_rejected(self):
        data = TestDataFactory.create_benchmark_record(context_length_p50=2048, context_length_p99=512)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)

    def test_invalid_modality_rejected(self):
        data = TestDataFactory.create_benchmark_record(modality="audio")
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)

    def test_concurrency_zero_rejected(self):
        data = TestDataFactory.create_benchmark_record(concurrency_level=0)
        with pytest.raises(ValidationError):
            BenchmarkRecord(**data)

    def test_serialization_roundtrip(self):
        data = TestDataFactory.create_benchmark_record()
        record = BenchmarkRecord(**data)
        dumped = record.model_dump()
        restored = BenchmarkRecord(**dumped)
        assert restored == record


class TestBenchmarkTelemetry:
    def test_auto_id(self):
        data = TestDataFactory.create_benchmark_record()
        telemetry = BenchmarkTelemetry(
            provider_id="json", source_ref="test.json", records=[BenchmarkRecord(**data)]
        )
        assert telemetry.id
        assert len(telemetry.id) > 0

    def test_auto_timestamp(self):
        data = TestDataFactory.create_benchmark_record()
        telemetry = BenchmarkTelemetry(
            provider_id="json", source_ref="test.json", records=[BenchmarkRecord(**data)]
        )
        assert telemetry.ingested_at is not None


class TestDimensionScore:
    def test_valid_score(self):
        score = DimensionScore(level=DimensionLevel.MEDIUM, score=0.5, raw_inputs={"a": 1.0})
        assert score.score == 0.5

    def test_score_out_of_range(self):
        with pytest.raises(ValidationError):
            DimensionScore(level=DimensionLevel.LOW, score=1.5, raw_inputs={})

    def test_negative_score_rejected(self):
        with pytest.raises(ValidationError):
            DimensionScore(level=DimensionLevel.LOW, score=-0.1, raw_inputs={})


class TestWorkloadClassification:
    def test_valid_classification(self):
        data = TestDataFactory.create_classification_dict()
        cls = WorkloadClassification(**data)
        assert cls.primary_category == ClassificationCategory.GENERAL_PURPOSE

    def test_confidence_range(self):
        data = TestDataFactory.create_classification_dict(confidence=1.5)
        with pytest.raises(ValidationError):
            WorkloadClassification(**data)


class TestInfrastructureRecommendation:
    def test_valid_recommendation(self):
        data = TestDataFactory.create_recommendation_dict()
        rec = InfrastructureRecommendation(**data)
        assert rec.model_family.recommendation == "general-purpose"

    def test_all_dimensions_present(self):
        data = TestDataFactory.create_recommendation_dict()
        rec = InfrastructureRecommendation(**data)
        dims = ["model_family", "runtime", "hardware_suitability", "deployment_topology", "scheduling_policy"]
        for dim in dims:
            assert getattr(rec, dim) is not None
