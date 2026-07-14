"""Flyweight provider definitions for telemetry ingestion formats."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderDefinition:
    """Immutable flyweight definition for a telemetry data provider."""

    provider_id: str
    supported_extensions: tuple[str, ...]
    supported_mime_types: tuple[str, ...]
    description: str


PROVIDER_DEFINITIONS: dict[str, ProviderDefinition] = {
    "json": ProviderDefinition(
        provider_id="json",
        supported_extensions=(".json",),
        supported_mime_types=("application/json",),
        description="JSON telemetry data provider.",
    ),
    "csv": ProviderDefinition(
        provider_id="csv",
        supported_extensions=(".csv",),
        supported_mime_types=("text/csv", "application/csv"),
        description="CSV telemetry data provider.",
    ),
}
