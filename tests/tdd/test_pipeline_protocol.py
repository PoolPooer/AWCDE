"""Tier 1 TDD: CSP pipeline stage contracts."""

from __future__ import annotations

import pytest

from awcde.pipeline.protocol import PipelineStage
from awcde.signatures.service import SignatureService
from awcde.classification.classifier import WorkloadClassifier
from awcde.flyweight.registry import FlyweightRegistry


pytestmark = pytest.mark.unit


class TestPipelineStageProtocol:
    def test_signature_service_has_process_method(self):
        registry = FlyweightRegistry()
        service = SignatureService(registry)
        assert hasattr(service, "process")
        assert callable(service.process)

    def test_classifier_has_process_method(self):
        registry = FlyweightRegistry()
        classifier = WorkloadClassifier(registry)
        assert hasattr(classifier, "process")
        assert callable(classifier.process)
