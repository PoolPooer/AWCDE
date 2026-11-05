# Reference Workloads

## Purpose

This document defines the reference workloads used to evaluate telemetry providers and validate the AWCDE behavioural model.

Reference workloads provide controlled, repeatable scenarios that can be executed across multiple benchmarking tools while keeping the model, runtime, hardware, prompts, and generation parameters consistent.

AWCDE is not intended to become a benchmarking framework. These workloads exist solely to provide consistent evidence for telemetry normalization, behavioural interpretation, and Workload Signature validation.

---

## Design Principles

Reference workloads should:

- Represent recognizable AI inference use cases.
- Remain small enough to execute repeatedly.
- Use fixed and documented parameters.
- Be reproducible across supported telemetry providers.
- Minimize provider-specific behaviour.
- Preserve all raw benchmark artifacts.
- Record the software and hardware environment used for each run.

---

## Workload Catalogue

| ID | Workload | Primary Behaviour | Status |
|----|----------|-------------------|--------|
| RW-001 | Interactive Chat | Low-concurrency interactive generation | Active |
| RW-002 | Code Assistant | Interactive generation with longer output | Future |
| RW-003 | Batch Summarization | Throughput-oriented batch processing | Future |
| RW-004 | Long Context Analysis | Context and memory-intensive generation | Future |
| RW-005 | RAG Question Answering | Mixed latency and context behaviour | Future |

---

## RW-001 — Interactive Chat

### Objective

Represent a straightforward interactive chat-completion workload that can be reproduced across GuideLLM, NVIDIA AIPerf, MLPerf-compatible tooling, and the vLLM benchmark suite.

The workload is intended to expose telemetry related to:

- Time to First Token
- Inter-token latency
- Time per output token
- End-to-end request latency
- Output throughput
- Request throughput
- Latency distributions
- Request success and failure rates

### Intended Behaviour

RW-001 represents:

- A user-facing interaction
- Low request concurrency
- Streaming text generation
- A moderate output length
- Greater emphasis on responsiveness than aggregate throughput

The expected behavioural interpretation is a latency-sensitive interactive workload.

This expectation is a research hypothesis and must be validated against the collected telemetry.

---

## Controlled Variables

The following should remain constant when comparing telemetry providers:

- Host hardware
- Operating system and WSL environment
- NVIDIA driver and CUDA versions
- Model and model revision
- Inference runtime and runtime version
- Prompt dataset
- Number of requests
- Input and output token targets
- Concurrency
- Sampling configuration
- Streaming configuration

Any unavoidable provider-specific differences must be recorded with the benchmark evidence.

---

## Evidence Collection

Each provider directory should contain:

- Raw structured output
- Terminal logs
- Benchmark command
- Provider version
- Runtime version
- Start and completion timestamps
- Any provider-specific configuration
- Notes describing warnings, failures, or deviations

Benchmark results should not be manually modified.

Derived or normalized artifacts must be stored separately from the original provider output.

---

## Initial Providers

RW-001 will initially be evaluated using:

- GuideLLM
- NVIDIA AIPerf
- vLLM benchmark tooling
- MLPerf Inference, where practical

The provider evaluation may conclude that some tools are unsuitable for the MVP.

---

## Future Evolution

Additional workloads should only be introduced when they provide behavioural evidence not adequately represented by the existing catalogue.

The initial priority is to validate one complete and reproducible workload across the selected telemetry providers.
