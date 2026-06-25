# REST API Contract

**Version**: 1.0.0  
**Base URL**: `http://localhost:8000`  
**Framework**: FastAPI (single application, modular monolith)

Primary interface for AWCDE MVP. CLI is deferred to a later phase.

## Pipeline Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/ingest` | Ingest benchmark telemetry via Provider |
| POST | `/signatures` | Derive workload signature from telemetry |
| GET | `/signatures/{id}` | Retrieve stored signature |
| POST | `/classifications` | Classify a stored signature |
| GET | `/classifications/{id}` | Retrieve classification result |
| POST | `/recommendations` | Generate recommendations from classification |
| GET | `/recommendations/{id}` | Retrieve recommendation result |
| GET | `/health` | Service health check |
| GET | `/providers` | List registered Providers and status |

---

## POST /ingest

Ingest benchmark telemetry using a registered Provider.

**Request** (multipart/form-data):
- `file`: benchmark file upload
- `provider`: Provider ID (`json` or `csv` for Phase 1)

**Response** 201:
```json
{
  "telemetry_id": "tel_abc123",
  "provider_id": "json",
  "source_ref": "benchmark-latency-critical.json",
  "record_count": 1,
  "records": [ "..." ]
}
```

**Errors**: 422 validation failure, 400 unsupported provider

---

## POST /signatures

Derive a versioned workload signature from ingested telemetry.

**Request**:
```json
{ "telemetry_id": "tel_abc123" }
```

**Response** 201: WorkloadSignature (see [workload-signature.schema.md](./workload-signature.schema.md))

---

## GET /signatures/{id}

Retrieve a stored WorkloadSignature by ID.

**Response** 200: WorkloadSignature  
**Errors** 404 not found

---

## POST /classifications

Classify a stored workload signature into deployment-relevant categories.

**Request**:
```json
{ "signature_id": "sig_def456" }
```

**Response** 201: WorkloadClassification (see [workload-classification.schema.md](./workload-classification.schema.md))

---

## GET /classifications/{id}

Retrieve a stored WorkloadClassification.

**Response** 200: WorkloadClassification  
**Errors** 404 not found

---

## POST /recommendations

Generate explainable infrastructure recommendations by consulting KnowledgeBase rules
against a WorkloadClassification and its source WorkloadSignature.

**Request**:
```json
{ "classification_id": "cls_ghi789" }
```

**Response** 201: InfrastructureRecommendation (see [recommendation-output.schema.md](./recommendation-output.schema.md))

---

## GET /recommendations/{id}

Retrieve a stored InfrastructureRecommendation.

**Response** 200: InfrastructureRecommendation  
**Errors** 404 not found

---

## GET /providers

List registered Providers.

**Response** 200:
```json
{
  "providers": [
    { "provider_id": "json", "status": "active", "formats": [".json"] },
    { "provider_id": "csv", "status": "active", "formats": [".csv"] },
    { "provider_id": "guidellm", "status": "planned", "formats": [] },
    { "provider_id": "vllm", "status": "planned", "formats": [] },
    { "provider_id": "prometheus", "status": "planned", "formats": [] },
    { "provider_id": "opentelemetry", "status": "planned", "formats": [] }
  ]
}
```

Phase 1: only `json` and `csv` are active. Planned Providers return HTTP 501 if invoked.

---

## Constitution Constraints

- No autonomous deployment endpoints
- No Kubernetes controller APIs
- No message queue or async job submission endpoints
- No live telemetry stream endpoints (WebSocket, SSE) in Phase 1
- No ML inference or black-box scoring endpoints
