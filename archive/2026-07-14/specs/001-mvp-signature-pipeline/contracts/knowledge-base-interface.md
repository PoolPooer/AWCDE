# KnowledgeBase Interface Contract

**Version**: 1.0.0

KnowledgeBase is a first-class domain concept holding deployment recommendation rules.
The recommendation engine MUST consult KnowledgeBase rather than hard-coding reasoning.

## KnowledgeBase Protocol

```python
class KnowledgeBase(Protocol):
    def load(self, rules_path: Path) -> None:
        """Load rules from static source (Phase 1: YAML file)."""

    def query(
        self,
        classification: WorkloadClassification,
        signature: WorkloadSignature,
    ) -> list[RuleMatch]:
        """Find applicable rules and return matches with rationale."""

    def get_rule(self, rule_id: str) -> KnowledgeRule | None:
        """Retrieve a single rule by ID for evidence tracing."""
```

## KnowledgeRule Structure

| Field | Type | Required | Description |
|---|---|---|---|
| `rule_id` | string | yes | Stable identifier (e.g. `kb-latency-001`) |
| `version` | string | yes | Rule set version |
| `description` | string | yes | Human-readable rule purpose |
| `conditions` | list[RuleCondition] | yes | Match criteria |
| `recommendations` | dict | yes | Values per recommendation dimension |
| `rationale_template` | string | yes | Template with `{placeholders}` |

### RuleCondition

| Field | Type | Description |
|---|---|---|
| `field` | string | Path: signature dimension, classification category, or attribute |
| `operator` | enum | `eq`, `gt`, `gte`, `lt`, `lte`, `in` |
| `value` | any | Comparison value |

### RuleMatch (query result)

| Field | Type | Description |
|---|---|---|
| `rule_id` | string | Matched rule |
| `recommendations` | dict | Recommendation values from rule |
| `rationale` | string | Rendered rationale from template |
| `matched_conditions` | list | Conditions that evaluated true |

## Phase 1 Implementation: StaticKnowledgeBase

- Rules loaded from `data/knowledge/rules.yaml` at startup
- Manual/static rule definitions only
- No ML, no learned weights, no black-box scoring
- Rules editable without changing recommendation engine code

## Example Rule (YAML)

```yaml
- rule_id: kb-latency-001
  version: "1.0.0"
  description: Latency-critical workloads need low-latency runtime and real-time scheduling
  conditions:
    - field: classification.primary_category
      operator: eq
      value: latency_critical
  recommendations:
    runtime: vllm-low-latency
    scheduling_policy: real-time-priority
    deployment_topology: single-node-dedicated
  rationale_template: >
    Workload classified as {classification.primary_category} with latency
    sensitivity score {signature.latency_sensitivity.score}. Rule {rule_id}
    recommends low-latency runtime configuration.
```

## Recommendation Engine Integration

The recommendation engine (`recommendations/engine.py`):
1. Receives WorkloadClassification + WorkloadSignature
2. Calls `KnowledgeBase.query(classification, signature)`
3. Aggregates RuleMatch results into five recommendation dimensions
4. Builds evidence traces linking each recommendation to `rule_id` and matched conditions
5. Does NOT embed rule logic directly — all rules live in KnowledgeBase

## Constitution Compliance

- Explainable: every recommendation traceable to KnowledgeBase rule
- Rule-based: static conditions only in Phase 1
- No ML: KnowledgeBase contains no model weights or learned parameters
