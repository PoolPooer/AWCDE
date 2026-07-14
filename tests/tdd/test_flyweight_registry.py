"""Tier 1 TDD: FlyweightRegistry caching and instance sharing."""

from __future__ import annotations

import pytest

from awcde.flyweight.registry import FlyweightRegistry
from awcde.flyweight.dimensions import DimensionEvaluator, DIMENSION_DEFINITIONS
from awcde.flyweight.categories import CategoryEvaluator, CATEGORY_DEFINITIONS


pytestmark = pytest.mark.unit


class TestFlyweightRegistry:
    @pytest.fixture
    def registry(self):
        return FlyweightRegistry()

    def test_returns_dimension_evaluator(self, registry):
        evaluator = registry.get_dimension_evaluator("latency_sensitivity")
        assert isinstance(evaluator, DimensionEvaluator)
        assert evaluator.definition.name == "latency_sensitivity"

    def test_caches_dimension_evaluator(self, registry):
        e1 = registry.get_dimension_evaluator("latency_sensitivity")
        e2 = registry.get_dimension_evaluator("latency_sensitivity")
        assert e1 is e2

    def test_get_all_dimension_evaluators(self, registry):
        evaluators = registry.get_all_dimension_evaluators()
        assert len(evaluators) == 8
        names = {e.definition.name for e in evaluators}
        assert names == set(DIMENSION_DEFINITIONS.keys())

    def test_returns_category_evaluator(self, registry):
        evaluator = registry.get_category_evaluator("latency_critical")
        assert isinstance(evaluator, CategoryEvaluator)

    def test_caches_category_evaluator(self, registry):
        e1 = registry.get_category_evaluator("latency_critical")
        e2 = registry.get_category_evaluator("latency_critical")
        assert e1 is e2

    def test_get_all_category_evaluators(self, registry):
        evaluators = registry.get_all_category_evaluators()
        assert len(evaluators) == 6

    def test_unknown_dimension_raises(self, registry):
        with pytest.raises(KeyError):
            registry.get_dimension_evaluator("nonexistent")

    def test_unknown_category_raises(self, registry):
        with pytest.raises(KeyError):
            registry.get_category_evaluator("nonexistent")
