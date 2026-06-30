"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 4.3: Context Object
===============================

This chapter defines the Context Object shared between the Engine and all
planning modules during one engine execution.

It is consistent with the Standard Module Interface (Chapter 4.2), which
references Context Object as an abstract interface concept. This chapter
provides the complete specification of that concept.

==============================================================================
1. Definition
==============================================================================

The Context Object is the standardized data object shared during one engine
execution.

It acts as the single source of truth for the current execution only. Every
module receives the same Context Object as its input. The Engine updates the
Context Object as modules complete. No other component holds authoritative
execution state.

The Context Object is scoped to exactly one execution session. There is a
one-to-one relationship between an engine execution instance and its
Context Object.

==============================================================================
2. Purpose
==============================================================================

The Context Object exists to provide:

- Consistent Input: Every module receives the same structured context,
  regardless of its position in the execution sequence. No module requires
  special input formatting or data pre-processing.

- Elimination of Duplicated Information: All shared data resides in exactly
  one location. Modules do not hold copies of shared state. There is no
  data duplication between modules.

- Shared Execution State: The Context Object holds the accumulated state
  of the planning session as it progresses. Any component can determine
  what has been completed and what outputs have been produced by inspecting
  the Context Object.

- Modular Execution: Because all shared data passes through the Context
  Object, modules have no direct dependency on each other. A module depends
  only on the Context Object, not on other modules' internal state or
  output format.

==============================================================================
3. Responsibilities
==============================================================================

The Context Object is responsible for:

a) Standardized Context Schema

   The Context Object MUST maintain a well-defined, standardized structure.
   Every consumer MUST be able to rely on the shape of the Context Object
   without inspecting its contents. The schema defines the sections and
   their relationships, not the specific data values within them.

b) Shared Execution Data

   The Context Object MUST hold the data that is common to the entire
   planning session. This includes project-level information established
   at session start and shared across all modules.

c) Module Data

   The Context Object MUST store data produced or consumed by individual
   modules. Each module's data MUST be stored in an identifiable section
   associated with that module. The ordering of module data MUST reflect
   the execution sequence.

d) Aggregated Results

   The Context Object MUST accumulate the output of every executed module
   into a unified result set. The accumulated results represent the
   complete planning output for the session.

e) Execution Metadata

   The Context Object MAY carry metadata about the execution session itself,
   such as session identifiers or execution status. This metadata MUST NOT
   include module logic, implementation details, or persistent storage
   information.

==============================================================================
4. Does NOT Own
==============================================================================

The Context Object MUST NOT own:

- Business Logic: The Context Object MUST NOT contain or execute planning
  logic. It is a data container only.

- Module Execution: The Context Object MUST NOT invoke, control, or
  influence module execution. Execution management is the responsibility
  of the Engine and Runner.

- Decision Making: The Context Object MUST NOT make planning decisions.
  It holds the data that decisions are based upon, but does not evaluate
  or act upon that data.

- Context Lifecycle: The Context Object MUST NOT manage its own creation,
  initialization, or destruction. Lifecycle management is the
  responsibility of the Engine.

- Persistence: The Context Object MUST NOT persist data beyond the current
  execution session. It is an in-memory object with no storage
  responsibility.

- Database: The Context Object MUST NOT function as a database or data
  store. It is not designed for query, indexing, or data retrieval beyond
  direct access.

- Long-Term Memory: The Context Object MUST NOT maintain state across
  execution sessions. Each session creates a new Context Object.

- Caching: The Context Object MUST NOT cache data from external sources.
  It holds only the data produced during the current execution.

- Prompt Management: The Context Object MUST NOT manage, store, or
  generate prompts. Prompts are the responsibility of individual modules.

==============================================================================
5. Core Structure
==============================================================================

The Context Object consists of four top-level sections. Each section serves
a distinct purpose within the execution session.

a) Project

   The Project section holds the immutable project-level information that
   defines the current planning session. This includes the original input
   that initiated the session and any session-level identifiers. This
   section MUST be populated at context creation and MUST NOT be modified
   during execution.

b) Modules

   The Modules section represents shared module-owned data produced or
   consumed during execution. This section contains the distinct planning
   outputs generated by each module, such as purpose, problem, target
   outcome, success criteria, scope, constraints, assumptions, and any
   other module-specific data. This section MUST NOT contain execution
   configuration, execution order, scheduling information, enable or
   disable flags, or runtime control directives.

c) Results

   The Results section stores the accumulated output of each executed
   module as a unified result set. Each entry in this section MUST be
   associated with a specific module, MUST contain that module's
   ModuleResult, and MUST be stored in execution order. This section
   starts empty and is populated as modules complete.

d) Metadata

   The Metadata section holds execution-scoped information that is neither
   project input nor module output. This MAY include session status,
   execution timing, or invocation identifiers. This section MUST NOT
   contain planning data or module logic.

The Context Object has no other top-level sections. Any data that does not
fit into one of these four sections is outside the scope of the context.

==============================================================================
6. Lifecycle
==============================================================================

The Context Object follows a defined lifecycle during engine execution:

1. Create Context

   The Engine creates an empty Context Object with the standard structure.
   At this point, the Project section is populated with the session input.
   The Modules section contains the expected module data layout. The
   Results section is empty. The Metadata section contains initial
   execution metadata.

