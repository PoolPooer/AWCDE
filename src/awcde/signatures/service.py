"""Signature pipeline stage service.

Wraps SignatureDerivation as a CSP PipelineStage, accepting
BenchmarkTelemetry and producing a WorkloadSignature.
"""

from __future__ import annotations

from awcde.flyweight.registry import FlyweightRegistry
from awcde.models.signature import WorkloadSignature
from awcde.models.telemetry import BenchmarkTelemetry
from awcde.signatures.derivation import SignatureDerivation


class SignatureService:
    """Pipeline stage that derives workload signatures from telemetry.

    Delegates all computation to SignatureDerivation while presenting
    the standard PipelineStage interface.
    """

    def __init__(self, flyweight_registry: FlyweightRegistry) -> None:
        self._derivation = SignatureDerivation(flyweight_registry)

    def process(self, telemetry: BenchmarkTelemetry) -> WorkloadSignature:
        """Process benchmark telemetry into a workload signature.

        Args:
            telemetry: The benchmark telemetry to derive a signature from.

        Returns:
            A WorkloadSignature with all eight dimensions scored.
        """
        return self._derivation.derive(telemetry)
