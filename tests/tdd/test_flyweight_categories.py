"""Tier 1 TDD: Flyweight category definitions and evaluators."""

from __future__ import annotations

import pytest
from dataclasses import FrozenInstanceError

from awcde.flyweight.categories import (
    CategoryDefinition,
    CategoryEvaluator,
    CATEGORY_DEFINITIONS,
)
from awcde.models.signature import WorkloadSignature, DimensionScore, DimensionLevel
from tests.conftest import TestDataFactory


pytestmark = pytest.mark.unit


class TestCategoryDefinitions:
    def test_all_6_categories_defined(self):
        expected = {
            "latency_critical", "throughput_optimized", "memory_intensive",
            "burst_tolerant", "hardware_specialized", "general_purpose",
        }
        assert set(CATEGORY_DEFINITIONS.keys()) == expected

    def test_definitions_are_frozen(self):
        defn = CATEGORY_DEFINITIONS["latency_critical"]
        with pytest.raises(FrozenInstanceError):
            defn.name = "something_else"

    def test_each_has_dominant_dimension(self):
        for name, defn in CATEGORY_DEFINITIONS.items():
            if name != "general_purpose":
                assert defn.dominant_dimension, f"{name} has no dominant dimension"

    def test_min_score_in_range(self):
        for name, defn in CATEGORY_DEFINITIONS.items():
            assert 0.0 <= defn.min_score <= 1.0, f"{name} min_score out of range"


class TestCategoryEvaluator:
    def _make_signature_with_dimension(self, dim_name: str, score: float) -> WorkloadSignature:
        sig_data = TestDataFactory.create_signature_dict()
        sig_data[dim_name] = TestDataFactory.create_dimension_score(
            score=score,
            level="high" if score >= 0.7 else "medium" if score >= 0.3 else "low",
        )
        return WorkloadSignature(**sig_data)

    def test_latency_critical_matches_high_latency(self):
        sig = self._make_signature_with_dimension("latency_sensitivity", 0.85)
        evaluator = CategoryEvaluator(CATEGORY_DEFINITIONS["latency_critical"])
        matches, confidence = evaluator.matches(sig)
        assert matches
        assert confidence > 0.0

    def test_latency_critical_no_match_on_low_latency(self):
        sig = self._make_signature_with_dimension("latency_sensitivity", 0.2)
        evaluator = CategoryEvaluator(CATEGORY_DEFINITIONS["latency_critical"])
        matches, _ = evaluator.matches(sig)
        assert not matches

    def test_general_purpose_always_matches(self):
        sig = WorkloadSignature(**TestDataFactory.create_signature_dict())
        evaluator = CategoryEvaluator(CATEGORY_DEFINITIONS["general_purpose"])
        matches, confidence = evaluator.matches(sig)
        assert matches
