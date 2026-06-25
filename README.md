# AWCDE

**Adaptive Workload Characterization and Deployment Engine**

AWCDE is a research project exploring how AI inference telemetry can be transformed into reusable workload intelligence and explainable infrastructure recommendations.

Rather than requiring engineers to manually interpret benchmark results, runtime metrics, and operational telemetry, AWCDE derives behavioural workload signatures that characterize how an inference workload behaves. These signatures are then used to generate transparent deployment recommendations for models, runtimes, hardware, and infrastructure configuration.

---

## Vision

```
Telemetry
      │
      ▼
Workload Characterization
      │
      ▼
Workload Signature
      │
      ▼
Workload Classification
      │
      ▼
Knowledge Base
      │
      ▼
Infrastructure Recommendation
```

The long-term vision extends this pipeline with production telemetry and continuous feedback, allowing recommendations to evolve as workloads change over time.

---

## Current Status

### ✅ Phase 0 — Architecture & Specification

Completed:

* Repository initialization
* Spec Kit integration
* Project constitution
* MVP specification
* Architecture baseline
* Data model
* API and provider contracts
* Research and planning documentation

### 🚧 Phase 1 — Behavioural Model

Currently in progress:

* Workload Signature Specification
* Recommendation Engine design
* Knowledge Base design
* Telemetry Provider architecture
* Architecture Decision Records (ADRs)

### Future Phases

* FastAPI backend
* Provider implementations
* Signature generation engine
* Classification engine
* Recommendation engine
* Production feedback loop

---

## Repository Structure

```
.specify/      Spec-driven development workflow
specs/         MVP specifications and implementation planning
docs/
├── adr/           Architecture Decision Records
├── architecture/  Long-term system design
├── research/      Supporting research and references
└── examples/      Example telemetry, signatures and recommendations
```

---

## Design Principles

* Explainable recommendations over opaque decision making
* Behavioural workload characterization rather than benchmark reporting
* Deterministic workload signature generation
* Provider-based telemetry ingestion
* Single-application MVP before platform expansion
* Architecture-first, implementation-second

---

## Project Status

This repository currently contains the architectural foundation of AWCDE.

Implementation of the MVP has intentionally not started while the behavioural model and workload signature specification are being refined.
