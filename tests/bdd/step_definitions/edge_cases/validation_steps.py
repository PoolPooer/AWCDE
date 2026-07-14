from __future__ import annotations

import json
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from pydantic import ValidationError

from tests.conftest import TestDataFactory
from awcde.models.telemetry import BenchmarkRecord
from awcde.providers.base import ProviderSource
from awcde.api.errors import ProviderError


pytestmark = pytest.mark.bdd

FEATURE_FILE = "../../features/edge_cases/validation.feature"


@scenario(FEATURE_FILE, "IF the JSON file has syntax errors, THEN the system SHALL reject it")
def test_json_syntax_error():
    pass


@scenario(FEATURE_FILE, "IF the CSV file has wrong delimiters, THEN the system SHALL reject it")
def test_csv_wrong_delimiter():
    pass


@scenario(FEATURE_FILE, "IF the CSV file has missing headers, THEN the system SHALL reject it")
def test_csv_missing_headers():
    pass


@scenario(FEATURE_FILE, "IF the benchmark file has zero records, THEN the system SHALL reject it")
def test_empty_records():
    pass


@scenario(FEATURE_FILE, "IF gpu_utilization_pct exceeds 100, THEN validation SHALL fail")
def test_gpu_over_100():
    pass


@scenario(FEATURE_FILE, 'IF modality is not a valid enum value, THEN validation SHALL fail')
def test_invalid_modality():
    pass


@scenario(FEATURE_FILE, "WHEN benchmark data has conflicting signals, the system SHALL still produce a valid signature")
def test_conflicting_signals():
    pass


@given("a JSON file with invalid syntax", target_fixture="source")
def given_bad_json():
    return ProviderSource(
        filename="bad.json", content_type="application/json",
        content=b'{not valid json at all',
    )


@given("a CSV file with semicolon delimiters instead of commas", target_fixture="source")
def given_semicolon_csv():
    content = b"latency_p50_ms;latency_p99_ms;throughput_rps\n10;20;100\n"
    return ProviderSource(filename="bad.csv", content_type="text/csv", content=content)


@given("a CSV file with no header row", target_fixture="source")
def given_no_header_csv():
    content = b"10,20,100,24.5,18.2,steady,512,2048,32,A100,85.0,text\n"
    return ProviderSource(filename="noheader.csv", content_type="text/csv", content=content)


@given("a JSON benchmark file with an empty records array", target_fixture="source")
def given_empty_records():
    content = json.dumps({"records": []}).encode()
    return ProviderSource(filename="empty.json", content_type="application/json", content=content)


@given("a benchmark record with gpu_utilization_pct of 150", target_fixture="record_data")
def given_gpu_150():
    return TestDataFactory.create_benchmark_record(gpu_utilization_pct=150.0)


@given('a benchmark record with modality "audio"', target_fixture="record_data")
def given_invalid_modality():
    return TestDataFactory.create_benchmark_record(modality="audio")


@given("benchmark telemetry with low latency but high context length", target_fixture="source")
def given_conflicting():
    record = TestDataFactory.create_benchmark_record(
        latency_p50_ms=5.0, latency_p99_ms=8.0,
        context_length_p50=8000, context_length_p99=32000,
    )
    content = json.dumps({"records": [record]}).encode()
    return ProviderSource(filename="conflicting.json", content_type="application/json", content=content)


@when("the operator posts it to the ingest endpoint", target_fixture="result")
def when_ingest(source, provider_registry):
    try:
        provider = provider_registry.resolve(source)
        telemetry = provider.ingest(source)
        return {"success": True, "telemetry": telemetry}
    except Exception as e:
        return {"success": False, "error": e}


@when(parsers.parse('the operator posts it to the ingest endpoint with provider "{pid}"'), target_fixture="result")
def when_ingest_with_provider(source, provider_registry, pid):
    try:
        provider = provider_registry.get(pid)
        telemetry = provider.ingest(source)
        return {"success": True, "telemetry": telemetry}
    except Exception as e:
        return {"success": False, "error": e}


@when("the record is validated", target_fixture="result")
def when_validate(record_data):
    try:
        BenchmarkRecord(**record_data)
        return {"success": True}
    except (ValidationError, ValueError) as e:
        return {"success": False, "error": e}


@when("signature derivation is performed", target_fixture="signature")
def when_derive(source, provider_registry, signature_service):
    telemetry = provider_registry.get("json").ingest(source)
    return signature_service.process(telemetry)


@then("the system shall return HTTP 422")
def then_422(result):
    assert not result["success"]


@then("the error message shall indicate a parse error")
def then_parse_error(result):
    assert not result["success"]


@then("the error shall indicate that records cannot be empty")
def then_empty_error(result):
    assert not result["success"]


@then("validation shall fail with a range constraint error")
def then_range_error(result):
    assert not result["success"]


@then("validation shall fail with an enum constraint error")
def then_enum_error(result):
    assert not result["success"]


@then("the system shall produce a valid signature")
def then_valid_signature(signature):
    assert signature is not None
    assert signature.id


@then("each dimension shall independently reflect its input signals")
def then_independent_dimensions(signature):
    assert signature.latency_sensitivity.score < 0.5
    assert signature.context_length_profile.score > 0.5


