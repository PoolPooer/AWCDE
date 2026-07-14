"""Deterministic signature identity computation.

Produces a SHA-256 hash from normalized telemetry data and schema
version, ensuring identical inputs always yield the same signature ID.
"""

from __future__ import annotations

import hashlib
import json
from enum import Enum
from typing import Any

from awcde.models.telemetry import BenchmarkTelemetry


def _normalize_value(value: Any) -> Any:
    """Normalize a value for canonical JSON serialization."""
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, float):
        return round(value, 10)
    return value


def _record_sort_key(record_dict: dict[str, Any]) -> tuple:
    """Create a sort key from a record dict for deterministic ordering."""
    return tuple(
        str(record_dict[k])
        for k in sorted(record_dict.keys())
    )


def compute_signature_id(
    telemetry: BenchmarkTelemetry,
    schema_version: str,
) -> str:
    """Compute a deterministic signature ID from telemetry data.

    Normalizes the telemetry records into a canonical form, serializes
    to JSON, and produces a SHA-256 hex digest. Identical telemetry
    and schema version always produce the same ID.

    Args:
        telemetry: The benchmark telemetry containing one or more records.
        schema_version: The schema version string to include in the hash.

    Returns:
        A SHA-256 hex digest string.
    """
    # Convert each record to a dict with normalized values
    record_dicts: list[dict[str, Any]] = []
    for record in telemetry.records:
        raw = record.model_dump()
        normalized = {
            k: _normalize_value(v) for k, v in raw.items()
        }
        record_dicts.append(normalized)

    # Sort records by all fields for deterministic ordering
    record_dicts.sort(key=_record_sort_key)

    # Build the canonical payload
    canonical = {
        "schema_version": schema_version,
        "records": record_dicts,
    }

    # Serialize to canonical JSON (sorted keys, no whitespace variation)
    canonical_json = json.dumps(canonical, sort_keys=True, separators=(",", ":"))

    # Compute SHA-256 hash
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
