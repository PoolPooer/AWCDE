"""Tier 1 TDD: WorkloadClassifier tests."""

from __future__ import annotations

import json
import pytest

from awcde.classification.classifier import WorkloadClassifier
from awcde.flyweight.registry import FlyweightRegistry
from awcde.models.signature import WorkloadSignature
from awcde.models.classification import WorkloadClassification, ClassificationCategory
from tests.conftest import TestDataFactory


pytestmark = pytest.mark.unit


class TestWorkloadClassifier:
    @pytest.fixture
    def classifier(self):
        return WorkloadClassifier(FlyweightRegistry())

    def _make_signature(self, **dimension_overrides) -> WorkloadSignature:
        sig_data = TestDataFactory.create_signature_dict()
        for dim, score in dimension_overrides.items():
            sig_data[dim] = TestDataFactory.create_dimension_score(
                score=score,
                level="high" if score >= 0.7 else "medium" if score >= 0.3 else "low",
            )
        return WorkloadSignature(**sig_data)

    def test_classify_returns_classification(self, classifier):
        sig = self._make_signature()
        cls = classifier.process(sig)
        assert isinstance(cls, WorkloadClassification)

    def test_high_latency_classified_as_latency_critical(self, classifier):
        sig = self._make_signature(latency_sensitivity=0.9)
        cls = classifier.process(sig)
        assert cls.primary_category == ClassificationCategory.LATENCY_CRITICAL

    def test_high_throughput_classified(self, classifier):
        sig = self._make_signature(throughput_orientation=0.9)
        cls = classifier.process(sig)
        assert cls.primary_category == ClassificationCategory.THROUGHPUT_OPTIMIZED

    def test_high_memory_classified(self, classifier):
        sig = self._make_signature(memory_intensity=0.9)
        cls = classifier.process(sig)
        assert cls.primary_category == ClassificationCategory.MEMORY_INTENSIVE

    def test_balanced_classified_as_general(self, classifier):
        sig = self._make_signature(
            latency_sensitivity=0.4, throughput_orientation=0.4,
            memory_intensity=0.4, burst_behaviour=0.2,
        )
        cls = classifier.process(sig)
        assert cls.primary_category == ClassificationCategory.GENERAL_PURPOSE

    def test_confidence_in_range(self, classifier):
        sig = self._make_signature()
        cls = classifier.process(sig)
        assert 0.0 <= cls.confidence <= 1.0

    def test_rationale_not_empty(self, classifier):
        sig = self._make_signature()
        cls = classifier.process(sig)
        assert cls.rationale
        assert len(cls.rationale) > 10

    def test_dimension_summary_present(self, classifier):
        sig = self._make_signature()
        cls = classifier.process(sig)
        assert cls.dimension_summary
        assert len(cls.dimension_summary) > 0

    def test_references_signature_id(self, classifier):
        sig = self._make_signature()
        cls = classifier.process(sig)
        assert cls.signature_id == sig.id
