# Benchmark JSON Schema

**Schema ID**: `https://awcde.local/schemas/benchmark-json/v1`  
**Provider**: JSONProvider

Input schema for JSON benchmark file ingestion.

```json
{
  "type": "object",
  "required": ["records"],
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "benchmark_name": { "type": "string" },
        "run_date": { "type": "string", "format": "date-time" },
        "tool": { "type": "string" }
      }
    },
    "records": {
      "type": "array",
      "minItems": 1,
      "items": {
        "required": [
          "latency_p50_ms", "latency_p99_ms", "throughput_rps",
          "peak_memory_gb", "avg_memory_gb", "request_arrival_pattern",
          "context_length_p50", "context_length_p99", "concurrency_level",
          "accelerator_type", "gpu_utilization_pct", "modality"
        ],
        "properties": {
          "latency_p50_ms": { "type": "number", "minimum": 0 },
          "latency_p99_ms": { "type": "number", "minimum": 0 },
          "throughput_rps": { "type": "number", "minimum": 0 },
          "peak_memory_gb": { "type": "number", "minimum": 0 },
          "avg_memory_gb": { "type": "number", "minimum": 0 },
          "request_arrival_pattern": { "enum": ["steady", "bursty"] },
          "context_length_p50": { "type": "integer", "minimum": 0 },
          "context_length_p99": { "type": "integer", "minimum": 0 },
          "concurrency_level": { "type": "integer", "minimum": 1 },
          "accelerator_type": { "type": "string" },
          "gpu_utilization_pct": { "type": "number", "minimum": 0, "maximum": 100 },
          "modality": { "enum": ["text", "vision", "multimodal"] }
        }
      }
    }
  }
}
```

See also [benchmark-csv-format.md](./benchmark-csv-format.md) for CSV equivalent.
