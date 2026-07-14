"""Tier 3 Integration: Full pipeline through REST API."""

from __future__ import annotations

import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


class TestFullPipelineViaAPI:
    async def test_end_to_end_pipeline(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()

        ingest_resp = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        assert ingest_resp.status_code == 200
        telemetry_id = ingest_resp.json()["id"]

        derive_resp = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": telemetry_id},
        )
        assert derive_resp.status_code == 200
        signature_id = derive_resp.json()["id"]

        classify_resp = await client.post(
            "/api/v1/classifications/classify",
            json={"signature_id": signature_id},
        )
        assert classify_resp.status_code == 200
        classification_id = classify_resp.json()["id"]

        rec_resp = await client.post(
            "/api/v1/recommendations/generate",
            json={
                "classification_id": classification_id,
                "signature_id": signature_id,
            },
        )
        assert rec_resp.status_code == 200
        rec_data = rec_resp.json()
        assert rec_data["classification_id"] == classification_id
        assert rec_data["signature_id"] == signature_id
        assert rec_data["model_family"]["recommendation"]
        assert rec_data["runtime"]["recommendation"]

    async def test_traceability_across_pipeline(self, client):
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
        sig_data = derive_resp.json()
        assert sig_data["telemetry_id"] == telemetry_id

        classify_resp = await client.post(
            "/api/v1/classifications/classify",
            json={"signature_id": sig_data["id"]},
        )
        cls_data = classify_resp.json()
        assert cls_data["signature_id"] == sig_data["id"]

        rec_resp = await client.post(
            "/api/v1/recommendations/generate",
            json={
                "classification_id": cls_data["id"],
                "signature_id": sig_data["id"],
            },
        )
        rec_data = rec_resp.json()
        assert rec_data["classification_id"] == cls_data["id"]
        assert rec_data["signature_id"] == sig_data["id"]

    async def test_health_endpoint(self, client):
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
