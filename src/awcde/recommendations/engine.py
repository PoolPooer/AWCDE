"""Recommendation engine pipeline stage.

Queries the knowledge base for matching rules, aggregates results
into five recommendation blocks, and builds evidence traces and
explanations for full traceability.
"""

from __future__ import annotations

from datetime import datetime, timezone

from awcde.knowledge.static_kb import StaticKnowledgeBase
from awcde.models.classification import WorkloadClassification
from awcde.models.knowledge import RuleMatch
from awcde.models.recommendation import (
    InfrastructureRecommendation,
    RecommendationBlock,
    RecommendationEvidence,
)
from awcde.models.signature import WorkloadSignature
from awcde.recommendations.evidence import EvidenceCollector
from awcde.recommendations.explainer import RecommendationExplainer

# The five recommendation dimensions that must be populated.
_RECOMMENDATION_DIMENSIONS = (
    "model_family",
    "runtime",
    "hardware_suitability",
    "deployment_topology",
    "scheduling_policy",
)

# Fallback recommendations when no rules match.
_FALLBACK_RECOMMENDATIONS: dict[str, str] = {
    "model_family": "general-purpose",
    "runtime": "vllm-standard",
    "hardware_suitability": "gpu-shared-pool",
    "deployment_topology": "multi-replica-balanced",
    "scheduling_policy": "fair-share",
}


class RecommendationEngine:
    """Pipeline stage that produces infrastructure recommendations.

    Queries the knowledge base for applicable rules, aggregates
    their recommendations across five dimensions, and provides
    full evidence traces and explanations.
    """

    def __init__(self, knowledge_base: StaticKnowledgeBase) -> None:
        self._knowledge_base = knowledge_base
        self._evidence_collector = EvidenceCollector()
        self._explainer = RecommendationExplainer()

    def process(
        self,
        classification: WorkloadClassification,
        signature: WorkloadSignature,
    ) -> InfrastructureRecommendation:
        """Generate infrastructure recommendations for a classified workload.

        Steps:
        1. Query the knowledge base for matching rules
        2. Aggregate rule matches into five recommendation blocks
        3. Build evidence traces linking recommendations to rules
        4. Build explanations for each recommendation dimension

        If no rules match, fallback recommendations are provided with
        appropriate reasoning.

        Args:
            classification: The workload classification result.
            signature: The workload signature.

        Returns:
            An InfrastructureRecommendation with all five blocks populated.
        """
        rule_matches = self._knowledge_base.query(classification, signature)

        # Collect all evidence across all matching rules
        all_evidence: list[RecommendationEvidence] = []
        for match in rule_matches:
            all_evidence.extend(
                self._evidence_collector.collect(match, classification, signature)
            )

        # Build recommendation blocks for each dimension
        blocks: dict[str, RecommendationBlock] = {}
        for dimension in _RECOMMENDATION_DIMENSIONS:
            blocks[dimension] = self._build_block(
                dimension, rule_matches, all_evidence, classification, signature
            )

        return InfrastructureRecommendation(
            classification_id=classification.id,
            signature_id=signature.id,
            generated_at=datetime.now(timezone.utc),
            **blocks,
        )

    def _build_block(
        self,
        dimension: str,
        rule_matches: list[RuleMatch],
        all_evidence: list[RecommendationEvidence],
        classification: WorkloadClassification,
        signature: WorkloadSignature,
    ) -> RecommendationBlock:
        """Build a single recommendation block for a dimension.

        Finds the most specific rule that provides a recommendation
        for this dimension (last match with most conditions wins),
        collects relevant evidence, and builds the reasoning.

        Args:
            dimension: The recommendation dimension name.
            rule_matches: All matched rules from the knowledge base.
            all_evidence: All evidence collected across all rules.
            classification: The workload classification.
            signature: The workload signature.

        Returns:
            A RecommendationBlock with recommendation, reasoning,
            and evidence.
        """
        # Find rules that provide a recommendation for this dimension
        relevant_matches: list[RuleMatch] = [
            m for m in rule_matches if dimension in m.recommendations
        ]

        if relevant_matches:
            # Pick the most specific rule: most conditions, last in order
            best_match = max(
                relevant_matches,
                key=lambda m: len(m.matched_conditions),
            )
            recommendation = best_match.recommendations[dimension]

            # Gather evidence from all relevant rules for this dimension
            relevant_rule_ids = {m.rule_id for m in relevant_matches}
            dimension_evidence = [
                e for e in all_evidence if e.rule_id in relevant_rule_ids
            ]
        else:
            recommendation = _FALLBACK_RECOMMENDATIONS[dimension]
            dimension_evidence = []

        # Build reasoning
        reasoning = self._explainer.build_reasoning(
            relevant_matches, dimension, classification, signature
        )

        return RecommendationBlock(
            recommendation=recommendation,
            reasoning=reasoning,
            evidence=dimension_evidence,
        )
