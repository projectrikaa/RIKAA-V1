"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 6.3: Hermes Communication Contract — Runtime → Hermes Request
========================================================================

Defines the standardized request contract sent from Runtime to Hermes.

This chapter describes only the communication contract. It does not
describe Hermes internal implementation, execution logic, planning logic,
or Runtime workflow.

==============================================================================
6.3.1 Purpose
==============================================================================

HermesRequest is the standardized interface used by Runtime to invoke
Hermes. It defines the structure, fields, and validation rules for all
communication sent from Runtime to Hermes.

The request contract provides:

- Standardized Communication: Every Runtime-to-Hermes interaction uses
  the same request structure, ensuring consistency across all requests
  regardless of source or context.

- Independent Validation: Hermes validates every request against the
  contract before execution begins. Requests that do not conform to the
  contract are rejected with a standardised validation error.

- Stable Interface: The contract defines a stable interface that Runtime
  and Hermes both commit to honouring. Changes to either component's
  internal implementation do not affect the other as long as the request
  contract is honoured.

- Version Compatibility: The contract includes a version field that
  enables Runtime and Hermes to agree on a compatible schema version.
  Version mismatches are detected before execution.

==============================================================================
6.3.2 HermesRequest Schema
==============================================================================

The HermesRequest contains the following fields:

| Field          | Type     | Required | Description |
|----------------|----------|----------|-------------|
| version        | string   | Required | Schema version of the request contract |
| request_id     | string   | Required | Unique identifier for this request |
| trace_id       | string   | Required | Trace identifier for cross-component correlation |
| runtime_context| object   | Required | Runtime execution context and metadata |
| user_input     | string   | Required | Original user input or request |
| conversation   | array    | Optional | Conversation history for multi-turn interactions |
| knowledge      | array    | Optional | Knowledge base references or context |
| constraints    | object   | Optional | Execution constraints and limitations |
| config         | object   | Optional | Runtime configuration for Hermes execution |

==============================================================================
6.3.3 Required Fields
==============================================================================

The following fields are required in every HermesRequest. Hermes must
reject any request that omits a required field before execution begins.

version
-------

The schema version of the request contract. Enables Runtime and Hermes
to agree on a compatible contract version. Requests with unsupported
versions must be rejected.

request_id
----------

A unique identifier for this request. Enables request tracing,
correlation with responses, and deduplication. Each request must have
a unique identifier.

trace_id
--------

A trace identifier shared across components for end-to-end request
correlation. Enables Runtime, Hermes, and other components to correlate
log entries, errors, and metrics for a single request lifecycle.

runtime_context
---------------

The Runtime execution context required by Hermes to process the request.
Contains metadata about the execution environment, pipeline state, and
contextual information from the Runtime Context.

user_input
----------

The original user input or request that initiated the pipeline. Hermes
uses the user input as the primary source for planning and analytical
work.

==============================================================================
6.3.4 Optional Fields
==============================================================================

The following fields are optional in a HermesRequest. Hermes applies
documented default behaviour when optional fields are absent.

conversation
------------

Conversation history for multi-turn interactions. When present, Hermes
uses the conversation history to maintain context across multiple
requests. When absent, Hermes processes the request without conversation
context.

knowledge
---------

Knowledge base references or context that may inform execution. When
present, Hermes may use the knowledge references to augment its
planning and analysis. When absent, Hermes processes the request without
external knowledge.

constraints
-----------

Execution constraints and limitations that apply to this request. When
present, Hermes must honour the specified constraints during execution.
When absent, Hermes applies default constraints defined by its internal
configuration.

config
------

Runtime configuration parameters for Hermes execution. When present,
Hermes uses the specified configuration to adjust its execution
behaviour. When absent, Hermes applies default configuration.

==============================================================================
6.3.5 Field Definitions
==============================================================================

version
-------

Purpose: Identifies the schema version of the request contract.

Ownership: Runtime (set by Dispatcher when constructing the request).

Usage: Hermes reads the version to determine which schema rules apply
to the request. Runtime and Hermes must agree on a supported version
before communication can proceed.

request_id
----------

Purpose: Provides a unique identifier for each request.

Ownership: Runtime (generated by the Input Handler or Orchestrator).

Usage: Hermes returns the request_id in the response for correlation.
Runtime uses the request_id to match responses to requests.

trace_id
--------

Purpose: Provides a trace identifier for cross-component correlation.

Ownership: Runtime (generated at pipeline initiation).

