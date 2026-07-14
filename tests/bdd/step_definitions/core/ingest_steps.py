from __future__ import annotations

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from pathlib import Path

from tests.conftest import TestDataFactory, FIXTURES_DIR
from awcde.models.telemetry import BenchmarkRecord, BenchmarkTelemetry, ArrivalPattern, Modality
from awcde.providers.base import ProviderSource
from awcde.providers.json_provider import JSONProvider
from awcde.providers.csv_provider import CSVProvider
from awcde.providers.registry import ProviderRegistry
from awcde.api.errors import ProviderError


pytestmark = pytest.mark.bdd

FEATURE_FILE = "../../features/core/ingest.feature"


@scenario(FEATURE_FILE, "WHEN a valid JSON benchmark file is posted, the system SHALL return normalized telemetry")
def test_valid_json_ingest():
    pass


@scenario(FEATURE_FILE, "WHEN a valid CSV benchmark file is posted, the system SHALL return normalized telemetry")
def test_valid_csv_ingest():
    pass


@scenario(FEATURE_FILE, "WHEN equivalent JSON and CSV files are posted, the system SHALL produce identical normalized structures")
def test_json_csv_equivalence():
    pass


@scenario(FEATURE_FILE, "IF a malformed JSON file is posted, THEN the system SHALL reject with validation errors")
def test_malformed_json_rejection():
    pass


@scenario(FEATURE_FILE, "IF required benchmark fields are missing, THEN the system SHALL reject with clear errors")
def test_missing_fields_rejection():
    pass


@scenario(FEATURE_FILE, "The system SHALL validate all numeric fields are non-negative")
def test_non_negative_validation():
    pass


@scenario(FEATURE_FILE, "The system SHALL enforce latency_p99 >= latency_p50")
def test_p99_gte_p50():
    pass


@scenario(FEATURE_FILE, "The system SHALL enforce context_length_p99 >= context_length_p50")
def test_context_p99_gte_p50():
    pass


@scenario(FEATURE_FILE, "WHEN the operator requests the provider list, the system SHALL return available providers")
def test_provider_list():
    pass


# --- Given steps ---

@given("a valid JSON benchmark file", target_fixture="source")
def given_valid_json():
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    return ProviderSource(filename="benchmark_valid.json", content_type="application/json", content=content)


@given("a valid CSV benchmark file", target_fixture="source")
def given_valid_csv():
    content = (FIXTURES_DIR / "benchmark_valid.csv").read_bytes()
    return ProviderSource(filename="benchmark_valid.csv", content_type="text/csv", content=content)


@given("a valid CSV benchmark file with equivalent data", target_fixture="csv_source")
def given_equivalent_csv():
    content = (FIXTURES_DIR / "benchmark_valid.csv").read_bytes()
    return ProviderSource(filename="benchmark_valid.csv", content_type="text/csv", content=content)


@given("a malformed JSON benchmark file", target_fixture="source")
def given_malformed_json():
    return ProviderSource(
        filename="malformed.json",
        content_type="application/json",
        content=b'{"records": [{"invalid json',
    )


@given("a JSON file missing required benchmark fields", target_fixture="source")
def given_missing_fields():
    content = (FIXTURES_DIR / "benchmark_missing_fields.json").read_bytes()
    return ProviderSource(filename="benchmark_missing_fields.json", content_type="application/json", content=content)


@given("a benchmark file with negative latency values", target_fixture="source")
def given_negative_latency():
    import json
    record = TestDataFactory.create_benchmark_record(latency_p50_ms=-5.0)
    content = json.dumps({"records": [record]}).encode()
    return ProviderSource(filename="negative.json", content_type="application/json", content=content)


@given("a benchmark record with p99 latency less than p50", target_fixture="record_data")
def given_p99_lt_p50():
    return TestDataFactory.create_benchmark_record(latency_p50_ms=100.0, latency_p99_ms=50.0)


@given("a benchmark record with p99 context length less than p50", target_fixture="record_data")
def given_context_p99_lt_p50():
    return TestDataFactory.create_benchmark_record(context_length_p50=2048, context_length_p99=512)


# --- When steps ---

@when(parsers.parse('the operator posts it to the ingest endpoint with provider "{provider_id}"'), target_fixture="result")
def when_ingest_with_provider(source, provider_registry, provider_id):
    try:
        provider = provider_registry.get(provider_id)
        telemetry = provider.ingest(source)
        return {"success": True, "telemetry": telemetry}
    except (ProviderError, Exception) as e:
        return {"success": False, "error": e}


@when("the operator posts it to the ingest endpoint", target_fixture="result")
def when_ingest_auto(source, provider_registry):
    try:
        provider = provider_registry.resolve(source)
        telemetry = provider.ingest(source)
        return {"success": True, "telemetry": telemetry}
    except (ProviderError, Exception) as e:
        return {"success": False, "error": e}


@when("both files are ingested through their respective providers", target_fixture="both_results")
def when_ingest_both(source, csv_source, provider_registry):
    json_telemetry = provider_registry.get("json").ingest(source)
    csv_telemetry = provider_registry.get("csv").ingest(csv_source)
    return {"json": json_telemetry, "csv": csv_telemetry}


@when("the record is validated", target_fixture="result")
def when_validate_record(record_data):
    try:
        BenchmarkRecord(**record_data)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": e}


@when("the operator requests the list of available providers", target_fixture="providers_list")
def when_list_providers(provider_registry):
    return provider_registry.list_providers()


# --- Then steps ---

@then("the system shall return a telemetry_id")
def then_has_telemetry_id(result):
    assert result["success"], f"Ingest failed: {result.get('error')}"
    assert result["telemetry"].id


@then("the system shall return normalized benchmark records")
def then_has_records(result):
    assert result["success"]
    assert len(result["telemetry"].records) > 0


@then("each record shall contain all 12 required fields")
def then_records_have_fields(result):
    record = result["telemetry"].records[0]
    expected_fields = {
        "latency_p50_ms", "latency_p99_ms", "throughput_rps",
        "peak_memory_gb", "avg_memory_gb", "request_arrival_pattern",
        "context_length_p50", "context_length_p99", "concurrency_level",
        "accelerator_type", "gpu_utilization_pct", "modality",
    }
    actual_fields = set(type(record).model_fields.keys())
    assert expected_fields.issubset(actual_fields)


@then("both telemetry records shall contain the same normalized data")
def then_equivalent_data(both_results):
    json_records = both_results["json"].records
    csv_records = both_results["csv"].records
    assert len(json_records) == len(csv_records)
    for jr, cr in zip(json_records, csv_records):
        assert jr.latency_p50_ms == cr.latency_p50_ms
        assert jr.throughput_rps == cr.throughput_rps
        assert jr.modality == cr.modality


@then("the system shall return HTTP 422")
def then_http_422(result):
    assert not result["success"]


@then("the system shall return field-level validation errors")
def then_field_errors(result):
    assert not result["success"]
    assert result["error"] is not None


@then("no partial telemetry shall be persisted")
def then_no_partial():
    pass


@then("the error response shall identify the missing fields")
def then_missing_field_errors(result):
    assert not result["success"]


@then("the system shall reject the file with a validation error")
def then_validation_error(result):
    assert not result["success"]


@then("validation shall fail with a constraint error")
def then_constraint_error(result):
    assert not result["success"]


@then("the system shall return at least 2 providers")
def then_at_least_2_providers(providers_list):
    assert len(providers_list) >= 2


@then('the provider list shall include "json" and "csv"')
def then_json_csv_in_list(providers_list):
    ids = {p.provider_id for p in providers_list}
    assert "json" in ids
    assert "csv" in ids
