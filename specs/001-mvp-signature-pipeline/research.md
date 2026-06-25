# Research: AWCDE MVP — Benchmark-to-Recommendation Pipeline

**Date**: 2026-06-24

Phase 0 research resolving technical unknowns for the FastAPI backend-first architecture.

> **Architecture context**: See [architecture.md](./architecture.md) for the long-term
> AWCDE vision. AWCDE ultimately ingests benchmark data, runtime metrics, and production
> telemetry. Phase 1 implements file-based benchmark input only. The Workload
> Characterization Engine produces Workload Signature Profiles; the Deployment Decision
> Engine maps them to model/runtime/infrastructure recommendations. Production
> deployment and continuous feedback loops are future phases.

---

## 1. Application Interface

**Decision**: FastAPI REST API as the primary interface; CLI deferred to a later phase.

**Rationale**: REST endpoints integrate naturally with operator workflows (curl, HTTP
clients, future UI) while keeping the MVP a single process. FastAPI provides automatic
OpenAPI documentation, request validation via Pydantic, and async-ready structure
without requiring async in Phase 1.

**Alternatives considered**:
- Typer CLI-first — rejected per architecture revision; REST is now primary
- gRPC — rejected; unnecessary complexity for MVP operator use
- Separate API + worker services — rejected; violates single-application constitution

**Endpoints (Phase 1)**:
- `POST /ingest` — accept file upload or path reference; route to Provider
- `POST /signatures` — derive signature from ingested telemetry
- `GET /signatures/{id}` — retrieve stored signature
- `POST /classifications` — classify a stored signature
- `GET /classifications/{id}` — retrieve classification result
- `POST /recommendations` — generate recommendations from classification
- `GET /recommendations/{id}` — retrieve recommendation result

---

## 2. Language and Framework

**Decision**: Python 3.12 with FastAPI + Uvicorn.

**Rationale**: Strong JSON/CSV ecosystem, Pydantic validation, fast MVP iteration,
single-process deployment. FastAPI aligns with backend-first architecture.

**Alternatives considered**:
- Go + Gin — more boilerplate for rule/KnowledgeBase iteration
- Rust + Axum — slower MVP velocity

---

## 3. Telemetry Provider Architecture

**Decision**: Provider protocol with registry pattern. Phase 1 implements
`JSONProvider` and `CSVProvider` only.

**Rationale**: Treats telemetry sources as pluggable adapters. File-based Providers
satisfy constitution (no live streams). Registry allows future Providers without
changing API or pipeline core.

**Phase 1 Providers**:
| Provider | Input | Status |
|---|---|---|
| `JSONProvider` | `.json` benchmark files | Implement |
| `CSVProvider` | `.csv` benchmark files | Implement |

**Future Providers (architecture only — not Phase 1)**:
| Provider | Input | Status |
|---|---|---|
| `GuideLLMProvider` | GuideLLM benchmark output | Deferred |
| `vLLMProvider` | vLLM benchmark metrics | Deferred |
| `PrometheusProvider` | Prometheus query results | Deferred |
| `OpenTelemetryProvider` | OTel trace/metric exports | Deferred |

**Provider contract** (see `contracts/provider-interface.md`):
- `provider_id`: stable identifier
- `supports(source)`: detect whether this Provider handles the input
- `ingest(source) -> BenchmarkTelemetry`: parse and normalize

---

## 4. Pipeline: Classification Layer

**Decision**: Insert `WorkloadClassification` between `WorkloadSignature` and
`InfrastructureRecommendation`.

**Rationale**: Signatures describe raw workload characteristics (8 dimensions).
Classification maps signatures into deployment-relevant categories (e.g.,
latency-critical-interactive, throughput-batch, memory-bound-long-context) that
KnowledgeBase rules target. Separating classification from recommendation keeps
rules simpler and explanations clearer.

**Classification categories (Phase 1 initial taxonomy)**:
- `latency_critical` — tight p99 latency requirements
- `throughput_optimized` — high RPS, relaxed latency
- `memory_intensive` — high memory footprint or long context
- `burst_tolerant` — spiky arrival patterns
- `hardware_specialized` — strong accelerator affinity
- `general_purpose` — no dominant characteristic (fallback)

A signature may map to one primary category plus optional secondary tags.

---

## 5. KnowledgeBase

**Decision**: KnowledgeBase as a first-class domain concept. Phase 1 uses static
manual rules loaded from YAML files in `data/knowledge/rules.yaml`.

**Rationale**: Constitution requires explainable rule-based recommendations. Separating
rules into KnowledgeBase prevents hard-coding reasoning in the recommendation engine.
Engine evaluates rules against WorkloadClassification + WorkloadSignature; rules
produce recommendation candidates with built-in rationale templates.

**Alternatives considered**:
- Rules embedded in Python code — rejected; harder to audit and extend
- ML-based recommendation — rejected; constitution violation for Phase 1
- External rules engine (Drools, etc.) — rejected; over-engineering for MVP

**KnowledgeBase contract** (see `contracts/knowledge-base-interface.md`):
- `load(rules_path)` — load static rules
- `query(classification, signature) -> RuleMatch[]` — find applicable rules
- Each rule: `rule_id`, `conditions`, `recommendations`, `rationale_template`

---

## 6. Validation and Schemas

**Decision**: Pydantic v2 models with JSON Schema export for contracts.

**Rationale**: Schema versioning for signatures, validation at API boundaries,
contract files generated from or aligned with Pydantic models.

---

## 7. Storage

**Decision**: SQLite embedded database.

**Rationale**: Zero-config, single-application fit, supports querying signatures,
classifications, and recommendations by ID. No external database dependency.

**Alternatives considered**:
- Flat JSON files — rejected; poor query/retrieval ergonomics
- PostgreSQL — rejected; overkill for MVP single operator

---

## 8. Signature Identity

**Decision**: SHA-256 hash of normalized telemetry JSON + schema version.

**Rationale**: Deterministic, reusable signatures (FR-009). Same input → same ID.

**Alternatives considered**:
- UUID — non-deterministic, breaks reusability requirement

---

## 9. Benchmark Input Schema

**Decision**: Minimal required fields mapping to 8 signature dimensions.

**Minimum fields per benchmark record**:

| Field | Maps to dimension |
|---|---|
| `latency_p50_ms`, `latency_p99_ms` | Latency sensitivity |
| `throughput_rps` | Throughput orientation |
| `peak_memory_gb`, `avg_memory_gb` | Memory intensity |
| `request_arrival_pattern` (steady/bursty) | Burst behaviour |
| `context_length_p50`, `context_length_p99` | Context length profile |
| `concurrency_level` | Concurrency profile |
| `accelerator_type`, `gpu_utilization_pct` | Hardware affinity |
| `modality` (text/vision/multimodal) | Modality |

Full schema in `contracts/benchmark-json.schema.json` and
`contracts/benchmark-csv-format.md`.

---

## 10. Constitution Compliance Summary

| Principle | How satisfied |
|---|---|
| Single application | One FastAPI process, modular monolith |
| File-based ingestion | JSONProvider + CSVProvider only |
| Explainable recommendations | KnowledgeBase rules with rationale + evidence |
| Versioned signatures | `schema_version` on WorkloadSignature |
| No K8s/MQ/autonomous deploy | Advisory recommendations only |
| No live telemetry | Provider registry extensible but streams not implemented |
| No ML | Static KnowledgeBase rules only |
