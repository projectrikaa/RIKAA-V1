"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 6.2: Hermes Communication Contract — Hermes Role
===========================================================

Describes Hermes from the Runtime perspective only. Hermes is treated as
a black-box execution component. This chapter defines what Runtime knows
about Hermes, not how Hermes works internally.

This chapter specifies architectural contracts only. It does not introduce
implementation logic, algorithms, or executable code.

==============================================================================
6.2.1 Purpose
==============================================================================

From the Runtime perspective, Hermes is the execution component
responsible for the planning and analytical work requested by Runtime.
Runtime communicates with Hermes only through the Hermes Communication
Contract. Runtime does not depend on Hermes implementation, internal
architecture, or execution strategy.

Hermes is a black-box component. Runtime sends a request and receives a
response. Everything that happens between request and response is
internal to Hermes and invisible to Runtime.

==============================================================================
6.2.2 Responsibilities
==============================================================================

From the Runtime perspective, Hermes has the following externally
observable responsibilities:

1. Receive Runtime Request

   Hermes accepts a valid HermesRequest sent by Runtime through the
   Dispatcher. The request contains the DecisionOutput, Optimization-
   Result, and execution context required for execution.

2. Perform Planning

   Hermes plans the execution steps required to fulfil the request.
   The planning process is internal to Hermes. Runtime observes only
   the results of planning through the execution outputs.

3. Perform Decision Analysis

   Hermes analyses the decision context provided in the request and
   makes the decisions required for execution. The decision analysis
   process is internal to Hermes. Runtime observes only the results.

4. Perform ROI Analysis

   Hermes analyses the optimisation recommendation provided in the
   request to guide execution. The ROI analysis process is internal to
   Hermes. Runtime observes only the results.

5. Produce Standardized Execution Results

   Hermes produces a standardised ExecutionBlueprint containing the
   modules executed, execution order, tool calls, generated outputs,
   and execution metadata.

6. Return Standardized Execution Results to Runtime

   Hermes returns a HermesResponse containing the ExecutionBlueprint,
   execution status, metadata, and any error information. The
   HermesResponse is not the Runtime Response. The Runtime Response is
   constructed by the Runtime Response Builder (Chapter 0.5) using the
   HermesResponse as one of its inputs.

Hermes is NOT required to:

- Expose internal modules, workflows, or agents to Runtime
- Disclose its reasoning process or algorithms
- Reveal model selection or configuration details
- Explain internal execution strategy
- Provide visibility into intermediate states during execution

==============================================================================
6.2.3 Runtime Visibility
==============================================================================

Runtime assumes only the following about Hermes:

1. Hermes Accepts a Valid Runtime Request

   Runtime assumes that Hermes accepts a HermesRequest that conforms to
   the Hermes Communication Contract. Runtime does not assume anything
   about how Hermes validates, processes, or prioritises requests
   internally.

2. Hermes Performs the Requested Planning and Analytical Work

   Runtime assumes that Hermes performs the planning and analytical work
   requested in the HermesRequest. Runtime does not assume anything
   about the internal steps, order, or strategy Hermes uses to complete
   the work.

3. Hermes Returns Standardized Execution Results

   Runtime assumes that Hermes returns a HermesResponse that conforms to
   the Hermes Communication Contract. The HermesResponse contains
   execution results, not the final Runtime Response. Runtime does not
   assume anything about how Hermes constructs the response internally.

Runtime must not rely on any Hermes internal behaviour, implementation
details, or undocumented outputs. All interactions are governed
exclusively by the Hermes Communication Contract.

==============================================================================
6.2.4 Communication Contract Dependency
==============================================================================

The Hermes Communication Contract is the only dependency between Runtime
and Hermes. Both components commit to honouring the contract. Neither
component depends on the other's internal implementation.

This dependency model ensures that:

- Runtime can change its internal implementation without affecting
  Hermes, as long as it continues to produce valid HermesRequest
  objects.

- Hermes can evolve its internal architecture, algorithms, models, or
  execution strategy independently without affecting Runtime, provided
  the Hermes Communication Contract remains backward compatible.

- The contract can be versioned independently of either component.
  Contract versioning enables controlled evolution without breaking
  existing deployments.

==============================================================================
6.2.5 Non-Responsibilities
==============================================================================

From the Runtime perspective, Hermes is NOT responsible for:

- Runtime orchestration: Hermes does not control the Runtime pipeline
  sequence. It only responds to Runtime requests.

- Runtime state management: Hermes does not create, modify, or finalise
  the Runtime Context. It only receives context through the request and
  returns results through the response.

- Runtime response construction: Hermes does not construct the final
  RuntimeResponse. It returns execution results that the Runtime
  Response Builder (Chapter 0.5) uses as input.

- Runtime lifecycle management: Hermes does not manage the Runtime
  lifecycle. It is invoked during the execution stage and returns
  results before the response stage.

These responsibilities remain with Runtime components as defined in
their respective chapters.
