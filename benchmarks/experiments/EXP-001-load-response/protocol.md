# EXP 001 Load response and queue evidence

Status: Draft for AWC-03. Not ready to execute until the open parameters below are resolved.

## Question and hypotheses

Does increasing offered request rate in a fixed deployment produce repeatable latency changes associated with queueing, with the same bounded interpretation across two tools? Alternatives include no detectable change, tool-specific workload/measurement effects, and insufficient server evidence. None of these outcomes establishes universal workload behaviour.

## Controls

Hold hardware, model/tokenizer revision, runtime build and flags, quantization, batching, cache policy, endpoint, streaming mode and client placement fixed. Use open-loop offered-rate generation in both tools. Record actual send times, achieved rate, pending client requests and any concurrency cap so client saturation is not mistaken for server queueing.

Use a versioned prompt corpus and record post-template token lengths and actual output lengths. Fix EOS handling where supported; document differences instead of assuming max_tokens equals actual output. Control prefix caching deliberately; repeating a single identical prompt may change cache behaviour. Match warmup, retry, timeout, failure inclusion and measurement-window policies.

## Evidence and timing

Capture request outcomes, client latency definitions, TTFT if compatible, achieved throughput, actual arrival patterns and output token provenance. Record queue wait duration or queue depth with its exact definition, labels and sampling interval. Record clock basis and alignment; reject unsupported attribution across disjoint windows. Queue depth alone is a weaker association than per-request queue wait and must be reported accordingly.

Preserve failed and timed-out requests and offered versus completed demand. Do not average percentiles across runs; retain per-run distributions or raw observations and document any pooled estimator. Server execution/cache signals are supplementary confounder checks, not automatic bottleneck diagnoses.

## Procedure

1. Smoke-test the endpoint and collection. Verify the queue signal changes plausibly under controlled demand.
2. Pilot several increasing offered rates to locate low-load and queue-building conditions safely. Stop before uncontrolled overload; define timeout, queue and resource limits before the pilot.
3. Use pilot variability to choose repetitions, run duration/request count, uncertainty estimation and equivalence tolerances. Prefer independent run-level uncertainty rather than treating temporally correlated requests as independent replicates.
4. Freeze a protocol version and analysis criteria. Run fresh validation sweeps with tool order alternated or randomized; allow queue drain and documented warmup/reset between runs.
5. Compare matched load levels and conditional findings, including failed requests and telemetry gaps. If matched experiments remain different, investigate client effects before attributing behaviour to the workload.
6. Repeat analysis after removing queue evidence. Introduce a known workload mismatch in a separate labelled control. Neither case should support an unqualified queueing conclusion.
7. Compare with a baseline report of metrics, variability and explicit comparability checks. Record interpretation time and whether the added finding changes a concrete engineering next step.

## Open parameters and execution gate

| Parameter | Required decision |
| --- | --- |
| Environment and endpoint | Hardware/client placement, runtime/model versions, access and telemetry. |
| Tool A and B | Pinned versions and actual export samples. |
| Corpus and generation | Corpus hash, token distributions, EOS/cache policy. |
| Rate sweep | Numeric rates, duration, repetitions and ordering. |
| Safety limits | Queue, timeout, failure and resource limits; drain/reset procedure. |
| Measurements | Exact field definitions, inclusion rules, telemetry cadence and clocks. |
| Statistical plan | Primary metrics, effect definition, equivalence bounds and uncertainty method. |
| Review | Protocol version, reviewer/date and resolution of every gate above. |

No measurements or acceptance outcomes are recorded yet. AWC-03 remains open until this table is resolved. If server queue evidence is unavailable, document the limitation and revise the question before execution rather than inventing a queueing inference.
