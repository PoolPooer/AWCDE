# Workload Classification JSON Schema

**Schema ID**: `https://awcde.local/schemas/workload-classification/v1`  
**Schema version**: 1.0.0

Canonical schema for WorkloadClassification API responses and storage.

```json
{
  "type": "object",
  "required": [
    "id", "signature_id", "classified_at", "primary_category",
    "confidence", "rationale", "dimension_summary"
  ],
  "properties": {
    "id": { "type": "string" },
    "signature_id": { "type": "string" },
    "classified_at": { "type": "string", "format": "date-time" },
    "primary_category": {
      "enum": [
        "latency_critical", "throughput_optimized", "memory_intensive",
        "burst_tolerant", "hardware_specialized", "general_purpose"
      ]
    },
    "secondary_tags": { "type": "array", "items": { "type": "string" } },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "rationale": { "type": "string", "minLength": 1 },
    "dimension_summary": { "type": "object" }
  }
}
```

See [data-model.md](../data-model.md) for category definitions.
