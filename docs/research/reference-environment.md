# Reference environment selection

Status: Unselected for the current POC. The July Windows/WSL2/RTX 5090 proposal is historical and has not been verified as available.

Choose one accessible environment with a stable endpoint, sufficient model capacity, exportable server queue metrics and access to record the exact runtime configuration. Use a single fixed serving instance initially so aggregation and routing do not obscure queue evidence.

Record hardware model and count, memory, host and client placement, OS, driver, runtime image digest or commit, model and tokenizer revisions, quantization, cache and batching settings, power limits, background activity and thermal conditions. Redact credentials while retaining the information needed for interpretation.

A smoke test must demonstrate successful streaming requests, actual input/output accounting and readable queue telemetry. Resource access and compatible model/tool choices are prerequisites to execution, not facts established by this repo.
