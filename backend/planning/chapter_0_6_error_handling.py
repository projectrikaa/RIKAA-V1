"""
RIKAA V1.2 — Planning Engine Blueprint
Runtime 0.6: Error Handling
=========================================

Defines the Runtime Error Handling framework as the unified error
management mechanism for the Runtime Pipeline.

This chapter specifies architectural contracts only. It does not introduce
implementation logic, algorithms, or executable code.

==============================================================================
0.6.1 Purpose
==============================================================================

Runtime Error Handling is the unified error management framework for the
Runtime Pipeline. It classifies runtime failures, normalizes error
information, propagates errors upward, preserves pipeline consistency,
terminates execution when necessary, and produces standardized error
responses.

Runtime Error Handling manages execution failures only. It never performs
replanning, fixes business logic, retries modules, performs optimisation,
or changes execution decisions. Those responsibilities belong to
downstream modules and layers.

Runtime Error Handling ensures that every error is captured, normalised,
and recorded in the Runtime Context before the pipeline terminates. It
does not attempt to recover from failures or alter the execution path.

==============================================================================
0.6.2 Responsibilities
==============================================================================

Runtime Error Handling is responsible for:

1. Define Runtime Error Types

   Establishing a standard classification of errors that can occur within
   the Runtime Pipeline.

2. Capture Pipeline Exceptions

   Intercepting errors and exceptions raised by any component within the
   Runtime Pipeline.

3. Normalize Error Information

   Converting captured errors into a standardised RuntimeErrorInfo
   structure for consistent handling and reporting.

4. Update Runtime Context

   Recording normalised error information in the Runtime Context errors
   section for diagnostic and audit purposes.

5. Stop Pipeline Execution

   Terminating pipeline execution when an unrecoverable error occurs.
   The pipeline does not continue past the point of failure.

6. Produce Standard Runtime Errors

   Producing standardised error outputs that the Response Builder can
   consume when constructing error responses.

Runtime Error Handling does NOT:

- Perform replanning
- Fix business logic errors
- Retry failed modules or layers
- Perform optimisation
- Change execution decisions
- Alter layer outputs
- Generate user-facing error messages
- Recover from failures

User-facing error responses are generated exclusively by the Response
Builder (Runtime 0.5).

==============================================================================
0.6.3 Error Categories
==============================================================================

Runtime Error Handling defines five error categories that cover all
failure modes within the Runtime Pipeline.

Invalid Request
---------------

Errors that occur when the incoming request cannot be accepted by the
Runtime.

Examples:

- Malformed request structure
- Missing required fields
- Unsupported request type
- Invalid request schema

Pipeline Stage: Input Handler (Runtime 0.1)

Decision Error
--------------

Errors that occur during the decision-making process within the Decision
Layer.

Examples:

- Planner failure
- Policy violation
- Missing execution strategy
- Decision Engine failure

Pipeline Stage: Dispatcher (Runtime 0.4)

Optimization Error
------------------

Errors that occur during the optimisation process within the ROI
Optimization Framework.

Examples:

- Optimisation timeout
- Scoring failure
- Ranking failure
- Optimisation constraint violation

Pipeline Stage: Dispatcher (Runtime 0.4)

Hermes Error
------------

Errors that occur during execution by Hermes.

Examples:

- Tool failure
- Execution timeout
- Model exception
- Invalid tool response

Pipeline Stage: Dispatcher (Runtime 0.4)

Runtime Infrastructure Error
----------------------------

Errors that occur within the Runtime infrastructure itself, as distinct
from business or decision failures.

Examples:

- Runtime Context corruption
- Dispatcher failure
- Response Builder failure
- Unexpected runtime exception

Pipeline Stage: Runtime (any stage)

==============================================================================
0.6.4 Standard Error Structure
==============================================================================

Every error captured by Runtime Error Handling is normalised into a
standard RuntimeErrorInfo structure.

RuntimeErrorInfo contains the following fields:

- category: The error category (Invalid Request, Decision Error,
  Optimization Error, Hermes Error, Runtime Infrastructure Error).

- code: A unique identifier for the specific error type within its
  category.

- message: A human-readable description of the error.

- source: The component or module that produced the error.

- recoverable: A boolean indicating whether the error is recoverable or
  terminal.

- details: Additional structured information about the error context.

- timestamp: The time at which the error occurred.

The recoverable field is determined by the producing component. Runtime
never evaluates recoverability itself. It only records and propagates
this metadata.

Example:

  category: "Decision Error"
  code: "DEC_001"
  message: "Decision Engine returned no valid strategy"
  source: "Decision Engine"
  recoverable: false
  details: { "strategy_count": 0, "input_status": "completed" }
  timestamp: "2026-06-30T16:30:00Z"

All errors within the Runtime Pipeline are represented using this
standard structure. No component produces a non-standard error format.

==============================================================================
0.6.5 Error Propagation
==============================================================================

All errors propagate upward through the Runtime Pipeline. Each layer
captures errors from the components it invokes and forwards them to the
next layer.

Error propagation follows this path:

Module
    ↓
Dispatcher
    ↓
Runtime Context
    ↓
Response Builder
    ↓
RuntimeResponse

1. A module or component within the pipeline produces an error.

2. The Dispatcher (Runtime 0.4) captures the error and normalises it
   into a RuntimeErrorInfo structure.

3. The Runtime Context (Runtime 0.2) records the error in its errors
   section and updates the pipeline status.

4. The Response Builder (Runtime 0.5) reads the error from the Runtime
   Context and constructs the final RuntimeResponse.

5. The RuntimeResponse is delivered to the caller.

Only the Response Builder generates user-facing error responses. No other
component produces error output that reaches the caller directly.

==============================================================================
0.6.6 Recovery Strategy
==============================================================================

Runtime itself performs NO recovery from errors. Recovery is not a Runtime
responsibility.

Possible recovery strategies that may be implemented by downstream
components or future layers include:

- Retry: Re-executing the failed operation.
- Skip: Skipping the failed operation and continuing.
- Fallback: Using an alternative strategy or module.
- Escalation: Escalating the error to a higher authority.
- Abort: Terminating execution without recovery.

Runtime does not implement any of these strategies. It only records
recovery metadata and execution state in the Runtime Context so that
downstream components or external systems can make recovery decisions.

These strategies are defined and executed by downstream components.
Runtime only records the selected strategy and execution state.

The Runtime Context preserves the following information for recovery
purposes:

- The error category and code
- The stage at which the error occurred
- The component that produced the error
- The pipeline state at the point of failure
- Whether the error is potentially recoverable

==============================================================================
0.6.7 Pipeline Behavior
==============================================================================

When an error occurs within the Runtime Pipeline, the following sequence
is executed:

Current Module
      ↓
Capture Error
      ↓
Normalize Error
      ↓
Store Runtime Context
      ↓
Determine Pipeline Status
      ↓
Continue or Abort
      ↓
Response Builder

1. Current Module

   A module or component detects a failure and raises an error.

2. Capture Error

   The error is intercepted by the error handling mechanism of the
   current layer.

3. Normalize Error

   The error is converted into the standard RuntimeErrorInfo structure.

4. Store Runtime Context

   The normalised error is recorded in the Runtime Context errors
   section. The pipeline status is updated to reflect the error.

5. Determine Pipeline Status

   Pipeline status is derived from the Runtime Context together with the
   producing component's execution result. Runtime Error Handling does
   not independently decide whether execution should continue.

   The error's recoverable flag determines whether the pipeline can
   continue:

   - If recoverable is true, the pipeline may continue execution.
   - If recoverable is false, the pipeline is aborted immediately.

6. Continue or Abort

   Based on the recoverability determination:

   - Continue: The pipeline proceeds to the next stage. The error is
     preserved in the Runtime Context for reference.

   - Abort: The pipeline terminates. No further stages are executed.
     The Runtime Context is preserved in its current state.

7. Response Builder

   The Runtime Context is forwarded to the Response Builder, which
   constructs the final RuntimeResponse including any error information.

Continuation depends on the module's recoverability. Runtime does not
override the recoverability flag set by the producing component.

==============================================================================
0.6.8 Outputs
==============================================================================

Runtime Error Handling produces the following outputs:

RuntimeErrorInfo
----------------

A standardised error record containing the category, code, message,
source, recoverable flag, details, and timestamp. Produced for every
error that occurs within the pipeline.

Runtime Status
--------------

The updated pipeline status after an error occurs. Runtime Status
is produced from pipeline execution state and consumed by the
Response Builder. Possible values include:

- Success: Execution completed without errors.
- Partial Failure: Execution completed with recoverable errors.
- Failed: Execution terminated due to an unrecoverable error.

Recovery Metadata
-----------------

Metadata recorded in the Runtime Context that supports recovery
decisions by downstream components or external systems. Includes the
error category, stage, component, pipeline state, and recoverability
indicator.

Error Log
---------

An append-only log of all errors that occurred during the pipeline
execution. Preserved in the Runtime Context errors section. Available
for diagnostic and audit purposes after pipeline completion.

RuntimeResponse
---------------

The final response produced by the Response Builder. For error
scenarios, the RuntimeResponse contains the error information in a
standardised format suitable for the target consumer.

==============================================================================
0.6.9 Design Principles
==============================================================================

Runtime Error Handling adheres to the following design principles:

1. Runtime Never Fixes Business Logic

   Runtime manages execution failures only. Business logic errors are
   the responsibility of the layer that produced them.

2. Runtime Never Replans

   Runtime does not replan or re-decide when an error occurs. Planning
   and decision errors are preserved and reported, not corrected.

3. Runtime Only Manages Execution Failures

   Runtime Error Handling is scoped to execution infrastructure
   failures. It does not handle domain-level or business-level errors.

4. Errors Are Normalized Before Propagation

   Every error is converted into the standard RuntimeErrorInfo structure
   before it is propagated upward. Non-standard error formats are not
   permitted.

5. User Responses Are Generated Only by Response Builder

   Runtime Error Handling produces standardised error structures. The
   Response Builder (Runtime 0.5) is the only component that generates
   user-facing error responses.

6. Runtime Context Always Preserves Pipeline State

   The Runtime Context preserves all pipeline state at the point of
   failure. No state is discarded when an error occurs.

7. Every Runtime Error Is Traceable

   Every error recorded in the Runtime Context includes the source
   component, stage, category, code, and timestamp. Errors are fully
   traceable for diagnostic purposes.