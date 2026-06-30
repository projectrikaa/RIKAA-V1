"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 6.7: Hermes Communication Contract — End-to-End Runtime Flow
======================================================================

Provides the complete execution lifecycle of the Runtime pipeline,
demonstrating how all Runtime components and the Hermes Communication
Contract work together during a single execution.

This chapter is an integration overview rather than a specification of
any individual component.

==============================================================================
6.7.1 Purpose
==============================================================================

This chapter provides the complete execution lifecycle of the Runtime
pipeline. It demonstrates how all Runtime components and the Hermes
Communication Contract work together during a single execution.

Readers should be able to understand the entire request/response
lifecycle without referring back to previous chapters. The flow
described here integrates:

- Runtime components (Input Handler, Orchestrator, Dispatcher, Response
  Builder) as defined in Chapter 0.

- The Hermes Communication Contract (HermesRequest, Execution Result,
  error mapping) as defined in Chapters 6.0 through 6.6.

- Hermes as the independent execution component.

This chapter is an integration overview. It does not specify the
internal behaviour of any individual component.

==============================================================================
6.7.2 High-Level Runtime Pipeline
==============================================================================

The following diagram illustrates the complete Runtime pipeline:

                         Runtime Pipeline

┌──────────┐
│   User   │
└────┬─────┘
     │
     ▼
┌──────────────────────┐
│ Input Handler        │
│ • Parse Input        │
│ • Validate           │
│ • Normalize          │
└────┬─────────────────┘
     │ RuntimeContext
     ▼
┌──────────────────────┐
│ Orchestrator         │
│ • Execute Pipeline   │
│ • Manage Flow        │
└────┬─────────────────┘
     │
     ▼
┌──────────────────────┐
│ Dispatcher           │
│ • Build HermesRequest│
│ • Invoke Hermes      │
└────┬─────────────────┘
     │
     │ HermesRequest
     ▼
═══════════════════════════════════════
        Hermes Communication Contract
═══════════════════════════════════════
     │
     ▼
┌──────────────────────┐
│ Hermes               │
│ • Execute            │
│ • Return Execution   │
│   Result             │
└────┬─────────────────┘
     │
     │ Execution Result
     ▼
═══════════════════════════════════════
        Hermes Communication Contract
═══════════════════════════════════════
     │
     ▼
┌──────────────────────┐
│ Dispatcher           │
│ • Map Errors         │
│ • Update Context     │
└────┬─────────────────┘
     │ RuntimeContext
     ▼
┌──────────────────────┐
│ Response Builder     │
│ • Build Runtime      │
│   Response           │
└────┬─────────────────┘
     │ RuntimeResponse
     ▼
┌──────────┐
│   User   │
└──────────┘

Key architectural rules illustrated by this pipeline:

- Runtime owns the complete execution pipeline. Runtime coordinates
  every stage from input reception to response delivery.

- Hermes is an independent execution component. It performs the planning
  and analytical work requested by Runtime but does not participate in
  pipeline coordination.

- Communication occurs only through the standardized Hermes Communication
  Contract. There is no direct Runtime access to Hermes internals and no
  direct Hermes access to Runtime internals.

- RuntimeContext never crosses the Runtime-Hermes boundary. The
  Dispatcher constructs a HermesRequest from the RuntimeContext and
  updates the RuntimeContext from the Execution Result, but the
  RuntimeContext itself remains within Runtime at all times.

==============================================================================
6.7.3 Runtime → Hermes Flow
==============================================================================

The Runtime-to-Hermes flow proceeds through the following stages:

1. User Submits Input

   The user submits a request to the system. The request enters the
   Runtime pipeline through the Input Handler.

2. Input Handler Validates and Normalizes

   The Input Handler (Runtime 0.1) parses, validates, and normalizes the
   user input. Invalid inputs are rejected before pipeline execution
   begins.

3. RuntimeContext Is Created

   The Runtime Context (Runtime 0.2) is created and initialized with the
   validated input and execution metadata. The RuntimeContext serves as
   the single source of truth for the duration of the execution.

4. Orchestrator Executes the Pipeline

   The Orchestrator (Runtime 0.3) controls the execution sequence. It
   invokes the Dispatcher when the pipeline reaches the execution stage.

5. Dispatcher Determines the Hermes Invocation

   The Dispatcher (Runtime 0.4) determines that Hermes execution is
   required based on the current pipeline state and RuntimeContext.

6. Dispatcher Builds a HermesRequest

   The Dispatcher constructs a HermesRequest from the RuntimeContext.
   The request includes the version, request_id, trace_id, runtime_
   context, user_input, and any optional fields (conversation, knowledge,
   constraints, config) that are available. The HermesRequest structure
   is defined in Chapter 6.3.

7. HermesRequest Crosses the Communication Contract

   The Dispatcher dispatches the HermesRequest across the Hermes
   Communication Contract boundary. This is the only interaction path
   between Runtime and Hermes.

8. Hermes Receives the Request

   Hermes receives the HermesRequest and begins execution. Hermes
   validates the request before performing any planning or analytical
   work.

