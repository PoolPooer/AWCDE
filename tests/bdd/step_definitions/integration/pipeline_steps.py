from __future__ import annotations

import json
import time
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from pathlib import Path

from tests.conftest import TestDataFactory, FIXTURES_DIR
from awcde.models.telemetry import BenchmarkTelemetry
from awcde.models.signature import WorkloadSignature
from awcde.models.classification import WorkloadClassification
from awcde.models.recommendation import InfrastructureRecommendation
from awcde.providers.base import ProviderSource


pytestmark = pytest.mark.bdd

FEATURE_FILE = "../../features/integration/pipeline.feature"


@scenario(FEATURE_FILE, "WHEN the full pipeline is executed, the system SHALL produce recommendations from raw telemetry")
def test_full_pipeline():
    pass


@scenario(FEATURE_FILE, "The system SHALL maintain traceability across the full pipeline")
def test_traceability():
    pass


@scenario(FEATURE_FILE, "WHEN a latency-critical benchmark is processed end-to-end, the system SHALL recommend appropriate infrastructure")
def test_latency_critical_pipeline():
    pass


@scenario(FEATURE_FILE, "WHEN a throughput-oriented benchmark is processed end-to-end, the system SHALL recommend batching")
def test_throughput_pipeline():
    pass


@scenario(FEATURE_FILE, "The pipeline SHALL complete within performance bounds")
def test_performance():
    pass


@given("a valid JSON benchmark file", target_fixture="source")
def given_valid_json():
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    return ProviderSource(filename="test.json", content_type="application/json", content=content)


@given("a valid JSON benchmark file processed through the full pipeline", target_fixture="pipeline_result")
def given_processed(provider_registry, signature_service, classifier, recommendation_engine):
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    telemetry = provider_registry.get("json").ingest(source)
    signature = signature_service.process(telemetry)
    classification = classifier.process(signature)
    recommendation = recommendation_engine.process(classification, signature)
    return {
        "telemetry": telemetry,
        "signature": signature,
        "classification": classification,
        "recommendation": recommendation,
    }


@given("a benchmark file representing a latency-critical workload", target_fixture="source")
def given_latency_critical_file():
    record = TestDataFactory.create_benchmark_record_latency_critical()
    content = json.dumps({"records": [record]}).encode()
    return ProviderSource(filename="test.json", content_type="application/json", content=content)


@given("a benchmark file representing a throughput-oriented workload", target_fixture="source")
def given_throughput_file():
    record = TestDataFactory.create_benchmark_record_throughput_optimized()
    content = json.dumps({"records": [record]}).encode()
    return ProviderSource(filename="test.json", content_type="application/json", content=content)


@given("a valid benchmark file under 10 MB", target_fixture="source")
def given_small_file():
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    assert len(content) < 10 * 1024 * 1024
    return ProviderSource(filename="test.json", content_type="application/json", content=content)


@when("the operator runs the full pipeline", target_fixture="pipeline_result")
def when_run_pipeline(source, provider_registry, signature_service, classifier, recommendation_engine):
    start = time.time()
    telemetry = provider_registry.get("json").ingest(source)
    signature = signature_service.process(telemetry)
    classification = classifier.process(signature)
    recommendation = recommendation_engine.process(classification, signature)
    elapsed = time.time() - start
    return {
        "telemetry": telemetry,
        "signature": signature,
        "classification": classification,
        "recommendation": recommendation,
        "elapsed": elapsed,
    }


@then("the system shall produce a BenchmarkTelemetry")
def then_has_telemetry(pipeline_result):
    assert isinstance(pipeline_result["telemetry"], BenchmarkTelemetry)


@then("the system shall derive a WorkloadSignature with all 8 dimensions")
def then_has_signature(pipeline_result):
    sig = pipeline_result["signature"]
    assert isinstance(sig, WorkloadSignature)
    dims = [
        "latency_sensitivity", "throughput_orientation", "memory_intensity",
        "burst_behaviour", "context_length_profile", "concurrency_profile",
        "hardware_affinity", "modality",
    ]
    for dim in dims:
        assert getattr(sig, dim) is not None


@then("the system shall produce a WorkloadClassification")
def then_has_classification(pipeline_result):
    assert isinstance(pipeline_result["classification"], WorkloadClassification)


@then("the system shall generate an InfrastructureRecommendation with all 5 dimensions")
def then_has_recommendation(pipeline_result):
    rec = pipeline_result["recommendation"]
    assert isinstance(rec, InfrastructureRecommendation)
    for dim in ["model_family", "runtime", "hardware_suitability", "deployment_topology", "scheduling_policy"]:
        assert getattr(rec, dim) is not None


@then("the signature shall reference the telemetry_id")
def then_sig_refs_telemetry(pipeline_result):
    assert pipeline_result["signature"].telemetry_id == pipeline_result["telemetry"].id


@then("the classification shall reference the signature_id")
def then_cls_refs_signature(pipeline_result):
    assert pipeline_result["classification"].signature_id == pipeline_result["signature"].id


@then("the recommendation shall reference both classification_id and signature_id")
def then_rec_refs_both(pipeline_result):
    rec = pipeline_result["recommendation"]
    assert rec.classification_id == pipeline_result["classification"].id
    assert rec.signature_id == pipeline_result["signature"].id


@then(parsers.parse('the classification shall be "{category}"'))
def then_classification_is(pipeline_result, category):
    assert pipeline_result["classification"].primary_category.value == category


@then("the recommendations shall include latency-optimized configuration")
def then_latency_optimized(pipeline_result):
    rec = pipeline_result["recommendation"]
    assert "latency" in rec.runtime.recommendation.lower() or "latency" in rec.runtime.reasoning.lower()


@then("the recommendations shall include batched processing configuration")
def then_batched(pipeline_result):
    rec = pipeline_result["recommendation"]
    assert "batch" in rec.runtime.recommendation.lower() or "batch" in rec.scheduling_policy.recommendation.lower()


@then("the pipeline shall complete within 30 seconds")
def then_within_30s(pipeline_result):
    assert pipeline_result["elapsed"] < 30.0
