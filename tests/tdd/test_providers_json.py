"""Tier 1 TDD: JSONProvider tests."""

from __future__ import annotations

import json
import pytest

from awcde.providers.json_provider import JSONProvider
from awcde.providers.base import ProviderSource
from awcde.models.telemetry import BenchmarkTelemetry
from awcde.api.errors import ProviderError
from tests.conftest import TestDataFactory, FIXTURES_DIR


pytestmark = pytest.mark.unit


class TestJSONProvider:
    @pytest.fixture
    def provider(self):
        return JSONProvider()

    def test_provider_id(self, provider):
        assert provider.provider_id == "json"

    def test_supports_json_file(self, provider):
        source = ProviderSource(filename="test.json", content=b"{}")
        assert provider.supports(source)

    def test_supports_json_content_type(self, provider):
        source = ProviderSource(filename="test", content_type="application/json", content=b"{}")
        assert provider.supports(source)

    def test_does_not_support_csv(self, provider):
        source = ProviderSource(filename="test.csv", content=b"")
        assert not provider.supports(source)

    def test_ingest_valid_json(self, provider):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        source = ProviderSource(filename="test.json", content=content)
        telemetry = provider.ingest(source)
        assert isinstance(telemetry, BenchmarkTelemetry)
        assert len(telemetry.records) == 2
        assert telemetry.provider_id == "json"

    def test_ingest_invalid_json_syntax(self, provider):
        source = ProviderSource(filename="bad.json", content=b"{not valid}")
        with pytest.raises(ProviderError):
            provider.ingest(source)

    def test_ingest_missing_fields(self, provider):
        content = (FIXTURES_DIR / "benchmark_missing_fields.json").read_bytes()
        source = ProviderSource(filename="missing.json", content=content)
        with pytest.raises(ProviderError):
            provider.ingest(source)

    def test_ingest_invalid_types(self, provider):
        content = (FIXTURES_DIR / "benchmark_invalid_types.json").read_bytes()
        source = ProviderSource(filename="types.json", content=content)
        with pytest.raises(ProviderError):
            provider.ingest(source)

    def test_ingest_empty_records(self, provider):
        content = json.dumps({"records": []}).encode()
        source = ProviderSource(filename="empty.json", content=content)
        with pytest.raises(ProviderError):
            provider.ingest(source)
