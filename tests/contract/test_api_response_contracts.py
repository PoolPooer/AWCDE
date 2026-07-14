"""Tier 4 Contract: API response schema compliance tests."""

from __future__ import annotations

import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"

pytestmark = [pytest.mark.contract, pytest.mark.asyncio]


TELEMETRY_REQUIRED_FIELDS = {"id", "provider_id", "source_ref", "ingested_at", "records"}
RECORD_REQUIRED_FIELDS = {
    "latency_p50_ms", "latency_p99_ms", "throughput_rps",
    "peak_memory_gb", "avg_memory_gb", "request_arrival_pattern",
    "context_length_p50", "context_length_p99", "concurrency_level",
    "accelerator_type", "gpu_utilization_pct", "modality",
}
SIGNATURE_REQUIRED_FIELDS = {
    "id", "schema_version", "telemetry_id", "derived_at",
    "latency_sensitivity", "throughput_orientation", "memory_intensity",
    "burst_behaviour", "context_length_profile", "concurrency_profile",
    "hardware_affinity", "modality",
}
CLASSIFICATION_REQUIRED_FIELDS = {
    "id", "signature_id", "classified_at", "primary_category",
    "confidence", "rationale", "dimension_summary",
}
RECOMMENDATION_REQUIRED_FIELDS = {
    "id", "classification_id", "signature_id", "generated_at",
    "model_family", "runtime", "hardware_suitability",
    "deployment_topology", "scheduling_policy",
}
BLOCK_REQUIRED_FIELDS = {"recommendation", "reasoning", "evidence"}


class TestIngestResponseContract:
    async def test_ingest_response_has_required_fields(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        response = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        data = response.json()
        assert TELEMETRY_REQUIRED_FIELDS.issubset(set(data.keys()))

    async def test_ingest_records_have_required_fields(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        response = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        for record in response.json()["records"]:
            assert RECORD_REQUIRED_FIELDS.issubset(set(record.keys()))


class TestSignatureResponseContract:
    async def test_derive_response_has_required_fields(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        ingest_resp = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        response = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": ingest_resp.json()["id"]},
        )
        data = response.json()
        assert SIGNATURE_REQUIRED_FIELDS.issubset(set(data.keys()))

    async def test_dimension_score_shape(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        ingest_resp = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        response = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": ingest_resp.json()["id"]},
        )
        data = response.json()
        for dim_name in [
            "latency_sensitivity", "throughput_orientation", "memory_intensity",
            "burst_behaviour", "context_length_profile", "concurrency_profile",
            "hardware_affinity",
        ]:
            dim = data[dim_name]
            assert "level" in dim
            assert "score" in dim
            assert "raw_inputs" in dim
            assert dim["level"] in ("low", "medium", "high")
            assert 0 <= dim["score"] <= 1


class TestClassificationResponseContract:
    async def test_classify_response_has_required_fields(self, client):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        ingest_resp = await client.post(
            "/api/v1/ingest",
            files={"file": ("benchmark.json", content, "application/json")},
        )
        derive_resp = await client.post(
            "/api/v1/signatures/derive",
            json={"telemetry_id": ingest_resp.json()["id"]},
        )
        response = await client.post(
            "/api/v1/classifications/classify",
            json={"signature_id": derive_resp.json()["id"]},
        )
        data = response.json()
        assert CLASSIFICATION_REQUIRED_FIELDS.issubset(set(data.keys()))
        assert data["primary_category"] in {
            "latency_critical", "throughput_optimized", "memory_intensive",
            "burst_tolerant", "hardware_specialized", "general_purpose",
        }
        assert 0 <= data["confidence"] <= 1


class TestRecommendationResponseContract:
    async def test_recommendation_response_has_required_fields(self, client):
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
        response = await client.post(
            "/api/v1/recommendations/generate",
            json={
                "classification_id": classify_resp.json()["id"],
                "signature_id": sig_id,
            },
        )
        data = response.json()
        assert RECOMMENDATION_REQUIRED_FIELDS.issubset(set(data.keys()))

    async def test_recommendation_blocks_shape(self, client):
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
        response = await client.post(
            "/api/v1/recommendations/generate",
            json={
                "classification_id": classify_resp.json()["id"],
                "signature_id": sig_id,
            },
        )
        data = response.json()
        for dim in ["model_family", "runtime", "hardware_suitability",
                     "deployment_topology", "scheduling_policy"]:
            block = data[dim]
            assert BLOCK_REQUIRED_FIELDS.issubset(set(block.keys()))
            assert isinstance(block["evidence"], list)


class TestErrorResponseContract:
    async def test_404_response_has_detail(self, client):
        response = await client.get("/api/v1/signatures/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    async def test_422_response_has_detail(self, client):
        response = await client.post(
            "/api/v1/ingest",
            params={"provider_id": "nonexistent"},
            files={"file": ("data.json", b"{}", "application/json")},
        )
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