2. Execute Module

   The Runner provides the Context Object to the current module. The module
   reads the Context Object and produces a ModuleResult. The module MUST
   NOT modify the Context Object directly.

3. Update Context

   The Runner writes the module's ModuleResult into the Results section of
   the Context Object. The Runner MAY update the Metadata section with
   execution progress information. The Project and Modules sections MUST
   NOT change during this step.

4. Execute Next Module

   The Runner provides the updated Context Object to the next module. The
   Context Object now reflects all prior module outputs. Steps 2 and 3
   repeat for each module in the execution sequence.

5. Final Context

   After all modules have executed, the Context Object contains the
   complete accumulated state of the planning session. The Project section
   holds the original input. The Results section contains all module
   outputs in execution order. The Metadata section contains the final
   execution status.

The Context Object MUST NOT be modified outside this lifecycle. No component
other than the Engine and Runner MAY update the Context Object.

==============================================================================
7. Design Principles
==============================================================================

The Context Object MUST adhere to the following design principles:

a) Standardized

   Every Context Object MUST conform to the same top-level structure.
   There MUST NOT be different context structures for different execution
   paths. The structure is fixed at design time.

b) Predictable

   The contents of a Context Object at any point in the lifecycle MUST be
   determinable from the execution sequence. There MUST NOT be conditional
   or path-dependent structural variations.

c) Serializable

   The Context Object SHOULD be serializable to enable inspection, logging,
   or transmission. Serialization MUST NOT alter the semantics of the data.

d) Extensible

   The Context Object MAY accommodate new data sections in future versions.
   However, V1.0 MUST define the complete set of sections. Extensibility
   does not permit undefined or open-ended sections.

e) Language-Independent

   The concept of the Context Object MUST NOT depend on any programming
   language feature, runtime, or type system. It is a logical structure
   that MAY be implemented in any language.

f) Deterministic

   Given the same project input and the same module execution sequence, the
   Context Object MUST produce the same final state. Non-deterministic data
   MUST NOT be introduced through the context structure itself.

==============================================================================
8. Acceptance Criteria
==============================================================================

An implementation satisfies the Context Object specification if:

1. A Context Object MUST be creatable before any module execution begins.

2. A Context Object MUST contain all four top-level sections at the point
   of creation.

3. Every module in the execution sequence MUST be able to read the Context
   Object.

4. The Context Object MUST store the output of every executed module in an
   identifiable section.

5. The order of stored module outputs MUST reflect the execution sequence.

6. The Context Object MUST support the full lifecycle from creation through
   final state without structural modification. Data values within sections
   are updated during execution; the section structure itself MUST remain
   unchanged.

7. The Context Object MUST produce a complete execution context after all
   modules have executed.

8. No module MUST be able to modify the Context Object through its read
   access.

9. The Project section MUST remain unchanged from creation to final state.

10. The Context Object MUST NOT contain any data that is not defined in its
    core structure.

==============================================================================
9. Failure Conditions
==============================================================================

The Context Object MAY encounter the following failure conditions:

a) Missing Required Data

   If a required field in the Project section is absent at creation time,
   the Context Object MUST be considered invalid. Execution MUST NOT
   proceed with an incomplete Context Object.

b) Invalid Structure

   If the Context Object does not conform to the standard structure at any
   point in its lifecycle, the execution session MUST be terminated. A
   structurally invalid Context Object cannot be repaired during execution.

c) Corrupted Module Outputs

   If a module produces output that cannot be stored in the Results section,
   the Context Object SHOULD transition to a failed state. Corrupted outputs
   MUST NOT be silently ignored.

d) Inconsistent Shared State

   If the Context Object detects inconsistency between its sections —
   for example, a mismatch between the Modules section and the Results
   section — the Context Object MUST be considered invalid.

e) Unexpected Schema Changes

   If any component attempts to modify the structure of the Context Object
   during execution — by adding, removing, or renaming sections — the
   Context Object MUST reject the modification and the execution MUST be
   terminated.

These failure conditions are detected by the Context Object infrastructure.
Recovery from these conditions is the responsibility of the Engine, not
the Context Object itself.

==============================================================================
10. V1 Scope
==============================================================================

The Context Object for V1.0 includes:

- Single Execution Context: Exactly one Context Object per engine execution
  session. There MUST NOT be multiple active context objects within one
  session.

- In-Memory Context: The Context Object exists only in memory during the
  execution session. There is no persistent storage, file system
  representation, or network transmission of the context.

- Standardized Schema: The four-section structure (Project, Modules,
  Results, Metadata) is fixed for V1.0. No optional or conditional sections
  are permitted.

- Shared Execution Data: All data produced during execution is accessible
  through the Context Object. No module output exists outside the context.

The Context Object for V1.0 explicitly excludes:

- Persistence: The context MUST NOT be saved, loaded, or restored across
  sessions.

- Distributed Execution: The context MUST NOT be shared across process or
  network boundaries.

- Synchronization: The context MUST NOT require concurrency control or
  locking mechanisms.

- Version History: The context MUST NOT maintain historical versions of
  its state. Only the current state is accessible.

- Multi-User Context: The context MUST NOT support concurrent access by
  multiple users or agents.

- Long-Term Memory: The context MUST NOT retain state between independent
  execution sessions.

This scope is defined for V1.0 only. Future versions MAY extend the Context
Object specification.