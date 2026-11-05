# RW-001 — Interactive Chat

## Purpose

RW-001 is the first controlled reference workload used by AWCDE.

It represents a low-concurrency, user-facing chat-completion workload and is intended to be executed consistently across candidate telemetry providers.

---

## Test Configuration

| Parameter | Initial Value |
|-----------|---------------|
| Workload ID | RW-001 |
| Workload Name | Interactive Chat |
| Model | TBD |
| Model Revision | TBD |
| Runtime | vLLM |
| Runtime Version | TBD |
| Endpoint | OpenAI-compatible chat completions |
| Requests | 100 |
| Concurrency | 1 |
| Streaming | Enabled |
| Temperature | 0.0 |
| Top-p | 1.0 |
| Maximum Output Tokens | 256 |
| Seed | Fixed where supported |
| Request Timeout | 120 seconds |
| Warm-up Requests | 5 |

The final model will be selected after confirming compatibility with all candidate tools and the RTX 5090 reference environment.

---

## Reference Prompt

The canonical prompt is stored in:

```text
prompt.txt
