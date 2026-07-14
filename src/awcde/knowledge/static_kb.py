"""Static YAML-based knowledge base implementation."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from awcde.models.classification import WorkloadClassification
from awcde.models.knowledge import KnowledgeRule, RuleCondition, RuleMatch, RuleOperator
from awcde.models.signature import WorkloadSignature


class StaticKnowledgeBase:
    """Knowledge base that loads rules from a YAML file.

    Rules are evaluated against workload classifications and signatures
    using simple condition-based matching. Each rule specifies conditions
    on classification or signature fields, and when all conditions match,
    the rule's recommendations are returned with a rendered rationale.
    """

    def __init__(self) -> None:
        self._rules: list[KnowledgeRule] = []

    def load(self, rules_path: Path) -> None:
        """Load rules from a YAML file.

        The YAML file should contain a list of rule objects, each with
        rule_id, version, description, conditions, recommendations,
        and rationale_template fields.

        Args:
            rules_path: Path to the YAML rules file.

        Raises:
            FileNotFoundError: If the rules file does not exist.
            yaml.YAMLError: If the YAML is malformed.
            ValueError: If the rules structure is invalid.
        """
        with open(rules_path) as f:
            raw_rules = yaml.safe_load(f)

        if not isinstance(raw_rules, list):
            raise ValueError(f"Rules file must contain a YAML list, got {type(raw_rules).__name__}")

        self._rules = []
        for raw_rule in raw_rules:
            rule = KnowledgeRule.model_validate(raw_rule)
            self._rules.append(rule)

    def query(
        self,
        classification: WorkloadClassification,
        signature: WorkloadSignature,
    ) -> list[RuleMatch]:
        """Evaluate all rules against the given classification and signature.

        A rule matches when ALL of its conditions evaluate to true.

        Args:
            classification: The workload classification to match against.
            signature: The workload signature to match against.

        Returns:
            A list of RuleMatch instances for all matching rules.
        """
        matches: list[RuleMatch] = []

        for rule in self._rules:
            matched_conditions: list[RuleCondition] = []
            all_match = True

            for condition in rule.conditions:
                actual_value = _resolve_field(condition.field, classification, signature)
                if actual_value is None:
                    all_match = False
                    break
                if _evaluate_condition(condition.operator, actual_value, condition.value):
                    matched_conditions.append(condition)
                else:
                    all_match = False
                    break

            if all_match and matched_conditions:
                rationale = _render_rationale(
                    rule.rationale_template,
                    rule.rule_id,
                    classification,
                    signature,
                )
                matches.append(
                    RuleMatch(
                        rule_id=rule.rule_id,
                        recommendations=rule.recommendations,
                        rationale=rationale,
                        matched_conditions=matched_conditions,
                    )
                )

        return matches

    def get_rule(self, rule_id: str) -> KnowledgeRule | None:
        """Retrieve a single rule by its ID.

        Args:
            rule_id: The unique identifier of the rule.

        Returns:
            The KnowledgeRule if found, or None.
        """
        for rule in self._rules:
            if rule.rule_id == rule_id:
                return rule
        return None


def _resolve_field(
    field_path: str,
    classification: WorkloadClassification,
    signature: WorkloadSignature,
) -> Any:
    """Resolve a dotted field path against classification or signature objects.

    Supported field path patterns:
        - classification.<attr> (e.g., classification.primary_category)
        - signature.<dimension>.<attr> (e.g., signature.latency_sensitivity.score)

    Args:
        field_path: Dotted path string.
        classification: The workload classification.
        signature: The workload signature.

    Returns:
        The resolved value, or None if the path is invalid.
    """
    parts = field_path.split(".")
    if len(parts) < 2:
        return None

    root = parts[0]
    if root == "classification":
        obj: Any = classification
        for part in parts[1:]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return None
        # Convert enums to their value for comparison
        if hasattr(obj, "value"):
            return obj.value
        return obj
    elif root == "signature":
        obj = signature
        for part in parts[1:]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return None
        if hasattr(obj, "value"):
            return obj.value
        return obj
    else:
        return None


def _evaluate_condition(operator: RuleOperator, actual: Any, expected: Any) -> bool:
    """Evaluate a single condition.

    Args:
        operator: The comparison operator to apply.
        actual: The actual value from the object.
        expected: The expected value from the rule condition.

    Returns:
        True if the condition is satisfied.
    """
    if operator == RuleOperator.EQ:
        return actual == expected
    elif operator == RuleOperator.GT:
        return float(actual) > float(expected)
    elif operator == RuleOperator.GTE:
        return float(actual) >= float(expected)
    elif operator == RuleOperator.LT:
        return float(actual) < float(expected)
    elif operator == RuleOperator.LTE:
        return float(actual) <= float(expected)
    elif operator == RuleOperator.IN:
        if isinstance(expected, list):
            return actual in expected
        return False
    return False


def _render_rationale(
    template: str,
    rule_id: str,
    classification: WorkloadClassification,
    signature: WorkloadSignature,
) -> str:
    """Render a rationale template by replacing {placeholders} with actual values.

    Supported placeholders:
        - {rule_id}: The rule's identifier
        - {classification.<field>}: Classification attributes
        - {signature.<dimension>.<field>}: Signature dimension attributes

    Args:
        template: The rationale template string with {placeholders}.
        rule_id: The rule ID for {rule_id} substitution.
        classification: The classification for {classification.*} substitution.
        signature: The signature for {signature.*} substitution.

    Returns:
        The rendered rationale string.
    """
    def replace_placeholder(match: re.Match) -> str:
        placeholder = match.group(1)
        if placeholder == "rule_id":
            return rule_id
        value = _resolve_field(placeholder, classification, signature)
        if value is not None:
            return str(value)
        return match.group(0)  # Return original if unresolvable

    return re.sub(r"\{([^}]+)\}", replace_placeholder, template)
