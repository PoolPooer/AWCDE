"""Tier 1 TDD: Recommendation explainer tests."""

from __future__ import annotations

import pytest

from awcde.recommendations.explainer import RecommendationExplainer
from awcde.models.knowledge import RuleMatch, RuleCondition
from awcde.models.signature import WorkloadSignature
from awcde.models.classification import WorkloadClassification
from tests.conftest import TestDataFactory


pytestmark = pytest.mark.unit


class TestRecommendationExplainer:
    @pytest.fixture
    def explainer(self):
        return RecommendationExplainer()

    @pytest.fixture
    def classification_and_signature(self):
        sig = WorkloadSignature(**TestDataFactory.create_signature_dict())
        cls = WorkloadClassification(**TestDataFactory.create_classification_dict(signature_id=sig.id))
        return cls, sig

    def test_build_reasoning_returns_string(self, explainer, classification_and_signature):
        cls, sig = classification_and_signature
        match = RuleMatch(
            rule_id="kb-test-001",
            recommendations={"runtime": "vllm-standard"},
            rationale="Test rule matched.",
            matched_conditions=[
                RuleCondition(field="classification.primary_category", operator="eq", value="general_purpose")
            ],
        )
        reasoning = explainer.build_reasoning([match], "runtime", cls, sig)
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_references_rule(self, explainer, classification_and_signature):
        cls, sig = classification_and_signature
        match = RuleMatch(
            rule_id="kb-latency-001",
            recommendations={"runtime": "vllm-low-latency"},
            rationale="Latency-critical workload detected.",
            matched_conditions=[],
        )
        reasoning = explainer.build_reasoning([match], "runtime", cls, sig)
        assert "kb-latency-001" in reasoning or "latency" in reasoning.lower()

    def test_reasoning_for_no_matches(self, explainer, classification_and_signature):
        cls, sig = classification_and_signature
        reasoning = explainer.build_reasoning([], "runtime", cls, sig)
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0
