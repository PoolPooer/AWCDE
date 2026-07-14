"""Tier 1 TDD: KnowledgeBase tests."""

from __future__ import annotations

import pytest

from awcde.knowledge.static_kb import StaticKnowledgeBase
from awcde.models.knowledge import KnowledgeRule
from awcde.models.signature import WorkloadSignature
from awcde.models.classification import WorkloadClassification, ClassificationCategory
from tests.conftest import TestDataFactory, FIXTURES_DIR


pytestmark = pytest.mark.unit


class TestStaticKnowledgeBase:
    @pytest.fixture
    def kb(self):
        kb = StaticKnowledgeBase()
        kb.load(FIXTURES_DIR / "rules_test.yaml")
        return kb

    def test_load_rules(self, kb):
        rule = kb.get_rule("kb-latency-001")
        assert rule is not None
        assert rule.rule_id == "kb-latency-001"

    def test_get_unknown_rule(self, kb):
        assert kb.get_rule("nonexistent") is None

    def test_query_latency_critical(self, kb):
        sig_data = TestDataFactory.create_signature_dict()
        sig_data["latency_sensitivity"] = TestDataFactory.create_dimension_score(score=0.85, level="high")
        sig = WorkloadSignature(**sig_data)

        cls_data = TestDataFactory.create_classification_dict(
            primary_category="latency_critical",
            signature_id=sig.id,
        )
        cls = WorkloadClassification(**cls_data)

        matches = kb.query(cls, sig)
        assert len(matches) > 0
        rule_ids = {m.rule_id for m in matches}
        assert "kb-latency-001" in rule_ids

    def test_query_general_purpose(self, kb):
        sig = WorkloadSignature(**TestDataFactory.create_signature_dict())
        cls_data = TestDataFactory.create_classification_dict(
            primary_category="general_purpose",
            signature_id=sig.id,
        )
        cls = WorkloadClassification(**cls_data)

        matches = kb.query(cls, sig)
        assert len(matches) > 0
        rule_ids = {m.rule_id for m in matches}
        assert "kb-general-001" in rule_ids

    def test_matches_have_rendered_rationale(self, kb):
        sig = WorkloadSignature(**TestDataFactory.create_signature_dict())
        cls_data = TestDataFactory.create_classification_dict(
            primary_category="general_purpose",
            signature_id=sig.id,
        )
        cls = WorkloadClassification(**cls_data)

        matches = kb.query(cls, sig)
        for match in matches:
            assert match.rationale
            assert len(match.rationale) > 0
