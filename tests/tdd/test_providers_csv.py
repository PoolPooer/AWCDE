"""Tier 1 TDD: CSVProvider tests."""

from __future__ import annotations

import pytest

from awcde.providers.csv_provider import CSVProvider
from awcde.providers.base import ProviderSource
from awcde.models.telemetry import BenchmarkTelemetry
from awcde.api.errors import ProviderError
from tests.conftest import FIXTURES_DIR


pytestmark = pytest.mark.unit


class TestCSVProvider:
    @pytest.fixture
    def provider(self):
        return CSVProvider()

    def test_provider_id(self, provider):
        assert provider.provider_id == "csv"

    def test_supports_csv_file(self, provider):
        source = ProviderSource(filename="test.csv", content=b"")
        assert provider.supports(source)

    def test_supports_csv_content_type(self, provider):
        source = ProviderSource(filename="test", content_type="text/csv", content=b"")
        assert provider.supports(source)

    def test_does_not_support_json(self, provider):
        source = ProviderSource(filename="test.json", content=b"")
        assert not provider.supports(source)

    def test_ingest_valid_csv(self, provider):
        content = (FIXTURES_DIR / "benchmark_valid.csv").read_bytes()
        source = ProviderSource(filename="test.csv", content=content)
        telemetry = provider.ingest(source)
        assert isinstance(telemetry, BenchmarkTelemetry)
        assert len(telemetry.records) == 2
        assert telemetry.provider_id == "csv"

    def test_csv_json_equivalence(self):
        from awcde.providers.json_provider import JSONProvider

        json_content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        csv_content = (FIXTURES_DIR / "benchmark_valid.csv").read_bytes()

        json_source = ProviderSource(filename="test.json", content=json_content)
        csv_source = ProviderSource(filename="test.csv", content=csv_content)

        json_telemetry = JSONProvider().ingest(json_source)
        csv_telemetry = CSVProvider().ingest(csv_source)

        for jr, cr in zip(json_telemetry.records, csv_telemetry.records):
            assert jr.latency_p50_ms == cr.latency_p50_ms
            assert jr.throughput_rps == cr.throughput_rps
            assert jr.modality == cr.modality
            assert jr.concurrency_level == cr.concurrency_level

    def test_ingest_empty_csv(self, provider):
        source = ProviderSource(filename="empty.csv", content=b"")
        with pytest.raises(ProviderError):
            provider.ingest(source)
