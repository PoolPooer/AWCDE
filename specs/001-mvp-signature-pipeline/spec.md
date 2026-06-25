# Feature Specification: AWCDE MVP — Benchmark-to-Recommendation Pipeline

**Feature Branch**: `001-mvp-signature-pipeline`

**Created**: 2026-06-24

**Status**: Draft

**Input**: User description: "MVP shall ingest benchmark telemetry from JSON and CSV files, derive a versioned workload signature, store workload signatures, and generate explainable infrastructure recommendations. Single FastAPI application following AWCDE constitution."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ingest Benchmark Telemetry (Priority: P1)

Platform engineer uploads AI inference benchmark results as JSON or CSV files via the
REST API. The system validates structure, normalizes telemetry through Provider
adapters, and reports validation errors clearly.

**Why this priority**: Ingestion is the foundation; without validated input, signatures
and recommendations cannot be trusted.

**Independent Test**: POST valid and invalid sample files to `/ingest`; valid files
produce normalized benchmark records; invalid files produce actionable field-level
error messages without partial state corruption.

**Acceptance Scenarios**:

1. **Given** a valid JSON benchmark file, **When** the operator POSTs it to `/ingest`
   with `provider=json`, **Then** the system returns a `telemetry_id` and normalized
   benchmark records
2. **Given** a valid CSV benchmark file with equivalent data, **When** the operator
   POSTs it to `/ingest` with `provider=csv`, **Then** the system produces the same
   normalized structure as the JSON input
3. **Given** a malformed or schema-invalid file, **When** the operator POSTs it to
   `/ingest`, **Then** the system returns HTTP 422 with clear validation errors and
   persists no partial telemetry

---

### User Story 2 - Derive and Store Versioned Workload Signatures (Priority: P2)

System transforms normalized benchmark telemetry into a versioned workload signature
with eight profile dimensions and persists it for later retrieval.

**Why this priority**: Versioned, reusable signatures are the core artifact AWCDE
exists to validate.

**Independent Test**: POST `/signatures` with a `telemetry_id`; GET `/signatures/{id}`
returns all eight dimensions with schema version; identical input produces identical
signature ID.

**Acceptance Scenarios**:

1. **Given** ingested benchmark telemetry, **When** the operator POSTs to
   `/signatures`, **Then** a WorkloadSignature is returned with all eight dimensions,
   `schema_version`, and deterministic `id`
2. **Given** a stored signature ID, **When** the operator GETs `/signatures/{id}`,
   **Then** the full signature is returned with schema version intact
3. **Given** identical benchmark input and schema version, **When** signature
   derivation is run twice, **Then** both runs produce the same signature ID

---

### User Story 3 - Classify and Recommend with Explainability (Priority: P3)

System classifies a stored workload signature into deployment-relevant categories,
then generates explainable infrastructure recommendations by consulting KnowledgeBase
rules. Every recommendation includes human-readable reasoning and supporting evidence.

**Why this priority**: Validates the core hypothesis that signatures can drive
explainable deployment guidance.

**Independent Test**: POST `/classifications` then POST `/recommendations`; response
includes all five recommendation dimensions, each with reasoning and KnowledgeBase
evidence traceable to signature attributes.

**Acceptance Scenarios**:

1. **Given** a stored signature with high latency sensitivity, **When** the operator
   POSTs to `/classifications`, **Then** a WorkloadClassification is returned with
   `primary_category`, `confidence`, and human-readable `rationale`
2. **Given** a stored classification, **When** the operator POSTs to
   `/recommendations`, **Then** recommendations cover model family, runtime, hardware
   suitability, deployment topology, and scheduling policy
3. **Given** a generated recommendation set, **When** a domain expert reviews the
   output, **Then** every dimension includes reasoning and evidence referencing
   KnowledgeBase rule IDs and signature attributes — without reading source code
4. **Given** any recommendation response, **When** reviewed, **Then** no autonomous
   deployment or actuation is triggered

### Edge Cases

- Malformed JSON or CSV (syntax errors, wrong delimiter, missing headers)
- Valid file format but missing required benchmark fields
- Benchmark data with conflicting signals (e.g., low latency requirement but high
  context length)
- Empty or zero-row benchmark files
- Re-ingestion of the same benchmark file (idempotent signature generation)
- Signature schema version mismatch on retrieval
- Signature dimensions that cannot be derived from available telemetry (partial
  signature with explicit gaps noted)
- Classification when signature has incomplete dimensions
- Recommendation when no KnowledgeBase rule matches (graceful fallback with explanation)

## Requirements *(mandatory)*

### Constitution Alignment

This feature complies with AWCDE constitution v1.0.0:

