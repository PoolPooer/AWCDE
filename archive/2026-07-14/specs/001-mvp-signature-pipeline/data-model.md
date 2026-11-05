# Data Model: AWCDE MVP — Benchmark-to-Recommendation Pipeline

**Date**: 2026-06-24

> **Architecture context**: In the long-term AWCDE vision, three input source categories
> (benchmark data, runtime metrics, production telemetry) feed a Workload
> Characterization Engine producing Workload Signature Profiles, which a Deployment
> Decision Engine maps to model/runtime/infrastructure recommendations. Phase 1
> implements benchmark file input only. See [architecture.md](./architecture.md).

## Pipeline Overview

**Phase 1 MVP pipeline** (production deployment and feedback loop excluded):

```text
Provider.ingest() → BenchmarkTelemetry          ← Benchmark Data input (Phase 1 only)
                         ↓ derive                ← Workload Characterization Engine
                   WorkloadSignature (stored)     ← Workload Signature Profile
                         ↓ classify
                   WorkloadClassification (stored)
                         ↓ recommend (via KnowledgeBase)  ← Deployment Decision Engine
                   InfrastructureRecommendation (stored)  ← Model / Runtime / Infrastructure
                         ↓
                   [STOP — advisory only; no deployment or feedback loop]
```

---

## BenchmarkTelemetry

Normalized inference benchmark measurements produced by a Provider adapter.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | auto | Unique ingest record identifier |
| `provider_id` | string | yes | Source Provider (`json`, `csv`) |
| `source_ref` | string | yes | Original file path or upload reference |
| `ingested_at` | datetime | auto | Ingestion timestamp (ISO 8601) |
| `records` | list[BenchmarkRecord] | yes | One or more benchmark measurement records |

### BenchmarkRecord

| Field | Type | Required | Description |
|---|---|---|---|
| `latency_p50_ms` | float | yes | 50th percentile latency (ms) |
| `latency_p99_ms` | float | yes | 99th percentile latency (ms) |
| `throughput_rps` | float | yes | Requests per second |
| `peak_memory_gb` | float | yes | Peak memory usage (GB) |
| `avg_memory_gb` | float | yes | Average memory usage (GB) |
| `request_arrival_pattern` | enum | yes | `steady` or `bursty` |
| `context_length_p50` | int | yes | Median context/token length |
| `context_length_p99` | int | yes | 99th percentile context length |
| `concurrency_level` | int | yes | Concurrent request count |
| `accelerator_type` | string | yes | e.g. `A100`, `H100`, `CPU` |
| `gpu_utilization_pct` | float | yes | GPU utilization 0–100 |
| `modality` | enum | yes | `text`, `vision`, `multimodal` |

**Validation rules**:
- All numeric fields MUST be non-negative
- `latency_p99_ms` >= `latency_p50_ms`
- `context_length_p99` >= `context_length_p50`
- `gpu_utilization_pct` in range 0–100
- `modality` MUST be one of defined enum values

**State**: ingested (no further state transitions in Phase 1)

---

## WorkloadSignature

Versioned, reusable workload characterization derived from BenchmarkTelemetry.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Deterministic hash (SHA-256 of normalized input + schema version) |
| `schema_version` | string | yes | Semver, initial `1.0.0` |
| `telemetry_id` | string | yes | FK to source BenchmarkTelemetry |
| `derived_at` | datetime | auto | Derivation timestamp |
| `latency_sensitivity` | DimensionScore | yes | See DimensionScore below |
| `throughput_orientation` | DimensionScore | yes | |
| `memory_intensity` | DimensionScore | yes | |
| `burst_behaviour` | DimensionScore | yes | |
| `context_length_profile` | DimensionScore | yes | |
| `concurrency_profile` | DimensionScore | yes | |
| `hardware_affinity` | DimensionScore | yes | |
| `modality` | DimensionScore | yes | |

### DimensionScore

| Field | Type | Description |
|---|---|---|
| `level` | enum | Categorical band: `low`, `medium`, `high` |
| `score` | float | Normalized score 0.0–1.0 |
| `raw_inputs` | dict | Source benchmark values used in derivation |

**Validation rules**:
- All eight dimensions MUST be present
- `score` in range 0.0–1.0
- Identical telemetry under same `schema_version` MUST produce identical `id`

**State transitions**: `derived` → `stored`

---

## WorkloadClassification

