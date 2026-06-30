"""
RIKAA V1.2 — Planning Engine Blueprint
Runtime 0.3: Orchestrator
=========================================

Defines the Orchestrator as the Runtime coordinator that controls execution
order across the pipeline.

This chapter specifies architectural contracts only. It does not introduce
implementation logic, algorithms, or executable code.

==============================================================================
0.3.1 Purpose
==============================================================================

The Orchestrator is the Runtime coordinator. It controls execution order
across the pipeline, manages the Runtime lifecycle, and invokes the Runtime
Dispatcher and Runtime Response Builder at the appropriate stages.

The Orchestrator coordinates execution only. It never performs business
logic, planning, decision making, ROI optimisation, Hermes logic, or
response formatting. Its sole responsibility is to ensure that each stage
executes in the correct order and that the RuntimeContext flows correctly
through the pipeline.

The Orchestrator does not dispatch Decision Layer components directly.
Decision Engine, ROI Framework, and Hermes invocations belong entirely to
the Runtime Dispatcher (Chapter 0.4).

==============================================================================
0.3.2 Responsibilities
==============================================================================

The Orchestrator is responsible for:

- Controlling the execution order of the Runtime pipeline
- Managing the Runtime lifecycle from initialization through completion
- Invoking the Runtime Dispatcher to execute Decision Layer components
- Invoking the Runtime Response Builder to construct the final response
- Passing the RuntimeContext to each stage
- Receiving outputs from each stage and updating the RuntimeContext
- Detecting errors and halting execution when an error occurs
- Forwarding the final RuntimeContext to the Response Builder

The Orchestrator is NOT responsible for:

- Performing business logic
- Performing planning
- Performing decision making
- Performing ROI optimisation
- Performing Hermes logic
- Dispatching Decision Layer components directly
- Formatting responses
- Recovering from errors
- Modifying layer outputs

The Orchestrator invokes Runtime components and coordinates their
execution. It does not interpret, modify, or act upon their outputs.

==============================================================================
0.3.3 Runtime Sequence
==============================================================================

The Orchestrator executes the following sequence for every request:

RuntimeRequest
    ↓
Input Handler
    ↓
Runtime Context
    ↓
Runtime Orchestrator
    ↓
Runtime Dispatcher
    ↓
Runtime Response Builder
    ↓
Runtime Response

The sequence is deterministic and sequential. Each stage must complete
before the next stage begins. No stage is skipped, reordered, or executed
in parallel.

Decision Layer details (Decision Engine, ROI Framework, Hermes) are
handled by the Runtime Dispatcher and are not part of the Orchestrator's
direct sequence. The Orchestrator invokes the Dispatcher as a single
stage; the Dispatcher manages the internal dispatch order.

==============================================================================
0.3.4 Receive Request
==============================================================================

Purpose
-------

The Orchestrator receives the RuntimeRequest produced by the Input Handler
(Runtime 0.1). This is the first action performed by the Orchestrator.

Inputs
------

- RuntimeRequest: A fully validated and normalized request object produced
  by the Input Handler.

Outputs
-------

- RuntimeRequest (forwarded): The Orchestrator passes the RuntimeRequest to
  the Runtime Context creation stage unchanged.

Context Updates
--------------

No RuntimeContext exists at this stage. The Orchestrator has not yet
created the Runtime Context.

==============================================================================
0.3.5 Create Context
==============================================================================

Purpose
-------

The Orchestrator creates the RuntimeContext and initializes it with the
RuntimeRequest. This establishes the Single Source of Truth for the
execution lifecycle.

Inputs
------

- RuntimeRequest: The validated request produced by the Input Handler.

Outputs
-------

- RuntimeContext (initialized): A new RuntimeContext with the request
  section populated and status set to INITIALIZED.

Context Updates
--------------

The RuntimeContext is created with:
- request_context populated from the RuntimeRequest
- metadata.start_time set to the current time
- status set to INITIALIZED
- All other sections empty

==============================================================================
0.3.6 Execute Dispatcher
==============================================================================

Purpose
-------

The Orchestrator invokes the Runtime Dispatcher (Chapter 0.4) to execute
all Decision Layer components. The Dispatcher handles the invocation of
the Decision Engine, ROI Framework, and Hermes in the correct order.

Inputs
------

- RuntimeContext: Contains the request context populated during
  initialization. The Dispatcher extracts the inputs required by each
  Decision Layer component.

Outputs
-------

- Updated RuntimeContext: The Dispatcher populates the decision_context,
  optimization_context, and execution_context sections with outputs
  produced by the Decision Engine, ROI Framework, and Hermes respectively.

- DispatcherResult: The Dispatcher returns a DispatcherResult containing
  all Decision Layer outputs. The Orchestrator stores this result in the
  RuntimeContext.

Context Updates
--------------

The Orchestrator:
- Sets status to EXECUTION
- Passes the RuntimeContext to the Runtime Dispatcher
- Receives the updated RuntimeContext with Decision Layer sections
  populated
- Stores the DispatcherResult in the RuntimeContext
- If the Dispatcher returns an error, halts execution

==============================================================================
0.3.7 Build Response
==============================================================================

Purpose
-------

The Orchestrator invokes the Runtime Response Builder to construct the
final RuntimeResponse from the completed RuntimeContext.

Inputs
------

- RuntimeContext: Contains all sections populated by previous stages
  (request context, planning context, decision context, optimization
  context, execution context).

- DispatcherResult: The collected outputs from all Decision Layer
  components.

Outputs
-------

- RuntimeResponse: The final response produced from the RuntimeContext.

Context Updates
--------------

The Orchestrator:
- Sets status to RESPONSE
- Passes the RuntimeContext to the Response Builder
- Receives the RuntimeResponse
- Finalizes the RuntimeContext by setting metadata.end_time,
  metadata.duration, and status to COMPLETED

==============================================================================
0.3.8 Error Propagation
==============================================================================

When any stage in the pipeline returns an error, the Orchestrator follows
a defined error propagation procedure:

1. Component Returns RuntimeError

   Any component invoked by the Orchestrator — including the Runtime
   Dispatcher — may return a RuntimeError instead of a successful result.
   The RuntimeError contains the error code, stage, component, message,
   and timestamp.

2. Orchestrator Immediately Stops Execution

   Upon receiving a RuntimeError, the Orchestrator halts execution
   immediately. No further stages are invoked. The pipeline is terminated.

3. Current RuntimeContext is Preserved

   The RuntimeContext at the point of failure is preserved in its current
   state. All data accumulated up to the failed stage remains available
   for diagnostic purposes.

4. Error is Forwarded to Response Builder

   The Orchestrator forwards the RuntimeError and the current
   RuntimeContext to the Response Builder. The Response Builder constructs
   a RuntimeErrorResponse.

5. Orchestrator Does Not Recover Errors

   The Orchestrator does not attempt to recover from errors. Error
   recovery is not a Runtime responsibility. The Orchestrator's only
   action on error is to stop execution and forward the error.

==============================================================================
0.3.9 Outputs
==============================================================================

The Orchestrator produces two possible outputs depending on execution
outcome:

Successful Execution
--------------------

RuntimeResponse contains:

- Runtime Status: The final status of the execution (COMPLETED).
- Execution Metadata: Timing information, trace identifiers, and version
  data from the RuntimeContext metadata section.
- Final Result: The response data produced by the Response Builder,
  including all layer outputs.

Failed Execution
----------------

RuntimeErrorResponse contains:

- Runtime Status: The terminal status of the execution (FAILED).
- Execution Metadata: Timing information and diagnostics available at the
  point of failure.
- Final Result: The error information, including the error code, stage,
  component, and message from the RuntimeError.

Both outputs are produced by the Response Builder using the RuntimeContext
and, in the case of failure, the RuntimeError. The Orchestrator does not
construct responses directly.

==============================================================================
Responsibility Boundary
==============================================================================

The Runtime Orchestrator coordinates Runtime components.

The Runtime Dispatcher coordinates Decision Layer components.

The Runtime Orchestrator never dispatches Decision Layer components
directly. It invokes the Dispatcher as a single coordinated stage. The
Dispatcher manages all interactions with the Decision Engine, ROI
Framework, and Hermes.

This separation ensures single ownership for every responsibility:

| Responsibility | Owner |
|----------------|-------|
| Runtime pipeline coordination | Runtime Orchestrator |
| Runtime lifecycle management | Runtime Orchestrator |
| Dispatcher invocation | Runtime Orchestrator |
| Response Builder invocation | Runtime Orchestrator |
| Decision Engine invocation | Runtime Dispatcher |
| ROI Framework invocation | Runtime Dispatcher |
| Hermes invocation | Runtime Dispatcher |
| DispatcherResult generation | Runtime Dispatcher |
| Response construction | Runtime Response Builder |