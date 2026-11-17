# AWCDE Constitution

Version: 3.0.0 | Originally ratified: 2026-06-24 | Revised: 2026-11-17

## Scope and precedence

This revision preserves the evidence-first core in ADR-0010 and amends the recommendation exclusion through ADR-0011 to permit a separately gated LLM advisory experiment. It supersedes v1.0.0 and the archived benchmark-to-recommendation specification. Read this file with `specs/002-evidence-poc/spec.md`. Archived documents are historical material, not active instructions.

## Principles

1. Validate one bounded inference question before expanding the architecture. A negative result is valid.
2. Separate observed measurements, inferred findings and explicit customer requirements. Retain hardware, model, runtime and protocol context.
3. Check actual workload and measurement equivalence before comparing tools. A common schema alone is insufficient.
4. Preserve source artifacts, units, metric definitions, missingness and transformation versions. Make every finding traceable and reanalysis reproducible.
5. Use transparent calculations or rules and document uncertainty. Withhold conclusions when required evidence is absent. Do not fabricate confidence scores, causality or hardware independence.
6. Reuse existing tools and schemas where they meet the demonstrated requirement. Two file formats do not count as two independent benchmark tools.
7. Keep implementation small: a local script or CLI analyzing saved evidence. Capturing server telemetry during controlled experiments is permitted; a production streaming platform is out of scope.

8. Keep the LLM advisory layer optional and downstream of structured findings. It may explain evidence, relate it to explicit requirements and propose tests, but cannot alter calculations, evidence status or uncertainty. Validate outputs and retain a plain-report fallback. Advice does not authorize execution.

## Exclusions

The core experiment excludes recommendations. A planned follow-on may evaluate bounded advice under ADR-0011; unrestricted deployment recommendations and automatic execution remain excluded. No classifiers with fixed workload categories, mandatory eight-dimensional signatures, knowledge base, API service, UI, scheduler, placement engine, autonomous actuation, production feedback loop or TTS implementation in this POC.

## Workflow and quality gates

Use specification, plan, tasks and implementation in that order. Review the protocol and freeze analysis criteria before validation runs. Pilot observations may inform thresholds but cannot also serve as independent validation. Record later protocol changes as new versions.

Validate ingestion, units, metric semantics, provenance, abstention, comparability and repeatability. Compare against simple metric summaries and explicit comparability rules. Do not build abstractions solely to satisfy historical contracts.

## Governance

Record scope changes and their rationale in an ADR and update dependent templates and specifications together. Major revisions change principles or scope; minor revisions add compatible requirements; patches clarify wording. No amendment is evidence that experiments have passed.

## Advisory gate

Design and synthetic evaluation cases may be prepared now. Real-evidence evaluation depends on validated core findings and an explicit follow-on budget decision. Freeze the evaluation rubric before held-out evaluation. Compare with the same plain report and a simple template; review factual support and uncertainty as well as usefulness, time and cost. No model/provider is selected. Record inputs, prompts, model versions/settings and outputs; exact generated wording need not be deterministic.

## Revision impact

Version 3.0.0 adds a planned advisory extension without claiming implementation or expanding the initial core budget. Updates README, architecture, specification, plan and template scope checks together. Version 2.0.0 replaced the mandatory FastAPI, signatures, classifications and recommendations pipeline. Permits experimental server telemetry capture. Updates the plan and spec template checks. Preserves the previous constitution unchanged under `archive/2026-07-14/.specify/memory/constitution.md`.
