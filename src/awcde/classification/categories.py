"""Classification category constants and descriptions.

Supplements the flyweight CategoryDefinition with detailed
human-readable descriptions for each workload classification category.
"""

from __future__ import annotations

CATEGORY_DESCRIPTIONS: dict[str, str] = {
    "latency_critical": (
        "Workload with high sensitivity to response latency. These workloads "
        "require consistently low response times and are typically "
        "user-facing or real-time applications where tail latency "
        "directly impacts user experience or SLA compliance."
    ),
    "throughput_optimized": (
        "Workload optimized for maximum request throughput. These workloads "
        "prioritize processing the highest volume of requests per second, "
        "often involving batch inference, offline processing, or "
        "high-volume API serving where aggregate throughput matters "
        "more than individual request latency."
    ),
    "memory_intensive": (
        "Workload with high memory requirements. These workloads consume "
        "significant GPU or system memory due to large model sizes, "
        "long context windows, or high-dimensional embeddings, requiring "
        "careful memory management and potentially model parallelism."
    ),
    "burst_tolerant": (
        "Workload exhibiting burst request patterns. These workloads "
        "experience significant traffic spikes interspersed with "
        "quieter periods, requiring elastic scaling capabilities "
        "and queue-based request management to handle load variance "
        "without over-provisioning during idle periods."
    ),
    "hardware_specialized": (
        "Workload with strong affinity to specific hardware accelerators. "
        "These workloads achieve significantly better performance on "
        "particular GPU architectures or specialized accelerators, "
        "making hardware selection a critical deployment decision "
        "that directly impacts cost-efficiency and throughput."
    ),
    "general_purpose": (
        "Balanced workload with no single dominant characteristic. "
        "These workloads show moderate scores across all dimensions "
        "without a clear specialization, suitable for standard "
        "deployment configurations with balanced resource allocation "
        "and general-purpose scheduling policies."
    ),
}
