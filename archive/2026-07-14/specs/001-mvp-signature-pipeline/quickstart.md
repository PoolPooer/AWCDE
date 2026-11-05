# Quickstart: AWCDE MVP — Benchmark-to-Recommendation Pipeline

**Date**: 2026-06-24

Validation guide for the FastAPI backend. All scenarios use HTTP requests against
the running service. No implementation code included — this documents expected
behavior for manual or integration validation.

> **Scope note**: Phase 1 validates the benchmark-data path through the Workload
> Characterization Engine and Deployment Decision Engine. Runtime metrics, production
> telemetry, production deployment, and feedback loops are future phases. See
> [architecture.md](./architecture.md).

## Prerequisites

- AWCDE service running locally (default `http://localhost:8000`)
- Sample benchmark fixtures in `tests/fixtures/`:
  - `benchmark-latency-critical.json`
  - `benchmark-throughput-batch.csv`
  - `benchmark-invalid-missing-fields.json`
- OpenAPI docs available at `http://localhost:8000/docs`

## Scenario 1: Ingest JSON Benchmark (US1)

**Goal**: Validate JSONProvider ingestion via REST API.

```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@tests/fixtures/benchmark-latency-critical.json" \
  -F "provider=json"
```

**Expected outcome**:
- HTTP 201 with `telemetry_id`, `provider_id: "json"`, `record_count`
- Normalized benchmark records returned in response body
- Invalid files return HTTP 422 with field-level error details

## Scenario 2: Ingest CSV Benchmark (US1)

**Goal**: Confirm CSVProvider produces equivalent normalization to JSON.

```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@tests/fixtures/benchmark-throughput-batch.csv" \
  -F "provider=csv"
```

**Expected outcome**:
- HTTP 201 with normalized records matching equivalent JSON schema fields
- Column mapping documented in [benchmark-csv-format.md](./contracts/benchmark-csv-format.md)

## Scenario 3: Derive and Store Workload Signature (US2)

**Goal**: Transform ingested telemetry into a versioned signature.

```bash
curl -X POST http://localhost:8000/signatures \
  -H "Content-Type: application/json" \
  -d '{"telemetry_id": "<telemetry_id from Scenario 1>"}'
```

**Expected outcome**:
- HTTP 201 with `signature_id`, `schema_version: "1.0.0"`
- All eight dimensions populated with `level`, `score`, and `raw_inputs`
- Re-running with same `telemetry_id` returns identical `signature_id`

## Scenario 4: Retrieve Stored Signature (US2)

```bash
curl http://localhost:8000/signatures/<signature_id>
```

**Expected outcome**:
- HTTP 200 with full WorkloadSignature including schema version
- HTTP 404 for unknown ID

## Scenario 5: Classify Workload (Classification layer)

**Goal**: Map signature to deployment-relevant category.

```bash
curl -X POST http://localhost:8000/classifications \
  -H "Content-Type: application/json" \
  -d '{"signature_id": "<signature_id from Scenario 3>"}'
```

**Expected outcome**:
- HTTP 201 with `classification_id`, `primary_category`, `confidence`, `rationale`
- `rationale` references specific signature dimensions
- Latency-critical fixture → `primary_category: "latency_critical"`

## Scenario 6: Generate Explainable Recommendations (US3)

**Goal**: Produce recommendations via KnowledgeBase rules.

```bash
curl -X POST http://localhost:8000/recommendations \
  -H "Content-Type: application/json" \
  -d '{"classification_id": "<classification_id from Scenario 5>"}'
```

**Expected outcome**:
- HTTP 201 with all five recommendation dimensions
- Each dimension includes `recommendation`, `reasoning`, and `evidence[]`
- Every evidence entry references a `rule_id` from KnowledgeBase
- No autonomous deployment actions triggered

## Scenario 7: Retrieve Recommendation

```bash
curl http://localhost:8000/recommendations/<recommendation_id>
```

**Expected outcome**:
- HTTP 200 with full recommendation including evidence traces
- Domain expert can trace each recommendation to signature attributes without
  reading source code

## Scenario 8: Invalid Input Handling

```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@tests/fixtures/benchmark-invalid-missing-fields.json" \
  -F "provider=json"
```

**Expected outcome**:
- HTTP 422 with clear validation errors
- No partial telemetry or signature state persisted

## Scenario 9: End-to-End Pipeline

Execute Scenarios 1 → 3 → 5 → 6 sequentially using returned IDs.

**Expected outcome**:
- Complete pipeline completes in under 30 seconds for 10 MB input
- Full traceability: telemetry → signature → classification → recommendation

## Scenario 10: Constitution Exclusions Verification

Confirm the running service:
- Does NOT expose Kubernetes controller endpoints
- Does NOT use message queues or async job brokers
- Does NOT connect to live telemetry streams (Prometheus, OTel)
- Does NOT perform autonomous deployment
- Does NOT use ML model endpoints for recommendations

## Provider Registry (informational)

Phase 1 registered Providers: `json`, `csv`.

Future Providers visible in registry documentation but return HTTP 501 if invoked:
`guidellm`, `vllm`, `prometheus`, `opentelemetry`.

## Reference Documents

- [REST API contract](./contracts/rest-api.md)
- [Provider interface](./contracts/provider-interface.md)
- [KnowledgeBase interface](./contracts/knowledge-base-interface.md)
- [Data model](../data-model.md)
