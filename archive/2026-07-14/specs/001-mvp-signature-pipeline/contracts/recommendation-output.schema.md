# Recommendation Output JSON Schema

**Schema ID**: `https://awcde.local/schemas/recommendation-output/v1`  
**Schema version**: 1.0.0

Canonical schema for InfrastructureRecommendation API responses and storage.

```json
{
  "type": "object",
  "required": [
    "id", "classification_id", "signature_id", "generated_at",
    "model_family", "runtime", "hardware_suitability",
    "deployment_topology", "scheduling_policy"
  ],
  "properties": {
    "id": { "type": "string" },
    "classification_id": { "type": "string" },
    "signature_id": { "type": "string" },
    "generated_at": { "type": "string", "format": "date-time" },
    "model_family": { "$ref": "#/recommendation_block" },
    "runtime": { "$ref": "#/recommendation_block" },
    "hardware_suitability": { "$ref": "#/recommendation_block" },
    "deployment_topology": { "$ref": "#/recommendation_block" },
    "scheduling_policy": { "$ref": "#/recommendation_block" }
  },
  "recommendation_block": {
    "type": "object",
    "required": ["recommendation", "reasoning", "evidence"],
    "properties": {
      "recommendation": { "type": "string" },
      "reasoning": { "type": "string" },
      "evidence": {
        "type": "array",
        "minItems": 1,
        "items": {
          "required": ["rule_id", "source_type", "attribute", "attribute_value", "condition_matched"],
          "properties": {
            "rule_id": { "type": "string" },
            "source_type": { "enum": ["signature", "classification", "telemetry"] },
            "attribute": { "type": "string" },
            "attribute_value": {},
            "condition_matched": { "type": "string" }
          }
        }
      }
    }
  }
}
```

Every `evidence.rule_id` MUST reference a KnowledgeBase rule. See
[knowledge-base-interface.md](./knowledge-base-interface.md).
