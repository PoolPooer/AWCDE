"""JSON benchmark data provider."""

from __future__ import annotations

import json
import uuid

from pydantic import ValidationError

from awcde.api.errors import ProviderError
from awcde.models.telemetry import BenchmarkRecord, BenchmarkTelemetry
from awcde.providers.base import ProviderSource


class JSONProvider:
    """Provider that ingests benchmark data from JSON files.

    Expected JSON format:
        {"records": [{"latency_p50_ms": ..., ...}, ...]}

    Each record must contain all 12 BenchmarkRecord fields.
    """

    provider_id: str = "json"
    supported_formats: list[str] = [".json", "application/json"]
    description: str = "Ingests benchmark data from JSON files"

    def supports(self, source: ProviderSource) -> bool:
        """Check if the source is a JSON file or has JSON content type."""
        if source.content_type and source.content_type.lower() == "application/json":
            return True
        return source.filename.lower().endswith(".json")

    def ingest(self, source: ProviderSource) -> BenchmarkTelemetry:
        """Parse JSON content into BenchmarkTelemetry.

        Args:
            source: The data source containing JSON benchmark data.

        Returns:
            A BenchmarkTelemetry instance with parsed records.

        Raises:
            ProviderError: If JSON parsing or validation fails.
        """
        try:
            raw = json.loads(source.content)
        except json.JSONDecodeError as e:
            raise ProviderError(
                provider_id=self.provider_id,
                message=f"Invalid JSON: {e}",
                field=None,
            ) from e

        if not isinstance(raw, dict):
            raise ProviderError(
                provider_id=self.provider_id,
                message="JSON root must be an object with a 'records' key",
                field=None,
            )

        if "records" not in raw:
            raise ProviderError(
                provider_id=self.provider_id,
                message="JSON must contain a 'records' key",
                field="records",
            )

        raw_records = raw["records"]
        if not isinstance(raw_records, list):
            raise ProviderError(
                provider_id=self.provider_id,
                message="'records' must be a list",
                field="records",
            )

        if len(raw_records) == 0:
            raise ProviderError(
                provider_id=self.provider_id,
                message="'records' must contain at least one record",
                field="records",
            )

        records: list[BenchmarkRecord] = []
        for i, raw_record in enumerate(raw_records):
            if not isinstance(raw_record, dict):
                raise ProviderError(
                    provider_id=self.provider_id,
                    message=f"Record at index {i} must be an object",
                    field=f"records[{i}]",
                )
            try:
                record = BenchmarkRecord.model_validate(raw_record)
                records.append(record)
            except ValidationError as e:
                errors = e.errors()
                field_details = "; ".join(
                    f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}"
                    for err in errors
                )
                raise ProviderError(
                    provider_id=self.provider_id,
                    message=f"Validation failed for record {i}: {field_details}",
                    field=f"records[{i}]",
                ) from e

        return BenchmarkTelemetry(
            id=str(uuid.uuid4()),
            provider_id=self.provider_id,
            source_ref=source.filename,
            records=records,
        )
