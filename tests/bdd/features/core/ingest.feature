Feature: Benchmark Telemetry Ingestion
  As a platform engineer
  I want to ingest AI inference benchmark results via REST API
  So that the system can analyze workload behaviour

  # EARS: Event-driven
  Scenario: WHEN a valid JSON benchmark file is posted, the system SHALL return normalized telemetry
    Given a valid JSON benchmark file
    When the operator posts it to the ingest endpoint with provider "json"
    Then the system shall return a telemetry_id
    And the system shall return normalized benchmark records
    And each record shall contain all 12 required fields

  # EARS: Event-driven
  Scenario: WHEN a valid CSV benchmark file is posted, the system SHALL return normalized telemetry
    Given a valid CSV benchmark file
    When the operator posts it to the ingest endpoint with provider "csv"
    Then the system shall return a telemetry_id
    And the system shall return normalized benchmark records

  # EARS: Event-driven
  Scenario: WHEN equivalent JSON and CSV files are posted, the system SHALL produce identical normalized structures
    Given a valid JSON benchmark file
    And a valid CSV benchmark file with equivalent data
    When both files are ingested through their respective providers
    Then both telemetry records shall contain the same normalized data

  # EARS: Unwanted
  Scenario: IF a malformed JSON file is posted, THEN the system SHALL reject with validation errors
    Given a malformed JSON benchmark file
    When the operator posts it to the ingest endpoint
    Then the system shall return HTTP 422
    And the system shall return field-level validation errors
    And no partial telemetry shall be persisted

  # EARS: Unwanted
  Scenario: IF required benchmark fields are missing, THEN the system SHALL reject with clear errors
    Given a JSON file missing required benchmark fields
    When the operator posts it to the ingest endpoint with provider "json"
    Then the system shall return HTTP 422
    And the error response shall identify the missing fields

  # EARS: Ubiquitous
  Scenario: The system SHALL validate all numeric fields are non-negative
    Given a benchmark file with negative latency values
    When the operator posts it to the ingest endpoint
    Then the system shall reject the file with a validation error

  # EARS: Ubiquitous
  Scenario: The system SHALL enforce latency_p99 >= latency_p50
    Given a benchmark record with p99 latency less than p50
    When the record is validated
    Then validation shall fail with a constraint error

  # EARS: Ubiquitous
  Scenario: The system SHALL enforce context_length_p99 >= context_length_p50
    Given a benchmark record with p99 context length less than p50
    When the record is validated
    Then validation shall fail with a constraint error

  # EARS: Event-driven
  Scenario: WHEN the operator requests the provider list, the system SHALL return available providers
    When the operator requests the list of available providers
    Then the system shall return at least 2 providers
    And the provider list shall include "json" and "csv"
