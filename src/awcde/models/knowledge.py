"""Knowledge rule models for the recommendation engine."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class RuleOperator(str, Enum):
    """Comparison operators for rule conditions."""

    EQ = "eq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"


class RuleCondition(BaseModel):
    """A single condition within a knowledge rule."""

    field: str
    operator: RuleOperator
    value: float | int | str | list


class KnowledgeRule(BaseModel):
    """A knowledge base rule mapping conditions to recommendations."""

    rule_id: str
    version: str
    description: str
    conditions: list[RuleCondition]
    recommendations: dict[str, str]
    rationale_template: str


class RuleMatch(BaseModel):
    """Result of evaluating a knowledge rule against a workload."""

    rule_id: str
    recommendations: dict[str, str]
    rationale: str
    matched_conditions: list[RuleCondition]
