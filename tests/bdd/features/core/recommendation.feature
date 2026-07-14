Feature: Infrastructure Recommendations
  As a platform engineer
  I want explainable infrastructure recommendations based on workload classification
  So that I can make informed deployment decisions without reading source code

  # EARS: Event-driven
  Scenario: WHEN recommendations are generated, the system SHALL cover all 5 dimensions
    Given a stored workload classification
    When the operator requests recommendations
    Then the system shall return an InfrastructureRecommendation
    And the recommendation shall include model_family
    And the recommendation shall include runtime
    And the recommendation shall include hardware_suitability
    And the recommendation shall include deployment_topology
    And the recommendation shall include scheduling_policy

  # EARS: Ubiquitous
  Scenario: The system SHALL include reasoning in every recommendation dimension
    Given a stored workload classification
    When the operator requests recommendations
    Then every recommendation dimension shall have non-empty reasoning

  # EARS: Ubiquitous
  Scenario: The system SHALL include evidence in every recommendation dimension
    Given a stored workload classification
    When the operator requests recommendations
    Then every recommendation dimension shall have at least one evidence entry

  # EARS: Ubiquitous
  Scenario: The system SHALL trace every evidence entry to a KnowledgeBase rule
    Given a stored workload classification
    When the operator requests recommendations
    Then every evidence entry shall reference a rule_id
    And every evidence entry shall reference a source_type
    And every evidence entry shall include the matched attribute and value

  # EARS: Event-driven
  Scenario: WHEN a latency-critical workload is classified, the system SHALL recommend low-latency configuration
    Given a workload classified as "latency_critical"
    When the operator requests recommendations
    Then the runtime recommendation shall reference low-latency configuration

  # EARS: Unwanted
  Scenario: IF no KnowledgeBase rule matches, THEN the system SHALL provide fallback recommendations
    Given a classification with no matching KnowledgeBase rules
    When the operator requests recommendations
    Then the system shall still return all 5 recommendation dimensions
    And the reasoning shall explain that no specific rules matched

  # EARS: Ubiquitous
  Scenario: The system SHALL NOT perform autonomous deployment or actuation
    Given any recommendation response
    When reviewed
    Then no deployment action shall have been triggered
    And the response shall be advisory only
