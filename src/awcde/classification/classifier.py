"""Workload classification pipeline stage.

Evaluates a WorkloadSignature against all category definitions to
determine the primary classification category, confidence score,
and supporting rationale.
"""

from __future__ import annotations

from datetime import datetime, timezone

from awcde.classification.categories import CATEGORY_DESCRIPTIONS
from awcde.flyweight.registry import FlyweightRegistry
from awcde.models.classification import (
    ClassificationCategory,
    WorkloadClassification,
)
from awcde.models.signature import WorkloadSignature

# The 8 dimension fields on WorkloadSignature used for the summary.
_DIMENSION_FIELDS = (
    "latency_sensitivity",
    "throughput_orientation",
    "memory_intensity",
    "burst_behaviour",
    "context_length_profile",
    "concurrency_profile",
    "hardware_affinity",
    "modality",
)


class WorkloadClassifier:
    """Pipeline stage that classifies workload signatures into categories.

    Evaluates all flyweight CategoryEvaluators against a signature,
    picks the best match (highest confidence), and falls back to
    general_purpose when no category meets its threshold.
    """

    def __init__(self, flyweight_registry: FlyweightRegistry) -> None:
        self._registry = flyweight_registry

    def process(self, signature: WorkloadSignature) -> WorkloadClassification:
        """Classify a workload signature into a category.

        Evaluates every registered category evaluator against the
        signature. The category with the highest confidence score
        that meets its minimum threshold wins. If none match,
        general_purpose is used as a fallback.

        Args:
            signature: The workload signature to classify.

        Returns:
            A WorkloadClassification with category, confidence,
            rationale, and dimension summary.
        """
        evaluators = self._registry.get_all_category_evaluators()

        best_category: ClassificationCategory | None = None
        best_confidence: float = -1.0
        secondary_tags: list[str] = []

        # Track all matching categories for secondary tags
        for evaluator in evaluators:
            # Skip general_purpose during the main matching pass;
            # it is the fallback and always matches.
            if evaluator.definition.name == "general_purpose":
                continue

            is_match, confidence = evaluator.matches(signature)
            if is_match:
                secondary_tags.append(evaluator.definition.name)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_category = evaluator.category

        # Fallback to general_purpose if nothing matched
        if best_category is None:
            best_category = ClassificationCategory.GENERAL_PURPOSE
            gp_evaluator = self._registry.get_category_evaluator("general_purpose")
            _, best_confidence = gp_evaluator.matches(signature)

        # Remove the primary category from secondary tags
        primary_name = best_category.value
        secondary_tags = [t for t in secondary_tags if t != primary_name]

        # Build dimension summary
        dimension_summary: dict[str, float] = {}
        for field_name in _DIMENSION_FIELDS:
            dim_score = getattr(signature, field_name)
            dimension_summary[field_name] = dim_score.score

        # Build rationale
        rationale = self._build_rationale(
            best_category, best_confidence, dimension_summary, secondary_tags
        )

        return WorkloadClassification(
            signature_id=signature.id,
            classified_at=datetime.now(timezone.utc),
            primary_category=best_category,
            secondary_tags=secondary_tags,
            confidence=best_confidence,
            rationale=rationale,
            dimension_summary=dimension_summary,
        )

    @staticmethod
    def _build_rationale(
        category: ClassificationCategory,
        confidence: float,
        dimension_summary: dict[str, float],
        secondary_tags: list[str],
    ) -> str:
        """Build a human-readable rationale for the classification decision.

        Args:
            category: The selected primary category.
            confidence: The confidence score for the primary category.
            dimension_summary: Scores for all eight dimensions.
            secondary_tags: Other categories that also matched.

        Returns:
            A rationale string explaining the classification.
        """
        category_name = category.value
        description = CATEGORY_DESCRIPTIONS.get(category_name, "")

        # Find the top scoring dimensions
        sorted_dims = sorted(
            dimension_summary.items(), key=lambda x: x[1], reverse=True
        )
        top_dims = [f"{name}={score:.2f}" for name, score in sorted_dims[:3]]

        parts = [
            f"Classified as '{category_name}' with confidence {confidence:.2f}.",
            f"{description}",
            f"Top dimensions: {', '.join(top_dims)}.",
        ]

        if secondary_tags:
            parts.append(
                f"Secondary matches: {', '.join(secondary_tags)}."
            )

        return " ".join(parts)
