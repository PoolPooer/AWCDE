"""CSV benchmark data provider."""

from __future__ import annotations

import csv
import io
import uuid

from pydantic import ValidationError

from awcde.api.errors import ProviderError
from awcde.models.telemetry import BenchmarkRecord, BenchmarkTelemetry
from awcde.providers.base import ProviderSource

# Fields that must be converted from CSV strings to float
_FLOAT_FIELDS: set[str] = {
    "latency_p50_ms",
    "latency_p99_ms",
    "throughput_rps",
    "peak_memory_gb",
    "avg_memory_gb",
    "gpu_utilization_pct",
}

# Fields that must be converted from CSV strings to int
_INT_FIELDS: set[str] = {
    "context_length_p50",
    "context_length_p99",
    "concurrency_level",
}

# All expected header fields matching BenchmarkRecord
_EXPECTED_HEADERS: set[str] = {
    "latency_p50_ms",
    "latency_p99_ms",
    "throughput_rps",
    "peak_memory_gb",
    "avg_memory_gb",
    "request_arrival_pattern",
    "context_length_p50",
    "context_length_p99",
    "concurrency_level",
    "accelerator_type",
    "gpu_utilization_pct",
    "modality",
}


class CSVProvider:
    """Provider that ingests benchmark data from CSV files.

    Expected CSV format: header row with BenchmarkRecord field names,
    followed by one or more data rows.
    """

    provider_id: str = "csv"
    supported_formats: list[str] = [".csv", "text/csv"]
    description: str = "Ingests benchmark data from CSV files"

    def supports(self, source: ProviderSource) -> bool:
        """Check if the source is a CSV file or has CSV content type."""
        if source.content_type and source.content_type.lower() == "text/csv":
            return True
        return source.filename.lower().endswith(".csv")

    def ingest(self, source: ProviderSource) -> BenchmarkTelemetry:
        """Parse CSV content into BenchmarkTelemetry.

        Args:
            source: The data source containing CSV benchmark data.

        Returns:
            A BenchmarkTelemetry instance with parsed records.

        Raises:
            ProviderError: If CSV parsing or validation fails.
        """
        try:
            text = source.content.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ProviderError(
                provider_id=self.provider_id,
                message=f"CSV content is not valid UTF-8: {e}",
                field=None,
            ) from e

        reader = csv.DictReader(io.StringIO(text))

        if reader.fieldnames is None:
            raise ProviderError(
                provider_id=self.provider_id,
                message="CSV file is empty or has no header row",
                field=None,
            )

        headers = set(reader.fieldnames)
        missing_headers = _EXPECTED_HEADERS - headers
        if missing_headers:
            raise ProviderError(
                provider_id=self.provider_id,
                message=f"CSV is missing required headers: {sorted(missing_headers)}",
                field=None,
            )

        records: list[BenchmarkRecord] = []
        for i, row in enumerate(reader):
            try:
                converted = _convert_row(row, i)
                record = BenchmarkRecord.model_validate(converted)
                records.append(record)
            except ProviderError:
                raise
            except ValidationError as e:
                errors = e.errors()
                field_details = "; ".join(
                    f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}"
                    for err in errors
                )
                raise ProviderError(
                    provider_id=self.provider_id,
                    message=f"Validation failed for row {i}: {field_details}",
                    field=f"row[{i}]",
                ) from e

        if len(records) == 0:
            raise ProviderError(
                provider_id=self.provider_id,
                message="CSV must contain at least one data row",
                field=None,
            )

        return BenchmarkTelemetry(
            id=str(uuid.uuid4()),
            provider_id=self.provider_id,
            source_ref=source.filename,
            records=records,
        )


def _convert_row(row: dict[str, str], row_index: int) -> dict[str, float | int | str]:
    """Convert CSV string values to appropriate Python types.

    Args:
        row: A dictionary of field name to string value from CSV.
        row_index: The zero-based row index for error reporting.

    Returns:
        A dictionary with values converted to the correct types.

    Raises:
        ProviderError: If a value cannot be converted to the expected type.
    """
    converted: dict[str, float | int | str] = {}

    for field, value in row.items():
        if field not in _EXPECTED_HEADERS:
            continue

        if field in _FLOAT_FIELDS:
            try:
                converted[field] = float(value)
            except (ValueError, TypeError) as e:
                msg = (
                    f"Cannot convert '{value}' to float "
                    f"for field '{field}' in row {row_index}"
                )
                raise ProviderError(
                    provider_id="csv",
                    message=msg,
                    field=f"row[{row_index}].{field}",
                ) from e
        elif field in _INT_FIELDS:
            try:
                converted[field] = int(float(value))
            except (ValueError, TypeError) as e:
                msg = (
                    f"Cannot convert '{value}' to int "
                    f"for field '{field}' in row {row_index}"
                )
                raise ProviderError(
                    provider_id="csv",
                    message=msg,
                    field=f"row[{row_index}].{field}",
                ) from e
        else:
            converted[field] = value.strip()

    return converted
