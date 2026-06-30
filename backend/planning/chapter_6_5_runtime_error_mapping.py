"""
RIKAA V1.2 — Planning Engine Blueprint
Chapter 6.5: Hermes Communication Contract — Runtime Error Mapping
====================================================================

Defines how Hermes execution errors are translated into standardized
Runtime Errors.

This chapter defines mapping rules only. It does not describe how Hermes
detects or generates errors, how Runtime handles errors, Runtime Response
construction, retry logic, or logging implementation.

==============================================================================
6.5.1 Purpose
==============================================================================

Runtime never exposes Hermes-specific error types. All Hermes execution
errors are translated into standardized Runtime Errors before continuing
through the Runtime pipeline.

The purpose of this mapping is twofold:

1. Provide a stable interface: Runtime depends on a fixed set of error
   categories. Changes to Hermes internal error types do not propagate
   to Runtime as long as the mapping is maintained.

2. Enable independent evolution: Hermes can change its internal error
   detection and classification without affecting Runtime, provided the
   mapping rules defined in this chapter are honoured.

==============================================================================
6.5.2 Mapping Principles
==============================================================================

The Hermes-to-Runtime error mapping adheres to the following principles:

1. Runtime Never Exposes Hermes Error Types

   Error types defined by Hermes shall not appear in the Runtime error
   space. Every Hermes error is translated to a Runtime error category
   before entering the Runtime pipeline.

2. Every Hermes Error Maps to Exactly One Runtime Error Category

   The mapping is one-to-one. A Hermes error shall not map to multiple
   Runtime error categories, and multiple Hermes errors shall not map to
   the same Runtime error category unless explicitly specified.

3. Mapping Shall Be Deterministic

   Given the same Hermes error input, the mapping shall always produce
   the same Runtime error output. Non-deterministic mapping is not
   permitted.

4. Error Category Shall Be Preserved

   The semantic meaning of the error category shall be preserved through
   the mapping. A timeout error on the Hermes side shall map to a timeout
   error on the Runtime side.

5. Error Message May Be Preserved

   The original error message from Hermes may be preserved in the Runtime
   error metadata for diagnostic purposes. The message may be adapted to
   remove implementation-specific details.

6. Metadata Should Be Preserved Whenever Possible

   Metadata accompanying the Hermes error should be preserved in the
   Runtime error metadata where applicable.

7. Trace Information Should Be Preserved When Available

   Trace identifiers from Hermes should be preserved in the Runtime error
   trace information for cross-component correlation.

8. Hermes Implementation Details Shall Not Leak into Runtime

   The mapping shall not expose Hermes internal architecture, component
   names, or implementation details in the Runtime error output.

==============================================================================
6.5.3 Standard Mapping
==============================================================================

The following table defines the standard mapping between Hermes errors
and Runtime errors:

| Hermes Error              | Runtime Error                |
|---------------------------|------------------------------|
| HermesTimeout             | RuntimeTimeoutError          |
| HermesValidationError     | RuntimeValidationError       |
| HermesInternalError       | RuntimeInternalError         |
| HermesExecutionError      | RuntimeExecutionError        |
| HermesConfigurationError  | RuntimeConfigurationError    |

This mapping shall be applied whenever a Hermes error crosses the
Runtime-Hermes boundary. No Hermes error shall reach Runtime without
being mapped.

The mapping preserves the error category semantics:

- Timeout errors remain timeout errors.
- Validation errors remain validation errors.
- Internal errors remain internal errors.
- Execution errors remain execution errors.
- Configuration errors remain configuration errors.

The specific error codes, messages, and metadata may vary between the
Hermes error and the corresponding Runtime error, but the category
semantics shall be preserved.

==============================================================================
6.5.4 Mapping Rules
==============================================================================

When translating a Hermes error to a Runtime error, the following rules
shall be observed:

1. Translate Error Category

   Determine the Hermes error category and look up the corresponding
   Runtime error category in the mapping table. The Runtime error shall
   use the mapped category.

2. Preserve Error Message

   The original Hermes error message should be preserved in the Runtime
   error metadata. If the message contains implementation-specific
   details, those details should be removed or generalized to prevent
   implementation leakage.

3. Preserve Metadata

   Any metadata accompanying the Hermes error should be preserved in the
   Runtime error metadata where applicable. Metadata that contains
   implementation-specific details should be excluded.

4. Preserve Trace Information

   Trace identifiers from the Hermes error should be preserved in the
   Runtime error trace information. Trace information enables cross-
   component correlation during diagnostics.

5. Do Not Expose Hermes Implementation Details

   The mapped Runtime error shall not contain Hermes internal component
   names, architecture details, or implementation specifics. The mapped
   error shall be indistinguishable from a Runtime-native error.

6. Mapping Behavior Shall Be Deterministic

   Multiple mappings of the same Hermes error shall produce the same
   Runtime error. The mapping shall not depend on Runtime state,
   execution context, or external conditions.

==============================================================================
6.5.5 Scope
==============================================================================

This chapter defines mapping only. The following topics belong to other
Blueprint chapters and are not specified here:

- Hermes Error Generation: How Hermes detects and produces errors is
  internal to Hermes and outside the scope of this contract.

- Hermes Internal Exception Handling: How Hermes handles exceptions
  internally is not part of the Runtime-Hermes communication contract.

- Runtime Error Handling (Chapter 0.6): How Runtime processes, records,
  and propagates errors after mapping is defined in the Runtime Error
  Handling specification.

- Runtime Response Construction (Chapter 0.5): How the Response Builder
  constructs error responses is defined in the Response Builder
  specification.

- Retry Policies: Retry logic is not part of the Runtime-Hermes
  communication contract.

- Logging Implementation: How errors are logged is an implementation
  detail not specified here.