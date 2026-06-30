"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 5.2: Optimization Objectives
=========================================

Define the optimization goals of the Execution Layer without introducing any
planning responsibilities.

==============================================================================
Purpose
==============================================================================

Optimization Objectives define the optimization goals that guide execution
strategy selection within the Execution Layer.

The Execution Layer does not redefine planning decisions. Instead, it
optimises how approved work is executed according to measurable operational
objectives.

==============================================================================
Core Objectives
==============================================================================

The Execution Layer pursues four primary optimization objectives:

| Objective           | Description                                                      |
|---------------------|------------------------------------------------------------------|
| Cost Optimization   | Minimize execution cost while preserving required outcomes.      |
| Time Optimization   | Minimize completion time and execution latency.                  |
| Resource Optimization | Maximize utilisation of available models, tools, and infrastructure. |
| Quality Optimization | Maximize execution reliability and output quality while satisfying the required acceptance criteria. |

All four objectives are architectural concerns. They define what the
Execution Layer optimises for, not how optimisation is achieved.

==============================================================================
Optimization Principles
==============================================================================

Execution may prioritize one optimization objective over another depending
on execution context. Different execution scenarios warrant different
trade-offs between objectives.

For example:

- Faster execution may require accepting higher cost.
- Lower cost may require accepting longer completion time.
- Higher quality may require additional computational resources.
- Resource-efficient execution may be prioritised for routine tasks.

Execution strategy determines these trade-offs while remaining consistent
with the approved Decision Blueprint. The choice of which objective to
prioritise is determined by execution policy, not by planning logic.

No single objective is inherently superior. The appropriate objective
depends on the execution context and the policies governing that context.

==============================================================================
Fundamental Constraint
==============================================================================

Optimization improves execution only and never changes approved intent.

Execution optimization may improve:

- Efficiency
- Cost
- Execution speed
- Resource usage
- Quality

However, it must never modify:

- Approved objectives
- Execution scope
- Acceptance criteria
- Decision outcomes

These responsibilities belong exclusively to the Planning Layer. The
Execution Layer optimises how approved work is executed, not what work
is approved.

==============================================================================
Out of Scope
==============================================================================

This chapter does NOT:

- Redefine planning objectives. Planning objectives are defined by the
  Planning Layer (Chapter 3) and are not modifiable by the Execution
  Layer.

- Modify decision priorities. Decision priorities are established during
  planning and are not altered during execution.

- Approve or reject execution requests. Approval authority belongs to
  the Planning Layer and to the governance policies defined outside the
  scope of this chapter.

These responsibilities belong to the Planning Layer.