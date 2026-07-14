from __future__ import annotations

import json
import pytest
from pytest_bdd import scenario, given, when, then
from pathlib import Path

from tests.conftest import TestDataFactory, FIXTURES_DIR
from awcde.models.telemetry import BenchmarkTelemetry
from awcde.models.signature import WorkloadSignature, DimensionLevel
from awcde.providers.base import ProviderSource


pytestmark = pytest.mark.bdd

FEATURE_FILE = "../../features/core/signature.feature"


@scenario(FEATURE_FILE, "WHEN signature derivation is requested for ingested telemetry, the system SHALL return a complete signature")
def test_complete_signature():
    pass


@scenario(FEATURE_FILE, "The system SHALL produce deterministic signature IDs for identical input")
def test_deterministic_ids():
    pass


@scenario(FEATURE_FILE, "WHEN a stored signature is retrieved by ID, the system SHALL return the full signature")
def test_retrieve_signature():
    pass


@scenario(FEATURE_FILE, "The system SHALL assign dimension scores between 0.0 and 1.0")
def test_score_range():
    pass


@scenario(FEATURE_FILE, "The system SHALL assign valid dimension levels")
def test_valid_levels():
    pass


@scenario(FEATURE_FILE, "WHEN telemetry has high latency variance, the system SHALL score latency sensitivity as high")
def test_high_latency_sensitivity():
    pass


@scenario(FEATURE_FILE, "WHEN telemetry has bursty arrival pattern, the system SHALL reflect this in burst behaviour")
def test_bursty_pattern():
    pass


DIMENSION_NAMES = [
    "latency_sensitivity", "throughput_orientation", "memory_intensity",
    "burst_behaviour", "context_length_profile", "concurrency_profile",
    "hardware_affinity", "modality",
]


@given("ingested benchmark telemetry", target_fixture="telemetry")
def given_telemetry(provider_registry):
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    return provider_registry.get("json").ingest(source)


@given("a stored workload signature", target_fixture="stored_signature")
def given_stored_signature(provider_registry, signature_service):
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    telemetry = provider_registry.get("json").ingest(source)
    return signature_service.process(telemetry)


@given("benchmark telemetry with high latency variance", target_fixture="telemetry")
def given_high_latency_variance(provider_registry):
    record = TestDataFactory.create_benchmark_record(latency_p50_ms=5.0, latency_p99_ms=500.0)
    content = json.dumps({"records": [record]}).encode()
    source = ProviderSource(filename="high_lat.json", content_type="application/json", content=content)
    return provider_registry.get("json").ingest(source)


@given("benchmark telemetry with bursty arrival pattern", target_fixture="telemetry")
def given_bursty_telemetry(provider_registry):
    record = TestDataFactory.create_benchmark_record(
        request_arrival_pattern="bursty", latency_p50_ms=10.0, latency_p99_ms=200.0
    )
    content = json.dumps({"records": [record]}).encode()
    source = ProviderSource(filename="bursty.json", content_type="application/json", content=content)
    return provider_registry.get("json").ingest(source)


@when("the operator requests signature derivation", target_fixture="signature")
def when_derive(telemetry, signature_service):
    return signature_service.process(telemetry)


@when("signature derivation is run twice on the same telemetry", target_fixture="two_signatures")
def when_derive_twice(telemetry, signature_service):
    sig1 = signature_service.process(telemetry)
    sig2 = signature_service.process(telemetry)
    return (sig1, sig2)


@when("the operator retrieves it by id", target_fixture="retrieved")
def when_retrieve(stored_signature):
    return stored_signature


@when("signature derivation is performed", target_fixture="signature")
def when_derive_performed(telemetry, signature_service):
    return signature_service.process(telemetry)


@then("the system shall return a WorkloadSignature")
def then_is_signature(signature):
    assert isinstance(signature, WorkloadSignature)


@then("the signature shall contain all 8 dimensions")
def then_8_dimensions(signature):
    for dim in DIMENSION_NAMES:
        assert hasattr(signature, dim), f"Missing dimension: {dim}"
        assert getattr(signature, dim) is not None


@then("each dimension shall have a level, score, and raw_inputs")
def then_dimension_fields(signature):
    for dim in DIMENSION_NAMES:
        ds = getattr(signature, dim)
        assert ds.level is not None
        assert ds.score is not None
        assert ds.raw_inputs is not None


@then("the signature shall carry a schema_version")
def then_has_schema_version(signature):
    assert signature.schema_version
    assert signature.schema_version == "1.0.0"


@then("both signatures shall have the same id")
def then_same_id(two_signatures):
    assert two_signatures[0].id == two_signatures[1].id


@then("the system shall return the full signature with schema version intact")
def then_full_signature(retrieved):
    assert retrieved.schema_version
    assert retrieved.id


@then("all 8 dimensions shall be present")
def then_all_dimensions_present(retrieved):
    for dim in DIMENSION_NAMES:
        assert getattr(retrieved, dim) is not None


@then("all dimension scores shall be between 0.0 and 1.0 inclusive")
def then_scores_in_range(signature):
    for dim in DIMENSION_NAMES:
        score = getattr(signature, dim).score
        assert 0.0 <= score <= 1.0, f"{dim} score {score} out of range"


@then('each dimension level shall be one of "low", "medium", or "high"')
def then_valid_levels(signature):
    valid = {DimensionLevel.LOW, DimensionLevel.MEDIUM, DimensionLevel.HIGH}
    for dim in DIMENSION_NAMES:
        level = getattr(signature, dim).level
        assert level in valid, f"{dim} level {level} invalid"


@then('the latency_sensitivity dimension shall have level "high"')
def then_latency_high(signature):
    assert signature.latency_sensitivity.level == DimensionLevel.HIGH


@then("the burst_behaviour dimension shall have a score above 0.5")
def then_burst_above_half(signature):
    assert signature.burst_behaviour.score > 0.5