Usage: All components in the pipeline share the same trace_id for a
single request lifecycle. Hermes includes the trace_id in log entries,
errors, and metrics.

runtime_context
---------------

Purpose: Provides the Runtime execution context required by Hermes.

Ownership: Runtime (populated from the Runtime Context).

Usage: Hermes reads the runtime_context to understand the execution
environment, pipeline state, and contextual information. The runtime_
context is read-only during execution.

user_input
----------

Purpose: Provides the original user input or request.

Ownership: Runtime (received by the Input Handler).

Usage: Hermes uses the user_input as the primary source for its
planning and analytical work. The user_input is the original request
content before any processing by Runtime.

conversation
------------

Purpose: Provides conversation history for multi-turn interactions.

Ownership: Runtime (retrieved from the Runtime Context).

Usage: Hermes uses conversation history to maintain context across
multiple requests in a session. Each entry in the conversation array
represents a previous exchange.

knowledge
---------

Purpose: Provides knowledge base references or context.

Ownership: Runtime (retrieved from the Knowledge Layer, if available).

Usage: Hermes may use knowledge references to augment its planning and
analysis. Knowledge entries are references, not inline content. Hermes
resolves references using its own knowledge access mechanisms.

constraints
-----------

Purpose: Specifies execution constraints and limitations.

Ownership: Runtime (derived from the planning and optimization stages).

Usage: Hermes must honour the specified constraints during execution.
Constraints may include resource limits, time bounds, or policy
restrictions defined during planning.

config
------

Purpose: Provides Runtime configuration for Hermes execution.

Ownership: Runtime (derived from pipeline configuration).

Usage: Hermes uses configuration parameters to adjust its execution
behaviour. Configuration may include execution mode, verbosity, or
behavioural flags.

==============================================================================
6.3.6 Validation Rules
==============================================================================

Before Hermes begins execution, it must validate the HermesRequest
against the following rules:

1. Supported Schema Version

   Hermes must verify that the version field specifies a supported
   schema version. Requests specifying an unsupported or unknown version
   must be rejected.

2. Required Fields Present

   Hermes must verify that all required fields are present in the
   request. Requests missing any required field must be rejected before
   execution begins.

3. Correct Field Types

   Hermes must verify that each field conforms to its expected type as
   defined in the schema. Requests with type mismatches must be
   rejected.

4. Valid Structure

   Hermes must verify that the overall structure of the request is well-
   formed. Requests with structural defects must be rejected.

5. Valid Identifiers

   Hermes must verify that identifiers (request_id, trace_id) are valid.
   Requests with malformed or empty identifiers must be rejected.

6. No Malformed Request

   Hermes must verify that the request is not malformed in any way that
   prevents processing. Malformed requests must be rejected.

If validation fails, Hermes must return a standardised validation error
in the HermesResponse. The error must indicate the specific validation
rule that was violated.

==============================================================================
6.3.7 Versioning
==============================================================================

Every HermesRequest includes a version field that specifies the schema
version of the request contract.

- Runtime and Hermes communicate using an agreed contract version. Both
  components must support at least one common version.

- Future schema evolution must preserve backward compatibility whenever
  practical. Additive changes (new optional fields, new validation
  rules) shall not break existing consumers.

- Breaking changes to the schema (removing fields, changing type
  requirements) must increment the version number. Runtime and Hermes
  may support multiple versions during transition periods.

- The contract version is independent of Runtime and Hermes component
  versions. Component version upgrades do not require contract version
  changes unless the schema itself changes.

==============================================================================
6.3.8 Design Principles
==============================================================================

The HermesRequest contract adheres to the following design principles:

1. Standardized Request Format

   Every Runtime-to-Hermes interaction uses the same request structure.
   There is no ad-hoc or custom request format.

2. Runtime Constructs Requests

   Runtime is solely responsible for constructing HermesRequest objects.
   Hermes never initiates communication with Runtime.

3. Hermes Validates Requests

   Hermes validates every request against the contract before execution.
   Invalid requests are rejected with a standardised error.

4. Immutable Request During Execution

   The HermesRequest is immutable during execution. Hermes must not
   modify the request. Runtime must not modify the request after
   sending it.

5. Clear Ownership Boundaries

   Each field in the request has a defined owner. Runtime owns the
   request construction. Hermes owns the request validation and
   processing.

6. Forward-Compatible Schema Evolution

   The schema supports additive evolution. New optional fields and new
   validation rules can be added without breaking existing consumers.