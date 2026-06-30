"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 4.2: Standard Module Interface
=========================================

This chapter defines the universal interface contract that every planning
module must follow. It establishes the common execution interface only.

It does NOT define module responsibilities, module logic, prompts, execution
order, or planning policy. Those concerns belong to their respective chapters.

==============================================================================
Definition
==============================================================================

Standard Module Interface defines the contract that every planning module
must satisfy to be compatible with the Planning Engine.

This interface is universal. Every module, regardless of its specific planning
responsibility, adheres to the same structural contract. The Engine never
requires special-case logic to accommodate individual module differences.

The interface covers:

- The input a module receives
- The output a module returns
- The structure of that output
- The execution guarantees a module must uphold
- The error behaviour a module must follow

The interface does NOT define:

- What a module does internally
- How a module produces its output
- The order in which modules execute
- How modules communicate with each other

==============================================================================
Purpose
==============================================================================

The Standard Module Interface exists to ensure:

- Uniformity: Every module presents the same external shape. The Engine can
  invoke any module without knowing its internal logic.

- Replaceability: Any module can be replaced by another module that fulfils
  the same interface contract, without modifying the Engine or other modules.

- Testability: Because all modules share the same input and output structure,
  a single test harness can verify any module.

- Predictability: The Engine knows exactly what to expect from every module
  invocation. There are no surprises, no optional fields, no conditional
  behaviours at the interface level.

- Engine Simplicity: The Engine does not need to interpret module-specific
  output formats. It relies on a uniform result structure for all modules.

This interface is designed for V1.0. It includes no provisions for plugin
systems, dynamic module loading, or runtime interface negotiation.

==============================================================================
Responsibility
==============================================================================

The Standard Module Interface is owned by the architecture. It is not owned
by individual modules, the Engine, or the Runner.

The interface defines:

- What every module must accept
- What every module must return
- How every module must behave at the boundary
- What every module must guarantee in terms of execution semantics

The interface does NOT define:

- Module implementation strategies
- Module internal algorithms
- Module-specific behaviour
- Module sequencing or workflow

==============================================================================
Boundary
==============================================================================

This chapter defines the Standard Module Interface only.

It does NOT define:

- Module responsibilities (see Chapter 3)
- Module design or implementation (see Chapter 3)
- Module prompts or prompt structure (see Chapter 3)
- Execution order or sequencing (see Chapter 4.8)
- Execution flow or workflow (see Chapter 4.8)
- Context structure or data model (see Chapter 4.3)
- Context passing mechanics (see Chapter 4.4)
- Error handling or recovery strategies (see Chapter 4.6)
- Planning policy or decision rules

==============================================================================
Required Input
==============================================================================

Every module receives exactly one input: a shared Context Object.

Context Object is a read-only view of the accumulated planning state. It
contains all outputs produced by previously executed modules. A module
may read any portion of the Context Object. It must not modify it.

The Context Object provides a module with:

- The complete set of outputs from all prior modules in the planning session
- A consistent snapshot of planning state at the time of invocation
- No module-specific or session-specific metadata beyond planning outputs

Every module receives the same type of input. The content of the
Context Object grows as the planning session progresses, but the interface
through which it is delivered remains identical for all modules.

No module receives raw user input, session identifiers, engine metadata,
or any data outside the Context Object.

==============================================================================
Required Output
==============================================================================

Every module returns exactly one output: a standardized ModuleResult.

ModuleResult is a uniform structure that every module produces. The Engine
and Runner depend on this uniform structure to process module outputs
without module-specific knowledge.

The ModuleResult contains:

- The module's structured planning output
- A status indicator for the execution outcome
- A result identifier for traceability

Every module returns the same type of output. The content varies by module,
but the structure and interface contract are identical across all modules.

No module returns execution metadata, Engine instructions, workflow control
signals, or any data outside the standardized result structure.

==============================================================================
Standard Result Structure
==============================================================================

Every ModuleResult consists of three components:

1. Output Data

   The structured planning output produced by the module. This is the
   substantive result that contributes to the planning process. The
   structure of the output data is module-specific and defined in the
   module's own specification (Chapter 3). The interface requires only
   that this output data is present and well-formed.

2. Status

   A status indicator that communicates the outcome of the module's
   execution. The status is a predefined value that the Engine can
   interpret deterministically. It is not freeform text. The set of
   allowed status values and their semantics are defined by Chapter 4.6
   (Error Handling).

