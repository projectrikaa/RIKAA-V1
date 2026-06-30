"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 6.6: Hermes Communication Contract — Runtime Lifecycle
================================================================

Describes the complete lifecycle of a Runtime invocation involving
Hermes.

This chapter is descriptive rather than normative. It does not introduce
new protocols, schemas, or behaviours. It explains how the communication
contract defined in previous chapters is applied throughout a complete
Runtime invocation.

==============================================================================
6.6.1 Purpose
==============================================================================

This chapter describes the complete lifecycle between Runtime and Hermes,
from request creation to final RuntimeResponse. It consolidates the
communication structures defined in:

- Chapter 6.3 (Runtime → Hermes Request): The HermesRequest structure
  and validation rules.

- Chapter 6.4 (Hermes → Runtime Response): The HermesResponse structure
  and processing rules.

- Chapter 6.5 (Runtime Error Mapping): The error mapping rules that
  translate Hermes errors into Runtime errors.

The lifecycle described here is the Runtime-facing view. It describes
what Runtime does at each stage, not how Hermes executes internally.

==============================================================================
6.6.2 Lifecycle Overview
==============================================================================

The Runtime invocation lifecycle proceeds through the following stages:

RuntimeContext
      │
      ▼
Create HermesRequest
      │
      ▼
Validate Request
      │
      ├────────► Validation Failed
      │
      ▼
Dispatched
      │
      ▼
Hermes Execution
      │
      ▼
Receive Execution Result
      │
      ▼
Validate Response
      │
      ▼
Map Errors
      │
      ▼
Update RuntimeContext
      │
      ▼
Build RuntimeResponse
      │
      ▼
Return RuntimeResponse

Each stage is described in detail in Section 6.6.3.

==============================================================================
6.6.3 Lifecycle Steps
==============================================================================

Step 1: Create HermesRequest
-----------------------------

Responsibility: Runtime (Dispatcher).

What Happens: Runtime constructs a HermesRequest from the current
RuntimeContext. The request includes the version, request_id, trace_id,
runtime_context, user_input, and any optional fields (conversation,
knowledge, constraints, config) that are available.

What Does NOT Happen: Runtime does not modify the RuntimeContext during
request construction. Runtime does not execute any planning or analytical
work. Runtime does not validate the request content beyond ensuring the
required fields are present.

Step 2: Validate Request
-------------------------

Responsibility: Runtime (Dispatcher).

What Happens: Runtime validates the HermesRequest against the schema
defined in Chapter 6.3. Validation checks include supported schema
version, required fields present, correct field types, valid structure,
and valid identifiers.

What Does NOT Happen: Runtime does not validate the semantic content of
the request fields. Runtime does not execute any Hermes logic. Runtime
does not modify the request after validation.

Step 3: Dispatch to Hermes
---------------------------

Responsibility: Runtime (Dispatcher).

What Happens: The Runtime Dispatcher dispatches the validated
HermesRequest to Hermes across the Hermes Communication Contract
boundary. Runtime waits for Hermes to complete execution and return an
Execution Result.

What Does NOT Happen: Runtime does not access Hermes internal state.
Runtime does not monitor Hermes execution progress. Runtime does not
intervene in Hermes execution.

Step 4: Hermes Execution
-------------------------

Responsibility: Hermes.

What Happens: Hermes receives the HermesRequest and performs the
planning and analytical work required to fulfil the request. Hermes
produces a decision, confidence assessment, execution plan, and any
warnings, metrics, and trace information.

What Does NOT Happen: Runtime does not participate in execution. Runtime
does not observe Hermes internal state. Runtime does not receive
intermediate results.

Step 5: Receive Execution Result
---------------------------------

Responsibility: Runtime (Dispatcher).

What Happens: Runtime receives the Execution Result from Hermes. The
Execution Result contains the execution outputs produced by Hermes.

What Does NOT Happen: Runtime does not modify the Execution Result.
Runtime does not interpret the result content at this stage. Runtime
does not initiate additional communication with Hermes.

Step 6: Validate Response
--------------------------

Responsibility: Runtime (Dispatcher).

What Happens: Runtime validates the Execution Result against the schema
defined in Chapter 6.4. Validation checks include supported schema
version, required fields present, correct field types, and valid
structure.

What Does NOT Happen: Runtime does not validate the semantic content of
the result fields. Runtime does not modify the result after validation.

Step 7: Map Errors
-------------------

Responsibility: Runtime (Dispatcher).

What Happens: If the Execution Result status is FAILED, Runtime
translates the Hermes error into a standardized Runtime error using the
mapping defined in Chapter 6.5. The mapped error is propagated through
Runtime Error Handling (Chapter 0.6).

What Does NOT Happen: Runtime does not expose Hermes error types. Runtime
does not retry execution. Runtime does not modify the Execution Result.

Step 8: Update RuntimeContext
------------------------------

Responsibility: Runtime (Dispatcher).

What Happens: Runtime updates the RuntimeContext using the validated
Execution Result. The decision, confidence, execution_plan, warnings,
metrics, and trace are stored in their respective RuntimeContext sections.

What Does NOT Happen: No business logic, planning, reasoning, or
execution occurs during this stage. Runtime does not modify the Execution
Result. Runtime does not interpret the decision or execution_plan
contents. Runtime does not execute the execution_plan.

