# Provider Interface Contract

**Version**: 1.0.0

Telemetry sources are modeled as **Providers**. Each Provider adapts a specific
benchmark or telemetry format into normalized `BenchmarkTelemetry`.

## Provider Protocol

All Providers MUST implement:

```python
class Provider(Protocol):
    provider_id: str

    def supports(self, source: ProviderSource) -> bool:
        """Return True if this Provider can handle the given source."""

    def ingest(self, source: ProviderSource) -> BenchmarkTelemetry:
        """Parse and normalize source into BenchmarkTelemetry."""
```

## ProviderSource

| Field | Type | Description |
|---|---|---|
| `filename` | string | Original file name |
| `content_type` | string | MIME type if available |
| `content` | bytes | Raw file content |

## Phase 1 Implementations

### JSONProvider

| Property | Value |
|---|---|
| `provider_id` | `json` |
| Formats | `.json`, `application/json` |
| Schema | [benchmark-json.schema.md](./benchmark-json.schema.md) |

### CSVProvider

| Property | Value |
|---|---|
| `provider_id` | `csv` |
| Formats | `.csv`, `text/csv` |
| Schema | [benchmark-csv-format.md](./benchmark-csv-format.md) |

Both Providers MUST produce identical `BenchmarkTelemetry` structure for equivalent data.

## Future Providers (Architecture Only — Not Phase 1)

| Provider | `provider_id` | Expected Input | Status |
|---|---|---|---|
| GuideLLMProvider | `guidellm` | GuideLLM benchmark output | Planned |
| vLLMProvider | `vllm` | vLLM benchmark metrics | Planned |
| PrometheusProvider | `prometheus` | Prometheus query results | Planned |
| OpenTelemetryProvider | `opentelemetry` | OTel trace/metric exports | Planned |

Future Providers MUST:
- Register via Provider registry without modifying pipeline core
- Return HTTP 501 Not Implemented when invoked before implementation
- NOT introduce live telemetry streams in Phase 1

## Provider Registry

```python
class ProviderRegistry:
    def register(self, provider: Provider) -> None: ...
    def get(self, provider_id: str) -> Provider: ...
    def list_providers(self) -> list[ProviderInfo]: ...
    def resolve(self, source: ProviderSource) -> Provider: ...
```

Registry is initialized at application startup with Phase 1 Providers only.

## Error Handling

Providers MUST raise structured validation errors with:
- `field`: affected field path
- `message`: human-readable error
- `provider_id`: source Provider

No partial BenchmarkTelemetry on validation failure.
