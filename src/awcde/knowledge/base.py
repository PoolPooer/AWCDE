"""KnowledgeBase protocol definition."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from awcde.models.classification import WorkloadClassification
from awcde.models.knowledge import KnowledgeRule, RuleMatch
from awcde.models.signature import WorkloadSignature


class KnowledgeBaseProtocol(Protocol):
    """Protocol for knowledge base implementations.

    A knowledge base holds deployment recommendation rules and can evaluate
    them against workload classifications and signatures to produce matches.
    """

    def load(self, rules_path: Path) -> None:
        """Load rules from a static source.

        Args:
            rules_path: Path to the rules file (Phase 1: YAML).
        """
        ...

    def query(
        self,
        classification: WorkloadClassification,
        signature: WorkloadSignature,
    ) -> list[RuleMatch]:
        """Find applicable rules and return matches with rationale.

        Args:
            classification: The workload classification to match against.
            signature: The workload signature to match against.

        Returns:
            A list of RuleMatch instances for all matching rules.
        """
        ...

    def get_rule(self, rule_id: str) -> KnowledgeRule | None:
        """Retrieve a single rule by ID for evidence tracing.

        Args:
            rule_id: The unique identifier of the rule.

        Returns:
            The KnowledgeRule if found, or None.
        """
        ...
