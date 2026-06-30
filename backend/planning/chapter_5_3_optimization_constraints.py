"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 5.3: Optimization Constraints
==========================================

Defines the constraints that govern execution optimization within the
Execution Layer.

==============================================================================
Purpose
==============================================================================

Optimization operates only within the constraints approved by the Planning
Layer. The Execution Layer may improve execution efficiency, but it shall
never violate predefined execution constraints.

=======================================================================
Constraint Categories
=======================================================================

| Constraint           | Description                                                    |
|----------------------|----------------------------------------------------------------|
| Budget Constraints   | Execution shall remain within approved cost limits, including   |
|                      | financial budgets, token usage, API costs, infrastructure       |
|                      | expenses, or other allocated resources.                         |
| Resource Constraints | Execution shall respect available resources such as compute     |
|                      | capacity, execution time, personnel availability, system        |
|                      | throughput, and external dependencies.                          |
| Policy Constraints   | Execution shall comply with organisational policies, security   |
|                      | requirements, legal restrictions, compliance rules, and         |
|                      | execution permissions.                                          |

==============================================================================
Optimization Boundary
==============================================================================

Execution optimization shall never:

- exceed approved budgets
- consume unavailable resources
- violate defined policies
- modify planning decisions

When multiple constraints cannot be fully optimized simultaneously, the
Execution Layer shall select the execution strategy that best satisfies the
optimization objectives while remaining within the approved constraints.

==============================================================================
Design Principle
==============================================================================

> Constraints take precedence over optimization objectives.

Execution optimization is a constrained optimization process. Optimization
may improve execution efficiency only within the boundaries approved by the
Planning Layer. Constraint compliance shall always have higher priority
than optimization gains.