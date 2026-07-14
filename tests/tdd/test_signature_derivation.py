"""Tier 1 TDD: Signature derivation logic."""

from __future__ import annotations

import json
import pytest

from awcde.signatures.service import SignatureService
from awcde.signatures.derivation import SignatureDerivation
from awcde.flyweight.registry import FlyweightRegistry
from awcde.models.telemetry import BenchmarkTelemetry, BenchmarkRecord
from awcde.models.signature import WorkloadSignature, DimensionLevel
from awcde.providers.base import ProviderSource
from awcde.providers.json_provider import JSONProvider
from tests.conftest import TestDataFactory, FIXTURES_DIR


pytestmark = pytest.mark.unit


DIMENSION_NAMES = [
    "latency_sensitivity", "throughput_orientation", "memory_intensity",
    "burst_behaviour", "context_length_profile", "concurrency_profile",
    "hardware_affinity", "modality",
]


class TestSignatureDerivation:
    @pytest.fixture
    def derivation(self):
        return SignatureDerivation(FlyweightRegistry())

    @pytest.fixture
    def telemetry(self):
        provider = JSONProvider()
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        source = ProviderSource(filename="test.json", content_type="application/json", content=content)
        return provider.ingest(source)

    def test_derives_all_8_dimensions(self, derivation, telemetry):
        sig = derivation.derive(telemetry)
        for dim in DIMENSION_NAMES:
            assert getattr(sig, dim) is not None, f"Missing {dim}"

    def test_signature_has_schema_version(self, derivation, telemetry):
        sig = derivation.derive(telemetry)
        assert sig.schema_version == "1.0.0"

    def test_signature_references_telemetry(self, derivation, telemetry):
        sig = derivation.derive(telemetry)
        assert sig.telemetry_id == telemetry.id

    def test_deterministic_id(self, derivation, telemetry):
        sig1 = derivation.derive(telemetry)
        sig2 = derivation.derive(telemetry)
        assert sig1.id == sig2.id

    def test_all_scores_in_range(self, derivation, telemetry):
        sig = derivation.derive(telemetry)
        for dim in DIMENSION_NAMES:
            score = getattr(sig, dim).score
            assert 0.0 <= score <= 1.0, f"{dim} score {score} out of range"


class TestSignatureIdentity:
    def test_same_input_same_id(self):
        from awcde.signatures.identity import compute_signature_id
        provider = JSONProvider()
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        source = ProviderSource(filename="test.json", content_type="application/json", content=content)
        t1 = provider.ingest(source)
        t2 = provider.ingest(source)
        id1 = compute_signature_id(t1, "1.0.0")
        id2 = compute_signature_id(t2, "1.0.0")
        assert id1 == id2

    def test_different_version_different_id(self):
        from awcde.signatures.identity import compute_signature_id
        provider = JSONProvider()
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        source = ProviderSource(filename="test.json", content_type="application/json", content=content)
        t1 = provider.ingest(source)
        id1 = compute_signature_id(t1, "1.0.0")
        id2 = compute_signature_id(t1, "2.0.0")
        assert id1 != id2
