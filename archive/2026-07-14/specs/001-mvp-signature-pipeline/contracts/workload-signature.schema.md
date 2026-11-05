# Workload Signature JSON Schema

**Schema ID**: `https://awcde.local/schemas/workload-signature/v1`  
**Schema version**: 1.0.0

Canonical schema for WorkloadSignature API responses and storage. Equivalent to
`workload-signature.schema.json` (JSON Schema format deferred to implementation).

```json
{
  "type": "object",
  "required": [
    "id", "schema_version", "telemetry_id", "derived_at",
    "latency_sensitivity", "throughput_orientation", "memory_intensity",
    "burst_behaviour", "context_length_profile", "concurrency_profile",
    "hardware_affinity", "modality"
  ],
  "properties": {
    "id": { "type": "string", "description": "Deterministic SHA-256 hash" },
    "schema_version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "telemetry_id": { "type": "string" },
    "derived_at": { "type": "string", "format": "date-time" },
    "latency_sensitivity": { "$ref": "#/dimension_score" },
    "throughput_orientation": { "$ref": "#/dimension_score" },
    "memory_intensity": { "$ref": "#/dimension_score" },
    "burst_behaviour": { "$ref": "#/dimension_score" },
    "context_length_profile": { "$ref": "#/dimension_score" },
    "concurrency_profile": { "$ref": "#/dimension_score" },
    "hardware_affinity": { "$ref": "#/dimension_score" },
    "modality": { "$ref": "#/dimension_score" }
  },
  "dimension_score": {
    "type": "object",
    "required": ["level", "score"],
    "properties": {
      "level": { "enum": ["low", "medium", "high"] },
      "score": { "type": "number", "minimum": 0, "maximum": 1 },
      "raw_inputs": { "type": "object" }
    }
  }
}
```

See [data-model.md](../data-model.md) for field semantics.
