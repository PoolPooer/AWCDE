# Workload Dimensions

## Purpose

Workload Dimensions define the behavioural characteristics used to describe an AI inference workload.

Each dimension captures a different aspect of workload behaviour that may influence workload-aware decisions.

Workload Dimensions are independent of any benchmark framework or inference runtime. They describe behaviour rather than implementation.

The mathematical derivation of each dimension is defined separately.

---
## Design Philosophy

Rather than representing an AI inference workload as a single score or classification, AWCDE models workload behaviour across multiple independent dimensions.

Each dimension captures a different aspect of workload behaviour that may influence infrastructure decisions.

Together, these dimensions describe the behavioural profile that is captured within a Workload Signature.

---

## Behaviour versus Measurement

Workload Dimensions describe behavioural characteristics rather than individual performance metrics.

Raw telemetry captures **what was measured**.

Workload Dimensions capture **what those measurements imply about how a workload behaves**.

This separation allows deployment decisions to be based on behavioural understanding rather than isolated benchmark results, while preserving the underlying telemetry for users who require detailed analysis.

Behavioural understanding therefore becomes a reusable asset, while telemetry remains the underlying source of evidence.

---

## Characteristics of a Workload Dimension

Every Workload Dimension should:

- Describe one independent aspect of workload behaviour.
- Be derived from observable evidence.
- Be deterministic and reproducible.
- Be explainable.
- Influence one or more deployment decisions.
- Be independent of any specific benchmark framework.

---

## Behavioural Dimensions

The current behavioural model consists of the following dimensions:

- Latency Sensitivity
- Throughput Orientation
- Memory Intensity
- Context Profile
- Burst Behaviour
- Hardware Affinity
- Modality

These dimensions are intended to be largely independent, although relationships between dimensions may exist. Collectively they describe workload behaviour from the perspective of infrastructure decision making.

No single Workload Dimension is intended to fully characterize a workload.

Only the combination of multiple dimensions provides sufficient behavioural context for informed workload-aware decision making.

---

## Relationship to Workload Signatures

Workload Dimensions do not exist independently.

Each dimension describes one aspect of workload behaviour.

Together, these dimensions describe the behavioural profile captured within a Workload Signature.

A Workload Signature combines:

- Behavioural Dimensions
- Metadata
- Supporting Evidence
- Versioning Information

The Workload Signature therefore represents the workload as a whole, while individual dimensions describe specific aspects of its behaviour.

---

## Evolution

The behavioural model is expected to evolve as additional workload patterns are identified.

New dimensions may be introduced in future schema versions provided they:

- represent independent workload behaviour
- can be derived from observable evidence
- improve deployment recommendations
- remain compatible with previous Workload Signature versions

Existing dimensions should remain stable wherever possible to preserve comparability between Workload Signature schema versions.

---

# Latency Sensitivity

## Purpose

Latency Sensitivity describes the extent to which a workload depends on minimizing response latency to achieve its intended outcome.

It represents the importance of producing results quickly rather than maximizing overall system throughput.

---

## Why it Matters

Latency-sensitive workloads often require different deployment strategies than throughput-oriented workloads.

For example, they may benefit from:

- Lower queue depths
- Lower request concurrency
- Faster inference runtimes
- Higher-performance hardware
- Reduced scheduling latency

Understanding latency sensitivity enables AWCDE to recommend infrastructure optimized for responsiveness rather than overall utilization.

---

## Behaviour

A latency-sensitive workload typically exhibits one or more of the following characteristics:

- Interactive or user-facing requests
- Small batches of independent requests
- Consistent low-latency response requirements
- Sensitivity to queueing delays
- Preference for predictable latency over maximum throughput

Examples include:

- Chat assistants
- Interactive coding assistants
- Search
- Customer support agents
- Voice assistants

---

## Candidate Evidence

Latency Sensitivity may be inferred from observations such as:

- Response latency
- Latency distributions (P50/P95/P99)
- Queue depth
- Queue wait time
- Request concurrency
- Response time variance
- Service-level objectives (where available)

The precise derivation of Latency Sensitivity from candidate evidence is defined separately within the Behavioural Model specification.

This document defines **what** Latency Sensitivity represents rather than **how** it is calculated.

---

## Deployment Impact

Latency Sensitivity may influence workload-aware decisions including:

- Model family selection
- Runtime selection
- Hardware suitability
- Scheduling policy
- Request batching strategy
- Concurrency configuration

These workload-aware decisions are generated by the AWCDE Knowledge Base rather than by the Workload Dimension itself.

---

## Relationships

Latency Sensitivity is complementary to, but distinct from:

- Throughput Orientation
- Burst Behaviour
- Concurrency Behaviour

No individual Workload Dimension should be interpreted in isolation.

Deployment recommendations are expected to consider multiple behavioural dimensions simultaneously.

The relationships between dimensions are defined by the Knowledge Base rather than by the dimensions themselves.

---


