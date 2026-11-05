# ADR 0010 Evidence first POC

Status: Adopted for repository realignment on 4 November 2026. Experimental protocol remains draft.

## Context

The July constitution and MVP contracts require a FastAPI application, eight signature dimensions, classifications and recommendations. The research documents leave evidence interpretation unresolved. The uploaded snapshot contains no engine implementation or measured benchmark outputs. ADR files 0001–0009 are identical unfilled templates, not accepted decisions.

## Decision

Use a bounded two-tool experiment on a fixed text inference deployment. Collect relevant server telemetry, preserve evidence and test one conditional behavioural finding before expanding scope. Begin with saved files and a script or CLI. Reuse existing benchmark representations where possible.

Archive the original snapshot unchanged. The active specification is `002-evidence-poc`; constitution v2.0.0 governs current work. Retain 0001–0009 only in the archive and use 0010 to avoid confusing old filenames with new decisions.

## Alternatives

Continuing the API and recommendation pipeline would encode unvalidated assumptions. Archiving the project immediately would avoid investment but leave the bounded question untested. A short experiment with a decision checkpoint limits that investment.

## Consequences

The repo is a POC plan, not an implemented product. Hardware, model, two tools and tolerances still need selection. No hardware transfer claim is made. Upstream contribution or stopping are acceptable outcomes. Historical quickstarts and contracts must not drive new implementation.
