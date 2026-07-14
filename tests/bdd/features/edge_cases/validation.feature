Feature: Input Validation Edge Cases
  As a platform engineer
  I want robust validation of benchmark inputs
  So that invalid data never corrupts the pipeline

  # EARS: Unwanted
  Scenario: IF the JSON file has syntax errors, THEN the system SHALL reject it
    Given a JSON file with invalid syntax
    When the operator posts it to the ingest endpoint
    Then the system shall return HTTP 422
    And the error message shall indicate a parse error

  # EARS: Unwanted
  Scenario: IF the CSV file has wrong delimiters, THEN the system SHALL reject it
    Given a CSV file with semicolon delimiters instead of commas
    When the operator posts it to the ingest endpoint with provider "csv"
    Then the system shall return HTTP 422

  # EARS: Unwanted
  Scenario: IF the CSV file has missing headers, THEN the system SHALL reject it
    Given a CSV file with no header row
    When the operator posts it to the ingest endpoint with provider "csv"
    Then the system shall return HTTP 422

  # EARS: Unwanted
  Scenario: IF the benchmark file has zero records, THEN the system SHALL reject it
    Given a JSON benchmark file with an empty records array
    When the operator posts it to the ingest endpoint
    Then the system shall return HTTP 422
    And the error shall indicate that records cannot be empty

  # EARS: Unwanted
  Scenario: IF gpu_utilization_pct exceeds 100, THEN validation SHALL fail
    Given a benchmark record with gpu_utilization_pct of 150
    When the record is validated
    Then validation shall fail with a range constraint error

  # EARS: Unwanted
  Scenario: IF modality is not a valid enum value, THEN validation SHALL fail
    Given a benchmark record with modality "audio"
    When the record is validated
    Then validation shall fail with an enum constraint error

  # EARS: Event-driven
  Scenario: WHEN benchmark data has conflicting signals, the system SHALL still produce a valid signature
    Given benchmark telemetry with low latency but high context length
    When signature derivation is performed
    Then the system shall produce a valid signature
    And each dimension shall independently reflect its input signals