3. Result Identifier

   A unique identifier that associates the result with the specific
   module invocation. The identifier enables traceability and result
   correlation across the planning session. The identifier is generated
   by the Runner, not by the module itself.

The ModuleResult contains no other data. It does not contain error messages,
execution metrics, debugging information, or module-specific metadata.

==============================================================================
Execution Contract
==============================================================================

Every module must uphold the following execution guarantees:

1. Read-Only Access

   A module may read the Context Object. A module must not modify the
   Context Object. The Context Object is an immutable snapshot at the point
   of module invocation.

2. Single Responsibility

   A module produces output for exactly one planning concern. It does not
   produce output for multiple concerns. It does not supplement or correct
   output from other modules.

3. Self-Contained Execution

   A module executes independently. It does not call other modules. It
   does not depend on the execution state of other modules beyond the
   data available in the Context Object.

4. Deterministic Output Structure

   Given a Context Object, a module always returns a ModuleResult with the
   same structural shape. The content may vary, but the structure is fixed.
   A module does not conditionally include or exclude fields in its output.

5. No Side Effects

   A module produces no side effects beyond returning its ModuleResult.
   It does not write to external storage, modify shared state, or affect
   the execution environment.

6. No Workflow Control

   A module does not influence the execution sequence. It does not signal
   the Engine to skip, repeat, or reorder modules. Workflow decisions are
   the sole responsibility of the Engine.

==============================================================================
Status Definition
==============================================================================

Status is a standardized execution status returned by every module as part
of its ModuleResult.

The status is a predefined value that the Engine can interpret
deterministically. It is not freeform text.

The set of allowed status values and their semantics are defined by
Chapter 4.6 (Error Handling). Chapter 4.2 defines only that a status
exists and must be present in every ModuleResult.

The status belongs to the interface contract. The specific values belong
to the error handling specification.

==============================================================================
Error Contract
==============================================================================

Every module must follow these error rules:

1. Error Containment

   Errors are contained within the module that produced them. A module
   error does not propagate to other modules. Each module invocation is
   isolated from the error state of other invocations.

2. Failure Indication

   If a module cannot produce valid output, it sets its status to Failed.
   It does not return incomplete or partially valid output under a
   successful status.

3. No Recovery Within Module

   A module does not attempt to recover from errors internally. Recovery
   decisions belong to the Engine. The module's only responsibility on
   failure is to report the failure through the status indicator.

4. No Error Propagation

   A module does not throw exceptions or raise errors that cross the
   module boundary. All execution outcomes are communicated exclusively
   through the ModuleResult status field.

5. No Side Effects on Failure

   A failed module leaves no side effects. It does not modify the
   Context Object, write to external storage, or alter system state.

==============================================================================
Acceptance Criteria
==============================================================================

A module implementation satisfies the Standard Module Interface if:

1. It accepts a single input of type Context Object.

2. It returns a single output of type ModuleResult.

3. The ModuleResult contains output data, a status value, and a result
   identifier.

4. The status value is a predefined execution status consistent with
   the error handling specification (Chapter 4.6).

5. The output data structure is fixed and does not vary between
   invocations for the same module.

6. The module does not modify the Context Object.

7. The module does not invoke other modules.

8. The module does not produce side effects beyond returning its result.

9. The module does not attempt to control execution flow.

10. The module does not attempt error recovery.

11. The module communicates errors only through the status field.

12. The Engine can invoke the module without module-specific knowledge.

==============================================================================
Dependencies
==============================================================================

The Standard Module Interface has no internal dependencies. It is a
contract definition, not an implementation dependency.

The interface references the following external specifications:

- Context Object: Referenced as an abstract interface concept. The
  complete definition is specified in Chapter 4.3 (Context Object).

- Module-specific output structure: Defined in Chapter 3 for each
  individual module. The interface requires that each module defines its
  output structure, but the internal format of that output is outside
  the scope of this chapter.

- Status semantics: Defined in Chapter 4.6 (Error Handling). The
  interface defines that a status exists, but the allowed values and
  their interpretation are outside the scope of this chapter.

The interface has no dependency on:

- Programming language or runtime
- Module implementation technology
- Specific module implementations
- Engine or Runner implementation
- External libraries or frameworks