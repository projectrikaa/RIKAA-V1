"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 5.5: Optimization Process
=========================================

Defines the standard process used by the Execution Layer to produce an
optimized execution recommendation.

This chapter describes how optimization is performed, not planning or
decision making.

==============================================================================
Purpose
==============================================================================

Optimization Process defines the standard process used by the Execution
Layer to produce an optimized execution recommendation.

It describes how optimization is performed — how candidate strategies are
evaluated, compared, and recommended — without making planning decisions or
introducing new decision authority.

==============================================================================
Input
==============================================================================

The Optimization Process accepts only approved planning artifacts:

- Approved Decision Blueprint (Chapter 3)
- Execution Context (Chapter 4)
- Optimization Objectives (Chapter 5.2)
- Optimization Constraints (Chapter 5.3)
- Optimization Factors (Chapter 5.4)

No new planning inputs are introduced. The process operates exclusively on
artifacts produced by the Planning Layer and the Execution Layer's own
optimization specification.

==============================================================================
Evaluation
==============================================================================

Candidate execution strategies are evaluated using:

- Optimization Objectives: The goals that define what should be optimised
  for a given execution context.

- Optimization Constraints: The boundaries that define the permitted
  execution space within which strategies must operate.

- Optimization Factors: The criteria used to measure and compare the
  expected performance of each candidate.

Evaluation applies the same criteria to every candidate strategy. The
evaluation process is deterministic: identical candidates and inputs produce
identical evaluation outcomes.

The Evaluation section defines the evaluation process only. It does not rank
or select a strategy.

==============================================================================
Recommendation
==============================================================================

After evaluation, the evaluated candidates are compared to produce an
execution recommendation. The recommendation identifies the strategy that
best satisfies the optimization objectives while remaining within the
approved constraints.

The Optimization Process may recommend an execution strategy but shall not
modify or replace the approved Decision Blueprint.

The recommendation supports execution only. It does not constitute a new
planning decision, override approved objectives, or alter the scope of the
Decision Blueprint.

==============================================================================
Output
==============================================================================

The Optimization Process produces the following outputs:

- Recommended Execution Strategy: The execution strategy selected through
  the optimization process.

- Alternative Strategies: Other viable strategies that were evaluated but
  not selected, preserved for reference.

- Trade-off Analysis: Documentation of the trade-offs considered during
  evaluation and recommendation.

- Expected Execution Outcome: The anticipated result of executing the
  recommended strategy.

- Supporting Rationale: The reasoning that justifies the recommendation,
  including how objectives, constraints, and factors were applied.

All outputs remain within the Execution Layer. No output modifies planning
decisions or the Decision Blueprint.

==============================================================================
Dependencies
==============================================================================

The Optimization Process depends on:

- Chapter 3: Decision Blueprint — provides the approved planning output
  that the process executes against.

- Chapter 4: Execution Layer — provides the execution infrastructure and
  mechanisms.

- Chapter 5.2: Optimization Objectives — defines the goals that guide
  execution strategy selection.

- Chapter 5.3: Optimization Constraints — defines the boundaries within
  which execution optimization must operate.

- Chapter 5.4: Optimization Factors — defines the criteria used to
  evaluate and compare candidate execution strategies.

The Optimization Process does not introduce dependencies on any external
system, runtime, or implementation technology.

==============================================================================
Execution Principles
==============================================================================

The Optimization Process adheres to the following execution principles:

a) Blueprint Preservation

   The process never modifies the approved Decision Blueprint. It selects
   among execution strategies that already satisfy the Blueprint.

b) Constraint Compliance

   Every candidate strategy is validated against Optimization Constraints
   before evaluation. Strategies that violate constraints are excluded.

c) Objective Alignment

   The recommendation is aligned with the Optimization Objectives. The
   process does not introduce new objectives during evaluation.

d) Deterministic Evaluation

   Identical inputs produce identical evaluation outcomes. The process is
   repeatable and verifiable.

e) Execution Only

   The process operates strictly within the Execution Layer. It does not
   make planning decisions, approve new work, or modify planning outputs.
