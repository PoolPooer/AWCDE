# Implementation Plan: AWCDE MVP — Benchmark-to-Recommendation Pipeline

**Branch**: `001-mvp-signature-pipeline` | **Date**: 2026-06-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-mvp-signature-pipeline/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command.

## Summary

Single Python FastAPI application that ingests AI inference benchmark telemetry via
Provider adapters (JSON and CSV in Phase 1), derives versioned workload signatures
(8 dimensions), classifies workloads into deployment-relevant categories, and produces
explainable infrastructure recommendations by consulting a static KnowledgeBase.
REST API is the primary interface; CLI is deferred to a later phase.

See [architecture.md](./architecture.md) for long-term AWCDE vision and Phase 1
boundaries. Phase 1 implements file-based benchmark input only; runtime metrics,
production telemetry, deployment actuation, and feedback loops are future phases.

**Phase 1 pipeline flow**:

```text
BenchmarkTelemetry → WorkloadSignature → WorkloadClassification → InfrastructureRecommendation
         ↑                                      ↑
    Provider layer                      KnowledgeBase (static rules)
   (JSON/CSV only)                      (Deployment Decision Engine)
```

**Long-term input sources** (architecture context — Phase 1 implements benchmark
data only):

| Source | Phase 1 | Future Provider examples |
|---|---|---|
| Benchmark Data | JSONProvider, CSVProvider | GuideLLMProvider |
| Runtime Metrics | Not implemented | vLLMProvider, PrometheusProvider |
| Production Telemetry | Not implemented | OpenTelemetryProvider |

**Engine mapping**:

| Concept | Phase 1 module | Output |
|---|---|---|
| Workload Characterization Engine | `signatures/`, `classification/` | Workload Signature Profile |
| Deployment Decision Engine | `recommendations/`, `knowledge/` | Model, runtime, infrastructure recommendations |

Production deployment and continuous feedback loop are **not in Phase 1 scope**.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: FastAPI, Uvicorn, Pydantic v2 (validation/schemas), SQLite3
(embedded storage)

**Storage**: SQLite file (configurable path, default `~/.awcde/awcde.db`)

**Testing**: pytest (optional — not mandated by spec)

**Target Platform**: macOS/Linux server or workstation (single-process HTTP service)

**Project Type**: Single FastAPI web service (modular monolith)

**Performance Goals**: Ingest + signature + classification + recommend for 10 MB file
in under 30 seconds (per SC-001)

**Constraints**: File-based input via Providers only in Phase 1; rule-based logic
consulting KnowledgeBase; no live telemetry streams; no ML

**Scale/Scope**: Single operator; hundreds of signatures; dozens of KnowledgeBase rules;
extensible Provider registry for future telemetry sources

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **MVP scope**: End-to-end slice — ingest, signature, classification,
  recommendation; no platform/multi-service scope
- [x] **Single application**: FastAPI modular monolith; no microservices or message
  queues
- [x] **Explainability**: Recommendations consult KnowledgeBase rules with traceable
  reasoning and evidence; no ML/black-box
- [x] **Versioned signatures**: Pydantic models with `schema_version` field; semver
  policy
- [x] **File ingestion first**: JSONProvider and CSVProvider only; no live telemetry
- [x] **Phase 1 exclusions**: No K8s controllers, autonomous deploy, MQ, production
  self-tuning, or ML recommendations

## Project Structure

### Documentation (this feature)

```text
specs/001-mvp-signature-pipeline/
├── spec.md
├── plan.md
├── architecture.md    # Long-term vision and Phase 1 boundaries
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
src/awcde/
├── __init__.py
├── main.py                     # FastAPI app entrypoint
├── api/
│   ├── routes/
│   │   ├── ingest.py           # POST /ingest
│   │   ├── signatures.py       # POST /signatures, GET /signatures/{id}
│   │   ├── classifications.py  # POST /classifications, GET /classifications/{id}
│   │   └── recommendations.py  # POST /recommendations, GET /recommendations/{id}
│   └── dependencies.py
├── providers/
│   ├── base.py                 # Provider protocol / abstract base
│   ├── registry.py             # Provider registration and lookup
│   ├── json_provider.py        # Phase 1: JSONProvider
│   └── csv_provider.py         # Phase 1: CSVProvider
├── signatures/
│   ├── derivation.py           # 8-dimension profile builder
│   ├── schema.py               # Schema versioning
│   └── service.py              # Derive + persist orchestration
├── classification/
│   ├── classifier.py           # Signature → WorkloadClassification
│   └── categories.py           # Classification taxonomy
├── knowledge/
│   ├── base.py                 # KnowledgeBase protocol
│   └── static_kb.py            # Phase 1: static/manual rule knowledge
├── recommendations/
│   ├── engine.py               # Consults KnowledgeBase; builds recommendations
│   ├── explainer.py            # Human-readable reasoning assembly
│   └── evidence.py             # Evidence trace collector
├── storage/
│   └── repository.py           # SQLite persistence
└── models/
    ├── telemetry.py
    ├── signature.py
    ├── classification.py
    ├── recommendation.py
    └── knowledge.py

tests/
├── unit/
├── integration/
└── fixtures/                   # Sample benchmark JSON/CSV files

data/
└── knowledge/                  # Static KnowledgeBase rule files (Phase 1)
    └── rules.yaml
```

**Structure Decision**: Single-project FastAPI layout. All modules live under
`src/awcde/` in one deployable process. Provider and KnowledgeBase abstractions
allow future extension without restructuring. CLI deferred — not present in Phase 1.

## Complexity Tracking

> No constitution violations. Single application, file-based Providers, static
> KnowledgeBase, rule-based recommendations.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
