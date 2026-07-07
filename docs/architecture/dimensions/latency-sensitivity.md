# Latency Sensitivity

## Purpose

Latency Sensitivity describes the extent to which a workload depends on minimizing response latency to achieve its intended outcome.

It captures the importance of producing timely responses relative to maximizing aggregate throughput.

---

## Design Intent

Latency Sensitivity exists to separate workloads that benefit primarily from low response latency from those that benefit primarily from high aggregate throughput.

This distinction enables downstream components of AWCDE to reason about deployment trade-offs independently of any specific benchmark framework, runtime, or hardware platform.

---

## Behavioural Definition

Latency Sensitivity describes how strongly workload behaviour is affected by increases in response latency.

Workloads with high Latency Sensitivity benefit more from minimizing response latency than from maximizing aggregate throughput.

Conversely, workloads with low Latency Sensitivity are generally more tolerant of delayed execution provided that overall throughput or completion time remains acceptable.

Latency Sensitivity characterizes a behavioural preference rather than an observed performance metric.

---

## Candidate Evidence

Candidate evidence consists of observations that may contribute to the assessment of Latency Sensitivity.

No single observation is expected to determine the dimension in isolation.

Candidate evidence may include observations relating to:

- Response latency
- Latency distributions
- Queueing behaviour
- Concurrency
- Response time consistency
- Service-level objectives

---

## Behavioural Indicators

High Latency Sensitivity is commonly associated with workloads that:

- Interact directly with users.
- Require consistently low response latency to remain effective.
- Are negatively affected by queueing delays.
- Prioritize responsiveness over aggregate throughput.

Lower Latency Sensitivity is commonly associated with workloads that:

- Execute asynchronously.
- Operate in batch-oriented workflows.
- Can tolerate delayed execution.
- Prioritize throughput, utilization, or cost efficiency over immediate response.

---

## Deployment Implications

Latency Sensitivity may influence workload-aware decisions such as:

- Model family selection
- Runtime selection
- Hardware suitability
- Scheduling policy
- Batching strategy
- Concurrency configuration

The Workload Dimension itself does not generate recommendations.

Instead, it provides behavioural context that the AWCDE Knowledge Base uses when producing workload-aware decisions.

---

## Relationships

Latency Sensitivity should not be interpreted independently.

Its significance emerges only when considered alongside other Workload Dimensions, particularly:

- Throughput Orientation
- Burst Behaviour
- Context Profile
- Memory Intensity

The Knowledge Base is responsible for reasoning over these relationships when producing workload-aware decisions.

The Knowledge Base is responsible for reasoning over these relationships when producing workload-aware decisions.

As additional Workload Dimensions are introduced, these relationships may evolve to capture increasingly complex behavioural interactions.

---

## Formal Definition

The formal derivation of Latency Sensitivity is defined separately within the Behavioural Model specification.

This document defines the behavioural meaning of the dimension rather than its mathematical implementation.

---

## Examples

### Interactive Chat Assistant

**Typical Latency Sensitivity:** High

Reason: The user experience depends on quick response generation.

### Batch Embedding Job

**Typical Latency Sensitivity:** Low

Reason: Overall completion time and throughput are more important than individual request latency.

### Search or Retrieval System

**Typical Latency Sensitivity:** High

Reason: Delayed responses reduce usefulness for interactive users.

### Offline Data Processing Pipeline

**Typical Latency Sensitivity:** Low

Reason: Individual request latency has little impact provided that the workload completes within the required execution window.