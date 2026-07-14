from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestDataFactory:
    """Static factory for test data with partial overrides (ESI.ts pattern)."""

    @staticmethod
    def create_benchmark_record(**overrides) -> dict:
        defaults = {
            "latency_p50_ms": 15.0,
            "latency_p99_ms": 45.0,
            "throughput_rps": 1200.0,
            "peak_memory_gb": 24.5,
            "avg_memory_gb": 18.2,
            "request_arrival_pattern": "steady",
            "context_length_p50": 512,
            "context_length_p99": 2048,
            "concurrency_level": 32,
            "accelerator_type": "A100",
            "gpu_utilization_pct": 50.0,
            "modality": "text",
        }
        return {**defaults, **overrides}

    @staticmethod
    def create_benchmark_record_latency_critical(**overrides) -> dict:
        return TestDataFactory.create_benchmark_record(
            latency_p50_ms=5.0,
            latency_p99_ms=500.0,
            throughput_rps=800.0,
            concurrency_level=16,
            gpu_utilization_pct=30.0,
            **overrides,
        )

    @staticmethod
    def create_benchmark_record_throughput_optimized(**overrides) -> dict:
        return TestDataFactory.create_benchmark_record(
            latency_p50_ms=50.0,
            latency_p99_ms=100.0,
            throughput_rps=5000.0,
            concurrency_level=128,
            gpu_utilization_pct=40.0,
            **overrides,
        )

    @staticmethod
    def create_benchmark_record_memory_intensive(**overrides) -> dict:
        return TestDataFactory.create_benchmark_record(
            peak_memory_gb=75.0,
            avg_memory_gb=60.0,
            context_length_p50=4096,
            context_length_p99=16384,
            gpu_utilization_pct=40.0,
            **overrides,
        )

    @staticmethod
    def create_benchmark_record_bursty(**overrides) -> dict:
        return TestDataFactory.create_benchmark_record(
            request_arrival_pattern="bursty",
            latency_p50_ms=10.0,
            latency_p99_ms=200.0,
            gpu_utilization_pct=30.0,
            **overrides,
        )

    @staticmethod
    def create_telemetry_dict(records: list[dict] | None = None, **overrides) -> dict:
        defaults = {
            "id": str(uuid.uuid4()),
            "provider_id": "json",
            "source_ref": "test_file.json",
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "records": records or [TestDataFactory.create_benchmark_record()],
        }
        return {**defaults, **overrides}

    @staticmethod
    def create_dimension_score(**overrides) -> dict:
        defaults = {
            "level": "medium",
            "score": 0.5,
            "raw_inputs": {"latency_p50_ms": 15.0, "latency_p99_ms": 45.0},
        }
        return {**defaults, **overrides}

    @staticmethod
    def create_signature_dict(**overrides) -> dict:
        defaults = {
            "id": "sig-" + str(uuid.uuid4())[:8],
            "schema_version": "1.0.0",
            "telemetry_id": str(uuid.uuid4()),
            "derived_at": datetime.now(timezone.utc).isoformat(),
            "latency_sensitivity": TestDataFactory.create_dimension_score(
                raw_inputs={"latency_p50_ms": 15.0, "latency_p99_ms": 45.0}
            ),
            "throughput_orientation": TestDataFactory.create_dimension_score(
                raw_inputs={"throughput_rps": 1200.0, "concurrency_level": 32}
            ),
            "memory_intensity": TestDataFactory.create_dimension_score(
                raw_inputs={"peak_memory_gb": 24.5, "avg_memory_gb": 18.2}
            ),
            "burst_behaviour": TestDataFactory.create_dimension_score(
                score=0.2,
                level="low",
                raw_inputs={"request_arrival_pattern": "steady"},
            ),
            "context_length_profile": TestDataFactory.create_dimension_score(
                raw_inputs={"context_length_p50": 512, "context_length_p99": 2048}
            ),
            "concurrency_profile": TestDataFactory.create_dimension_score(
                raw_inputs={"concurrency_level": 32, "throughput_rps": 1200.0}
            ),
            "hardware_affinity": TestDataFactory.create_dimension_score(
                raw_inputs={"accelerator_type": "A100", "gpu_utilization_pct": 50.0}
            ),
            "modality": TestDataFactory.create_dimension_score(
                score=0.2,
                level="low",
                raw_inputs={"modality": "text"},
            ),
        }
        return {**defaults, **overrides}

    @staticmethod
    def create_classification_dict(**overrides) -> dict:
        defaults = {
            "id": str(uuid.uuid4()),
            "signature_id": "sig-" + str(uuid.uuid4())[:8],
            "classified_at": datetime.now(timezone.utc).isoformat(),
            "primary_category": "general_purpose",
            "secondary_tags": [],
            "confidence": 0.75,
            "rationale": "Balanced workload with no single dominant dimension.",
            "dimension_summary": {
                "latency_sensitivity": 0.5,
                "throughput_orientation": 0.5,
                "memory_intensity": 0.5,
            },
        }
        return {**defaults, **overrides}

    @staticmethod
    def create_recommendation_evidence(**overrides) -> dict:
        defaults = {
            "rule_id": "kb-general-001",
            "source_type": "classification",
            "attribute": "classification.primary_category",
            "attribute_value": "general_purpose",
            "condition_matched": "primary_category equals general_purpose",
        }
        return {**defaults, **overrides}

    @staticmethod
    def create_recommendation_block(**overrides) -> dict:
        defaults = {
            "recommendation": "general-purpose",
            "reasoning": "Balanced workload configuration recommended.",
            "evidence": [TestDataFactory.create_recommendation_evidence()],
        }
        return {**defaults, **overrides}

    @staticmethod
    def create_recommendation_dict(**overrides) -> dict:
        defaults = {
            "id": str(uuid.uuid4()),
            "classification_id": str(uuid.uuid4()),
            "signature_id": "sig-" + str(uuid.uuid4())[:8],
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "model_family": TestDataFactory.create_recommendation_block(
                recommendation="general-purpose"
            ),
            "runtime": TestDataFactory.create_recommendation_block(
                recommendation="vllm-standard"
            ),
            "hardware_suitability": TestDataFactory.create_recommendation_block(
                recommendation="gpu-shared-pool"
            ),
            "deployment_topology": TestDataFactory.create_recommendation_block(
                recommendation="multi-replica-balanced"
            ),
            "scheduling_policy": TestDataFactory.create_recommendation_block(
                recommendation="fair-share"
            ),
        }
        return {**defaults, **overrides}

    @staticmethod
    def create_knowledge_rule(**overrides) -> dict:
        defaults = {
            "rule_id": "kb-test-001",
            "version": "1.0.0",
            "description": "Test rule for unit testing",
            "conditions": [
                {
                    "field": "classification.primary_category",
                    "operator": "eq",
                    "value": "general_purpose",
                }
            ],
            "recommendations": {
                "model_family": "general-purpose",
                "runtime": "vllm-standard",
                "hardware_suitability": "gpu-shared-pool",
                "deployment_topology": "multi-replica-balanced",
                "scheduling_policy": "fair-share",
            },
            "rationale_template": "Test rule {rule_id} matched.",
        }
        return {**defaults, **overrides}


