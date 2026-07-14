"""Tier 3 Integration: Classifications API endpoint tests."""

from __future__ import annotations

import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

VALID_CATEGORIES = {
    "latency_critical", "throughput_optimized", "memory_intensive",
    "burst_tolerant", "hardware_specialized", "general_purpose",
}


class TestClassifyEndpoint:
    async def _ingest_and_derive(self, client) -> str:
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        ingest_resp = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        derive_resp = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": ingest_resp.json()["id"]},
        )
        return derive_resp.json()["id"]

    async def test_classify_signature(self, client):
        signature_id = await self._ingest_and_derive(client)
        response = await client.post(
            "/api/v1/classifications/classify",
            json={"signature_id": signature_id},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["signature_id"] == signature_id
        assert data["primary_category"] in VALID_CATEGORIES
        assert 0 <= data["confidence"] <= 1
        assert data["rationale"]

    async def test_classify_nonexistent_signature_returns_404(self, client):
        response = await client.post(
            "/api/v1/classifications/classify",
            json={"signature_id": "nonexistent"},
        )
        assert response.status_code == 404


class TestGetClassificationEndpoint:
    async def test_get_classification(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        ingest_resp = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        derive_resp = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": ingest_resp.json()["id"]},
        )
        classify_resp = await client.post(
            "/api/v1/classifications/classify",
            json={"signature_id": derive_resp.json()["id"]},
        )
        classification_id = classify_resp.json()["id"]

        response = await client.get(
            f"/api/v1/classifications/{classification_id}"
        )
        assert response.status_code == 200
        assert response.json()["id"] == classification_id

    async def test_get_nonexistent_classification_returns_404(self, client):
        response = await client.get("/api/v1/classifications/nonexistent")
        assert response.status_code == 404
