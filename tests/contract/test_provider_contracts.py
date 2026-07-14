"""Tier 4 Contract: Provider protocol compliance tests."""

from __future__ import annotations

import pytest

from awcde.providers.json_provider import JSONProvider
from awcde.providers.csv_provider import CSVProvider
from awcde.providers.base import ProviderSource
from awcde.models.telemetry import BenchmarkTelemetry
from tests.conftest import FIXTURES_DIR


pytestmark = pytest.mark.contract


class TestProviderProtocolCompliance:
    """Verify that all providers implement the Provider protocol correctly."""

    @pytest.fixture(params=["json", "csv"])
    def provider(self, request):
        if request.param == "json":
            return JSONProvider()
        return CSVProvider()

    def test_has_provider_id(self, provider):
        assert hasattr(provider, "provider_id")
        assert isinstance(provider.provider_id, str)
        assert len(provider.provider_id) > 0

    def test_has_supports_method(self, provider):
        assert hasattr(provider, "supports")
        assert callable(provider.supports)

    def test_has_ingest_method(self, provider):
        assert hasattr(provider, "ingest")
        assert callable(provider.ingest)

    def test_supports_returns_bool(self, provider):
        source = ProviderSource(filename="test.unknown", content=b"")
        result = provider.supports(source)
        assert isinstance(result, bool)

    def test_ingest_returns_benchmark_telemetry(self, provider):
        if provider.provider_id == "json":
            content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
            source = ProviderSource(filename="test.json", content=content)
        else:
            content = (FIXTURES_DIR / "benchmark_valid.csv").read_bytes()
            source = ProviderSource(filename="test.csv", content=content)

        result = provider.ingest(source)
        assert isinstance(result, BenchmarkTelemetry)
        assert result.provider_id == provider.provider_id
        assert len(result.records) > 0


class TestProviderEquivalence:
    """Verify JSON and CSV providers produce identical normalized output."""

    def test_same_data_same_records(self):
        json_content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        csv_content = (FIXTURES_DIR / "benchmark_valid.csv").read_bytes()

        json_tel = JSONProvider().ingest(
            ProviderSource(filename="test.json", content=json_content)
        )
        csv_tel = CSVProvider().ingest(
            ProviderSource(filename="test.csv", content=csv_content)
        )

        assert len(json_tel.records) == len(csv_tel.records)
        for jr, cr in zip(json_tel.records, csv_tel.records):
            assert jr.model_dump() == cr.model_dump()