Deployment-relevant category assignment derived from a WorkloadSignature.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | auto | Unique classification identifier |
| `signature_id` | string | yes | FK to WorkloadSignature |
| `classified_at` | datetime | auto | Classification timestamp |
| `primary_category` | enum | yes | Primary workload category |
| `secondary_tags` | list[string] | no | Additional classification tags |
| `confidence` | float | yes | Classification confidence 0.0–1.0 |
| `rationale` | string | yes | Human-readable explanation of classification |
| `dimension_summary` | dict | yes | Key dimension scores that drove classification |

### Classification Categories (Phase 1)

| Category | Typical triggers |
|---|---|
| `latency_critical` | High latency sensitivity, moderate concurrency |
| `throughput_optimized` | High throughput orientation, relaxed latency |
| `memory_intensive` | High memory intensity or long context profile |
| `burst_tolerant` | High burst behaviour score |
| `hardware_specialized` | Strong hardware affinity to specific accelerator |
| `general_purpose` | No single dominant characteristic |

**Validation rules**:
- `primary_category` MUST be one of defined enum values
- `confidence` in range 0.0–1.0
- `rationale` MUST reference at least one signature dimension

**State transitions**: `classified` → `stored`

---

## KnowledgeBase

First-class domain concept holding deployment recommendation rules.

### KnowledgeRule

| Field | Type | Required | Description |
|---|---|---|---|
| `rule_id` | string | yes | Stable rule identifier |
| `version` | string | yes | Rule set version |
| `description` | string | yes | Human-readable rule purpose |
| `conditions` | list[RuleCondition] | yes | Match criteria |
| `recommendations` | dict | yes | Recommendation values per dimension |
| `rationale_template` | string | yes | Template with `{placeholders}` for explanation |

### RuleCondition

| Field | Type | Description |
|---|---|---|
| `field` | string | Signature dimension, classification category, or attribute path |
| `operator` | enum | `eq`, `gt`, `gte`, `lt`, `lte`, `in` |
| `value` | any | Comparison value |

**Phase 1 implementation**: Static rules loaded from `data/knowledge/rules.yaml`.
No ML, no learned weights, no black-box scoring.

---

## InfrastructureRecommendation

Advisory deployment guidance produced by consulting KnowledgeBase rules against a
WorkloadClassification and its source WorkloadSignature.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | auto | Unique recommendation identifier |
| `classification_id` | string | yes | FK to WorkloadClassification |
| `signature_id` | string | yes | FK to WorkloadSignature (denormalized for traceability) |
| `generated_at` | datetime | auto | Generation timestamp |
| `model_family` | RecommendationBlock | yes | |
| `runtime` | RecommendationBlock | yes | |
| `hardware_suitability` | RecommendationBlock | yes | |
| `deployment_topology` | RecommendationBlock | yes | |
| `scheduling_policy` | RecommendationBlock | yes | |

### RecommendationBlock

| Field | Type | Required | Description |
|---|---|---|---|
| `recommendation` | string | yes | Suggested value |
| `reasoning` | string | yes | Human-readable explanation |
| `evidence` | list[RecommendationEvidence] | yes | Traceable supporting evidence |

### RecommendationEvidence

| Field | Type | Required | Description |
|---|---|---|---|
| `rule_id` | string | yes | KnowledgeBase rule that contributed |
| `source_type` | enum | yes | `signature`, `classification`, or `telemetry` |
| `attribute` | string | yes | Attribute path that matched |
| `attribute_value` | any | yes | Value at time of evaluation |
| `condition_matched` | string | yes | Human-readable condition description |

**Validation rules**:
- All five recommendation dimensions MUST be present
- Every block MUST have non-empty `reasoning` and at least one `evidence` entry
- Every `evidence.rule_id` MUST reference a KnowledgeBase rule

**State transitions**: `generated` → `stored`

---

## Entity Relationships

```text
BenchmarkTelemetry 1 ──→ 1 WorkloadSignature
WorkloadSignature  1 ──→ 1 WorkloadClassification
WorkloadClassification 1 ──→ 1 InfrastructureRecommendation
KnowledgeBase (static) ── consulted by ──→ RecommendationEngine
```

---

## Provider Registry (supporting concept)

| Field | Type | Description |
|---|---|---|
| `provider_id` | string | e.g. `json`, `csv` |
| `provider_class` | class | Provider implementation |
| `supported_formats` | list[string] | File extensions or MIME types |

Phase 1: `JSONProvider`, `CSVProvider`.
Future registry entries (not implemented): `GuideLLMProvider`, `vLLMProvider`,
`PrometheusProvider`, `OpenTelemetryProvider`.
