"""Evidence collection for recommendation traceability.

Extracts structured evidence from matched rule conditions, linking
each recommendation back to specific attributes in the classification
and signature that triggered the rule.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from awcde.models.classification import WorkloadClassification
from awcde.models.knowledge import RuleCondition, RuleMatch
from awcde.models.recommendation import RecommendationEvidence
from awcde.models.signature import WorkloadSignature


def _resolve_field(obj: Any, path_parts: list[str]) -> Any:
    """Navigate an object graph using a list of attribute names.

    Args:
        obj: The root object to start from.
        path_parts: Attribute names to traverse in order.

    Returns:
        The resolved value, with enums converted to their string value.
    """
    current = obj
    for part in path_parts:
        current = getattr(current, part)
    if isinstance(current, Enum):
        return current.value
    return current


class EvidenceCollector:
    """Collects structured evidence from matched rule conditions.

    For each matched condition in a rule, extracts the source type,
    attribute path, actual value, and a human-readable description
    of the condition that was satisfied.
    """

    def collect(
        self,
        rule_match: RuleMatch,
        classification: WorkloadClassification,
        signature: WorkloadSignature,
    ) -> list[RecommendationEvidence]:
        """Collect evidence from a matched rule.

        For each condition in the rule match, resolves the actual
        attribute value from the classification or signature and
        builds a RecommendationEvidence record.

        Args:
            rule_match: The matched rule with its conditions.
            classification: The workload classification.
            signature: The workload signature.

        Returns:
            A list of RecommendationEvidence objects, one per
            matched condition.
        """
        evidence_list: list[RecommendationEvidence] = []

        for condition in rule_match.matched_conditions:
            parts = condition.field.split(".")

            # Determine source type from the first path component
            source_type = parts[0] if parts[0] in ("classification", "signature") else "telemetry"

            # Resolve the actual attribute value
            if parts[0] == "classification":
                root_obj = classification
            elif parts[0] == "signature":
                root_obj = signature
            else:
                root_obj = None

            attribute_value: float | int | str = ""
            if root_obj is not None:
                try:
                    attribute_value = _resolve_field(root_obj, parts[1:])
                except (AttributeError, TypeError):
                    attribute_value = "unresolved"

            # Build human-readable condition string
            condition_matched = (
                f"{condition.field} {condition.operator.value} {condition.value}"
            )

            evidence_list.append(
                RecommendationEvidence(
                    rule_id=rule_match.rule_id,
                    source_type=source_type,
                    attribute=condition.field,
                    attribute_value=attribute_value,
                    condition_matched=condition_matched,
                )
            )

        return evidence_list