@pytest.fixture
def factory():
    return TestDataFactory


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture
def valid_json_content():
    return (FIXTURES_DIR / "benchmark_valid.json").read_bytes()


@pytest.fixture
def valid_csv_content():
    return (FIXTURES_DIR / "benchmark_valid.csv").read_bytes()


@pytest.fixture
def invalid_types_json_content():
    return (FIXTURES_DIR / "benchmark_invalid_types.json").read_bytes()


@pytest.fixture
def missing_fields_json_content():
    return (FIXTURES_DIR / "benchmark_missing_fields.json").read_bytes()


@pytest.fixture
def edge_values_json_content():
    return (FIXTURES_DIR / "benchmark_edge_values.json").read_bytes()


@pytest.fixture
def test_rules_path():
    return FIXTURES_DIR / "rules_test.yaml"


# --- Shared service fixtures (used by TDD orchestrator + BDD tests) ---


@pytest.fixture
def flyweight_registry():
    from awcde.flyweight.registry import FlyweightRegistry
    return FlyweightRegistry()


@pytest.fixture
def provider_registry():
    from awcde.providers.registry import ProviderRegistry
    from awcde.providers.json_provider import JSONProvider
    from awcde.providers.csv_provider import CSVProvider
    registry = ProviderRegistry()
    registry.register(JSONProvider())
    registry.register(CSVProvider())
    return registry


@pytest.fixture
def knowledge_base(test_rules_path):
    from awcde.knowledge.static_kb import StaticKnowledgeBase
    kb = StaticKnowledgeBase()
    kb.load(test_rules_path)
    return kb


@pytest.fixture
def signature_service(flyweight_registry):
    from awcde.signatures.service import SignatureService
    return SignatureService(flyweight_registry)


@pytest.fixture
def classifier(flyweight_registry):
    from awcde.classification.classifier import WorkloadClassifier
    return WorkloadClassifier(flyweight_registry)


@pytest.fixture
def recommendation_engine(knowledge_base):
    from awcde.recommendations.engine import RecommendationEngine
    return RecommendationEngine(knowledge_base)


@pytest.fixture
async def repository():
    from awcde.storage.repository import Repository
    repo = Repository(db_path=":memory:")
    await repo.init_db()
    return repo


@pytest.fixture
async def pipeline(provider_registry, signature_service, classifier, recommendation_engine, repository):
    from awcde.pipeline.orchestrator import PipelineOrchestrator
    return PipelineOrchestrator(
        provider_registry=provider_registry,
        signature_service=signature_service,
        classifier=classifier,
        recommendation_engine=recommendation_engine,
        repository=repository,
    )


# --- API test fixtures (used by integration + contract tests) ---


@pytest.fixture
async def test_app(provider_registry, flyweight_registry, knowledge_base, repository):
    from awcde.main import app
    from awcde.api.dependencies import (
        get_repository,
        get_knowledge_base,
        get_provider_registry,
        get_flyweight_registry,
        get_signature_service,
        get_classifier,
        get_recommendation_engine,
        get_pipeline,
    )
    from awcde.signatures.service import SignatureService
    from awcde.classification.classifier import WorkloadClassifier
    from awcde.recommendations.engine import RecommendationEngine
    from awcde.pipeline.orchestrator import PipelineOrchestrator

    sig_service = SignatureService(flyweight_registry)
    clf = WorkloadClassifier(flyweight_registry)
    rec_engine = RecommendationEngine(knowledge_base)
    pl = PipelineOrchestrator(
        provider_registry=provider_registry,
        signature_service=sig_service,
        classifier=clf,
        recommendation_engine=rec_engine,
        repository=repository,
    )

    app.dependency_overrides[get_repository] = lambda: repository
    app.dependency_overrides[get_knowledge_base] = lambda: knowledge_base
    app.dependency_overrides[get_provider_registry] = lambda: provider_registry
    app.dependency_overrides[get_flyweight_registry] = lambda: flyweight_registry
    app.dependency_overrides[get_signature_service] = lambda: sig_service
    app.dependency_overrides[get_classifier] = lambda: clf
    app.dependency_overrides[get_recommendation_engine] = lambda: rec_engine
    app.dependency_overrides[get_pipeline] = lambda: pl

    yield app

    app.dependency_overrides.clear()


@pytest.fixture
async def client(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
