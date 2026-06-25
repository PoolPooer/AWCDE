# Benchmark CSV Format

**Provider**: `CSVProvider`  
**Contract version**: 1.0.0

CSV benchmark files MUST include a header row with the following columns. Column names
are case-sensitive and map directly to BenchmarkRecord fields.

## Required Columns

| Column | Type | Description |
|---|---|---|
| `latency_p50_ms` | float | 50th percentile latency (ms) |
| `latency_p99_ms` | float | 99th percentile latency (ms) |
| `throughput_rps` | float | Requests per second |
| `peak_memory_gb` | float | Peak memory usage (GB) |
| `avg_memory_gb` | float | Average memory usage (GB) |
| `request_arrival_pattern` | string | `steady` or `bursty` |
| `context_length_p50` | integer | Median context/token length |
| `context_length_p99` | integer | 99th percentile context length |
| `concurrency_level` | integer | Concurrent request count |
| `accelerator_type` | string | Accelerator identifier |
| `gpu_utilization_pct` | float | GPU utilization 0–100 |
| `modality` | string | `text`, `vision`, or `multimodal` |

## Example

```csv
latency_p50_ms,latency_p99_ms,throughput_rps,peak_memory_gb,avg_memory_gb,request_arrival_pattern,context_length_p50,context_length_p99,concurrency_level,accelerator_type,gpu_utilization_pct,modality
120.5,450.0,85.2,32.0,24.5,bursty,4096,8192,16,A100,78.5,text
```

## Validation Rules

Same constraints as [benchmark-json.schema.json](./benchmark-json.schema.json):
- All numeric values non-negative
- `latency_p99_ms` >= `latency_p50_ms`
- `context_length_p99` >= `context_length_p50`
- `gpu_utilization_pct` in 0–100
- Enum fields must match allowed values

## Normalization

CSVProvider MUST produce BenchmarkTelemetry identical in structure to JSONProvider
output for equivalent data.
