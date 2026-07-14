"""Pipeline stage protocol for CSP-style message passing.

Defines the generic PipelineStage protocol that all pipeline stages
must implement. Each stage takes an immutable input and produces an
immutable output, enabling clean CSP-style data flow.
"""

from __future__ import annotations

from typing import Protocol, TypeVar

TInput = TypeVar("TInput", contravariant=True)
TOutput = TypeVar("TOutput", covariant=True)


class PipelineStage(Protocol[TInput, TOutput]):
    """Protocol for a single stage in the processing pipeline.

    Each stage receives an immutable Pydantic model as input and
    produces an immutable Pydantic model as output. Stages are
    composed sequentially by the PipelineOrchestrator.
    """

    def process(self, input_data: TInput) -> TOutput:
        """Process input data and produce output.

        Args:
            input_data: The immutable input for this stage.

        Returns:
            The immutable output produced by this stage.
        """
        ...
