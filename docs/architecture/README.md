# Minimal POC architecture

Status: Provisional requirements, not implemented components.

The analysis will consume saved benchmark artifacts and server telemetry through small tool-specific readers. The unit of support is a pinned tool/version with known semantics, not a generic JSON or CSV reader.

Before any combined finding, check workload equivalence and metric definitions. Preserve the source value and unit, observation window, token-count source, exclusions and transformation method. Unknown values remain unknown. Do not equate ITL with TPOT or client timings with server timings without a documented mapping.

The evidence bundle needs run identity, protocol and analysis versions, configuration, raw artifact paths and hashes, actual load and request outcomes, telemetry coverage and known deviations. Reuse a shared benchmark schema if adequate, keeping supplementary provenance beside it when needed. No new canonical schema is committed before sample inspection.

A finding needs its bounded claim, relevant runs, cited metrics/time windows, method, assumptions, uncertainty, comparability outcome and limitations. Separate comparability (comparable, incompatible, unresolved) from inference (supported, not supported, insufficient evidence). These are provisional report terms, not calibrated probabilities.

Prefer a small local script or CLI with deterministic reanalysis of identical evidence and configuration. Numeric analysis and report formatting should remain separable. No API, persistent service, recommendation rules or database is required. Add source modules and appropriate tests only after baseline evidence identifies the needed transformations.

## Optional advisory layer (planned)

[The advisory design](llm-advisory-layer.md) adds explicit customer requirements and an LLM explanation/advice step downstream of the structured finding. The core report remains available independently. Output checks must prevent unsupported numeric claims, invalid references and upgrades of evidence status; semantic support also requires evaluation and review. No advisory implementation or provider has been selected. See [ADR-0011](../adr/0011-evidence-grounded-advisory-layer.md).
