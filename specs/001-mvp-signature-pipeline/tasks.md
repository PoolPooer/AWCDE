# Tasks: AWCDE MVP — Benchmark-to-Recommendation Pipeline

**Input**: Design documents from `/specs/001-mvp-signature-pipeline/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Architecture**: FastAPI backend-first single application. Pipeline:
`BenchmarkTelemetry → WorkloadSignature → WorkloadClassification → InfrastructureRecommendation`

**Tests**: OPTIONAL — not requested in spec. No test tasks included.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label ([US1], [US2], [US3])

## Path Conventions

Single FastAPI application under `src/awcde/`. REST API is primary interface; CLI deferred.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and FastAPI application skeleton

- [ ] T001 Create `pyproject.toml` with Python 3.12, FastAPI, Uvicorn, Pydantic v2 dependencies
- [ ] T002 Create `src/awcde/` package structure per plan.md (api, providers, signatures, classification, knowledge, recommendations, storage, models)
- [ ] T003 [P] Create `tests/fixtures/` with sample benchmark JSON and CSV files
- [ ] T004 [P] Configure ruff/black in `pyproject.toml`
- [ ] T005 Create `README.md` with project overview, API startup, and install instructions
- [ ] T006 Create FastAPI app entrypoint in `src/awcde/main.py` with health check route

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain models, Provider registry, KnowledgeBase, storage, and API skeleton

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Define Pydantic models in `src/awcde/models/telemetry.py`, `signature.py`, `classification.py`, `recommendation.py`, `knowledge.py`
- [ ] T008 Implement SQLite storage layer in `src/awcde/storage/repository.py`
- [ ] T009 [P] Implement Provider protocol and registry in `src/awcde/providers/base.py` and `src/awcde/providers/registry.py`
- [ ] T010 [P] Implement KnowledgeBase protocol in `src/awcde/knowledge/base.py`
- [ ] T011 [P] Implement StaticKnowledgeBase with YAML loader in `src/awcde/knowledge/static_kb.py`
- [ ] T012 [P] Create initial static rules in `data/knowledge/rules.yaml`
- [ ] T013 [P] Implement signature schema versioning in `src/awcde/signatures/schema.py`
- [ ] T014 Implement classification taxonomy in `src/awcde/classification/categories.py`
- [ ] T015 Wire API router skeleton in `src/awcde/api/routes/` with dependency injection in `src/awcde/api/dependencies.py`
- [ ] T016 [P] Add shared API error handling in `src/awcde/api/errors.py`

**Checkpoint**: Foundation ready — Provider registry, KnowledgeBase, models, and storage operational

---

## Phase 3: User Story 1 — Ingest Benchmark Telemetry (Priority: P1) 🎯 MVP

**Goal**: Operator ingests JSON/CSV benchmark files via REST API using Provider adapters

**Independent Test**: POST valid/invalid files to `/ingest`; valid files return normalized telemetry; invalid files return field-level errors

### Implementation for User Story 1

- [ ] T017 [P] [US1] Implement JSONProvider in `src/awcde/providers/json_provider.py`
- [ ] T018 [P] [US1] Implement CSVProvider in `src/awcde/providers/csv_provider.py`
- [ ] T019 [US1] Register JSONProvider and CSVProvider in `src/awcde/providers/registry.py`
- [ ] T020 [US1] Implement ingest route in `src/awcde/api/routes/ingest.py` (POST /ingest)
- [ ] T021 [US1] Implement providers listing route in `src/awcde/api/routes/ingest.py` (GET /providers)
- [ ] T022 [US1] Add structured validation error responses for Provider failures

**Checkpoint**: JSON and CSV ingestion independently testable via REST API

---

## Phase 4: User Story 2 — Derive and Store Workload Signatures (Priority: P2)

**Goal**: Transform ingested telemetry into versioned, persisted workload signatures retrievable by ID

**Independent Test**: POST /signatures with telemetry_id; GET /signatures/{id} returns all 8 dimensions; identical input produces identical signature ID

### Implementation for User Story 2

- [ ] T023 [P] [US2] Implement 8-dimension derivation in `src/awcde/signatures/derivation.py`
- [ ] T024 [US2] Implement deterministic signature ID in `src/awcde/signatures/identity.py`
- [ ] T025 [US2] Implement signature service orchestration in `src/awcde/signatures/service.py`
- [ ] T026 [US2] Wire signature routes in `src/awcde/api/routes/signatures.py` (POST /signatures, GET /signatures/{id})

**Checkpoint**: Signatures derived, stored, and retrievable with schema version intact

---

## Phase 5: User Story 3 — Classify and Recommend (Priority: P3)

**Goal**: Classify signatures into deployment categories, then generate explainable recommendations via KnowledgeBase

**Independent Test**: POST /classifications then POST /recommendations; all 5 recommendation dimensions include reasoning and KnowledgeBase evidence

### Implementation for User Story 3

- [ ] T027 [P] [US3] Implement WorkloadClassifier in `src/awcde/classification/classifier.py`
- [ ] T028 [US3] Wire classification routes in `src/awcde/api/routes/classifications.py` (POST /classifications, GET /classifications/{id})
- [ ] T029 [P] [US3] Implement recommendation engine (KnowledgeBase consult) in `src/awcde/recommendations/engine.py`
- [ ] T030 [P] [US3] Implement explanation builder in `src/awcde/recommendations/explainer.py`
- [ ] T031 [P] [US3] Implement evidence trace collector in `src/awcde/recommendations/evidence.py`
- [ ] T032 [US3] Wire recommendation routes in `src/awcde/api/routes/recommendations.py` (POST /recommendations, GET /recommendations/{id})

**Checkpoint**: Full pipeline operational — telemetry → signature → classification → recommendation with explainability

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation, rule coverage, constitution compliance verification

- [ ] T033 [P] Validate all quickstart.md scenarios against running service
- [ ] T034 [P] Expand `data/knowledge/rules.yaml` to cover all 5 recommendation dimensions and 6 classification categories
- [ ] T035 Verify Phase 1 exclusions in codebase (no MQ, K8s, ML, live telemetry, autonomous deploy)
- [ ] T036 Register future Provider stubs (GuideLLM, vLLM, Prometheus, OpenTelemetry) returning HTTP 501 in `src/awcde/providers/registry.py`
- [ ] T037 Update `specs/001-mvp-signature-pipeline/quickstart.md` with any path corrections from validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **User Stories (Phase 3–5)**: All depend on Foundational completion
  - Sequential priority: US1 → US2 → US3 (each builds on prior artifacts)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: After Foundational — no dependency on other stories
- **US2 (P2)**: After Foundational — requires ingested telemetry from US1 for integration testing
- **US3 (P3)**: After Foundational — requires stored signatures (US2) and classifications for full pipeline

### Parallel Opportunities

- T017/T018: JSONProvider and CSVProvider in parallel
- T027/T029/T030/T031: Classifier, engine, explainer, evidence modules partially parallel
- T033/T034: Quickstart validation and rule expansion in parallel

---

## Parallel Example: User Story 1

```bash
# Launch both Providers together:
Task: "Implement JSONProvider in src/awcde/providers/json_provider.py"
Task: "Implement CSVProvider in src/awcde/providers/csv_provider.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (ingest via REST)
4. **STOP and VALIDATE**: POST /ingest with JSON and CSV fixtures

### Full Hypothesis Validation

1. Setup + Foundational
2. US1 → US2 → US3 sequentially
3. Validate full pipeline per quickstart.md Scenario 9
4. Polish phase for rule coverage and constitution verification

### Deferred (Not Phase 1)

- CLI interface (Typer commands)
- GuideLLMProvider, vLLMProvider, PrometheusProvider, OpenTelemetryProvider
- ML or learned recommendations
- Live telemetry streams

---

## Notes

- Constitution-driven task types: Provider adapters, signature schema versioning, classification layer, KnowledgeBase rules, explainability/evidence
- Recommendation engine MUST consult KnowledgeBase — no hard-coded reasoning in engine
- CLI explicitly deferred; REST API is the Phase 1 interface
