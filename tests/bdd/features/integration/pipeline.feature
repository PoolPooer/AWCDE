Feature: End-to-End Pipeline
  As a platform engineer
  I want to run the full pipeline from benchmark ingestion to infrastructure recommendations
  So that I can validate the complete hypothesis

  # EARS: Event-driven
  Scenario: WHEN the full pipeline is executed, the system SHALL produce recommendations from raw telemetry
    Given a valid JSON benchmark file
    When the operator runs the full pipeline
    Then the system shall produce a BenchmarkTelemetry
    And the system shall derive a WorkloadSignature with all 8 dimensions
    And the system shall produce a WorkloadClassification
    And the system shall generate an InfrastructureRecommendation with all 5 dimensions

  # EARS: Ubiquitous
  Scenario: The system SHALL maintain traceability across the full pipeline
    Given a valid JSON benchmark file processed through the full pipeline
    Then the signature shall reference the telemetry_id
    And the classification shall reference the signature_id
    And the recommendation shall reference both classification_id and signature_id

  # EARS: Event-driven
  Scenario: WHEN a latency-critical benchmark is processed end-to-end, the system SHALL recommend appropriate infrastructure
    Given a benchmark file representing a latency-critical workload
    When the operator runs the full pipeline
    Then the classification shall be "latency_critical"
    And the recommendations shall include latency-optimized configuration

  # EARS: Event-driven
  Scenario: WHEN a throughput-oriented benchmark is processed end-to-end, the system SHALL recommend batching
    Given a benchmark file representing a throughput-oriented workload
    When the operator runs the full pipeline
    Then the classification shall be "throughput_optimized"
    And the recommendations shall include batched processing configuration

  # EARS: Ubiquitous
  Scenario: The pipeline SHALL complete within performance bounds
    Given a valid benchmark file under 10 MB
    When the operator runs the full pipeline
    Then the pipeline shall complete within 30 seconds
