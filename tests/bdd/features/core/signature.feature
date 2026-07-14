Feature: Workload Signature Derivation
  As a platform engineer
  I want to derive versioned workload signatures from benchmark telemetry
  So that workload behaviour is captured in a standardized, reusable form

  # EARS: Event-driven
  Scenario: WHEN signature derivation is requested for ingested telemetry, the system SHALL return a complete signature
    Given ingested benchmark telemetry
    When the operator requests signature derivation
    Then the system shall return a WorkloadSignature
    And the signature shall contain all 8 dimensions
    And each dimension shall have a level, score, and raw_inputs
    And the signature shall carry a schema_version

  # EARS: Ubiquitous
  Scenario: The system SHALL produce deterministic signature IDs for identical input
    Given ingested benchmark telemetry
    When signature derivation is run twice on the same telemetry
    Then both signatures shall have the same id

  # EARS: Event-driven
  Scenario: WHEN a stored signature is retrieved by ID, the system SHALL return the full signature
    Given a stored workload signature
    When the operator retrieves it by id
    Then the system shall return the full signature with schema version intact
    And all 8 dimensions shall be present

  # EARS: Ubiquitous
  Scenario: The system SHALL assign dimension scores between 0.0 and 1.0
    Given ingested benchmark telemetry
    When signature derivation is performed
    Then all dimension scores shall be between 0.0 and 1.0 inclusive

  # EARS: Ubiquitous
  Scenario: The system SHALL assign valid dimension levels
    Given ingested benchmark telemetry
    When signature derivation is performed
    Then each dimension level shall be one of "low", "medium", or "high"

  # EARS: Event-driven
  Scenario: WHEN telemetry has high latency variance, the system SHALL score latency sensitivity as high
    Given benchmark telemetry with high latency variance
    When signature derivation is performed
    Then the latency_sensitivity dimension shall have level "high"

  # EARS: Event-driven
  Scenario: WHEN telemetry has bursty arrival pattern, the system SHALL reflect this in burst behaviour
    Given benchmark telemetry with bursty arrival pattern
    When signature derivation is performed
    Then the burst_behaviour dimension shall have a score above 0.5
