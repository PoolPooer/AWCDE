# AWCDE

**Adaptive Workload Characterization and Deployment Engine**

AWCDE is a research project investigating whether measurements from different AI inference benchmark tools can support consistent, evidence-backed conclusions about workload behaviour.

The intended users are platform and performance engineers who need to understand what benchmark results justify concluding, what evidence supports the interpretation, and what needs further testing.

**Status: POC planning.** This repository contains specifications, research planning and workflow tooling. The active POC has no implemented analysis engine or completed benchmark evidence. The earlier implementation in [PR #14](https://github.com/PoolPooer/AWCDE/pull/14) remains separate and is not incorporated here. Signatures, deployment recommendations and hardware-independent behaviour are not validated capabilities.

Updated: 5 November 2026.

## Start here

1. Read the [POC charter](docs/research/poc-charter.md).
2. Review the [repository audit](docs/research/repository-audit.md) and [scope decision](docs/adr/0010-evidence-first-poc.md).
3. Finalize the [experiment protocol](benchmarks/experiments/EXP-001-load-response/protocol.md), including the environment and two benchmark tools.
4. Track delivery using the [POC tasks](specs/002-evidence-poc/tasks.md). AWC-01–10 are planning references, not assigned Jira keys.

## The question

> Within a fixed deployment, does increasing offered request rate produce a reproducible rise in latency associated with server-side queueing, and do two benchmark tools support the same conclusion?

Agreement across tools under matched conditions does not establish transfer across hardware or runtimes. Queueing-related observations do not establish a hardware bottleneck or prove causality.

## Scope

The POC uses one fixed text inference endpoint, two benchmark tools, repeated offered-load sweeps and relevant server telemetry. It will preserve raw evidence, check comparability and produce one traceable finding through a script or CLI. It must be able to report that evidence is insufficient.

Model selection, quality evaluation, deployment recommendations, scheduling, optimization, knowledge bases, API services, UIs and production feedback loops are excluded. TTS remains a possible later application after the measurement and interpretation foundations are validated.

## Proposed workflow

Specify an experiment, collect evidence with existing tools, check workload and measurement equivalence, represent the evidence, derive a bounded finding, then validate it against repeat runs, failure cases and simpler baselines.

A shared schema does not make measurements equivalent. Reuse existing formats where suitable; define new abstractions only for demonstrated gaps. See the [minimal architecture](docs/architecture/README.md).

## Workload signatures and future value

A Workload Signature remains a candidate concept. The POC first tests one finding with explicit environment context, uncertainty and source references. It does not require eight dimensions or numeric confidence scores.

Longer term, this could help engineers establish the demand and conditions under which a deployment meets customer requirements. Requirements such as acceptable speech-start latency are explicit inputs, not properties inferred from telemetry. This is a potential application, not a current feature.

## Milestones

| Milestone | Planning references | Exit evidence |
| --- | --- | --- |
| Scope agreed | AWC-01–03 | Reviewed charter, audit and frozen experiment protocol. |
| Evidence collected | AWC-04–06 | Reproducible environment and sufficiently comparable repeat runs. |
| Finding demonstrated | AWC-07–09 | Traceable analysis, cross-tool validation and appropriate abstention. |
| Investment decision | AWC-10 | Demo, baseline comparison and proceed, pivot or stop decision. |

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
