"""Tier 1 TDD: Deterministic signature identity."""

from __future__ import annotations

import json
import pytest

from awcde.signatures.identity import compute_signature_id
from awcde.models.telemetry import BenchmarkTelemetry, BenchmarkRecord
from tests.conftest import TestDataFactory


pytestmark = pytest.mark.unit


class TestComputeSignatureId:
    def _make_telemetry(self, **record_overrides):
        record_data = TestDataFactory.create_benchmark_record(**record_overrides)
        record = BenchmarkRecord(**record_data)
        return BenchmarkTelemetry(
            provider_id="json", source_ref="test.json", records=[record]
        )

    def test_returns_hex_string(self):
        t = self._make_telemetry()
        sig_id = compute_signature_id(t, "1.0.0")
        assert isinstance(sig_id, str)
        assert len(sig_id) == 64  # SHA-256 hex digest

    def test_deterministic(self):
        t1 = self._make_telemetry()
        t2 = self._make_telemetry()
        assert compute_signature_id(t1, "1.0.0") == compute_signature_id(t2, "1.0.0")

    def test_different_data_different_id(self):
        t1 = self._make_telemetry(latency_p50_ms=10.0)
        t2 = self._make_telemetry(latency_p50_ms=20.0)
        assert compute_signature_id(t1, "1.0.0") != compute_signature_id(t2, "1.0.0")

    def test_different_version_different_id(self):
        t = self._make_telemetry()
        id1 = compute_signature_id(t, "1.0.0")
        id2 = compute_signature_id(t, "2.0.0")
        assert id1 != id2
