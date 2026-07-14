"""Tier 1 TDD: Provider registry tests."""

from __future__ import annotations

import pytest

from awcde.providers.registry import ProviderRegistry
from awcde.providers.json_provider import JSONProvider
from awcde.providers.csv_provider import CSVProvider
from awcde.providers.base import ProviderSource


pytestmark = pytest.mark.unit


class TestProviderRegistry:
    @pytest.fixture
    def registry(self):
        reg = ProviderRegistry()
        reg.register(JSONProvider())
        reg.register(CSVProvider())
        return reg

    def test_get_json_provider(self, registry):
        provider = registry.get("json")
        assert provider.provider_id == "json"

    def test_get_csv_provider(self, registry):
        provider = registry.get("csv")
        assert provider.provider_id == "csv"

    def test_get_unknown_raises(self, registry):
        with pytest.raises(KeyError):
            registry.get("unknown")

    def test_list_providers(self, registry):
        providers = registry.list_providers()
        assert len(providers) >= 2
        ids = {p.provider_id for p in providers}
        assert "json" in ids
        assert "csv" in ids

    def test_resolve_json(self, registry):
        source = ProviderSource(filename="test.json", content=b"{}")
        provider = registry.resolve(source)
        assert provider.provider_id == "json"

    def test_resolve_csv(self, registry):
        source = ProviderSource(filename="test.csv", content=b"")
        provider = registry.resolve(source)
        assert provider.provider_id == "csv"

    def test_resolve_unknown_raises(self, registry):
        source = ProviderSource(filename="test.xml", content=b"")
        with pytest.raises(ValueError):
            registry.resolve(source)