==============================================================================
6.7.4 Hermes → Runtime Flow
==============================================================================

The Hermes-to-Runtime flow proceeds through the following stages:

1. Hermes Executes

   Hermes performs the planning and analytical work required to fulfil
   the request. Execution is entirely internal to Hermes. Runtime does
   not participate in or observe execution.

2. Hermes Produces an Execution Result

   Hermes produces a structured Execution Result containing the decision,
   confidence, execution_plan, warnings, metrics, and trace information.
   The Execution Result structure is defined in Chapter 6.4.

3. Execution Result Crosses the Communication Contract

   Hermes returns the Execution Result across the Hermes Communication
   Contract boundary. The Dispatcher receives the result.

4. Dispatcher Maps Errors

   If the Execution Result status is FAILED, the Dispatcher translates
   the Hermes error into a standardized Runtime error using the mapping
   defined in Chapter 6.5. The mapped error is propagated through
   Runtime Error Handling (Runtime 0.6).

5. Dispatcher Updates RuntimeContext

   The Dispatcher updates the RuntimeContext using the validated
   Execution Result. The decision, confidence, execution_plan, warnings,
   metrics, and trace are stored in their respective RuntimeContext
   sections.

6. Response Builder Creates the RuntimeResponse

   The Response Builder (Runtime 0.5) constructs the final RuntimeResponse
   using the updated RuntimeContext. The RuntimeResponse includes the
   decision, execution results, warnings, and any other information
   required by the caller.

7. RuntimeResponse Is Returned to the User

   Runtime delivers the RuntimeResponse to the user. The user receives a
   standardized response that does not depend on Hermes implementation
   details.

Critical architectural rules:

- Hermes never creates RuntimeResponse. The RuntimeResponse is
  constructed exclusively by the Response Builder (Runtime 0.5).

- Hermes never modifies RuntimeContext. The RuntimeContext is updated
  exclusively by the Dispatcher (Runtime 0.4) using the validated
  Execution Result.

- The Dispatcher is responsible for integrating Hermes results into the
  Runtime pipeline. No other Runtime component communicates with Hermes.

==============================================================================
6.7.5 End-to-End Sequence
==============================================================================

The following simplified sequence diagram illustrates the end-to-end
execution flow:

User
 │
 │ Input
 ▼
Input Handler
 │
 ▼
RuntimeContext
 │
 ▼
Orchestrator
 │
 ▼
Dispatcher
 │
 │ HermesRequest
 ▼
Hermes
 │
 │ Execution Result
 ▼
Dispatcher
 │
 ▼
Response Builder
 │
 │ RuntimeResponse
 ▼
User

Every Runtime execution follows this deterministic lifecycle. The
sequence is identical for all Hermes invocations, regardless of the type
of planning or analytical work requested.

The lifecycle is unidirectional: each stage completes before the next
stage begins, and previous stages are never revisited.

==============================================================================
6.7.6 Design Principles
==============================================================================

The end-to-end Runtime flow adheres to the following architectural rules:

1. Runtime Owns the Execution Lifecycle

   Runtime coordinates every stage from input reception to response
   delivery. Hermes is invoked as part of the pipeline but does not
   control the pipeline sequence.

2. Hermes Performs Execution Only

   Hermes is responsible for planning and analytical work. It does not
   participate in pipeline coordination, state management, or response
   construction.

3. Dispatcher Is the Only Runtime Component That Communicates with
   Hermes

   No other Runtime component (Input Handler, Orchestrator, Response
   Builder) communicates with Hermes directly. The Dispatcher is the
   sole communication bridge.

4. All Runtime-Hermes Communication Uses the Standardized Communication
   Contract

   There is no ad-hoc communication, side channels, or shared state
   between Runtime and Hermes. All interaction occurs through the
   defined HermesRequest and Execution Result structures.

5. RuntimeContext Never Leaves Runtime

   The RuntimeContext remains within Runtime at all times. Hermes
   receives a HermesRequest constructed from the RuntimeContext but
   never accesses the RuntimeContext directly.

6. Hermes Never Constructs RuntimeResponse

   The RuntimeResponse is constructed exclusively by the Response
   Builder. Hermes returns an Execution Result that the Response Builder
   uses as input.

7. Response Builder Is the Only Component That Creates RuntimeResponse

   No other component constructs the final response. The Response
   Builder is the sole producer of RuntimeResponse.

8. Hermes Errors Are Translated Before Entering the Runtime Pipeline

   Hermes-specific error types are never exposed to Runtime. All Hermes
   errors are translated into standardized Runtime errors using the
   mapping defined in Chapter 6.5.

9. Every Execution Follows the Same Deterministic Lifecycle

   The lifecycle is identical for all Hermes invocations. The sequence
   of stages is fixed, unidirectional, and predictable.

This end-to-end flow represents the complete integration model between
Runtime and Hermes. It provides a stable, deterministic, and standardized
execution lifecycle for all future Runtime operations.