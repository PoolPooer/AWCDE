# ADR-0011: Evidence-grounded LLM advisory layer

Date: 17 November 2026
Status: Proposed for review; project direction requested by the maintainer, implementation not started.
Amends: ADR-0010 recommendation exclusion only for the gated extension below.

## Context

The core POC asks whether equivalent benchmark experiments support a repeatable bounded finding. Engineers also need to relate that finding to explicit requirements and decide what to test next. A structured report alone may leave this interpretation work to the reader. An LLM layer is a hypothesis for improving usefulness, not evidence that recommendations are trustworthy.

## Decision

Preserve the independent evidence engine and plain report. Plan an optional downstream LLM layer that accepts structured findings and customer requirements, explains the evidence, offers advice within tested conditions and proposes further tests. Calculations, comparability, inference status and uncertainty remain owned by the core. The LLM cannot create measurements, upgrade evidence or treat a proposed configuration as validated.

Design and synthetic cases may start now. Evaluation with real evidence follows core validation (#22/#23) and a separate budget decision at #24. Track the extension in #25. Keep the original core experiment and approximately ten-day initial budget intact.

## Boundaries

No autonomous deployment, benchmark execution, model selection catalogue, API/UI, knowledge base or retrieval infrastructure is required. TTS remains an illustrative future use case. No model/provider is selected. Advice is presented for engineer review, and missing requirements or evidence must lead to clarification or abstention.

## Acceptance and consequences

Use the [advisory contract and evaluation plan](../architecture/llm-advisory-layer.md). Compare with the same structured report and a simple template, freeze the rubric before held-out evaluation, and record semantic review as well as mechanical checks. If unsupported claims persist or usefulness does not improve, retain the core and stop or revise the wrapper. This introduces model/version variability and evaluation effort; it does not establish product differentiation by itself.

Constitution v3.0.0 reflects this scope change. ADR-0010 remains the historical decision for the core; the archived pipeline and PR #14 are not reinstated.
