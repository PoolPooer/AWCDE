from __future__ import annotations

import json
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from pathlib import Path

from tests.conftest import TestDataFactory, FIXTURES_DIR
from awcde.models.signature import WorkloadSignature, DimensionScore, DimensionLevel
from awcde.models.classification import WorkloadClassification, ClassificationCategory
from awcde.providers.base import ProviderSource


pytestmark = pytest.mark.bdd

FEATURE_FILE = "../../features/core/classification.feature"


@scenario(FEATURE_FILE, "WHEN a signature is classified, the system SHALL return a classification with category and confidence")
def test_basic_classification():
    pass


@scenario(FEATURE_FILE, "WHEN a signature has high latency sensitivity, the system SHALL classify as latency_critical")
def test_latency_critical():
    pass


@scenario(FEATURE_FILE, "WHEN a signature has high throughput orientation, the system SHALL classify as throughput_optimized")
def test_throughput_optimized():
    pass


@scenario(FEATURE_FILE, "WHEN a signature has high memory intensity, the system SHALL classify as memory_intensive")
def test_memory_intensive():
    pass


@scenario(FEATURE_FILE, "WHEN a signature has high burst behaviour, the system SHALL classify as burst_tolerant")
def test_burst_tolerant():
    pass


@scenario(FEATURE_FILE, "WHILE no single dimension dominates, the system SHALL classify as general_purpose")
def test_general_purpose():
    pass


@scenario(FEATURE_FILE, "The system SHALL include dimension summary in every classification")
def test_dimension_summary():
    pass


@scenario(FEATURE_FILE, "The system SHALL reference at least one signature dimension in the rationale")
def test_rationale_references_dimension():
    pass


def _make_signature_with_high_dimension(dim_name: str, provider_registry, signature_service) -> WorkloadSignature:
    """Helper to create a signature where one dimension dominates."""
    factory_map = {
        "latency_sensitivity": TestDataFactory.create_benchmark_record_latency_critical,
        "throughput_orientation": TestDataFactory.create_benchmark_record_throughput_optimized,
        "memory_intensity": TestDataFactory.create_benchmark_record_memory_intensive,
        "burst_behaviour": TestDataFactory.create_benchmark_record_bursty,
    }
    factory_fn = factory_map.get(dim_name, TestDataFactory.create_benchmark_record)
    record = factory_fn()
    content = json.dumps({"records": [record]}).encode()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    telemetry = provider_registry.get("json").ingest(source)
    return signature_service.process(telemetry)


@given("a stored workload signature", target_fixture="signature")
def given_stored_signature(provider_registry, signature_service):
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    telemetry = provider_registry.get("json").ingest(source)
    return signature_service.process(telemetry)


@given("a workload signature with high latency sensitivity", target_fixture="signature")
def given_high_latency(provider_registry, signature_service):
    return _make_signature_with_high_dimension("latency_sensitivity", provider_registry, signature_service)


@given("a workload signature with high throughput orientation", target_fixture="signature")
def given_high_throughput(provider_registry, signature_service):
    return _make_signature_with_high_dimension("throughput_orientation", provider_registry, signature_service)


@given("a workload signature with high memory intensity", target_fixture="signature")
def given_high_memory(provider_registry, signature_service):
    return _make_signature_with_high_dimension("memory_intensity", provider_registry, signature_service)


@given("a workload signature with high burst behaviour", target_fixture="signature")
def given_high_burst(provider_registry, signature_service):
    return _make_signature_with_high_dimension("burst_behaviour", provider_registry, signature_service)


@given("a workload signature with balanced dimensions", target_fixture="signature")
def given_balanced(provider_registry, signature_service):
    record = TestDataFactory.create_benchmark_record()
    content = json.dumps({"records": [record]}).encode()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    telemetry = provider_registry.get("json").ingest(source)
    return signature_service.process(telemetry)


@given("any workload signature", target_fixture="signature")
def given_any_signature(provider_registry, signature_service):
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    telemetry = provider_registry.get("json").ingest(source)
    return signature_service.process(telemetry)


@when("the operator requests classification", target_fixture="classification")
def when_classify(signature, classifier):
    return classifier.process(signature)


@then("the system shall return a WorkloadClassification")
def then_is_classification(classification):
    assert isinstance(classification, WorkloadClassification)


@then("the classification shall have a primary_category")
def then_has_category(classification):
    assert classification.primary_category is not None


@then("the classification shall have a confidence between 0.0 and 1.0")
def then_confidence_range(classification):
    assert 0.0 <= classification.confidence <= 1.0


@then("the classification shall have a human-readable rationale")
def then_has_rationale(classification):
    assert classification.rationale
    assert len(classification.rationale) > 10


@then(parsers.parse('the primary_category shall be "{category}"'))
def then_category_is(classification, category):
    assert classification.primary_category.value == category


@then("the classification shall include a dimension_summary with key scores")
def then_has_dimension_summary(classification):
    assert classification.dimension_summary
    assert len(classification.dimension_summary) > 0


@then("the rationale shall reference at least one dimension name")
def then_rationale_references_dimension(classification):
    dimension_names = [
        "latency", "throughput", "memory", "burst",
        "context", "concurrency", "hardware", "modality",
    ]
    rationale_lower = classification.rationale.lower()
    assert any(dim in rationale_lower for dim in dimension_names)
