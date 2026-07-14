"""Base provider protocol and shared types for benchmark data ingestion."""

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel

from awcde.models.telemetry import BenchmarkTelemetry


class ProviderSource(BaseModel):
    """Describes a data source to be ingested by a provider."""

    filename: str
    content_type: str = ""
    content: bytes


class ProviderInfo(BaseModel):
    """Metadata describing a registered provider."""

    provider_id: str
    supported_formats: list[str]
    description: str


class Provider(Protocol):
    """Protocol that all benchmark data providers must implement."""

    provider_id: str

    def supports(self, source: ProviderSource) -> bool:
        """Return True if this provider can handle the given source."""
        ...

    def ingest(self, source: ProviderSource) -> BenchmarkTelemetry:
        """Parse the source content and return structured telemetry data."""
        ...
