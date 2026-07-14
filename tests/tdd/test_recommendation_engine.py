"""Tier 1 TDD: Recommendation engine tests."""

from __future__ import annotations

import pytest

from awcde.recommendations.engine import RecommendationEngine
from awcde.knowledge.static_kb import StaticKnowledgeBase
from awcde.models.signature import WorkloadSignature
from awcde.models.classification import WorkloadClassification
from awcde.models.recommendation import InfrastructureRecommendation
from tests.conftest import TestDataFactory, FIXTURES_DIR


pytestmark = pytest.mark.unit

RECOMMENDATION_DIMENSIONS = [
    "model_family", "runtime", "hardware_suitability",
    "deployment_topology", "scheduling_policy",
]


class TestRecommendationEngine:
    @pytest.fixture
    def engine(self):
        kb = StaticKnowledgeBase()
        kb.load(FIXTURES_DIR / "rules_test.yaml")
        return RecommendationEngine(kb)

    @pytest.fixture
    def classification_and_signature(self):
        sig = WorkloadSignature(**TestDataFactory.create_signature_dict())
        cls = WorkloadClassification(**TestDataFactory.create_classification_dict(
            signature_id=sig.id,
        ))
        return cls, sig

    def test_produces_recommendation(self, engine, classification_and_signature):
        cls, sig = classification_and_signature
        rec = engine.process(cls, sig)
        assert isinstance(rec, InfrastructureRecommendation)

    def test_all_5_dimensions_present(self, engine, classification_and_signature):
        cls, sig = classification_and_signature
        rec = engine.process(cls, sig)
        for dim in RECOMMENDATION_DIMENSIONS:
            block = getattr(rec, dim)
            assert block is not None
            assert block.recommendation

    def test_all_dimensions_have_reasoning(self, engine, classification_and_signature):
        cls, sig = classification_and_signature
        rec = engine.process(cls, sig)
        for dim in RECOMMENDATION_DIMENSIONS:
            block = getattr(rec, dim)
            assert block.reasoning

    def test_all_dimensions_have_evidence(self, engine, classification_and_signature):
        cls, sig = classification_and_signature
        rec = engine.process(cls, sig)
        for dim in RECOMMENDATION_DIMENSIONS:
            block = getattr(rec, dim)
            assert len(block.evidence) >= 1

    def test_evidence_references_rule_ids(self, engine, classification_and_signature):
        cls, sig = classification_and_signature
        rec = engine.process(cls, sig)
        for dim in RECOMMENDATION_DIMENSIONS:
            for ev in getattr(rec, dim).evidence:
                assert ev.rule_id

    def test_references_classification_and_signature(self, engine, classification_and_signature):
        cls, sig = classification_and_signature
        rec = engine.process(cls, sig)
        assert rec.classification_id == cls.id
        assert rec.signature_id == sig.id


class TestRecommendationEngineFallback:
    def test_empty_kb_still_produces_recommendations(self):
        kb = StaticKnowledgeBase()
        engine = RecommendationEngine(kb)
        sig = WorkloadSignature(**TestDataFactory.create_signature_dict())
        cls = WorkloadClassification(**TestDataFactory.create_classification_dict(
            signature_id=sig.id,
        ))
        rec = engine.process(cls, sig)
        assert isinstance(rec, InfrastructureRecommendation)
        for dim in RECOMMENDATION_DIMENSIONS:
            assert getattr(rec, dim) is not None
