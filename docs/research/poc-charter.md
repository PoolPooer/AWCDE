# POC charter

Status: Core documentation baseline accepted through PR #15; advisory amendment proposed for review. Owner: project maintainer. Updated: 17 November 2026.

## Objective

Determine whether two benchmark tools support the same evidence-qualified conclusion about load response in one fixed deployment. The intended user is an engineer repeatedly interpreting inference performance experiments.

## Deliverable

A reproducible saved evidence bundle and a script or CLI that checks comparability, derives one finding, records its evidence and limitations, and abstains when the required evidence is absent. Deliver a readable report and a proceed, pivot or stop decision.

## Boundaries

One model and runtime configuration on one hardware environment; two measurement tools; multiple offered-load levels; independent repetitions; server queue evidence where available. The core excludes recommendations, API, knowledge base, UI, optimization or universal signature. See the [active specification](../../specs/002-evidence-poc/spec.md).

## Success and failure

Success requires traceability, repeatability, conditional cross-tool agreement, sensitivity to real changes and useful interpretation beyond baseline metric summaries and comparability rules. Failure includes unsupported causal labels, false certainty under missing evidence, conclusions that depend on tool identity after equivalence checks, or no added practical value.

Numeric tolerances and sampling requirements must be justified using pilot variation and metric definitions, then frozen before held-out validation. No success threshold is asserted yet.

## Investment gate

Initial budget: about ten focused engineering days. Review after baseline collection; do not automatically extend the budget. Proceed with another bounded experiment if value is demonstrated, pivot toward upstream methodology if appropriate, or stop the standalone engine.

## Review required

Confirm objective, exclusions and budget; finalize the protocol; record the review date and decision. PR #15 established the documentation baseline; no experimental success is claimed. The advisory amendment requires review through its PR.

## Product direction and advisory follow-on

The broader aim is explainable advice grounded in requirements and measurements. [ADR-0011](../adr/0011-evidence-grounded-advisory-layer.md) proposes an optional LLM layer to explain validated findings and suggest bounded next tests. This is a follow-on evaluation, not an additional core success criterion. It depends on core validation and a separate budget decision; the ten-day planning budget is not automatically extended. TTS and broad model/deployment selection remain future scope.
