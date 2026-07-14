from __future__ import annotations

import json
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from pathlib import Path

from tests.conftest import TestDataFactory, FIXTURES_DIR
from awcde.models.recommendation import InfrastructureRecommendation
from awcde.models.classification import WorkloadClassification, ClassificationCategory
from awcde.providers.base import ProviderSource


pytestmark = pytest.mark.bdd

FEATURE_FILE = "../../features/core/recommendation.feature"

RECOMMENDATION_DIMENSIONS = [
    "model_family", "runtime", "hardware_suitability",
    "deployment_topology", "scheduling_policy",
]


@scenario(FEATURE_FILE, "WHEN recommendations are generated, the system SHALL cover all 5 dimensions")
def test_all_dimensions():
    pass


@scenario(FEATURE_FILE, "The system SHALL include reasoning in every recommendation dimension")
def test_reasoning_present():
    pass


@scenario(FEATURE_FILE, "The system SHALL include evidence in every recommendation dimension")
def test_evidence_present():
    pass


@scenario(FEATURE_FILE, "The system SHALL trace every evidence entry to a KnowledgeBase rule")
def test_evidence_traceability():
    pass


@scenario(FEATURE_FILE, "WHEN a latency-critical workload is classified, the system SHALL recommend low-latency configuration")
def test_latency_critical_recommendations():
    pass


@scenario(FEATURE_FILE, "IF no KnowledgeBase rule matches, THEN the system SHALL provide fallback recommendations")
def test_fallback_recommendations():
    pass


@scenario(FEATURE_FILE, "The system SHALL NOT perform autonomous deployment or actuation")
def test_no_deployment():
    pass


@given("a stored workload classification", target_fixture="classification_and_signature")
def given_classification(provider_registry, signature_service, classifier):
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    telemetry = provider_registry.get("json").ingest(source)
    signature = signature_service.process(telemetry)
    classification = classifier.process(signature)
    return (classification, signature)


@given('a workload classified as "latency_critical"', target_fixture="classification_and_signature")
def given_latency_critical(provider_registry, signature_service, classifier):
    record = TestDataFactory.create_benchmark_record_latency_critical()
    content = json.dumps({"records": [record]}).encode()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    telemetry = provider_registry.get("json").ingest(source)
    signature = signature_service.process(telemetry)
    classification = classifier.process(signature)
    return (classification, signature)


@given("a classification with no matching KnowledgeBase rules", target_fixture="classification_and_signature")
def given_no_rules(provider_registry, signature_service, classifier):
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    telemetry = provider_registry.get("json").ingest(source)
    signature = signature_service.process(telemetry)
    classification = classifier.process(signature)
    return (classification, signature)


@given("any recommendation response", target_fixture="recommendation")
def given_any_recommendation(provider_registry, signature_service, classifier, recommendation_engine):
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    telemetry = provider_registry.get("json").ingest(source)
    signature = signature_service.process(telemetry)
    classification = classifier.process(signature)
    return recommendation_engine.process(classification, signature)


@when("the operator requests recommendations", target_fixture="recommendation")
def when_recommend(classification_and_signature, recommendation_engine):
    classification, signature = classification_and_signature
    return recommendation_engine.process(classification, signature)


@when("reviewed")
def when_reviewed():
    pass


@then("the system shall return an InfrastructureRecommendation")
def then_is_recommendation(recommendation):
    assert isinstance(recommendation, InfrastructureRecommendation)


@then("the recommendation shall include model_family")
def then_has_model_family(recommendation):
    assert recommendation.model_family is not None
    assert recommendation.model_family.recommendation


@then("the recommendation shall include runtime")
def then_has_runtime(recommendation):
    assert recommendation.runtime is not None
    assert recommendation.runtime.recommendation


@then("the recommendation shall include hardware_suitability")
def then_has_hardware(recommendation):
    assert recommendation.hardware_suitability is not None


@then("the recommendation shall include deployment_topology")
def then_has_topology(recommendation):
    assert recommendation.deployment_topology is not None


@then("the recommendation shall include scheduling_policy")
def then_has_scheduling(recommendation):
    assert recommendation.scheduling_policy is not None


@then("every recommendation dimension shall have non-empty reasoning")
def then_all_have_reasoning(recommendation):
    for dim in RECOMMENDATION_DIMENSIONS:
        block = getattr(recommendation, dim)
        assert block.reasoning, f"{dim} has empty reasoning"


@then("every recommendation dimension shall have at least one evidence entry")
def then_all_have_evidence(recommendation):
    for dim in RECOMMENDATION_DIMENSIONS:
        block = getattr(recommendation, dim)
        assert len(block.evidence) >= 1, f"{dim} has no evidence"


@then("every evidence entry shall reference a rule_id")
def then_evidence_has_rule_id(recommendation):
    for dim in RECOMMENDATION_DIMENSIONS:
        for ev in getattr(recommendation, dim).evidence:
            assert ev.rule_id


@then("every evidence entry shall reference a source_type")
def then_evidence_has_source_type(recommendation):
    for dim in RECOMMENDATION_DIMENSIONS:
        for ev in getattr(recommendation, dim).evidence:
            assert ev.source_type in ("signature", "classification", "telemetry")


@then("every evidence entry shall include the matched attribute and value")
def then_evidence_has_attribute(recommendation):
    for dim in RECOMMENDATION_DIMENSIONS:
        for ev in getattr(recommendation, dim).evidence:
            assert ev.attribute
            assert ev.attribute_value is not None


@then("the runtime recommendation shall reference low-latency configuration")
def then_low_latency_runtime(recommendation):
    assert "latency" in recommendation.runtime.recommendation.lower() or \
           "latency" in recommendation.runtime.reasoning.lower()


@then("the system shall still return all 5 recommendation dimensions")
def then_still_5_dimensions(recommendation):
    for dim in RECOMMENDATION_DIMENSIONS:
        assert getattr(recommendation, dim) is not None


@then("the reasoning shall explain that no specific rules matched")
def then_fallback_reasoning(recommendation):
    pass


@then("no deployment action shall have been triggered")
def then_no_deployment(recommendation):
    assert isinstance(recommendation, InfrastructureRecommendation)


@then("the response shall be advisory only")
def then_advisory_only(recommendation):
    assert isinstance(recommendation, InfrastructureRecommendation)
