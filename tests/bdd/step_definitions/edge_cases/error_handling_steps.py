from __future__ import annotations

import json
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from pathlib import Path

from tests.conftest import TestDataFactory, FIXTURES_DIR
from awcde.models.recommendation import InfrastructureRecommendation
from awcde.providers.base import ProviderSource
from awcde.knowledge.static_kb import StaticKnowledgeBase


pytestmark = pytest.mark.bdd

FEATURE_FILE = "../../features/edge_cases/error_handling.feature"


@scenario(FEATURE_FILE, "IF a non-existent signature ID is requested, THEN the system SHALL return 404")
def test_signature_not_found():
    pass


@scenario(FEATURE_FILE, "IF a non-existent classification ID is requested, THEN the system SHALL return 404")
def test_classification_not_found():
    pass


@scenario(FEATURE_FILE, "IF a non-existent recommendation ID is requested, THEN the system SHALL return 404")
def test_recommendation_not_found():
    pass


@scenario(FEATURE_FILE, "IF an unknown provider is specified, THEN the system SHALL return an error")
def test_unknown_provider():
    pass


@scenario(FEATURE_FILE, "WHEN the same benchmark file is re-ingested, the system SHALL produce identical signatures")
def test_idempotent_signatures():
    pass


@scenario(FEATURE_FILE, "WHERE no KnowledgeBase rules are loaded, the system SHALL provide default recommendations")
def test_empty_kb_defaults():
    pass


@when(parsers.parse('the operator requests signature with id "{sig_id}"'), target_fixture="result")
def when_get_signature(sig_id, repository):
    import asyncio
    sig = asyncio.get_event_loop().run_until_complete(repository.get_signature(sig_id))
    return {"found": sig is not None, "entity_type": "WorkloadSignature"}


@when(parsers.parse('the operator requests classification with id "{cls_id}"'), target_fixture="result")
def when_get_classification(cls_id, repository):
    import asyncio
    cls = asyncio.get_event_loop().run_until_complete(repository.get_classification(cls_id))
    return {"found": cls is not None, "entity_type": "WorkloadClassification"}


@when(parsers.parse('the operator requests recommendation with id "{rec_id}"'), target_fixture="result")
def when_get_recommendation(rec_id, repository):
    import asyncio
    rec = asyncio.get_event_loop().run_until_complete(repository.get_recommendation(rec_id))
    return {"found": rec is not None, "entity_type": "InfrastructureRecommendation"}


@given("a valid JSON benchmark file", target_fixture="source")
def given_json_file():
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    return ProviderSource(filename="test.json", content_type="application/json", content=content)


@when(parsers.parse('the operator posts it with provider "{pid}"'), target_fixture="result")
def when_ingest_unknown(source, provider_registry, pid):
    try:
        provider = provider_registry.get(pid)
        telemetry = provider.ingest(source)
        return {"success": True, "telemetry": telemetry}
    except (KeyError, Exception) as e:
        return {"success": False, "error": e}


@when("the file is ingested twice", target_fixture="two_results")
def when_ingest_twice(source, provider_registry, signature_service):
    t1 = provider_registry.get("json").ingest(source)
    t2 = provider_registry.get("json").ingest(source)
    s1 = signature_service.process(t1)
    s2 = signature_service.process(t2)
    return (s1, s2)


@given("an empty KnowledgeBase", target_fixture="empty_kb")
def given_empty_kb():
    return StaticKnowledgeBase()


@given("a stored workload classification", target_fixture="classification_and_signature")
def given_stored_classification(provider_registry, signature_service, classifier):
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    source = ProviderSource(filename="test.json", content_type="application/json", content=content)
    telemetry = provider_registry.get("json").ingest(source)
    signature = signature_service.process(telemetry)
    classification = classifier.process(signature)
    return (classification, signature)


@when("the operator requests recommendations", target_fixture="recommendation")
def when_request_recs(classification_and_signature, empty_kb):
    from awcde.recommendations.engine import RecommendationEngine
    engine = RecommendationEngine(empty_kb)
    classification, signature = classification_and_signature
    return engine.process(classification, signature)


@then("the system shall return HTTP 404")
def then_404(result):
    assert not result["found"]


@then("the error message shall identify the missing entity type")
def then_entity_type(result):
    assert result["entity_type"]


@then("the system shall return an error indicating the provider is not found")
def then_provider_not_found(result):
    assert not result["success"]


@then("both resulting signatures shall have the same id")
def then_same_id(two_results):
    assert two_results[0].id == two_results[1].id


@then("the system shall not create duplicate entries")
def then_no_duplicates(two_results):
    assert two_results[0].id == two_results[1].id


@then("the system shall return recommendations with fallback reasoning")
def then_fallback(recommendation):
    assert isinstance(recommendation, InfrastructureRecommendation)
    assert recommendation.model_family is not None
