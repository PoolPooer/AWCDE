# POC tasks

GitHub issues are the live source of delivery status: [tracker #16](https://github.com/PoolPooer/AWCDE/issues/16). AWC references below are retained planning aliases, not Jira tickets. PR #15 established the documentation baseline; no benchmark or implementation completion is claimed here.

| Planning alias | GitHub work |
| --- | --- |
| AWC-01–02 | Documentation baseline merged in PR #15 |
| AWC-03 | [#17](https://github.com/PoolPooer/AWCDE/issues/17) |
| AWC-04 | [#18](https://github.com/PoolPooer/AWCDE/issues/18) |
| AWC-05 | [#19](https://github.com/PoolPooer/AWCDE/issues/19) |
| AWC-06 | [#20](https://github.com/PoolPooer/AWCDE/issues/20) |
| AWC-07 | [#21](https://github.com/PoolPooer/AWCDE/issues/21) |
| AWC-08 | [#22](https://github.com/PoolPooer/AWCDE/issues/22) |
| AWC-09 | [#23](https://github.com/PoolPooer/AWCDE/issues/23) |
| AWC-10 | [#24](https://github.com/PoolPooer/AWCDE/issues/24) |
| Advisory follow-on | [#25](https://github.com/PoolPooer/AWCDE/issues/25) |

Epic: AWCDE Evidence backed workload characterization POC

GitHub issue dependencies and acceptance checklists define execution order; a Project board is optional.

## AWC-01 Define POC scope and success criteria

Baseline documentation reviewed in PR #15; experimental criteria remain unvalidated.

Depends on: None

Review docs/research/poc-charter.md. Confirm the user, exclusions, investment budget and decision criteria.

**Acceptance:** Reviewed charter with review date and explicit acceptance; no experimental success claimed.

## AWC-02 Audit and realign the repository

Baseline documentation reviewed in PR #15; experimental criteria remain unvalidated.

Depends on: AWC-01

Review docs/research/repository-audit.md and the migration manifest. Compare this July export against the actual current Git checkout before adopting the changes.

**Acceptance:** Audit accepted, historical files preserved, active docs and templates consistent, and differences from any newer checkout resolved.

## AWC-03 Finalize the first experiment

Live status: see #17.

Depends on: AWC-01

Resolve every execution gate in benchmarks/experiments/EXP-001-load-response/protocol.md. Select compatible tools, evidence definitions and a pilot procedure. Freeze validation criteria after the pilot and before fresh validation runs.

**Acceptance:** Protocol reviewed; controls, load levels, repetition policy, uncertainty method, tolerances and negative controls documented. Pilot-derived decisions are versioned before validation.

## AWC-04 Establish the reference environment

Live status: see linked GitHub issue.

Depends on: AWC-03 initial protocol

Provision or select one endpoint and record hardware/model/runtime configuration. Verify streaming, token accounting and server queue telemetry.

**Acceptance:** Repeatable setup, working smoke test and accessible queue evidence; exact versions and configuration recorded.

## AWC-05 Configure equivalent workloads in two tools

Live status: see linked GitHub issue.

Depends on: AWC-02, AWC-04

Pin two tools and verify actual arrival patterns, token distributions, warmup, cache policy, retries, timeouts and measurement boundaries.

**Acceptance:** Documented mapping and raw samples; mismatches and unresolved definitions explicitly recorded.

## AWC-06 Capture baseline and validation evidence

Live status: see linked GitHub issue.

Depends on: AWC-05; AWC-03 freeze before validation

Run the pilot, finalize criteria in AWC-03, then collect independent validation repetitions across the load sweep. Preserve complete raw outputs and telemetry.

**Acceptance:** Hashed evidence bundles, protocol versions, repeat variability and coverage checks; pilot and validation runs clearly separated.

## AWC-07 Implement minimal evidence ingestion

Live status: see linked GitHub issue.

Depends on: AWC-02, AWC-06

Evaluate shared report format against actual samples. Implement only the required readers and transformations. Preserve source fields, units, definitions, missingness and context.

**Acceptance:** Two real tool outputs ingested with traceable mappings; malformed inputs and unsupported semantics produce explicit errors or limitations.

## AWC-08 Implement one explainable finding

Live status: see linked GitHub issue.

Depends on: AWC-03, AWC-07

Derive the bounded load-response finding with transparent analysis. Separate observations from queue interpretation; report uncertainty and insufficient evidence.

**Acceptance:** Readable finding cites raw sources and analysis version. Missing queue evidence cannot produce an unqualified queueing interpretation.

## AWC-09 Validate consistency and failure cases

Live status: see linked GitHub issue.

Depends on: AWC-08

Test held-out repetitions, cross-tool agreement, actual workload changes, known mismatches and removed evidence against frozen criteria.

**Acceptance:** Results, disagreements and limitations recorded; deterministic reanalysis and appropriate abstention demonstrated or failures documented.

## AWC-10 Demonstrate and make an investment decision

Live status: see linked GitHub issue.

Depends on: AWC-09

Produce a repeatable CLI/script demo and report. Compare with metrics plus manual comparability checks, recording effort and usefulness.

**Acceptance:** Proceed, pivot or stop decision with evidence and unresolved limitations. A negative result is an acceptable completion.

## Dependency note

AWC-03 has two checkpoints: an initial executable pilot plan before environment work, and final frozen validation criteria after the pilot. AWC-06 includes the pilot but cannot begin validation until that second checkpoint is recorded. This avoids selecting arbitrary tolerances before measuring variability.

## Definition of done

Link the resulting artifact or evidence, record limitations and review outcome, update affected documentation and retain failed hypotheses as results. Documentation drafts do not close experimental tasks.

## Advisory follow-on (#25)

Design the contract and synthetic failure cases now. Real-evidence evaluation depends on #22/#23 and a separate budget decision at #24. Compare explanations and bounded advice with the same plain report and a simple template; preserve uncertainty, validate support and abstain when evidence is insufficient. See [the advisory design](../../docs/architecture/llm-advisory-layer.md). No automatic expansion of the core budget or execution privileges is implied.
