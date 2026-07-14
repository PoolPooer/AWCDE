"""Tier 3 Integration: Recommendations API endpoint tests."""

from __future__ import annotations

import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

RECOMMENDATION_DIMENSIONS = [
    "model_family", "runtime", "hardware_suitability",
    "deployment_topology", "scheduling_policy",
]


class TestGenerateRecommendationEndpoint:
    async def _full_pipeline(self, client) -> tuple[str, str]:
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        ingest_resp = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        derive_resp = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": ingest_resp.json()["id"]},
        )
        signature_id = derive_resp.json()["id"]
        classify_resp = await client.post(
            "/api/v1/classifications/classify",
            json={"signature_id": signature_id},
        )
        classification_id = classify_resp.json()["id"]
        return classification_id, signature_id

    async def test_generate_recommendation(self, client):
        classification_id, signature_id = await self._full_pipeline(client)
        response = await client.post(
            "/api/v1/recommendations/generate",
            json={
                "classification_id": classification_id,
                "signature_id": signature_id,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification_id"] == classification_id
        assert data["signature_id"] == signature_id

    async def test_all_5_dimensions_present(self, client):
        classification_id, signature_id = await self._full_pipeline(client)
        response = await client.post(
            "/api/v1/recommendations/generate",
            json={
                "classification_id": classification_id,
                "signature_id": signature_id,
            },
        )
        data = response.json()
        for dim in RECOMMENDATION_DIMENSIONS:
            assert dim in data
            assert "recommendation" in data[dim]
            assert "reasoning" in data[dim]
            assert "evidence" in data[dim]

    async def test_nonexistent_classification_returns_404(self, client):
        response = await client.post(
            "/api/v1/recommendations/generate",
            json={
                "classification_id": "nonexistent",
                "signature_id": "also-nonexistent",
            },
        )
        assert response.status_code == 404


class TestGetRecommendationEndpoint:
    async def test_get_recommendation(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        ingest_resp = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        derive_resp = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": ingest_resp.json()["id"]},
        )
        sig_id = derive_resp.json()["id"]
        classify_resp = await client.post(
            "/api/v1/classifications/classify",
            json={"signature_id": sig_id},
        )
        cls_id = classify_resp.json()["id"]
        rec_resp = await client.post(
            "/api/v1/recommendations/generate",
            json={"classification_id": cls_id, "signature_id": sig_id},
        )
        rec_id = rec_resp.json()["id"]

        response = await client.get(f"/api/v1/recommendations/{rec_id}")
        assert response.status_code == 200
        assert response.json()["id"] == rec_id

    async def test_get_nonexistent_recommendation_returns_404(self, client):
        response = await client.get("/api/v1/recommendations/nonexistent")
        assert response.status_code == 404
