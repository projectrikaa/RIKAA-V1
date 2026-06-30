"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 4.7: Engine Response
=================================

This chapter defines the Engine Response of the Planning Engine.

Engine Response is the standardized output returned by the Planning Engine
after execution completes. It represents the final output contract between
the Planning Engine and any consumer of its results.

==============================================================================
Definition
==============================================================================

Engine Response is the standardized output returned by the Planning Engine
after execution completes.

It wraps the final planning result, execution metadata, module outputs, and
execution status into a single, consistent response structure. It represents
the final output contract of the Planning Engine — every consumer receives
the same structural format regardless of the execution path.

The Engine Response is the outermost output boundary of the Planning Engine.
It is produced by the Engine after all modules have executed and the
Decision Output has been assembled.

==============================================================================
Purpose
==============================================================================

The Engine Response exists to provide:

- Standardized Output: Every execution produces a response with the same
  top-level structure, regardless of project type, module configuration, or
  execution outcome.

- Consistent Response Format: The consumer of an Engine Response can rely
  on a predictable structure across all planning sessions. There are no
  conditional fields, path-dependent variations, or format differences
  between success and failure responses.

- Final Planning Result: The Engine Response delivers the final planning
  determination produced by the session, including the decision and all
  supporting information.

- Execution Summary: The Engine Response includes a summary of the
  execution session, enabling consumers to understand what occurred during
  planning without inspecting module internals.

- Module Outputs: The Engine Response preserves the outputs produced by
  individual modules, making them available to consumers that require
  per-module detail.

- Execution Status: The Engine Response communicates the overall outcome
  of the execution session — whether it completed successfully, partially,
  or failed.

- Downstream Decoupling: By defining a fixed output contract, the Engine
  Response decouples the Planning Engine from its consumers. Downstream
  systems depend on the response structure, not on the internal workings
  of the Engine.

==============================================================================
Response Principles
==============================================================================

The Engine Response shall adhere to the following architecture-level
principles:

- Deterministic Structure: The Engine Response shall have a deterministic
  structure. Every execution with the same inputs and execution path
  produces the same response shape.

- Presentation Independence: The Engine Response shall remain independent
  from presentation. It defines data, not display. Any consumer may render
  or format the response according to its own needs.

- Transport Independence: The Engine Response shall remain independent
  from transport mechanisms. The response structure is defined without
  reference to how it is delivered, transmitted, or received.

- Public Boundary: The Engine Response shall expose only the public output
  of the Planning Engine. It is the outermost output boundary and contains
  no internal state, execution details, or component internals.

==============================================================================
Response Structure
==============================================================================

The Engine Response consists of four top-level sections:

Engine Response
├── Decision
├── Summary
├── Module Results
└── Status

Each section serves a distinct purpose within the response:

- Decision: The final planning determination produced by the session.
  This section contains the substantive planning output.

- Summary: A high-level overview of the execution session, including
  session metadata and execution characteristics.

- Module Results: The outputs produced by individual planning modules
  during execution, preserved for consumers that require module-level
  detail.

- Status: The overall execution outcome of the planning session.

The Engine Response has no other top-level sections. Any data that does
not fit into one of these four sections is outside the scope of the
response.

==============================================================================
Response Types
==============================================================================

a) Decision

   The Decision section contains the final planning determination produced
   by the session. This is the primary output that consumers of the
   Planning Engine receive.

   The Decision section is responsible for containing the substantive
   planning result. Its internal structure is defined by the Decision
   Output specification (Chapter 4.5).

b) Summary

   The Summary section provides a high-level overview of the execution
   session. It describes what occurred during planning without exposing
   module internals or implementation details.

   The Summary section is responsible for containing session-level
   execution information that aids understanding of the planning result.

c) Module Results

   The Module Results section preserves the outputs produced by each
   planning module during execution. It enables consumers that require
   per-module detail to access individual module outputs without
   additional processing.

   The Module Results section is responsible for containing the collected
   outputs of all executed modules. Each module entry is identifiable and
   traceable. The Engine Response aggregates module outputs without
   modifying their semantic meaning.

d) Status

   The Status section communicates the overall execution outcome of the
   planning session. Status represents execution completion rather than
   planning quality or decision correctness.

   The Status section is responsible for indicating the execution outcome
   in a standardized format that all consumers can interpret uniformly.

==============================================================================
Standard Fields
==============================================================================

The Engine Response contains the following mandatory top-level fields:

| Field           | Purpose                                                     |
|-----------------|-------------------------------------------------------------|
| Decision        | Contains the final planning determination                   |
| Summary         | Provides a high-level overview of the execution session     |
| Module Results  | Preserves the outputs produced by each planning module      |
| Status          | Indicates the overall execution outcome                     |

All four fields are mandatory. Every Engine Response MUST contain each
field, regardless of whether the execution succeeded or failed. The Engine
Response shall contain all standard fields in every execution outcome.

The internal structure of each field is defined by its respective
specification. The Engine Response itself defines only the top-level
field names and their responsibilities.

==============================================================================
Out of Scope
==============================================================================

The Engine Response MUST NOT include:

- Execution Logic: The Engine Response MUST NOT describe how the planning
  result was produced. It contains only the result itself.

- Planning Algorithms: The Engine Response MUST NOT include algorithm
  descriptions, reasoning steps, or internal computation details.

- Business Rules: The Engine Response MUST NOT contain business rule
  definitions or domain-specific logic.

- Context Construction: The Engine Response MUST NOT include instructions
  for constructing or reconstructing the execution Context.

- Module Orchestration: The Engine Response MUST NOT describe the order or
  manner in which modules were orchestrated during execution.

- API Specification: The Engine Response MUST NOT define how the response
  is delivered over an API. API specification is a separate concern.

- Transport Protocol: The Engine Response MUST NOT define the protocol
  used to transmit the response to consumers.

- Serialization: The Engine Response MUST NOT specify how the response is
  serialised. Serialisation format is an implementation concern.

- Streaming: The Engine Response MUST NOT support incremental or
  streamed delivery. The response is produced as a complete result.

- Rendering: The Engine Response MUST NOT include presentation or
  formatting instructions for visual rendering.

- UI: The Engine Response MUST NOT include user interface elements,
  display logic, or interactive components.

- Presentation Layer: The Engine Response MUST NOT define how the
  response is displayed to users.

- Persistence: The Engine Response MUST NOT define how or where the
  response is stored after delivery.

- Notifications: The Engine Response MUST NOT include notification
  logic, delivery confirmations, or acknowledgement mechanisms.