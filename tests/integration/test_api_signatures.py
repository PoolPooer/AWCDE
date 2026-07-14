"""Tier 3 Integration: Signatures API endpoint tests."""

from __future__ import annotations

import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


class TestDeriveSignatureEndpoint:
    async def _ingest(self, client) -> str:
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        response = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        return response.json()["id"]

    async def test_derive_signature(self, client):
        telemetry_id = await self._ingest(client)
        response = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": telemetry_id},
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["telemetry_id"] == telemetry_id
        assert data["schema_version"] == "1.0.0"

    async def test_derive_has_all_8_dimensions(self, client):
        telemetry_id = await self._ingest(client)
        response = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": telemetry_id},
        )
        data = response.json()
        dimensions = [
            "latency_sensitivity", "throughput_orientation", "memory_intensity",
            "burst_behaviour", "context_length_profile", "concurrency_profile",
            "hardware_affinity", "modality",
        ]
        for dim in dimensions:
            assert dim in data
            assert "level" in data[dim]
            assert "score" in data[dim]

    async def test_derive_nonexistent_telemetry_returns_404(self, client):
        response = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": "nonexistent-id"},
        )
        assert response.status_code == 404


class TestGetSignatureEndpoint:
    async def test_get_signature(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        ingest_resp = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        telemetry_id = ingest_resp.json()["id"]
        derive_resp = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": telemetry_id},
        )
        signature_id = derive_resp.json()["id"]

        response = await client.get(f"/api/v1/signatures/{signature_id}")
        assert response.status_code == 200
        assert response.json()["id"] == signature_id

    async def test_get_nonexistent_signature_returns_404(self, client):
        response = await client.get("/api/v1/signatures/nonexistent")
        assert response.status_code == 404
