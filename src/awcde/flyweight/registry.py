"""Flyweight registry for dimension and category evaluators.

Lazily creates and caches evaluator instances, ensuring each
DimensionDefinition and CategoryDefinition has at most one
corresponding evaluator object.
"""

from __future__ import annotations

from awcde.flyweight.categories import (
    CATEGORY_DEFINITIONS,
    CategoryEvaluator,
)
from awcde.flyweight.dimensions import (
    DIMENSION_DEFINITIONS,
    DimensionEvaluator,
)


class FlyweightRegistry:
    """Lazy-caching registry for flyweight evaluator instances.

    Evaluators are created on first access and cached for reuse, keeping
    memory overhead low while allowing shared definitions across the
    entire pipeline.
    """

    def __init__(self) -> None:
        self._dimension_evaluators: dict[str, DimensionEvaluator] = {}
        self._category_evaluators: dict[str, CategoryEvaluator] = {}

    def get_dimension_evaluator(self, name: str) -> DimensionEvaluator:
        """Get or create a DimensionEvaluator for the named dimension.

        Args:
            name: The dimension name (must exist in DIMENSION_DEFINITIONS).

        Returns:
            A cached DimensionEvaluator instance.

        Raises:
            KeyError: If the dimension name is not registered.
        """
        if name not in self._dimension_evaluators:
            if name not in DIMENSION_DEFINITIONS:
                msg = f"Unknown dimension: {name!r}"
                raise KeyError(msg)
            self._dimension_evaluators[name] = DimensionEvaluator(
                DIMENSION_DEFINITIONS[name]
            )
        return self._dimension_evaluators[name]

    def get_all_dimension_evaluators(self) -> list[DimensionEvaluator]:
        """Get evaluators for all registered dimensions.

        Returns:
            A list of DimensionEvaluator instances, one per registered dimension.
        """
        for name in DIMENSION_DEFINITIONS:
            self.get_dimension_evaluator(name)
        return list(self._dimension_evaluators.values())

    def get_category_evaluator(self, name: str) -> CategoryEvaluator:
        """Get or create a CategoryEvaluator for the named category.

        Args:
            name: The category name (must exist in CATEGORY_DEFINITIONS).

        Returns:
            A cached CategoryEvaluator instance.

        Raises:
            KeyError: If the category name is not registered.
        """
        if name not in self._category_evaluators:
            if name not in CATEGORY_DEFINITIONS:
                msg = f"Unknown category: {name!r}"
                raise KeyError(msg)
            self._category_evaluators[name] = CategoryEvaluator(
                CATEGORY_DEFINITIONS[name]
            )
        return self._category_evaluators[name]

    def get_all_category_evaluators(self) -> list[CategoryEvaluator]:
        """Get evaluators for all registered categories.

        Returns:
            A list of CategoryEvaluator instances, one per registered category.
        """
        for name in CATEGORY_DEFINITIONS:
            self.get_category_evaluator(name)
        return list(self._category_evaluators.values())
