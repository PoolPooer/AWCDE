"""Tier 1 TDD: SQLite repository tests."""

from __future__ import annotations

import pytest

from awcde.storage.repository import Repository
from awcde.models.telemetry import BenchmarkTelemetry, BenchmarkRecord
from awcde.models.signature import WorkloadSignature
from awcde.models.classification import WorkloadClassification
from awcde.models.recommendation import InfrastructureRecommendation
from tests.conftest import TestDataFactory


pytestmark = pytest.mark.unit


class TestRepository:
    @pytest.fixture
    async def repo(self):
        repo = Repository(db_path=":memory:")
        await repo.init_db()
        return repo

    @pytest.mark.asyncio
    async def test_save_and_get_telemetry(self, repo):
        record_data = TestDataFactory.create_benchmark_record()
        record = BenchmarkRecord(**record_data)
        telemetry = BenchmarkTelemetry(
            provider_id="json", source_ref="test.json", records=[record]
        )
        await repo.save_telemetry(telemetry)
        retrieved = await repo.get_telemetry(telemetry.id)
        assert retrieved is not None
        assert retrieved.id == telemetry.id
        assert len(retrieved.records) == 1

    @pytest.mark.asyncio
    async def test_get_nonexistent_telemetry(self, repo):
        result = await repo.get_telemetry("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_save_and_get_signature(self, repo):
        sig_data = TestDataFactory.create_signature_dict()
        sig = WorkloadSignature(**sig_data)
        await repo.save_signature(sig)
        retrieved = await repo.get_signature(sig.id)
        assert retrieved is not None
        assert retrieved.schema_version == sig.schema_version

    @pytest.mark.asyncio
    async def test_save_and_get_classification(self, repo):
        cls_data = TestDataFactory.create_classification_dict()
        cls = WorkloadClassification(**cls_data)
        await repo.save_classification(cls)
        retrieved = await repo.get_classification(cls.id)
        assert retrieved is not None
        assert retrieved.primary_category == cls.primary_category

    @pytest.mark.asyncio
    async def test_save_and_get_recommendation(self, repo):
        rec_data = TestDataFactory.create_recommendation_dict()
        rec = InfrastructureRecommendation(**rec_data)
        await repo.save_recommendation(rec)
        retrieved = await repo.get_recommendation(rec.id)
        assert retrieved is not None
