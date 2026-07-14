"""Flyweight pattern implementations for shared definitions and evaluators."""

from awcde.flyweight.categories import (
    CATEGORY_DEFINITIONS,
    CategoryDefinition,
    CategoryEvaluator,
)
from awcde.flyweight.dimensions import (
    DIMENSION_DEFINITIONS,
    DimensionDefinition,
    DimensionEvaluator,
)
from awcde.flyweight.providers import PROVIDER_DEFINITIONS, ProviderDefinition
from awcde.flyweight.registry import FlyweightRegistry

__all__ = [
    "CATEGORY_DEFINITIONS",
    "CategoryDefinition",
    "CategoryEvaluator",
    "DIMENSION_DEFINITIONS",
    "DimensionDefinition",
    "DimensionEvaluator",
    "FlyweightRegistry",
    "PROVIDER_DEFINITIONS",
    "ProviderDefinition",
]
