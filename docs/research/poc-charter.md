# POC charter

Status: Draft for AWC-01 review. Owner: project maintainer. Date: 4 November 2026.

## Objective

Determine whether two benchmark tools support the same evidence-qualified conclusion about load response in one fixed deployment. The intended user is an engineer repeatedly interpreting inference performance experiments.

## Deliverable

A reproducible saved evidence bundle and a script or CLI that checks comparability, derives one finding, records its evidence and limitations, and abstains when the required evidence is absent. Deliver a readable report and a proceed, pivot or stop decision.

## Boundaries

One model and runtime configuration on one hardware environment; two measurement tools; multiple offered-load levels; independent repetitions; server queue evidence where available. No recommendations, API, knowledge base, UI, optimization or universal signature. See the [active specification](../../specs/002-evidence-poc/spec.md).

## Success and failure

Success requires traceability, repeatability, conditional cross-tool agreement, sensitivity to real changes and useful interpretation beyond baseline metric summaries and comparability rules. Failure includes unsupported causal labels, false certainty under missing evidence, conclusions that depend on tool identity after equivalence checks, or no added practical value.

Numeric tolerances and sampling requirements must be justified using pilot variation and metric definitions, then frozen before held-out validation. No success threshold is asserted yet.

## Investment gate

Initial budget: about ten focused engineering days. Review after baseline collection; do not automatically extend the budget. Proceed with another bounded experiment if value is demonstrated, pivot toward upstream methodology if appropriate, or stop the standalone engine.

## Review required

Confirm objective, exclusions and budget; finalize the protocol; record the review date and decision. This draft does not close AWC-01 or authorize claims of POC success.
