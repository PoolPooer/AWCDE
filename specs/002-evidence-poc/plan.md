# POC delivery plan

Status: Draft; no implementation started.

1. Use the reviewed documentation baseline merged in PR #15; track execution in GitHub #16.
2. Select the environment and two tools against the protocol. Validate queue instrumentation and semantic mappings.
3. Run a pilot to establish feasible offered-load levels, collection coverage and repeat variability. Freeze the protocol and criteria before fresh validation runs.
4. Collect baseline evidence, then implement only the needed parsing, comparability checks and analysis. Keep raw evidence immutable and derived outputs separate.
5. Validate failure cases and conditional agreement; compare against simple baselines and record the investment decision.

## Technical decisions still open

Wetlab is the selected starting platform, pending verification of its exact configuration and isolation. Model, runtime version, two benchmark tools, exact commands, export format, sample size, tolerances and uncertainty method are unselected. The initial analysis interface is a local script or CLI. No framework or database dependency is required at this stage.

## Constitution check

- Evidence-first scope and one bounded claim.
- Environment context and measurement semantics retained.
- Unknowns and abstention supported.
- Saved-file analysis with experimental server telemetry allowed.
- No API, knowledge base or fixed signature dimensions in the core; advisory work follows ADR-0011 and a separate gate.

Review these checks when implementation is proposed; they are design constraints, not completed tests.

## Follow-on: LLM advisory evaluation

Track #25. Design the requirements/finding/advice contract and synthetic failure cases now. After #22/#23 provide validated findings, #24 records whether to fund a bounded advisory evaluation. Compare against the same report and a simple template using a frozen rubric. Preserve the plain report as a standalone result if the LLM adds no value. The initial core budget is unchanged, and no model, SDK, provider, UI or external service is selected.
