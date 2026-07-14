"""Tier 5 Fuzz: Property-based tests for classification invariants."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from awcde.models.signature import WorkloadSignature, DimensionScore, DimensionLevel
from awcde.models.classification import ClassificationCategory
from awcde.classification.classifier import WorkloadClassifier
from awcde.flyweight.registry import FlyweightRegistry


pytestmark = pytest.mark.fuzz


DIMENSION_NAMES = [
    "latency_sensitivity", "throughput_orientation", "memory_intensity",
    "burst_behaviour", "context_length_profile", "concurrency_profile",
    "hardware_affinity", "modality",
]

dimension_score_strategy = st.builds(
    DimensionScore,
    level=st.sampled_from([DimensionLevel.LOW, DimensionLevel.MEDIUM, DimensionLevel.HIGH]),
    score=st.floats(min_value=0.0, max_value=1.0),
    raw_inputs=st.just({"test_field": 1.0}),
)


def make_signature_strategy():
    return st.fixed_dictionaries({
        "id": st.just("sig-test"),
        "schema_version": st.just("1.0.0"),
        "telemetry_id": st.just("tel-test"),
        "derived_at": st.just("2026-01-01T00:00:00+00:00"),
        **{dim: dimension_score_strategy for dim in DIMENSION_NAMES},
    })


class TestClassificationInvariants:
    @given(data=make_signature_strategy())
    @settings(max_examples=200)
    def test_always_produces_valid_category(self, data):
        sig = WorkloadSignature(**data)
        classifier = WorkloadClassifier(FlyweightRegistry())
        classification = classifier.process(sig)
        valid_categories = {c.value for c in ClassificationCategory}
        assert classification.primary_category.value in valid_categories

    @given(data=make_signature_strategy())
    @settings(max_examples=200)
    def test_confidence_always_in_range(self, data):
        sig = WorkloadSignature(**data)
        classifier = WorkloadClassifier(FlyweightRegistry())
        classification = classifier.process(sig)
        assert 0.0 <= classification.confidence <= 1.0

    @given(data=make_signature_strategy())
    @settings(max_examples=100)
    def test_always_has_rationale(self, data):
        sig = WorkloadSignature(**data)
        classifier = WorkloadClassifier(FlyweightRegistry())
        classification = classifier.process(sig)
        assert classification.rationale
        assert len(classification.rationale) > 0

    @given(data=make_signature_strategy())
    @settings(max_examples=100)
    def test_always_has_dimension_summary(self, data):
        sig = WorkloadSignature(**data)
        classifier = WorkloadClassifier(FlyweightRegistry())
        classification = classifier.process(sig)
        assert classification.dimension_summary
        assert len(classification.dimension_summary) > 0
