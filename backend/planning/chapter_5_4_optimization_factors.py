"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 5.4: Optimization Factors
=========================================

Defines the evaluation dimensions used by the Execution Layer to compare and
select execution strategies.

This chapter does NOT redefine planning decisions, optimization objectives,
or execution constraints. Optimization Factors are only used to evaluate
candidate execution strategies that already satisfy the approved Decision
Blueprint.

==============================================================================
Purpose
==============================================================================

Optimization Factors define the criteria used to evaluate and compare
candidate execution strategies.

Their purpose is to support deterministic execution selection while
remaining within the Optimization Objectives (Chapter 5.2) and Optimization
Constraints (Chapter 5.3).

Optimization Factors do not modify planning decisions or create new
objectives.

==============================================================================
Relationship
==============================================================================

Optimization Factors operate within the following architectural hierarchy:

Decision Blueprint
        │
        ▼
Optimization Objectives
        │
        ▼
Optimization Constraints
        │
        ▼
Optimization Factors
        │
        ▼
Selected Execution Strategy

Objectives define what should be optimised. Constraints define the permitted
execution space. Factors define how candidate strategies are evaluated.

Each layer depends on the layer above. Factors never override Objectives or
Constraints.

==============================================================================
Core Factors
==============================================================================

1. Evaluation Factors
---------------------

Purpose: Measure the expected performance of each candidate execution
strategy.

Typical evaluation dimensions include:

- Execution Time
- Resource Usage
- Reliability
- Output Quality
- Predictability

The framework does not mandate specific metrics. Implementations MAY
introduce additional measurable evaluation factors when appropriate.

2. Trade-off Factors
--------------------

Purpose: Describe how candidate strategies are compared when optimization
objectives conflict.

Common trade-off comparisons include:

- Speed vs Accuracy
- Cost vs Quality
- Latency vs Resource Usage

Trade-off Factors do not define organisational policy. They provide
comparison principles between otherwise valid execution strategies. The
actual resolution of trade-offs is determined by policy, not by the factor
framework.

3. Priority Factors
-------------------

Purpose: Define precedence when trade-offs cannot satisfy every optimization
objective simultaneously.

Priority ordering provides deterministic conflict resolution. When two
candidate strategies each satisfy different objectives, priority factors
determine which strategy is selected.

A representative priority chain is illustrated below:

Reliability
    ↓
Quality
    ↓
Efficiency

Actual priority ordering is implementation-specific. The framework defines
the mechanism for expressing precedence, not the specific ordering itself.

==============================================================================
Processing Flow
==============================================================================

Candidate strategies flow through a deterministic evaluation pipeline:

Candidate Strategies
        │
        ▼
Evaluation
        │
        ▼
Trade-off Analysis
        │
        ▼
Priority Resolution
        │
        ▼
Selected Execution Strategy

Every candidate is evaluated using the same factor set before selection.
The evaluation is repeatable: identical candidates and factors produce
identical selection outcomes.

==============================================================================
Responsibilities
==============================================================================

Optimization Factors SHALL:

- Evaluate candidate strategies
- Compare execution alternatives
- Resolve optimization conflicts
- Support deterministic strategy selection

Optimization Factors SHALL NOT:

- Modify Decision Blueprints
- Create new Optimization Objectives
- Relax Optimization Constraints
- Approve new planning decisions

==============================================================================
Dependencies
==============================================================================

Depends on:

- Chapter 3: Decision Blueprint
- Chapter 5.2: Optimization Objectives
- Chapter 5.3: Optimization Constraints

Outputs:

- Evaluation Criteria
- Comparison Framework
- Priority Resolution Basis

==============================================================================
Design Principles
==============================================================================

The Optimization Factors framework adheres to the following design
principles:

a) Objective Evaluation

   Every candidate strategy is evaluated against the same factor set.
   Evaluation is impartial and independent of strategy origin.

b) Consistent Comparison

   The same factor set is applied across all candidates. Comparison is
   uniform and predictable.

c) Deterministic Selection

   Identical inputs produce identical selection outcomes. Selection is
   repeatable and verifiable.

d) Constraint Compliance

   Factors operate within the boundaries defined by Optimization
   Constraints. No factor may select a strategy that violates approved
   constraints.

e) Planning Independence

   Factors do not modify planning decisions. They only select among
   execution strategies that already satisfy the approved Decision
   Blueprint.