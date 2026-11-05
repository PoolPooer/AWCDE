# Telemetry Provider Evaluation

## Purpose

This document evaluates candidate telemetry providers for use within the AWCDE MVP.

The objective is not to identify the "best" benchmarking framework, but to determine which providers expose sufficient, structured telemetry to support the generation of standardized, explainable Workload Signatures.

Provider selection should therefore be evidence-driven and aligned with the research goals of AWCDE rather than personal preference or ecosystem popularity.

---

# Evaluation Methodology

Each provider is evaluated using a common set of criteria intended to measure its suitability as a telemetry source for workload characterization.

The evaluation focuses on the quality and usefulness of the telemetry produced rather than benchmark performance.

Where possible, representative benchmark outputs should be collected and analysed alongside documentation and publicly available benchmark reports.

The purpose of this evaluation is not to compare benchmark performance between providers.

Instead, the evaluation compares each provider's ability to expose sufficiently rich, structured evidence from which standardized Workload Signatures can be derived.

---

# Evaluation Criteria

The following criteria will be used when evaluating each provider.

| Criterion | Description | Importance |
|-----------|-------------|------------|
| Structured Output | Produces machine-readable JSON, CSV or equivalent structured telemetry. | High |
| Breadth of Telemetry | Exposes sufficient metrics to support behavioural interpretation. | High |
| Behavioural Interpretability | Exposes evidence that supports inference of workload behaviour rather than simply reporting performance metrics. | High |
| Metric Consistency | Metrics are consistently defined across benchmark executions. | High |
| Repeatability | Benchmark methodology is sufficiently repeatable. | High |
| Ease of Normalization | Metrics can be mapped into a provider-independent telemetry model. | High |
| Ease of Integration | Benchmark outputs can be consumed with minimal transformation. | High |
| Community Adoption | Widely used within the AI inference community. | Medium |
| Open Source | Provider is openly available for inspection and integration. | Medium |
| Active Maintenance | Project demonstrates ongoing development and support. | Medium |
| Roadmap & Ecosystem Viability | Evidence of an active roadmap and long-term sustainability. | Medium |
| Documentation | Documentation is complete and technically accurate. | Medium |
| Public Benchmark Availability | Public benchmark results are readily available for research and validation. | Medium |

---

# Candidate Providers

The initial evaluation focuses on telemetry providers capable of producing structured AI inference benchmark telemetry suitable for workload characterization.

Primary candidates include:

- GuideLLM
- NVIDIA AIPerf
- MLPerf Inference

Secondary candidates include:

- vLLM Benchmark Suite
- Additional providers identified during research

GenAI-Perf was initially considered during early research. NVIDIA has since announced that GenAI-Perf is being phased out in favour of AIPerf. Legacy GenAI-Perf outputs may remain useful for compatibility testing, but future evaluation will focus on AIPerf.

---

# Provider Evaluation Template

## Provider

### Overview

Brief description of the provider.

---

### Primary Use Case

Examples include:

- LLM benchmarking
- GPU benchmarking
- Production benchmarking
- Research benchmarking
- Continuous benchmarking

---

### Output Formats

Supported output formats.

Examples include:

- JSON
- CSV
- Terminal output
- HTML
- Prometheus metrics

---

### Representative Metrics

Examples of telemetry exposed by the provider.

| Metric | Available | Notes |
|---------|-----------|------|
| TTFT | | |
| ITL | | |
| TPOT | | |
| Throughput | | |
| Goodput | | |
| Request Latency | | |
| Percentiles | | |
| Concurrency | | |
| Queue Metrics | | |
| GPU Utilization | | |
| CPU Utilization | | |
| Memory Usage | | |
| Energy Metrics | | |

---

### Sample Output

Reference representative benchmark output collected during evaluation.

---

### Strengths

-

---

### Limitations

-

---

### Behavioural Coverage

How well does this provider support behavioural interpretation?

Questions to consider include:

- Can latency behaviour be inferred?
- Can throughput behaviour be inferred?
- Can burst behaviour be inferred?
- Can memory intensity be inferred?
- Can hardware affinity be inferred?
- Can workload context be inferred?
- Are sufficient metrics exposed to support explainable reasoning?

---

### Normalization Assessment

How easily can provider-specific telemetry be mapped into the AWCDE normalized telemetry model?

Potential challenges:

-

---

### Suitability Assessment

| Criterion | Rating (1–5) |
|-----------|--------------|
| Structured Output | |
| Breadth of Telemetry | |
| Behavioural Interpretability | |
| Metric Consistency | |
| Repeatability | |
| Ease of Normalization | |
| Ease of Integration | |
| Community Adoption | |
| Open Source | |
| Active Maintenance | |
| Roadmap & Ecosystem Viability | |
| Documentation | |
| Public Benchmark Availability | |

---

### Overall Assessment

Summary of suitability for AWCDE.

Recommended role:

- Primary MVP provider
- Secondary provider
- Future consideration
- Not recommended

---

# Comparison Matrix

| Provider | Structured Output | Behavioural Interpretability | Public Benchmark Data | Ease of Normalization | Community Adoption | Overall Recommendation |
|-----------|------------------|------------------------------|-----------------------|----------------------|--------------------|------------------------|
| GuideLLM | | | | | | |
| NVIDIA AIPerf | | | | | | |
| MLPerf Inference | | | | | | |
| vLLM Benchmark Suite | | | | | | |

---

# Related Benchmarking Platforms

The following platforms were reviewed during the research process.

Although they are not telemetry providers for the purposes of the AWCDE MVP, they provide valuable benchmark data, benchmarking methodologies, or architectural inspiration.

---

## Artificial Analysis

### Role

Benchmark aggregation platform.

### Value to AWCDE

- Large corpus of publicly available benchmark results.
- Public API exposing structured benchmark information.
- Useful source of reference benchmark evidence.
- Demonstrates effective presentation of AI benchmark information.

### Limitations

- Aggregates benchmark results rather than generating telemetry.
- Does not expose provider-independent behavioural interpretation.
- Not intended as a telemetry ingestion source.

### Relationship to AWCDE

Artificial Analysis complements AWCDE by providing benchmark evidence that may be interpreted using the behavioural model.

---

## vLLM Performance Dashboard

### Role

Continuous benchmarking and regression tracking platform.

### Value to AWCDE

- Demonstrates repeatable benchmarking methodology.
- Publishes benchmark results over time.
- Reinforces the importance of controlled benchmark environments.
- Supports longitudinal performance analysis.
- Provides inspiration for future Workload Signature evolution.

### Limitations

- Focused on benchmark regression tracking rather than workload characterization.
- Does not generate behavioural interpretations.

### Relationship to AWCDE

The vLLM Performance Dashboard measures benchmark performance over time.

AWCDE complements this by transforming benchmark evidence into reusable workload understanding.

---

# Findings

This section summarizes the evidence gathered during evaluation.

Questions to answer include:

- Which provider exposes the richest behavioural evidence?
- Which provider produces the most structured telemetry?
- Which provider is easiest to normalize?
- Which provider offers the strongest long-term ecosystem support?
- Which provider provides the best public benchmark evidence?
- Which provider is the most appropriate primary telemetry source for the AWCDE MVP?

---

# Recommendation

Based on the evidence collected, recommend the telemetry provider(s) that should be supported during the MVP.

The recommendation should be supported by the evaluation rather than predetermined.

Where multiple providers offer complementary capabilities, the recommendation should explain how each contributes to validating the behavioural model.

---

# Future Considerations

Potential future telemetry providers include:

- OpenTelemetry / OpenInference
- Triton Model Analyzer
- Hugging Face evaluation tooling
- Additional benchmarking frameworks as the ecosystem evolves

Future versions of AWCDE may also incorporate benchmark aggregators, continuous benchmarking platforms, and community-contributed benchmark evidence to strengthen behavioural model validation.

Provider support should expand only when it strengthens the behavioural model rather than increasing implementation complexity.