Step 9: Build RuntimeResponse
------------------------------

Responsibility: Runtime (Response Builder, Chapter 0.5).

What Happens: Runtime constructs the final RuntimeResponse using the
updated RuntimeContext. The RuntimeResponse includes the decision,
execution results, warnings, and any other information required by the
caller.

What Does NOT Happen: Runtime does not include Hermes internal
implementation details in the RuntimeResponse. Runtime does not expose
Hermes error types. Runtime does not include the raw Execution Result
unless explicitly configured to do so.

Step 10: Return RuntimeResponse
--------------------------------

Responsibility: Runtime (Response Builder).

What Happens: Runtime delivers the RuntimeResponse to the caller. The
caller receives a standardized response that does not depend on Hermes
implementation details.

What Does NOT Happen: Runtime does not expose Hermes internal state.
Runtime does not include Hermes-specific error types. Runtime does not
provide direct access to Hermes.

==============================================================================
6.6.4 Lifecycle Principles
==============================================================================

The Runtime invocation lifecycle adheres to the following principles:

1. Deterministic Lifecycle

   Every Runtime invocation follows the same lifecycle stages in the same
   order. The lifecycle is deterministic and predictable.

2. Request Validation Before Execution

   Runtime validates the HermesRequest before dispatching it to Hermes.
   Invalid requests are rejected before execution begins.

3. Response Validation Before State Update

   Runtime validates the Execution Result before updating the
   RuntimeContext. Invalid results are not written to Runtime state.

4. Runtime Owns RuntimeContext

   Runtime is the sole owner of the RuntimeContext. Hermes never accesses
   or modifies the RuntimeContext directly.

5. Hermes Owns Execution

   Hermes is the sole owner of execution. Runtime never participates in
   or observes Hermes internal execution.

6. Standardized Communication

   All communication between Runtime and Hermes uses standardized
   structures defined by the Hermes Communication Contract.

7. Runtime Never Exposes Hermes Internals

   Runtime never exposes Hermes internal implementation details, error
   types, or execution state in the RuntimeResponse.

8. Identical Lifecycle Regardless of Execution Type

   The lifecycle is identical for all Hermes invocations, regardless of
   the type of planning or analytical work requested.

9. Unidirectional Lifecycle

   Every stage completes before the next stage begins. Previous stages
   are never revisited. The lifecycle is a linear execution pipeline that
   progresses in one direction only.

==============================================================================
6.6.5 Responsibility Matrix
==============================================================================

The following table defines which component is responsible for each
stage of the lifecycle:

| Stage                  | Runtime | Hermes |
|------------------------|---------|--------|
| Create Request         | ✓       |        |
| Validate Request       | ✓       |        |
| Dispatch               | ✓       |        |
| Execute                |         | ✓      |
| Internal Retry         |         | ✓      |
| Tool Calling           |         | ✓      |
| Return Result          |         | ✓      |
| Validate Response      | ✓       |        |
| Error Mapping          | ✓       |        |
| Update RuntimeContext  | ✓       |        |
| Build RuntimeResponse  | ✓       |        |
| Return Response        | ✓       |        |

Runtime responsibilities:

- Create Request: Construct HermesRequest from RuntimeContext.
- Validate Request: Validate HermesRequest against schema.
- Dispatch: Send request to Hermes.
- Validate Response: Validate HermesResponse against schema.
- Error Mapping: Translate Hermes errors to Runtime errors.
- Update RuntimeContext: Copy response data into RuntimeContext.
- Build RuntimeResponse: Construct final response.
- Return Response: Deliver response to caller.

Hermes responsibilities:

- Execute: Perform planning and analytical work.
- Internal Retry: Handle recoverable failures internally.
- Tool Calling: Invoke tools required for execution.
- Return Result: Return HermesResponse to Runtime.

==============================================================================
6.6.6 Lifecycle State Transition
==============================================================================

The Runtime invocation lifecycle progresses through the following logical
states:

Created
   │
   ├────────► Validation Failed
   │
   ▼
Validated
   │
   ▼
Dispatched
   │
   ▼
Executing
   │
   ├────────► Failed
   │
   ▼
Completed
   │
   ▼
Response Built
   │
   ▼
Finished

State descriptions:

- Created: The HermesRequest has been constructed from the RuntimeContext
  but has not yet been validated.

- Validation Failed: Request validation failed. The error has been
  mapped to a Runtime error and propagated through Runtime Error
  Handling.

- Validated: The HermesRequest has been validated against the schema and
  is ready for dispatch.

- Dispatched: The HermesRequest has been dispatched to Hermes. Runtime
  is waiting for an Execution Result.

- Executing: Hermes is performing the requested planning and analytical
  work. This state is internal to Hermes and not observable by Runtime.

- Failed: Execution failed. The error has been mapped to a Runtime error
  and propagated through Runtime Error Handling.

- Completed: Execution completed successfully or partially. The
  Execution Result has been received and validated.

- Response Built: The RuntimeResponse has been constructed from the
  updated RuntimeContext.

- Finished: The RuntimeResponse has been delivered to the caller.

These states represent the logical invocation states from the Runtime
perspective. They do not represent Hermes internal implementation states.
