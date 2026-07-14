"""Tier 4 Contract: Pydantic models match documented schema fields."""

from __future__ import annotations

import pytest

from awcde.models.telemetry import BenchmarkRecord, BenchmarkTelemetry
from awcde.models.signature import WorkloadSignature, DimensionScore
from awcde.models.classification import WorkloadClassification, ClassificationCategory
from awcde.models.recommendation import (
    InfrastructureRecommendation,
    RecommendationBlock,
    RecommendationEvidence,
)
from awcde.models.knowledge import KnowledgeRule, RuleCondition, RuleMatch


pytestmark = pytest.mark.contract


class TestBenchmarkRecordContract:
    REQUIRED_FIELDS = {
        "latency_p50_ms", "latency_p99_ms", "throughput_rps",
        "peak_memory_gb", "avg_memory_gb", "request_arrival_pattern",
        "context_length_p50", "context_length_p99", "concurrency_level",
        "accelerator_type", "gpu_utilization_pct", "modality",
    }

    def test_has_all_12_required_fields(self):
        actual = set(BenchmarkRecord.model_fields.keys())
        assert self.REQUIRED_FIELDS.issubset(actual)
        assert len(self.REQUIRED_FIELDS) == 12


class TestBenchmarkTelemetryContract:
    REQUIRED_FIELDS = {"id", "provider_id", "source_ref", "ingested_at", "records"}

    def test_has_required_fields(self):
        actual = set(BenchmarkTelemetry.model_fields.keys())
        assert self.REQUIRED_FIELDS.issubset(actual)


class TestWorkloadSignatureContract:
    DIMENSION_FIELDS = {
        "latency_sensitivity", "throughput_orientation", "memory_intensity",
        "burst_behaviour", "context_length_profile", "concurrency_profile",
        "hardware_affinity", "modality",
    }
    METADATA_FIELDS = {"id", "schema_version", "telemetry_id", "derived_at"}

    def test_has_all_8_dimension_fields(self):
        actual = set(WorkloadSignature.model_fields.keys())
        assert self.DIMENSION_FIELDS.issubset(actual)

    def test_has_metadata_fields(self):
        actual = set(WorkloadSignature.model_fields.keys())
        assert self.METADATA_FIELDS.issubset(actual)

    def test_total_field_count(self):
        expected = len(self.DIMENSION_FIELDS) + len(self.METADATA_FIELDS)
        assert len(WorkloadSignature.model_fields) == expected


class TestDimensionScoreContract:
    def test_has_level_score_raw_inputs(self):
        fields = set(DimensionScore.model_fields.keys())
        assert {"level", "score", "raw_inputs"}.issubset(fields)


class TestClassificationContract:
    REQUIRED_FIELDS = {
        "id", "signature_id", "classified_at", "primary_category",
        "confidence", "rationale", "dimension_summary",
    }

    def test_has_required_fields(self):
        actual = set(WorkloadClassification.model_fields.keys())
        assert self.REQUIRED_FIELDS.issubset(actual)

    def test_6_classification_categories(self):
        categories = [c.value for c in ClassificationCategory]
        expected = {
            "latency_critical", "throughput_optimized", "memory_intensive",
            "burst_tolerant", "hardware_specialized", "general_purpose",
        }
        assert set(categories) == expected


class TestRecommendationContract:
    DIMENSION_FIELDS = {
        "model_family", "runtime", "hardware_suitability",
        "deployment_topology", "scheduling_policy",
    }
    METADATA_FIELDS = {"id", "classification_id", "signature_id", "generated_at"}

    def test_has_5_dimension_fields(self):
        actual = set(InfrastructureRecommendation.model_fields.keys())
        assert self.DIMENSION_FIELDS.issubset(actual)

    def test_has_metadata_fields(self):
        actual = set(InfrastructureRecommendation.model_fields.keys())
        assert self.METADATA_FIELDS.issubset(actual)


class TestRecommendationBlockContract:
    def test_has_required_fields(self):
        fields = set(RecommendationBlock.model_fields.keys())
        assert {"recommendation", "reasoning", "evidence"}.issubset(fields)


class TestRecommendationEvidenceContract:
    def test_has_required_fields(self):
        fields = set(RecommendationEvidence.model_fields.keys())
        expected = {"rule_id", "source_type", "attribute", "attribute_value", "condition_matched"}
        assert expected.issubset(fields)


class TestKnowledgeRuleContract:
    def test_has_required_fields(self):
        fields = set(KnowledgeRule.model_fields.keys())
        expected = {"rule_id", "version", "description", "conditions", "recommendations", "rationale_template"}
        assert expected.issubset(fields)
