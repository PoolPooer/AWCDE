Feature: Error Handling and Graceful Degradation
  As a platform engineer
  I want the system to handle error conditions gracefully
  So that failures are clear and never produce corrupt state

  # EARS: Unwanted
  Scenario: IF a non-existent signature ID is requested, THEN the system SHALL return 404
    When the operator requests signature with id "nonexistent-id"
    Then the system shall return HTTP 404
    And the error message shall identify the missing entity type

  # EARS: Unwanted
  Scenario: IF a non-existent classification ID is requested, THEN the system SHALL return 404
    When the operator requests classification with id "nonexistent-id"
    Then the system shall return HTTP 404

  # EARS: Unwanted
  Scenario: IF a non-existent recommendation ID is requested, THEN the system SHALL return 404
    When the operator requests recommendation with id "nonexistent-id"
    Then the system shall return HTTP 404

  # EARS: Unwanted
  Scenario: IF an unknown provider is specified, THEN the system SHALL return an error
    Given a valid JSON benchmark file
    When the operator posts it with provider "unknown_provider"
    Then the system shall return an error indicating the provider is not found

  # EARS: Event-driven
  Scenario: WHEN the same benchmark file is re-ingested, the system SHALL produce identical signatures
    Given a valid JSON benchmark file
    When the file is ingested twice
    Then both resulting signatures shall have the same id
    And the system shall not create duplicate entries

  # EARS: Optional
  Scenario: WHERE no KnowledgeBase rules are loaded, the system SHALL provide default recommendations
    Given an empty KnowledgeBase
    And a stored workload classification
    When the operator requests recommendations
    Then the system shall return recommendations with fallback reasoning
