# Repository audit and realignment

Date: 4 November 2026. Scope: uploaded AWCDE-main.zip, export dated 14 July 2026, identifying commit de0fd6a93a0a9e017c7643c5bac12fbaffc8bd6e. On 5 November 2026, public main was verified at the same commit. PR #14 was inspected separately at d0720581bf0440128dc17f88e1b72642446a483b and remains outside this change.

## Findings

| Area | Observed condition | Action |
| --- | --- | --- |
| Source and tests | No application package, dependency manifest, engine code or application tests in the export. Shell and PowerShell files are workflow tooling. | Report planning status; do not claim an existing backend was refactored or tested. |
| Constitution | v1.0.0 requires recommendation logic and reusable signatures and excludes live telemetry without distinguishing experimental capture. | Replace with v2.0.0 bounded POC principles; permit experimental capture and saved-file analysis. |
| MVP specification | REST endpoints, eight required dimensions, classifications and five recommendation categories are specified before validation. | Archive specification 001; introduce specification 002 with conditional findings and abstention. |
| Architecture | Strong platform independence claims and a lifecycle ending in recommendations. | Archive unchanged; write minimal provisional evidence requirements. |
| ADRs | Files 0001–0009 each contain the same unfilled ADR-0000 template. | Preserve as historical placeholders; add substantive ADR-0010. |
| Reference workload | RW-001 specifies concurrency one and 100 requests; prompt.txt is referenced but absent; README has an unclosed code fence. | Archive unchanged; replace active workload plan with a load sweep protocol. |
| Reference environment | RTX 5090/WSL2 is proposed with several TBD fields; metadata includes an unverified Threadripper description. | Record current environment as unselected; require verified inventory. |
| Examples | An index describes reference implementations, but no measured example artifacts are supplied. | Add an explicitly blank finding report template. |
| Spec Kit | Plan/spec templates enforce the superseded scope; context configuration targets an absent ignored Cursor file. | Update scope checks; target tracked AGENTS.md. Preserve other workflow tooling. |
| Execution evidence | No completed benchmark runs or measured validation results in the export. | Keep all experimental acceptance checks pending. |

## Preserved work

All 75 original files are retained byte-for-byte under archive/2026-07-14/, with original-sha256.json. This preserves both useful research questions and obsolete assumptions without making them active instructions. No source implementation existed to migrate. The active .specify scripts and generic scaffolding are retained; the two project-specific templates, constitution and context target are updated.

## Active deliverables

A concise README, constitution, scope ADR, charter, experiment protocol, run metadata aid, minimal architecture, report template, environment/related-work evaluation notes, new specification, plan, quickstart, checklist and Jira-ready tasks. The full path-level change inventory is in migration-manifest.json.

## Remaining work

Review the charter and this audit, compare against the current Git checkout, select hardware and two tools, resolve the protocol, then collect evidence. No dependency installation, benchmark execution, application test run or live upstream compatibility check was performed. Retained Bash scripts receive syntax checks and the prerequisite checker is exercised on the active feature branch; full Spec Kit/Cursor integration remains unverified.

The related-work links are candidates from the project discussion, not newly validated integration commitments. Numeric criteria are intentionally unresolved until pilot evidence supports them.

## Existing implementation PR

[PR #14](https://github.com/PoolPooer/AWCDE/pull/14) adds the previous FastAPI/signature/classification/recommendation pipeline and tests. Its fixed scoring heuristics and averaging of per-record percentiles do not establish the current POC hypothesis. Validation/error-handling and testing patterns may be selectively reusable after examining real benchmark outputs. It is left unchanged; no merge, closure or test-result claim is made here. The absence of application code above refers to the uploaded main snapshot, not all branches.
