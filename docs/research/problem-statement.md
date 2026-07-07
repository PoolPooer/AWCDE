# Problem Statement

## Background

Modern AI benchmarking and observability tools generate large volumes of AI inference telemetry.

Benchmarking frameworks such as GuideLLM and NVIDIA GenAI-Perf expose detailed performance metrics including latency, throughput, concurrency, request characteristics, and resource utilization. Runtime and production monitoring systems provide additional operational insight throughout the lifecycle of an AI application.

Collectively, these tools provide a comprehensive view of workload performance.

---

## The Problem

Although AI inference telemetry is increasingly available, interpreting it remains a specialist task.

Developers are expected to understand dozens of performance metrics—including concepts such as Time to First Token (TTFT), Inter-Token Latency (ITL), throughput, latency percentiles, batching behaviour, and concurrency—in order to determine what those results imply for real-world deployments.

Existing benchmarking tools are excellent at measuring performance, but they generally leave interpretation to the user.

As a result, engineers must manually translate benchmark results into practical decisions such as:

- Is this workload suitable for interactive use?
- Would a different runtime improve performance?
- Is the workload CPU or GPU constrained?
- Would batching improve efficiency?
- Is the current infrastructure appropriate for this workload?

Answering these questions requires significant inference engineering expertise and is often repeated for similar workloads across different teams and organizations.

---

## Consequences

As a result:

- Benchmark results remain difficult for non-specialists to interpret.
- Valuable telemetry is repeatedly analysed by humans rather than reused.
- Similar performance investigations are performed multiple times.
- Infrastructure decisions rely heavily on individual expertise.
- Deployment decisions become difficult to explain or reproduce.
- Organizations struggle to build reusable knowledge from benchmark results.

---

## Opportunity

There is an opportunity to standardize the interpretation of AI inference telemetry.

Rather than replacing existing benchmarking tools, AWCDE transforms heterogeneous benchmark results into a common behavioural model that is easier to understand, explain, and reuse.

By producing standardized Workload Signatures that preserve traceability back to the original telemetry, AWCDE enables developers to understand workload behaviour more quickly while providing a consistent foundation for workload-aware guidance and future automation.