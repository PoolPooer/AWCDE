"""Tier 3 Integration: Ingest API endpoint tests."""

from __future__ import annotations

import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


class TestIngestEndpoint:
    async def test_ingest_valid_json(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        response = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["provider_id"] == "json"
        assert len(data["records"]) == 2

    async def test_ingest_valid_csv(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.csv").read_bytes()
        response = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.csv", content, "text/csv")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["provider_id"] == "csv"
        assert len(data["records"]) == 2

    async def test_ingest_with_explicit_provider(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        response = await client.post(
            "/api/v1/ingest",
            params={"provider_id": "json"},
            files={"file": ("data.bin", content, "application/octet-stream")},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["provider_id"] == "json"

    async def test_ingest_invalid_provider_returns_422(self, client):
        response = await client.post(
            "/api/v1/ingest",
            params={"provider_id": "nonexistent"},
            files={"file": ("data.json", b"{}", "application/json")},
        )
        assert response.status_code == 422

    async def test_ingest_malformed_json_returns_error(self, client):
        response = await client.post(
            "/api/v1/ingest",
            files={"file": ("bad.json", b"not json at all", "application/json")},
        )
        assert response.status_code in (422, 500)

    async def test_ingest_persists_telemetry(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        response = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        telemetry_id = response.json()["id"]
        # Verify we can derive a signature from it (proves it was persisted)
        sig_response = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": telemetry_id},
        )
        assert sig_response.status_code == 200


class TestProvidersEndpoint:
    async def test_list_providers(self, client):
        response = await client.get("/api/v1/providers")
        assert response.status_code == 200
        providers = response.json()
        assert len(providers) >= 2
        ids = {p["provider_id"] for p in providers}
        assert "json" in ids
        assert "csv" in ids

    async def test_provider_has_metadata(self, client):
        response = await client.get("/api/v1/providers")
        for provider in response.json():
            assert "provider_id" in provider
            assert "description" in provider
