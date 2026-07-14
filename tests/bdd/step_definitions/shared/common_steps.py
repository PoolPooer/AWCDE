from __future__ import annotations

from pytest_bdd import given, when, then, parsers
from pathlib import Path

from tests.conftest import TestDataFactory, FIXTURES_DIR

from awcde.models.telemetry import BenchmarkRecord, BenchmarkTelemetry
from awcde.providers.base import ProviderSource


@given("a valid JSON benchmark file")
def valid_json_file():
    content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
    return ProviderSource(filename="benchmark_valid.json", content_type="application/json", content=content)


@given("a valid CSV benchmark file")
def valid_csv_file():
    content = (FIXTURES_DIR / "benchmark_valid.csv").read_bytes()
    return ProviderSource(filename="benchmark_valid.csv", content_type="text/csv", content=content)


@given("a valid CSV benchmark file with equivalent data")
def valid_csv_equivalent():
    content = (FIXTURES_DIR / "benchmark_valid.csv").read_bytes()
    return ProviderSource(filename="benchmark_valid.csv", content_type="text/csv", content=content)


@given("a malformed JSON benchmark file")
def malformed_json_file():
    return ProviderSource(
        filename="malformed.json",
        content_type="application/json",
        content=b'{"records": [{"invalid json',
    )


@given("a JSON file missing required benchmark fields")
def missing_fields_json():
    content = (FIXTURES_DIR / "benchmark_missing_fields.json").read_bytes()
    return ProviderSource(filename="benchmark_missing_fields.json", content_type="application/json", content=content)


@given("ingested benchmark telemetry")
def ingested_telemetry(provider_registry, valid_json_file):
    return provider_registry.get("json").ingest(valid_json_file)
