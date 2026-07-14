"""Recommendation explanation builder.

Constructs human-readable reasoning text that explains why a particular
recommendation was made, referencing matched rules, classification
category, and relevant signature dimensions.
"""

from __future__ import annotations

from awcde.models.classification import WorkloadClassification
from awcde.models.knowledge import RuleMatch
from awcde.models.signature import WorkloadSignature


class RecommendationExplainer:
    """Builds human-readable explanations for recommendations.

    Combines information from matched rules, the classification
    category, and the signature dimensions into a coherent
    reasoning string.
    """

    @staticmethod
    def build_reasoning(
        rule_matches: list[RuleMatch],
        dimension: str,
        classification: WorkloadClassification,
        signature: WorkloadSignature,
    ) -> str:
        """Build a reasoning explanation for a recommendation dimension.

        Constructs a multi-part explanation that references:
        - The matched rules and their rationale
        - The classification category
        - Relevant signature dimension scores

        Args:
            rule_matches: The rules that contributed to this recommendation.
            dimension: The recommendation dimension (e.g. 'model_family').
            classification: The workload classification.
            signature: The workload signature.

        Returns:
            A human-readable reasoning string.
        """
        if not rule_matches:
            return (
                f"No matching rules found for '{dimension}'. "
                f"Workload classified as '{classification.primary_category.value}'. "
                f"Using default recommendation."
            )

        parts: list[str] = []

        # Reference the classification
        parts.append(
            f"Workload classified as '{classification.primary_category.value}' "
            f"with confidence {classification.confidence:.2f}."
        )

        # Reference each matched rule
        for match in rule_matches:
            recommendation_value = match.recommendations.get(dimension, "N/A")
            parts.append(
                f"Rule '{match.rule_id}' recommends '{recommendation_value}' "
                f"for {dimension}. {match.rationale}"
            )

        # Reference top signature dimensions
        dim_summary = classification.dimension_summary
        if dim_summary:
            sorted_dims = sorted(
                dim_summary.items(), key=lambda x: x[1], reverse=True
            )
            top_dims = sorted_dims[:3]
            dim_strs = [f"{name}={score:.2f}" for name, score in top_dims]
            parts.append(
                f"Key signature dimensions: {', '.join(dim_strs)}."
            )

        return " ".join(parts)
