# Related work evaluation

Status: Evaluation checklist. No integration is selected and no live compatibility check is recorded here.

Evaluate [llm-d Benchmark Report](https://github.com/llm-d/llm-d-benchmark/tree/main/benchmark-report) for reusable evidence representation; [inference-perf](https://github.com/kubernetes-sigs/inference-perf) and [issue 481](https://github.com/kubernetes-sigs/inference-perf/issues/481) for cross-tool methodology; [GuideLLM](https://github.com/vllm-project/guidellm), vLLM benchmark tooling and AIPerf as candidate measurement sources.

For each candidate pin a version and record: offered-rate semantics, actual arrival records, streaming event boundaries, token count provenance, raw export fields, warmup/failure handling, queue telemetry integration, license and execution cost. Inspect a real sample before selecting the two tools.

Record gaps against the first question. Prefer existing upstream capabilities if they suffice. The July adjacent-technologies document is historical; its broad differentiation claims are not current evidence of novelty.
