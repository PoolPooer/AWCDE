# AWCDE Long-Term Architecture Context

**Date**: 2026-06-24  
**Scope**: Architecture vision and Phase 1 boundary — does NOT expand MVP implementation scope.

This document describes the long-term AWCDE architecture shown in the project concept
diagram. Phase 1 MVP implements only the subset marked **Phase 1** below.

---

## Concept Diagram Overview

```text
┌─────────────────────────────────────────────────────────────────┐
│                     INPUT SOURCES                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Benchmark    │  │ Runtime      │  │ Production           │  │
│  │ Data         │  │ Metrics      │  │ Telemetry            │  │
│  │ [Phase 1]    │  │ [Future]     │  │ [Future]             │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         └─────────────────┼─────────────────────┘               │
│                           ▼                                      │
│              ┌────────────────────────┐                          │
│              │ Workload               │                          │
│              │ Characterization Engine│  [Phase 1]               │
│              └───────────┬────────────┘                          │
│                          ▼                                       │
│              ┌────────────────────────┐                          │
│              │ Workload Signature     │                          │
│              │ Profile                │  [Phase 1]               │
│              └───────────┬────────────┘                          │
│                          ▼                                       │
│              ┌────────────────────────┐                          │
│              │ Deployment Decision    │                          │
│              │ Engine                 │  [Phase 1]               │
│              └───────────┬────────────┘                          │
│         ┌────────────────┼────────────────┐                      │
│         ▼                ▼                ▼                      │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────────┐      │
│  │ Model      │  │ Runtime    │  │ Infrastructure      │      │
│  │ Choice     │  │ Choice     │  │ Configuration       │      │
│  │ [Phase 1]  │  │ [Phase 1]  │  │ [Phase 1]           │      │
│  └─────┬──────┘  └─────┬──────┘  └──────────┬──────────┘      │
│        └───────────────┼─────────────────────┘                  │
│                        ▼                                         │
│              ┌────────────────────────┐                          │
│              │ Production Deployment  │  [Future — NOT MVP]     │
│              └───────────┬────────────┘                          │
│                          ▼                                       │
│              ┌────────────────────────┐                          │
│              │ Continuous Feedback    │  [Future — NOT MVP]     │
│              │ Loop                   │                          │
│              └───────────┬────────────┘                          │
│                          ▼                                       │
│              ┌────────────────────────┐                          │
│              │ Workload Profile       │  [Future — NOT MVP]     │
│              │ Update                 │                          │
│              └───────────┬────────────┘                          │
│                          │ (feeds back to Characterization)      │
└──────────────────────────┴──────────────────────────────────────┘
```

---

## Input Sources

AWCDE is designed to consume three categories of input over its lifetime:

| Input Source | Description | Phase 1 Status |
|---|---|---|
| **Benchmark Data** | Structured AI inference benchmark results (latency, throughput, memory, etc.) | **Implemented** — file-based JSON/CSV via JSONProvider and CSVProvider |
| **Runtime Metrics** | Live or collected serving metrics (GPU utilization, queue depth, batch sizes) | **Future** — architecture reserved via Provider registry (e.g., vLLMProvider, PrometheusProvider) |
| **Production Telemetry** | Operational traces and metrics from deployed inference workloads | **Future** — architecture reserved via Provider registry (e.g., OpenTelemetryProvider) |

Phase 1 MUST NOT implement runtime metrics or production telemetry ingestion. The
Provider registry pattern allows these sources to be added in later phases without
restructuring the pipeline.

---

## Core Engines

### Workload Characterization Engine (Phase 1)

Transforms input telemetry into a **Workload Signature Profile** — a versioned,
reusable characterization of workload behaviour.

**Phase 1 implementation**:
- `src/awcde/signatures/` — derives WorkloadSignature (8 profile dimensions)
- `src/awcde/classification/` — maps signature to WorkloadClassification
- REST API: `POST /signatures`, `POST /classifications`

**MVP mapping**: `WorkloadSignature` + `WorkloadClassification` = Workload Signature
Profile in the concept diagram.

### Deployment Decision Engine (Phase 1)

Maps Workload Signature Profiles to deployment recommendations by consulting the
KnowledgeBase.

**Phase 1 outputs** (advisory only — no actuation):

| Concept Diagram Output | MVP Recommendation Dimension |
|---|---|
| Model Choice | `model_family` |
| Runtime Choice | `runtime` |
| Infrastructure Configuration | `hardware_suitability`, `deployment_topology`, `scheduling_policy` |

**Phase 1 implementation**:
- `src/awcde/knowledge/` — static KnowledgeBase rules
- `src/awcde/recommendations/` — rule evaluation, explanation, evidence
- REST API: `POST /recommendations`

Recommendations are **advisory only**. The engine does NOT deploy, configure, or
actuate infrastructure in Phase 1.

---

## Future Phases (Explicitly Out of MVP Scope)

The following concept diagram elements are **NOT implemented in Phase 1**:

| Element | Why deferred |
|---|---|
| **Production Deployment** | Constitution excludes autonomous deployment; MVP validates recommendations only |
| **Continuous Feedback Loop** | Requires live production telemetry and closed-loop optimization — excluded in Phase 1 |
| **Workload Profile Update** | Depends on feedback loop; signatures are derived from static benchmark input in MVP |
| **Runtime Metrics input** | Live/streaming ingestion excluded; file-based benchmarks sufficient to validate hypothesis |
| **Production Telemetry input** | Same as above |

These remain long-term architecture goals and inform Provider registry design, but
adding them to Phase 1 would expand MVP scope beyond constitution constraints.

---

## Phase 1 MVP Pipeline (Implementation Scope)

```text
Benchmark Data (JSON/CSV files)
        ↓  JSONProvider / CSVProvider
  BenchmarkTelemetry
        ↓  Workload Characterization Engine
  WorkloadSignature  →  WorkloadClassification
        ↓  Deployment Decision Engine (KnowledgeBase)
  InfrastructureRecommendation
        ↓
   [STOP — advisory output only; no deployment or feedback loop]
```

This is the complete Phase 1 scope. See [plan.md](./plan.md) for implementation details
and [spec.md](./spec.md) for functional requirements.

---

## Terminology Mapping

| Concept Diagram Term | MVP Artifact / Module |
|---|---|
| Benchmark Data | `BenchmarkTelemetry` via JSONProvider/CSVProvider |
| Runtime Metrics | Future Provider (not implemented) |
| Production Telemetry | Future Provider (not implemented) |
| Workload Characterization Engine | `signatures/` + `classification/` |
| Workload Signature Profile | `WorkloadSignature` + `WorkloadClassification` |
| Deployment Decision Engine | `recommendations/` + `knowledge/` |
| Model Choice | `InfrastructureRecommendation.model_family` |
| Runtime Choice | `InfrastructureRecommendation.runtime` |
| Infrastructure Configuration | `hardware_suitability`, `deployment_topology`, `scheduling_policy` |
| Production Deployment | Not in Phase 1 |
| Continuous Feedback Loop | Not in Phase 1 |
| Workload Profile Update | Not in Phase 1 |
