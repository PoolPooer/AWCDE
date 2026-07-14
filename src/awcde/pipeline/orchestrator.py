"""Pipeline orchestrator for CSP-style workload analysis.

Composes the ingestion, signature derivation, classification, and
recommendation stages into a sequential pipeline where each stage
receives and produces immutable Pydantic models.
"""

from __future__ import annotations

from awcde.classification.classifier import WorkloadClassifier
from awcde.models.recommendation import InfrastructureRecommendation
from awcde.providers.base import ProviderSource
from awcde.providers.registry import ProviderRegistry
from awcde.recommendations.engine import RecommendationEngine
from awcde.signatures.service import SignatureService
from awcde.storage.repository import Repository


class PipelineOrchestrator:
    """Orchestrates the workload analysis pipeline.

    Composes four stages in sequence, each passing immutable Pydantic models
    to the next (CSP-style message passing):

        1. Ingest: raw source -> BenchmarkTelemetry
        2. Derive: BenchmarkTelemetry -> WorkloadSignature
        3. Classify: WorkloadSignature -> WorkloadClassification
        4. Recommend: (WorkloadClassification, WorkloadSignature) -> InfrastructureRecommendation

    All intermediate and final artifacts are persisted via the repository.
    """

    def __init__(
        self,
        provider_registry: ProviderRegistry,
        signature_service: SignatureService,
        classifier: WorkloadClassifier,
        recommendation_engine: RecommendationEngine,
        repository: Repository,
    ) -> None:
        self._provider_registry = provider_registry
        self._signature_service = signature_service
        self._classifier = classifier
        self._recommendation_engine = recommendation_engine
        self._repository = repository

    async def execute(
        self,
        provider_id: str,
        source: ProviderSource,
    ) -> InfrastructureRecommendation:
        """Execute the full analysis pipeline.

        Args:
            provider_id: Identifier for the ingestion provider (e.g. "json", "csv").
            source: The raw telemetry data source.

        Returns:
            The final InfrastructureRecommendation produced by the pipeline.
        """
        provider = self._provider_registry.get(provider_id)
        telemetry = provider.ingest(source)
        await self._repository.save_telemetry(telemetry)

        signature = self._signature_service.process(telemetry)
        await self._repository.save_signature(signature)

        classification = self._classifier.process(signature)
        await self._repository.save_classification(classification)

        recommendation = self._recommendation_engine.process(
            classification, signature
        )
        await self._repository.save_recommendation(recommendation)

        return recommendation
