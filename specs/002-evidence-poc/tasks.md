# POC tasks

These are suggested Jira entries, not synchronized issues. AWC references are placeholders. Status reflects this documentation delivery only; review is still required. No benchmark or implementation task is complete.

Epic: AWCDE Evidence backed workload characterization POC

Suggested board: Backlog → Ready → In progress → Review/Validation → Done, with a blocked flag.

## AWC-01 Define POC scope and success criteria

Suggested status: Review

Depends on: None

Review docs/research/poc-charter.md. Confirm the user, exclusions, investment budget and decision criteria.

**Acceptance:** Reviewed charter with review date and explicit acceptance; no experimental success claimed.

## AWC-02 Audit and realign the repository

Suggested status: Review

Depends on: AWC-01

Review docs/research/repository-audit.md and the migration manifest. Compare this July export against the actual current Git checkout before adopting the changes.

**Acceptance:** Audit accepted, historical files preserved, active docs and templates consistent, and differences from any newer checkout resolved.

## AWC-03 Finalize the first experiment

Suggested status: In progress

Depends on: AWC-01

Resolve every execution gate in benchmarks/experiments/EXP-001-load-response/protocol.md. Select compatible tools, evidence definitions and a pilot procedure. Freeze validation criteria after the pilot and before fresh validation runs.

**Acceptance:** Protocol reviewed; controls, load levels, repetition policy, uncertainty method, tolerances and negative controls documented. Pilot-derived decisions are versioned before validation.

## AWC-04 Establish the reference environment

Suggested status: Backlog

Depends on: AWC-03 initial protocol

Provision or select one endpoint and record hardware/model/runtime configuration. Verify streaming, token accounting and server queue telemetry.

**Acceptance:** Repeatable setup, working smoke test and accessible queue evidence; exact versions and configuration recorded.

## AWC-05 Configure equivalent workloads in two tools

Suggested status: Backlog

Depends on: AWC-02, AWC-04

Pin two tools and verify actual arrival patterns, token distributions, warmup, cache policy, retries, timeouts and measurement boundaries.

**Acceptance:** Documented mapping and raw samples; mismatches and unresolved definitions explicitly recorded.

## AWC-06 Capture baseline and validation evidence

Suggested status: Backlog

Depends on: AWC-05; AWC-03 freeze before validation

Run the pilot, finalize criteria in AWC-03, then collect independent validation repetitions across the load sweep. Preserve complete raw outputs and telemetry.

**Acceptance:** Hashed evidence bundles, protocol versions, repeat variability and coverage checks; pilot and validation runs clearly separated.

## AWC-07 Implement minimal evidence ingestion

Suggested status: Backlog

Depends on: AWC-02, AWC-06

Evaluate shared report format against actual samples. Implement only the required readers and transformations. Preserve source fields, units, definitions, missingness and context.

**Acceptance:** Two real tool outputs ingested with traceable mappings; malformed inputs and unsupported semantics produce explicit errors or limitations.

## AWC-08 Implement one explainable finding

Suggested status: Backlog

Depends on: AWC-03, AWC-07

Derive the bounded load-response finding with transparent analysis. Separate observations from queue interpretation; report uncertainty and insufficient evidence.

**Acceptance:** Readable finding cites raw sources and analysis version. Missing queue evidence cannot produce an unqualified queueing interpretation.

## AWC-09 Validate consistency and failure cases

Suggested status: Backlog

Depends on: AWC-08

Test held-out repetitions, cross-tool agreement, actual workload changes, known mismatches and removed evidence against frozen criteria.

**Acceptance:** Results, disagreements and limitations recorded; deterministic reanalysis and appropriate abstention demonstrated or failures documented.

## AWC-10 Demonstrate and make an investment decision

Suggested status: Backlog

Depends on: AWC-09

Produce a repeatable CLI/script demo and report. Compare with metrics plus manual comparability checks, recording effort and usefulness.

**Acceptance:** Proceed, pivot or stop decision with evidence and unresolved limitations. A negative result is an acceptable completion.

## Dependency note

AWC-03 has two checkpoints: an initial executable pilot plan before environment work, and final frozen validation criteria after the pilot. AWC-06 includes the pilot but cannot begin validation until that second checkpoint is recorded. This avoids selecting arbitrary tolerances before measuring variability.

## Definition of done

Link the resulting artifact or evidence, record limitations and review outcome, update affected documentation and retain failed hypotheses as results. Documentation drafts do not close experimental tasks.
