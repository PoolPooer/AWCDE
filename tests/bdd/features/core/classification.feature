Feature: Workload Classification
  As a platform engineer
  I want workload signatures classified into deployment-relevant categories
  So that I can understand the workload's primary characteristics

  # EARS: Event-driven
  Scenario: WHEN a signature is classified, the system SHALL return a classification with category and confidence
    Given a stored workload signature
    When the operator requests classification
    Then the system shall return a WorkloadClassification
    And the classification shall have a primary_category
    And the classification shall have a confidence between 0.0 and 1.0
    And the classification shall have a human-readable rationale

  # EARS: Event-driven
  Scenario: WHEN a signature has high latency sensitivity, the system SHALL classify as latency_critical
    Given a workload signature with high latency sensitivity
    When the operator requests classification
    Then the primary_category shall be "latency_critical"

  # EARS: Event-driven
  Scenario: WHEN a signature has high throughput orientation, the system SHALL classify as throughput_optimized
    Given a workload signature with high throughput orientation
    When the operator requests classification
    Then the primary_category shall be "throughput_optimized"

  # EARS: Event-driven
  Scenario: WHEN a signature has high memory intensity, the system SHALL classify as memory_intensive
    Given a workload signature with high memory intensity
    When the operator requests classification
    Then the primary_category shall be "memory_intensive"

  # EARS: Event-driven
  Scenario: WHEN a signature has high burst behaviour, the system SHALL classify as burst_tolerant
    Given a workload signature with high burst behaviour
    When the operator requests classification
    Then the primary_category shall be "burst_tolerant"

  # EARS: State-driven
  Scenario: WHILE no single dimension dominates, the system SHALL classify as general_purpose
    Given a workload signature with balanced dimensions
    When the operator requests classification
    Then the primary_category shall be "general_purpose"

  # EARS: Ubiquitous
  Scenario: The system SHALL include dimension summary in every classification
    Given any workload signature
    When the operator requests classification
    Then the classification shall include a dimension_summary with key scores

  # EARS: Ubiquitous
  Scenario: The system SHALL reference at least one signature dimension in the rationale
    Given any workload signature
    When the operator requests classification
    Then the rationale shall reference at least one dimension name
