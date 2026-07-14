"""Tier 1 TDD: Evidence collector tests."""

from __future__ import annotations

import pytest

from awcde.recommendations.evidence import EvidenceCollector
from awcde.models.knowledge import RuleMatch, RuleCondition
from awcde.models.recommendation import RecommendationEvidence
from awcde.models.signature import WorkloadSignature
from awcde.models.classification import WorkloadClassification
from tests.conftest import TestDataFactory


pytestmark = pytest.mark.unit


class TestEvidenceCollector:
    @pytest.fixture
    def collector(self):
        return EvidenceCollector()

    @pytest.fixture
    def classification_and_signature(self):
        sig = WorkloadSignature(**TestDataFactory.create_signature_dict())
        cls = WorkloadClassification(**TestDataFactory.create_classification_dict(signature_id=sig.id))
        return cls, sig

    def test_collect_returns_evidence_list(self, collector, classification_and_signature):
        cls, sig = classification_and_signature
        match = RuleMatch(
            rule_id="kb-test-001",
            recommendations={},
            rationale="Test",
            matched_conditions=[
                RuleCondition(field="classification.primary_category", operator="eq", value="general_purpose")
            ],
        )
        evidence = collector.collect(match, cls, sig)
        assert isinstance(evidence, list)
        assert len(evidence) >= 1

    def test_evidence_has_rule_id(self, collector, classification_and_signature):
        cls, sig = classification_and_signature
        match = RuleMatch(
            rule_id="kb-test-001",
            recommendations={},
            rationale="Test",
            matched_conditions=[
                RuleCondition(field="classification.primary_category", operator="eq", value="general_purpose")
            ],
        )
        evidence = collector.collect(match, cls, sig)
        for ev in evidence:
            assert ev.rule_id == "kb-test-001"

    def test_evidence_has_source_type(self, collector, classification_and_signature):
        cls, sig = classification_and_signature
        match = RuleMatch(
            rule_id="kb-test-001",
            recommendations={},
            rationale="Test",
            matched_conditions=[
                RuleCondition(field="classification.primary_category", operator="eq", value="general_purpose")
            ],
        )
        evidence = collector.collect(match, cls, sig)
        for ev in evidence:
            assert ev.source_type in ("signature", "classification", "telemetry")