- MVP First: end-to-end slice only (ingest → signature → classification → recommend)
- Single Application Architecture: one FastAPI process, no microservices or MQ
- Explainable Rule-Based Recommendations: KnowledgeBase rules with reasoning and evidence
- Versioned Workload Signatures: schema version and deterministic identifier
- Realistic Data Ingestion First: JSONProvider and CSVProvider file input only
- Phase 1 Scope Exclusions: no K8s, MQ, autonomous deploy, live telemetry, or ML

### Functional Requirements

**Ingestion (Providers)**
- **FR-001**: System MUST accept benchmark telemetry from JSON files via JSONProvider
- **FR-002**: System MUST accept benchmark telemetry from CSV files via CSVProvider
- **FR-003**: System MUST validate ingested files against a documented benchmark schema
  and reject invalid input with clear error messages
- **FR-004**: System MUST normalize valid benchmark telemetry into BenchmarkTelemetry
- **FR-005**: System MUST expose ingestion via REST API (`POST /ingest`)

**Signatures**
- **FR-006**: System MUST derive a WorkloadSignature from normalized benchmark telemetry
- **FR-007**: Workload signatures MUST include all eight dimensions: latency
  sensitivity, throughput orientation, memory intensity, burst behaviour, context
  length profile, concurrency profile, hardware affinity, modality
- **FR-008**: Every workload signature MUST carry a schema version and stable identifier
- **FR-009**: System MUST persist workload signatures for later retrieval
- **FR-010**: Identical benchmark input MUST produce identical signatures under the same
  schema version
- **FR-011**: System MUST expose signature derivation and retrieval via REST API
  (`POST /signatures`, `GET /signatures/{id}`)

**Classification**
- **FR-012**: System MUST classify a WorkloadSignature into a WorkloadClassification
  with primary category, confidence, and rationale
- **FR-013**: System MUST expose classification via REST API (`POST /classifications`,
  `GET /classifications/{id}`)

**Recommendations (KnowledgeBase)**
- **FR-014**: System MUST generate recommendations by consulting KnowledgeBase rules
  against WorkloadClassification and WorkloadSignature
- **FR-015**: Recommendations MUST cover model family, runtime, hardware suitability,
  deployment topology, and scheduling policy
- **FR-016**: Every recommendation dimension MUST include human-readable reasoning
- **FR-017**: Every recommendation dimension MUST include supporting evidence
  referencing KnowledgeBase rule IDs and signature/classification attributes
- **FR-018**: System MUST NOT perform autonomous deployment or actuation
- **FR-019**: System MUST expose recommendation generation via REST API
  (`POST /recommendations`, `GET /recommendations/{id}`)

**Architecture & Constitution**
- **FR-020**: MVP MUST be delivered as a single FastAPI application
- **FR-021**: System MUST NOT use ML or black-box models for recommendations in Phase 1
- **FR-022**: System MUST NOT ingest live telemetry streams in Phase 1
- **FR-023**: Provider architecture MUST allow future providers (GuideLLM, vLLM,
  Prometheus, OpenTelemetry) without Phase 1 implementation

### Key Entities

- **BenchmarkTelemetry**: Normalized inference benchmark measurements from Provider ingestion
- **Provider**: Adapter for telemetry source formats (JSONProvider, CSVProvider in Phase 1)
- **WorkloadSignature**: Versioned characterization with eight profile dimensions
- **WorkloadClassification**: Deployment-relevant category derived from a signature
- **KnowledgeBase**: First-class domain concept holding static recommendation rules
- **InfrastructureRecommendation**: Advisory deployment guidance across five dimensions
- **RecommendationEvidence**: Traceable link between recommendation, KnowledgeBase rule,
  and signature/classification attributes

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Operator can ingest a valid benchmark file via REST API and receive
  normalized records within 30 seconds for files up to 10 MB
- **SC-002**: 100% of valid benchmark ingests produce a workload signature containing
  all eight required dimensions
- **SC-003**: Stored signatures are retrievable by identifier with schema version intact
- **SC-004**: 100% of generated recommendation sets include all five recommendation
  dimensions, each with reasoning and supporting evidence
- **SC-005**: A domain expert can trace every recommendation back to at least one
  KnowledgeBase rule and signature attribute without inspecting source code
- **SC-006**: Re-running signature derivation on identical benchmark input produces
  identical signatures (determinism)
- **SC-007**: Full pipeline (ingest → signature → classification → recommendation)
  completes end-to-end via REST API

## Assumptions

- Target users are platform/ML ops engineers using HTTP clients or API tools
- Benchmark files represent realistic AI inference workloads
- Initial benchmark schema defined in plan contracts
- Signature storage is local SQLite within the single application
- KnowledgeBase starts with static YAML rules; grows iteratively
- REST API is primary interface; CLI deferred to later phase
- Phase 1 exclusions apply: no Kubernetes controllers, message queues, autonomous
  deployment, live telemetry streams, or production self-tuning
