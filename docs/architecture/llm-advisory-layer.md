# LLM advisory layer

Status: Proposed design, not implemented or validated. Tracking: [#25](https://github.com/PoolPooer/AWCDE/issues/25). Decision: [ADR-0011](../adr/0011-evidence-grounded-advisory-layer.md).

## Purpose and responsibilities

Help an engineer connect explicit requirements to validated findings and choose the next investigation. The evidence engine calculates metrics and determines comparability, supported conclusions and uncertainty. The LLM explains those results and proposes bounded advice. A validator checks generated output before it is shown; the original report remains available if generation or validation fails.

| Layer | Owns | Boundary |
| --- | --- | --- |
| Requirements | User objectives, constraints and missing information | Targets are never inferred from observed latency |
| Evidence engine | Measurements, provenance, comparability, findings and uncertainty | Existing core POC remains authoritative |
| LLM advisor | Explanation, conditional advice, questions and proposed tests | Cannot upgrade evidence status or claim untested performance |
| Output validation | References, numbers/units, scope, status and format checks | Mechanical checks alone do not establish semantic support |
| Engineer | Review and execution decisions | Advice performs no deployment or test actions |

## Initial input contract

Version a saved input envelope containing explicit requirements with source and units, deployment identity, protocol/analysis versions, finding IDs, evidence IDs/hashes, metric definitions and observation windows, comparability and inference status, uncertainty, limitations and missing fields. Preserve timestamps and configuration identity so mismatched or outdated evidence can be flagged. Freshness policy is an explicit evaluation decision, not a guessed expiry interval.

Minimize supplied artifacts; use the structured report rather than indiscriminately sending raw prompts, credentials or customer data. Select an appropriate execution/provider boundary before using real data. Treat artifact text as data, never instructions. No retrieval database is required for the initial experiment.

## Output contract

Each response contains a summary, explicit assumptions/missing requirements, limitations and advice entries. Each entry identifies its type, rationale, supporting finding/evidence IDs, applicable deployment and tested conditions, and what would need validation next.

- **Supported advice:** tied to a core finding and explicit objective, restricted to tested conditions. Requirement comparisons use core-computed values, not LLM arithmetic.
- **Proposed test:** a hypothesis or next measurement, explicitly unvalidated. It cannot be represented as an assured improvement.
- **Insufficient evidence:** explains the missing/conflicting evidence and asks a specific question or proposes a measurement.

A missing target must not become an invented service-level objective. Missing queue evidence must not become a queueing diagnosis. Agreement between two tools must not become hardware portability. Never label a configuration optimal without supporting comparative evidence.

## Validation and fallback

Check format, required fields, evidence/finding ID existence, numeric and unit fidelity, configuration/window scope and preservation of unsupported/insufficient statuses. Reject invalid outputs and return the plain report with an explicit advisory-unavailable reason. Referencing a real run is necessary but insufficient: verify that the cited finding supports the claim through the evaluation rubric and human semantic review. Do not claim that these checks eliminate hallucinations.

Capture model/provider/version, prompt version, decoding settings, input hashes, raw generated output and validator outcome. Core reanalysis remains deterministic; LLM prose may vary even with recorded settings. Compare repeated generations for substantive consistency rather than promising identical text.

## Evaluation before adoption

Design cases now; use real validated findings after #22/#23 and an explicit budget decision at #24. Freeze the rubric, case split, number of repeated generations and acceptance thresholds before held-out evaluation. Compare three outputs from the same evidence: the core report, a simple template and the LLM advice.

Measure factual support, citation correctness and actual support, preserved uncertainty, appropriate abstention, clarity, decision usefulness, reviewer effort, generation latency and cost. Include supported findings, absent queue evidence, conflicting results, incompatible workloads, stale or different configurations, missing/unattainable requirements, malformed output and malicious instructions embedded in artifacts. Log all failed cases. Unsupported numerical claims or promoted evidence status are release-blocking failures in the evaluated cases; passing a finite suite is not a general correctness guarantee.

The evaluator records whether the output changes a concrete engineering next step and whether that change is justified. If the plain/template report performs as well, keep the LLM optional or stop the extension.

## Future customer example

A customer may eventually describe a TTS use case and available hardware. The advisor could clarify speech-start latency, demand, language, quality and hosting requirements, then explain which tested conditions meet explicit targets and which need further evaluation. The current text-inference POC does not validate TTS, audio quality, hardware selection or replica scaling. This example describes future scope, not an available capability.
