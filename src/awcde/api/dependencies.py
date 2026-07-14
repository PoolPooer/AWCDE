from functools import lru_cache
from pathlib import Path

from awcde.flyweight.registry import FlyweightRegistry
from awcde.knowledge.static_kb import StaticKnowledgeBase
from awcde.providers.registry import ProviderRegistry
from awcde.providers.json_provider import JSONProvider
from awcde.providers.csv_provider import CSVProvider
from awcde.storage.repository import Repository
from awcde.pipeline.orchestrator import PipelineOrchestrator
from awcde.signatures.service import SignatureService
from awcde.classification.classifier import WorkloadClassifier
from awcde.recommendations.engine import RecommendationEngine


@lru_cache
def get_flyweight_registry() -> FlyweightRegistry:
    return FlyweightRegistry()


@lru_cache
def get_provider_registry() -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(JSONProvider())
    registry.register(CSVProvider())
    return registry


@lru_cache
def get_repository() -> Repository:
    return Repository()


@lru_cache
def get_knowledge_base() -> StaticKnowledgeBase:
    kb = StaticKnowledgeBase()
    rules_path = Path(__file__).parent.parent.parent.parent / "data" / "knowledge" / "rules.yaml"
    if rules_path.exists():
        kb.load(rules_path)
    return kb


@lru_cache
def get_signature_service() -> SignatureService:
    return SignatureService(get_flyweight_registry())


@lru_cache
def get_classifier() -> WorkloadClassifier:
    return WorkloadClassifier(get_flyweight_registry())


@lru_cache
def get_recommendation_engine() -> RecommendationEngine:
    return RecommendationEngine(get_knowledge_base())


@lru_cache
def get_pipeline() -> PipelineOrchestrator:
    return PipelineOrchestrator(
        provider_registry=get_provider_registry(),
        signature_service=get_signature_service(),
        classifier=get_classifier(),
        recommendation_engine=get_recommendation_engine(),
        repository=get_repository(),
    )
