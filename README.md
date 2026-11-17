# AWCDE

**Adaptive Workload Characterization and Deployment Engine**

AWCDE aims to turn AI workload requirements and benchmark evidence into explainable deployment advice, with a clear account of what has been tested and what remains uncertain.

The research foundation tests whether measurements from different inference benchmark tools support consistent, evidence-backed findings. A planned LLM advisory layer will explain those findings, relate them to explicit customer requirements and propose next tests. Neither layer is implemented or validated yet.

The intended users are platform and performance engineers who need to understand what benchmark results justify concluding, what evidence supports the interpretation, and what needs further testing.

**Status: POC planning.** This repository contains specifications, research planning and workflow tooling. The active POC has no implemented analysis engine or completed benchmark evidence. The earlier implementation in [PR #14](https://github.com/PoolPooer/AWCDE/pull/14) remains separate and is not incorporated here. Signatures, deployment recommendations and hardware-independent behaviour are not validated capabilities.

Updated: 17 November 2026.

## Start here

1. Read the [POC charter](docs/research/poc-charter.md).
2. Review the [repository audit](docs/research/repository-audit.md) and [scope decision](docs/adr/0010-evidence-first-poc.md).
3. Finalize the [experiment protocol](benchmarks/experiments/EXP-001-load-response/protocol.md), including the environment and two benchmark tools.
4. Track delivery in [GitHub tracker #16](https://github.com/PoolPooer/AWCDE/issues/16) and the [task mapping](specs/002-evidence-poc/tasks.md).
5. Review the planned [LLM advisory layer](docs/architecture/llm-advisory-layer.md) and [scope amendment](docs/adr/0011-evidence-grounded-advisory-layer.md).

## The question

> Within a fixed deployment, does increasing offered request rate produce a reproducible rise in latency associated with server-side queueing, and do two benchmark tools support the same conclusion?

Agreement across tools under matched conditions does not establish transfer across hardware or runtimes. Queueing-related observations do not establish a hardware bottleneck or prove causality.

## Scope

The POC uses one fixed text inference endpoint, two benchmark tools, repeated offered-load sweeps and relevant server telemetry. It will preserve raw evidence, check comparability and produce one traceable finding through a script or CLI. It must be able to report that evidence is insufficient.

The core experiment excludes model selection, quality evaluation, deployment recommendations, scheduling, optimization, knowledge bases, API services, UIs and production feedback loops. A separately gated follow-on evaluates evidence-grounded explanations, bounded advice and suggested next tests; it does not execute changes. TTS remains a possible later application after the measurement and interpretation foundations are validated.

## Proposed workflow

Specify an experiment, collect evidence with existing tools, check workload and measurement equivalence, represent the evidence, derive a bounded finding, then validate it against repeat runs, failure cases and simpler baselines.

A shared schema does not make measurements equivalent. Reuse existing formats where suitable; define new abstractions only for demonstrated gaps. See the [minimal architecture](docs/architecture/README.md).

## Planned LLM advisory layer

The evidence engine owns measurements, calculations, comparability checks and evidence status. The LLM consumes a structured finding plus explicit requirements; it must preserve limitations and cite supporting evidence. Supported advice, proposed tests and insufficient evidence are distinct outputs. Unknown requirements prompt clarification, and unsupported or invalid output falls back to the plain report.

The first evaluation compares the advisory output with the same structured report and a simple template. We will measure factual support, preserved uncertainty, decision usefulness, time, latency and cost. An LLM wrapper is useful only if this comparison demonstrates added value. See [issue #25](https://github.com/PoolPooer/AWCDE/issues/25).

## Workload signatures and future value

A Workload Signature remains a candidate concept. The POC first tests one finding with explicit environment context, uncertainty and source references. It does not require eight dimensions or numeric confidence scores.

Longer term, this could help engineers establish the demand and conditions under which a deployment meets customer requirements. Requirements such as acceptable speech-start latency are explicit inputs, not properties inferred from telemetry. This is a potential application, not a current feature.

## Milestones

| Milestone | Planning references | Exit evidence |
| --- | --- | --- |
| Scope agreed | AWC-01–03 | Reviewed charter, audit and frozen experiment protocol. |
| Evidence collected | AWC-04–06 | Reproducible environment and sufficiently comparable repeat runs. |
| Finding demonstrated | AWC-07–09 | Traceable analysis, cross-tool validation and appropriate abstention. |
| Investment decision | AWC-10 / #24 | Demo, baseline comparison and proceed, pivot or stop decision. |
| Advisory evaluation (follow-on) | #25 | Grounded advice evaluated against plain and template reports; separate budget decision. |

Allow approximately ten focused engineering days initially, with a checkpoint after baseline collection. This is a planning budget, not a promised completion date. Negative results are valid research outcomes.

## Repository map

| Location | Purpose |
| --- | --- |
| `.specify/memory/constitution.md` | Current POC principles and scope boundaries. |
| `.specify/` | Retained Spec Kit tooling and revised planning templates. |
| `specs/002-evidence-poc/` | Active specification, plan, tasks and validation checklist. |
| `docs/adr/` | Current scope decision and decision template. |
| `docs/research/` | Charter, audit, environment selection and related-work evaluation. |
| `docs/architecture/` | Provisional evidence and finding requirements. |
| `docs/examples/` | Clearly labelled report template; no measured findings. |
| `benchmarks/experiments/EXP-001-load-response/` | Draft protocol and run metadata template. |
| `archive/2026-07-14/` | Unchanged original snapshot, excluded from active planning. |

## Getting started

There is no application installation or benchmark execution command yet. Start with the [planning guide](specs/002-evidence-poc/quickstart.md). Record runnable commands only after tool versions, model and hardware are selected and tested.

## Decision criteria

Proceed only if the finding is repeatable, consistent across equivalent tools, sensitive to real changes, traceable and useful beyond metric summaries and comparability checks. Pivot upstream if the main value is evidence quality or methodology. Stop the standalone engine if it duplicates existing work or adds no practical interpretation.

## Working principles

Preserve evidence and measurement definitions. Keep observations, interpretations and customer objectives separate. Record unknowns without substituting defaults. Prefer transparent analysis and explicit limitations. Let experimental results determine the next implementation step.
