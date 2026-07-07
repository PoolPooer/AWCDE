# AWCDE

**Adaptive Workload Characterization and Deployment Engine**

AWCDE is an open research project that transforms AI inference telemetry into standardized, explainable workload intelligence.

Rather than requiring developers to manually interpret benchmark reports, runtime metrics, and performance dashboards, AWCDE ingests telemetry from existing AI benchmarking tools, normalizes heterogeneous metrics into a common behavioural model, and produces simplified workload signatures that describe how an inference workload behaves.

These workload signatures provide an explainable foundation for workload-aware guidance, helping developers understand benchmark results and make informed decisions about model selection, runtime configuration, hardware suitability, and deployment strategy.

---

# Vision

```
Benchmark Results
        │
        ▼
Telemetry Normalization
        │
        ▼
Behavioural Interpretation
        │
        ▼
Workload Signature
        │
        ▼
Knowledge Base
        │
        ▼
Workload-aware Guidance
```

The long-term vision extends this pipeline with runtime telemetry, production observability, and continuous feedback, allowing workload guidance to improve as systems evolve over time.

---

# Problem Statement

Modern AI benchmarking tools expose large volumes of valuable telemetry, but interpreting those results often requires specialist knowledge of inference systems.

Metrics such as Time to First Token (TTFT), Throughput, Inter-Token Latency (ITL), and latency percentiles provide important insight into workload behaviour, yet they rarely explain what those metrics imply for real-world deployment decisions.

AWCDE addresses this problem by standardizing the interpretation of AI inference telemetry rather than replacing existing benchmarking tools. It provides a common behavioural model that transforms complex benchmark results into explainable workload intelligence while preserving access to the original telemetry.

---

# Current Status

## ✅ Phase 0 — Architecture & Specification

Completed:

- Repository initialization
- Project governance
- Spec Kit integration
- Project constitution
- MVP specification
- Core architecture
- Data model
- API and provider contracts
- Research and planning documentation

## 🚧 Phase 1 — Behavioural Model

Currently in progress:

- Workload Signature specification
- Workload Dimension definitions
- Behavioural model
- Telemetry normalization model
- Knowledge Base architecture
- Provider architecture
- Architecture Decision Records (ADRs)

## Future Phases

- Telemetry provider implementations
- FastAPI backend
- Signature generation engine
- Knowledge Base implementation
- Guidance engine
- Runtime telemetry support
- Production feedback loop

---

# Repository Structure

```
.specify/      Spec-driven development workflow
specs/         MVP specifications and implementation planning
docs/
├── adr/           Architecture Decision Records
├── architecture/  System architecture and behavioural model
├── research/      Research, surveys and ecosystem analysis
└── examples/      Example telemetry, signatures and recommendations
```

---

# Design Principles

- Standardize interpretation rather than reinvent benchmarking.
- Explain workload behaviour rather than expose raw metrics.
- Preserve traceability from guidance back to original telemetry.
- Keep Workload Signatures deterministic, explainable, and reproducible.
- Support multiple benchmarking and telemetry providers through a common abstraction.
- Build an architecture-first MVP before expanding into a distributed platform.

---

# Project Status

AWCDE is currently focused on establishing the architectural and behavioural foundations of the platform.

The initial MVP will support structured benchmark results from existing AI benchmarking tools before expanding into live runtime telemetry and production observability.

Implementation intentionally follows architecture to ensure that the behavioural model remains provider-independent, explainable, and extensible.