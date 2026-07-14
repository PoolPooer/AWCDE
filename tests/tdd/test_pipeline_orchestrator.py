"""Tier 1 TDD: Pipeline orchestrator tests."""

from __future__ import annotations

import json
import pytest

from awcde.pipeline.orchestrator import PipelineOrchestrator
from awcde.providers.base import ProviderSource
from awcde.models.recommendation import InfrastructureRecommendation
from tests.conftest import TestDataFactory, FIXTURES_DIR


pytestmark = pytest.mark.unit


class TestPipelineOrchestrator:
    @pytest.fixture
    def source(self):
        content = (FIXTURES_DIR / "benchmark_valid.json").read_bytes()
        return ProviderSource(filename="test.json", content_type="application/json", content=content)

    @pytest.mark.asyncio
    async def test_execute_full_pipeline(self, pipeline, source):
        result = await pipeline.execute("json", source)
        assert isinstance(result, InfrastructureRecommendation)
        assert result.model_family is not None
        assert result.runtime is not None

    @pytest.mark.asyncio
    async def test_pipeline_stores_all_entities(self, pipeline, source, repository):
        result = await pipeline.execute("json", source)
        sig = await repository.get_signature(result.signature_id)
        assert sig is not None
        cls = await repository.get_classification(result.classification_id)
        assert cls is not None
