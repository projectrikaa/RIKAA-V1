# RIKAA Blueprint — Master Architecture Report

**Version:** 1.2
**Date:** 2026-06-30
**Status:** In Progress (4 of ~10 chapters completed)
**Purpose:** Master reference document for architecture reviews, implementation planning, onboarding, and gap analysis.

---

# Part I: Completed Chapters

---

## Chapter 3 — Planning Layer

### 1. Overview

| Field | Value |
|-------|-------|
| Chapter Name | Planning Layer |
| Status | Completed |
| Freeze Status | Approved for freeze |
| Number of Sections | 13 modules |
| Number of Subsections | ~65 subsections |

### 2. Purpose

The Planning Layer exists to decompose a user request into structured planning concerns. It answers: *what needs to be done, why, under what conditions, and with what risks?* Each module addresses one planning concern. Together they produce the Decision Blueprint consumed by downstream layers.

The architectural problem it solves is transforming unstructured input into structured, auditable, and verifiable planning artifacts.

### 3. Responsibilities

- Define the purpose of the execution
- Define the problem to be solved
- Define the target outcome
- Define success criteria
- Define scope boundaries
- Define anti-goals (what will not be done)
- Define constraints
- Define assumptions
- Collect supporting evidence
- Identify open questions
- Define validation strategy
- Identify decision risks
- Define sunset conditions

### 4. Out of Scope

- Execution logic
- Decision making
- Optimization
- Runtime coordination
- Response generation
- Business logic execution

### 5. Structure

```
Chapter 3: Planning Layer
├── 3.1 Purpose Module
├── 3.2 Problem Definition Module
├── 3.3 Target Outcome Module
├── 3.4 Success Criteria Module
├── 3.5 Scope Definition Module
├── 3.6 Anti-Goals Module
├── 3.7 Constraints Module
├── 3.8 Assumptions Module
├── 3.9 Evidence Module
├── 3.10 Open Questions Module
├── 3.11 Validation Strategy Module
├── 3.12 Decision Risks Module
└── 3.13 Sunset Conditions Module
```

### 6. Section Summary

#### 3.1 Purpose Module

| Field | Value |
|-------|-------|
| Purpose | Define the primary and secondary purpose of the execution |
| Input | User request (via Context Object) |
| Output | Purpose statement |
| Dependencies | None (first module) |
| Related Chapters | Consumed by all downstream modules |

#### 3.2 Problem Definition Module

| Field | Value |
|-------|-------|
| Purpose | Define the problem that needs to be solved |
| Input | Purpose statement |
| Output | Problem statement, root cause, impact, stakeholders |
| Dependencies | 3.1 Purpose |
| Related Chapters | Consumed by 3.3 Target Outcome |

#### 3.3 Target Outcome Module

| Field | Value |
|-------|-------|
| Purpose | Define the desired outcome of the execution |
| Input | Problem statement |
| Output | Target outcome, success indicators |
| Dependencies | 3.2 Problem |
| Related Chapters | Consumed by 3.4 Success Criteria |

#### 3.4 Success Criteria Module

| Field | Value |
|-------|-------|
| Purpose | Define measurable criteria for success |
| Input | Target outcome |
| Output | Success criteria, acceptance criteria |
| Dependencies | 3.3 Target Outcome |
| Related Chapters | Consumed by 3.5 Scope |

#### 3.5 Scope Definition Module

| Field | Value |
|-------|-------|
| Purpose | Define what is in scope and out of scope |
| Input | Success criteria |
| Output | Scope boundaries, inclusions, exclusions |
| Dependencies | 3.4 Success Criteria |
| Related Chapters | Consumed by 3.6 Anti-Goals |

#### 3.6 Anti-Goals Module

| Field | Value |
|-------|-------|
| Purpose | Define what will explicitly not be done |
| Input | Scope definition |
| Output | Anti-goals list |
| Dependencies | 3.5 Scope |
| Related Chapters | Consumed by 3.7 Constraints |

#### 3.7 Constraints Module

| Field | Value |
|-------|-------|
| Purpose | Define boundaries and limitations |
| Input | Anti-goals |
| Output | Constraint list |
| Dependencies | 3.6 Anti-Goals |
| Related Chapters | Consumed by 3.8 Assumptions |

#### 3.8 Assumptions Module

| Field | Value |
|-------|-------|
| Purpose | Document assumptions made during planning |
| Input | Constraints |
| Output | Assumption list |
| Dependencies | 3.7 Constraints |
| Related Chapters | Consumed by 3.9 Evidence |

#### 3.9 Evidence Module

| Field | Value |
|-------|-------|
| Purpose | Collect supporting evidence for planning decisions |
| Input | Assumptions |
| Output | Evidence records |
| Dependencies | 3.8 Assumptions |
| Related Chapters | Consumed by 3.10 Open Questions |

#### 3.10 Open Questions Module

| Field | Value |
|-------|-------|
| Purpose | Identify unresolved questions |
| Input | Evidence |
| Output | Open questions list |
| Dependencies | 3.9 Evidence |
| Related Chapters | Consumed by 3.11 Validation Strategy |

#### 3.11 Validation Strategy Module

| Field | Value |
|-------|-------|
| Purpose | Define how the plan will be validated |
| Input | Open questions |
| Output | Validation strategy |
| Dependencies | 3.10 Open Questions |
| Related Chapters | Consumed by 3.12 Decision Risks |

#### 3.12 Decision Risks Module

| Field | Value |
|-------|-------|
| Purpose | Identify risks associated with the plan |
| Input | Validation strategy |
| Output | Risk register |
| Dependencies | 3.11 Validation Strategy |
| Related Chapters | Consumed by 3.13 Sunset Conditions |

#### 3.13 Sunset Conditions Module

| Field | Value |
|-------|-------|
| Purpose | Define conditions under which the plan should be retired |
| Input | Decision risks |
| Output | Sunset conditions |
| Dependencies | 3.12 Decision Risks |
| Related Chapters | Final module — output consumed by Decision Engine |

### 7. Internal Execution Flow

```
User Request → 3.1 → 3.2 → 3.3 → 3.4 → 3.5 → 3.6 → 3.7 → 3.8 → 3.9 → 3.10 → 3.11 → 3.12 → 3.13
                                                                                                    ↓
                                                                                          Decision Blueprint
```

The flow is strictly sequential. Each module depends on the output of the previous module. The Context Object accumulates state as it passes through each module. Modules are read-only consumers of the Context Object.

### 8. External Dependencies

| Direction | Component | Relationship |
|-----------|-----------|--------------|
| Depends On | Context Object (Chapter 4.3) | Each module receives a read-only Context Object |
| Depends On | Standard Module Interface (Chapter 4.2) | Each module implements the universal contract |
| Used By | Decision Engine Runner (Chapter 4.4) | Runner invokes modules in sequence |
| Used By | Decision Output (Chapter 4.5) | Outputs are aggregated into Decision Blueprint |

### 9. Public Contracts

- **Module Interface:** Every module implements: `fn execute(context: ContextObject) -> ModuleResult`
- **Context Object:** Read-only shared state passed through the pipeline
- **ModuleResult:** Standardised output structure containing status, data, and errors
- **Execution Order:** Fixed sequential order (3.1 → 3.13)
- **Error Handling:** Modules return status codes; Runner handles propagation

### 10. Design Principles

- **Single Responsibility:** Each module owns exactly one planning concern
- **Sequential Execution:** Modules execute in fixed order; no parallel execution
- **Read-Only Context:** Modules read Context Object but never modify it
- **Deterministic Output:** Same inputs produce same ModuleResult
- **Immutable Pipeline:** Module order cannot be changed during execution

### 11. Key Design Decisions

- **13 separate modules** rather than one monolithic planner: Enables independent testing, replacement, and extension of individual planning concerns.
- **Sequential execution** rather than parallel: Planning concerns have natural dependencies (purpose before problem, problem before outcome). Sequential execution ensures consistency.
- **Read-only Context Object** rather than writable: Prevents modules from interfering with each other's state. Ensures data integrity.

### 12. Future Extension Points

- New planning modules can be added to the sequence if new planning concerns are identified
- Module order can be reconfigured for different planning methodologies
- Additional output formats can be added to ModuleResult

### 13. Revision History

- Initial creation of 13 planning modules
- Integration with Decision Engine Runner
- Standard Module Interface alignment

---

## Chapter 4 — Decision Engine

### 1. Overview

| Field | Value |
|-------|-------|
| Chapter Name | Decision Engine |
| Status | Completed |
| Freeze Status | Approved for freeze |
| Number of Sections | 8 chapters |
| Number of Subsections | ~50 subsections |

### 2. Purpose

The Decision Engine exists to execute the planning modules in sequence, manage their shared state, handle errors, and produce a structured Decision Output. It solves the architectural problem of orchestrating 13 independent planning modules into a coherent execution pipeline.

### 3. Responsibilities

- Define the static architecture of the engine
- Define the universal module interface contract
- Define the shared Context Object
- Execute modules in sequence via the Runner
- Aggregate module outputs into Decision Output
- Handle errors with standardised status semantics
- Produce the Engine Response
- Manage the Engine lifecycle

### 4. Out of Scope

- Planning logic (owned by Chapter 3)
- Business logic
- Optimization (owned by Chapter 5)
- Runtime coordination (owned by Chapter 0)
- Response formatting (owned by Chapter 0.5)

### 5. Structure

```
Chapter 4: Decision Engine
├── 4.1 Engine Architecture
├── 4.2 Standard Module Interface
├── 4.3 Context Object
├── 4.4 Runner
├── 4.5 Decision Output
├── 4.6 Error Handling
├── 4.7 Engine Response
└── 4.8 Engine Lifecycle
```

### 6. Section Summary

#### 4.1 Engine Architecture

| Field | Value |
|-------|-------|
| Purpose | Define the static composition of the Planning Engine |
| Responsibilities | Component boundaries, ownership, design principles |
| Dependencies | None (foundational chapter) |
| Related Chapters | All Chapter 4 sections |

#### 4.2 Standard Module Interface

| Field | Value |
|-------|-------|
| Purpose | Define the universal contract every module implements |
| Input | Context Object (read-only) |
| Output | ModuleResult |
| Dependencies | 4.1 Architecture |
| Related Chapters | 4.3 Context Object, 4.4 Runner |

#### 4.3 Context Object

| Field | Value |
|-------|-------|
| Purpose | Define the shared data object passed through the pipeline |
| Responsibilities | Accumulate planning state, enforce access rules |
| Dependencies | 4.2 Standard Module Interface |
| Related Chapters | 4.4 Runner, 4.5 Decision Output |

#### 4.4 Runner

| Field | Value |
|-------|-------|
| Purpose | Execute modules in sequence |
| Input | Context Object |
| Output | Completed Context Object with all module results |
| Dependencies | 4.2 Interface, 4.3 Context Object |
| Related Chapters | 4.5 Decision Output, 4.6 Error Handling |

#### 4.5 Decision Output

| Field | Value |
|-------|-------|
| Purpose | Aggregate all module results into structured output |
| Input | Completed Context Object |
| Output | Decision Blueprint |
| Dependencies | 4.4 Runner |
| Related Chapters | 4.7 Engine Response |

#### 4.6 Error Handling

| Field | Value |
|-------|-------|
| Purpose | Define error categories, status semantics, propagation |
| Responsibilities | Standardised error management within the Engine |
| Dependencies | 4.4 Runner |
| Related Chapters | 4.8 Engine Lifecycle |

#### 4.7 Engine Response

| Field | Value |
|-------|-------|
| Purpose | Wrap Decision Output in standard response envelope |
| Input | Decision Output |
| Output | EngineResponse |
| Dependencies | 4.5 Decision Output |
| Related Chapters | Consumed by Runtime Dispatcher (0.4) |

#### 4.8 Engine Lifecycle

| Field | Value |
|-------|-------|
| Purpose | Define lifecycle stages and state transitions |
| Responsibilities | Initialisation, execution, completion, termination |
| Dependencies | All Chapter 4 sections |
| Related Chapters | Runtime Orchestrator (0.3) |

### 7. Internal Execution Flow

```
Engine Lifecycle (4.8)
    ↓
Runner (4.4) invokes modules via Standard Module Interface (4.2)
    ↓
Context Object (4.3) accumulates state
    ↓
Decision Output (4.5) aggregates results
    ↓
Engine Response (4.7) wraps output
    ↓
Error Handling (4.6) manages failures at every stage
```

### 8. External Dependencies

| Direction | Component | Relationship |
|-----------|-----------|--------------|
| Depends On | Chapter 3 modules | Engine executes Chapter 3 modules |
| Used By | Runtime Dispatcher (0.4) | Dispatcher invokes Engine |
| Used By | Runtime Context (0.2) | Engine outputs stored in decision_context |

### 9. Public Contracts

- **Standard Module Interface:** `fn execute(context: ContextObject) -> ModuleResult`
- **Context Object:** Read-only shared state
- **ModuleResult:** Status + data + errors
- **EngineResponse:** Complete engine output
- **Lifecycle States:** 6 fixed stages with deterministic transitions

### 10. Design Principles

- **Single Responsibility:** Each engine component owns one concern
- **Deterministic Execution:** Same inputs produce same outputs
- **Immutable Context:** Modules read only; Engine writes
- **Standardised Errors:** All errors use defined status semantics
- **Sequential Lifecycle:** Stages execute in fixed order

### 11. Key Design Decisions

- **Separate Engine Architecture (4.1)** from implementation: Enables independent evolution of architecture and implementation.
- **Standard Module Interface (4.2)** as universal contract: Ensures all 13 modules can be invoked uniformly without special cases.
- **Read-only Context Object (4.3):** Prevents module interference and ensures data integrity.
- **Runner (4.4)** as dedicated execution component: Separates execution logic from module logic.

### 12. Future Extension Points

- New module types can implement the Standard Module Interface
- Runner can support different execution strategies (parallel, conditional)
- Additional lifecycle stages can be added
- New error categories can be defined

### 13. Revision History

- Initial creation of 8 engine chapters
- Standard Module Interface refined for consistency
- Context Object aligned with Runtime Context

---

## Chapter 5 — ROI Optimization Framework

### 1. Overview

| Field | Value |
|-------|-------|
| Chapter Name | ROI Optimization Framework |
| Status | Completed |
| Freeze Status | Approved for freeze (with minor fixes) |
| Number of Sections | 8 chapters |
| Number of Subsections | ~45 subsections |

### 2. Purpose

The ROI Optimization Framework exists to transform approved planning outputs into optimised execution strategies. It evaluates candidate strategies against defined objectives, constraints, and factors, and produces a recommendation. It solves the architectural problem of selecting the best execution approach without making final decisions.

### 3. Responsibilities

- Define the purpose and scope of the Execution Layer
- Define optimization objectives (cost, time, resource, quality)
- Define optimization constraints (hard, soft, dynamic)
- Define optimization factors (evaluation, trade-off, priority)
- Define the optimization process (evaluate, compare, recommend)
- Define the optimization result structure
- Define framework principles (determinism, explainability, extensibility, separation)
- Define the extension model for future capabilities

### 4. Out of Scope

- Planning decisions (owned by Chapter 3)
- Final decision authority (owned by external system)
- Business logic
- Implementation algorithms
- Execution mechanics (owned by Hermes)
- Runtime coordination (owned by Chapter 0)

### 5. Structure

```
Chapter 5: ROI Optimization Framework
├── 5.1 Purpose
├── 5.2 Optimization Objectives
├── 5.3 Optimization Constraints
├── 5.4 Optimization Factors
├── 5.5 Optimization Process
├── 5.6 Optimization Result
├── 5.7 Framework Principles
└── 5.8 Extension Model
```

### 6. Section Summary

#### 5.1 Purpose

| Field | Value |
|-------|-------|
| Purpose | Define the purpose, responsibilities, and scope of the Execution Layer |
| Responsibilities | Scope definition, design philosophy, layer boundaries |
| Dependencies | Chapter 3 (Decision Blueprint), Chapter 4 (Engine) |
| Related Chapters | All Chapter 5 sections |

#### 5.2 Optimization Objectives

| Field | Value |
|-------|-------|
| Purpose | Define measurable objectives that guide strategy selection |
| Output | Four core objectives: cost, time, resource, quality |
| Dependencies | 5.1 Purpose |
| Related Chapters | 5.3 Constraints, 5.4 Factors |

#### 5.3 Optimization Constraints

| Field | Value |
|-------|-------|
| Purpose | Define boundaries within which optimization must operate |
| Output | Three constraint categories: hard, soft, dynamic |
| Dependencies | 5.2 Objectives |
| Related Chapters | 5.4 Factors, 5.5 Process |

#### 5.4 Optimization Factors

| Field | Value |
|-------|-------|
| Purpose | Define criteria used to evaluate and compare strategies |
| Output | Evaluation factors, trade-off factors, priority factors |
| Dependencies | 5.3 Constraints |
| Related Chapters | 5.5 Process |

#### 5.5 Optimization Process

| Field | Value |
|-------|-------|
| Purpose | Define the standard process for producing recommendations |
| Input | Objectives, Constraints, Factors, Decision Blueprint |
| Output | Recommended Execution Strategy |
| Dependencies | 5.2, 5.3, 5.4 |
| Related Chapters | 5.6 Result |

#### 5.6 Optimization Result

| Field | Value |
|-------|-------|
| Purpose | Define standardized outputs of the Optimization Layer |
| Output | Optimization Recommendation, Optimization Report |
| Dependencies | 5.5 Process |
| Related Chapters | Consumed by Runtime Dispatcher (0.4) |

#### 5.7 Framework Principles

| Field | Value |
|-------|-------|
| Purpose | Define architectural principles governing all Execution Layer components |
| Output | Four principles: Determinism, Explainability, Extensibility, Separation |
| Dependencies | All Chapter 5 sections |
| Related Chapters | 5.8 Extension Model |

#### 5.8 Extension Model

| Field | Value |
|-------|-------|
| Purpose | Define how the Execution Layer may be extended |
| Output | Extension Policy, Compatibility Requirements, Boundary Definitions |
| Dependencies | 5.7 Principles |
| Related Chapters | Future extensions |

### 7. Internal Execution Flow

```
5.1 Purpose → 5.2 Objectives → 5.3 Constraints → 5.4 Factors → 5.5 Process → 5.6 Result
                                                                                        ↓
                                                                          5.7 Principles (governs all)
                                                                                        ↓
                                                                          5.8 Extension Model (evolution)
```

### 8. External Dependencies

| Direction | Component | Relationship |
|-----------|-----------|--------------|
| Depends On | Chapter 3 (Decision Blueprint) | Provides approved planning outputs |
| Depends On | Chapter 4 (EngineResponse) | Provides execution context |
| Used By | Runtime Dispatcher (0.4) | Dispatcher invokes ROI Framework |
| Used By | Runtime Context (0.2) | Outputs stored in optimization_context |

### 9. Public Contracts

- **Optimization Objectives:** Four measurable goals
- **Optimization Constraints:** Three constraint categories
- **Optimization Factors:** Evaluation, trade-off, priority factors
- **Optimization Process:** Evaluate → Compare → Recommend
- **Optimization Result:** Recommendation + Report
- **Framework Principles:** Determinism, Explainability, Extensibility, Separation

### 10. Design Principles

- **Blueprint Preservation:** Never modifies the Decision Blueprint
- **Constraint Compliance:** All strategies validated against constraints
- **Objective Alignment:** Recommendations aligned with objectives
- **Deterministic Evaluation:** Same inputs produce same outputs
- **Execution Only:** Operates strictly within Execution Layer

### 11. Key Design Decisions

- **"Recommended" not "Best":** Terminology refined from "best" to "recommended" to avoid implying decision authority.
- **Four separate chapters for objectives, constraints, factors, process:** Enables independent evolution of each concern.
- **Framework Principles (5.7) as separate chapter:** Ensures principles are explicitly documented and not buried in other chapters.
- **Extension Model (5.8) as separate chapter:** Explicitly defines how the framework evolves without redesign.

### 12. Future Extension Points

- New optimization objectives can be added (5.2)
- New constraint types can be defined (5.3)
- New evaluation factors can be introduced (5.4)
- New process strategies can be supported (5.5)
- New result formats can be added (5.6)
- Extensions follow the Extension Model (5.8)

### 13. Revision History

- Terminology refinement: "Best" → "Recommended"
- Execution Principles reordered by priority
- Decision Authority Review completed (no architectural leakage found)
- Cross-Chapter Architecture Review completed (approved with minor fixes)

---

## Runtime Layer — Chapter 0

### 1. Overview

| Field | Value |
|-------|-------|
| Chapter Name | Runtime Layer |
| Status | Completed |
| Freeze Status | Approved for freeze |
| Number of Sections | 8 chapters |
| Number of Subsections | ~60 subsections |

### 2. Purpose

The Runtime Layer exists to coordinate the complete execution pipeline from request reception through final response delivery. It acts as the outermost container that invokes the Planning Layer, Decision Engine, and Optimization Framework in the correct sequence. It solves the architectural problem of orchestrating multiple independent layers into a single, deterministic execution flow.

### 3. Responsibilities

- Receive and validate external requests
- Create and manage the Runtime Context
- Control the execution pipeline sequence
- Invoke the Dispatcher for Decision Layer execution
- Invoke the Response Builder for response construction
- Handle errors with standardised error management
- Produce the final RuntimeResponse
- Maintain stateless execution between requests

### 4. Out of Scope

- Planning logic (owned by Chapter 3)
- Decision making (owned by Chapter 3/4)
- Optimization (owned by Chapter 5)
- Business logic
- Module execution
- Response content generation
- State persistence across requests

### 5. Structure

```
Runtime Layer (Chapter 0)
├── 0.0 Runtime Foundation
├── 0.1 Input Handler
├── 0.2 Runtime Context
├── 0.3 Orchestrator
├── 0.4 Dispatcher
├── 0.5 Response Builder
├── 0.6 Error Handling
└── 0.7 End-to-End Runtime Flow
```

### 6. Section Summary

#### 0.0 Runtime Foundation

| Field | Value |
|-------|-------|
| Purpose | Establish the Runtime architecture, responsibilities, lifecycle, and design principles |
| Responsibilities | Define layer scope, components, flow, principles |
| Dependencies | None (foundational chapter) |
| Related Chapters | All Runtime sections |

#### 0.1 Input Handler

| Field | Value |
|-------|-------|
| Purpose | Single entry point for all external requests |
| Input | External request (User, API, CLI, Scheduler, Internal) |
| Output | RuntimeRequest |
| Dependencies | 0.0 Foundation |
| Related Chapters | 0.2 Runtime Context |

#### 0.2 Runtime Context

| Field | Value |
|-------|-------|
| Purpose | Shared state container for a single Runtime execution |
| Input | RuntimeRequest |
| Output | RuntimeContext (9 sections) |
| Dependencies | 0.1 Input Handler |
| Related Chapters | 0.3 Orchestrator, 0.4 Dispatcher, 0.5 Response Builder, 0.6 Error Handling |

#### 0.3 Orchestrator

| Field | Value |
|-------|-------|
| Purpose | Control execution order and manage Runtime lifecycle |
| Input | RuntimeContext |
| Output | RuntimeResponse or RuntimeErrorResponse |
| Dependencies | 0.2 Runtime Context |
| Related Chapters | 0.4 Dispatcher, 0.5 Response Builder |

#### 0.4 Dispatcher

| Field | Value |
|-------|-------|
| Purpose | Execution bridge between Runtime and Decision Layer |
| Input | RuntimeContext |
| Output | DispatcherResult (DecisionOutput + OptimizationResult + ExecutionBlueprint) |
| Dependencies | 0.3 Orchestrator |
| Related Chapters | Chapter 4, Chapter 5, Hermes |

#### 0.5 Response Builder

| Field | Value |
|-------|-------|
| Purpose | Final stage of the Runtime Pipeline |
| Input | RuntimeContext, DispatcherResult |
| Output | RuntimeResponse |
| Dependencies | 0.4 Dispatcher |
| Related Chapters | 0.6 Error Handling |

#### 0.6 Error Handling

| Field | Value |
|-------|-------|
| Purpose | Unified error management framework |
| Input | RuntimeError from any component |
| Output | RuntimeErrorInfo, Runtime Status, Error Log |
| Dependencies | All Runtime sections |
| Related Chapters | 0.5 Response Builder |

#### 0.7 End-to-End Runtime Flow

| Field | Value |
|-------|-------|
| Purpose | Illustrate the complete Runtime execution pipeline |
| Type | Documentation only |
| Dependencies | All Runtime sections |
| Related Chapters | All Blueprint chapters |

### 7. Internal Execution Flow

```
External Request
    ↓
0.1 Input Handler → RuntimeRequest
    ↓
0.2 Runtime Context (created and initialized)
    ↓
0.3 Orchestrator
    ↓
0.4 Dispatcher
    ├── Decision Engine (Chapter 4)
    ├── ROI Framework (Chapter 5)
    └── Hermes
    ↓
0.5 Response Builder
    ↓
RuntimeResponse
    ↑
0.6 Error Handling (cross-cutting — any stage may trigger)
```

### 8. External Dependencies

| Direction | Component | Relationship |
|-----------|-----------|--------------|
| Depends On | Chapter 4 (Decision Engine) | Dispatcher invokes Engine |
| Depends On | Chapter 5 (ROI Framework) | Dispatcher invokes Framework |
| Depends On | Hermes | Dispatcher invokes Hermes |
| Used By | External callers | RuntimeResponse is the only output |

### 9. Public Contracts

- **RuntimeRequest:** Validated and normalized request object
- **RuntimeContext:** 9-section shared state container
- **RuntimeResponse:** Status + Payload + Metadata + Warnings + Errors
- **RuntimeErrorInfo:** Category + Code + Message + Source + Recoverable + Details + Timestamp
- **DispatcherResult:** DecisionOutput + OptimizationResult + ExecutionBlueprint
- **Runtime States:** INITIALIZED → PLANNING → DECISION → OPTIMIZATION → EXECUTION → RESPONSE → COMPLETED | FAILED | CANCELLED

### 10. Design Principles

- **Single Responsibility:** Each Runtime component owns one concern
- **Stateless by Default:** No state between requests
- **Deterministic Flow:** Same inputs produce same outputs
- **Blueprint-driven:** Executes according to Blueprint architecture
- **Execution Separation:** Coordinates only; never performs logic
- **Immutable Previous Stages:** Completed stages cannot be modified
- **Append-only Pipeline:** Context grows as pipeline progresses
- **Layer Isolation:** Each layer owns its own Context section

### 11. Key Design Decisions

- **Orchestrator (0.3) vs Dispatcher (0.4) separation:** Originally Orchestrator directly invoked Decision Layer components. Refined to separate concerns: Orchestrator controls pipeline; Dispatcher handles Decision Layer invocation. Eliminated responsibility overlap.
- **Runtime Context (0.2) as central state container:** All layers read from and write to the Context. Eliminates duplicate state and ensures Single Source of Truth.
- **Error Handling (0.6) as cross-cutting concern:** Errors can occur at any stage. Centralised error management ensures consistent handling.
- **Response Builder (0.5) as only output producer:** No other component constructs the final response. Ensures consistent output format.

### 12. Future Extension Points

- New input sources can be added to Input Handler (0.1)
- New Context sections can be added (0.2)
- New pipeline stages can be added to Orchestrator (0.3)
- New Decision Layer components can be dispatched (0.4)
- New output formats can be added to Response Builder (0.5)
- New error categories can be defined (0.6)

### 13. Revision History

- Orchestrator (0.3) refined to remove responsibility overlap with Dispatcher (0.4)
- Error Handling (0.6) refined: "Runtime Error" → "Runtime Infrastructure Error"; recoverability clarified; pipeline status clarified
- Complete Runtime Layer review completed (approved for freeze)

---

# Part II: Cross-Chapter Analysis

## Overall Blueprint Architecture

The completed Blueprint forms a linear pipeline with four major layers:

```
External Request
    ↓
┌─────────────────────────────────────────────────────────────┐
│  Runtime Layer (Chapter 0)                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
│  │ Input    │→│ Context  │→│ Orchest- │→│ Dispatcher   │ │
│  │ Handler  │  │          │  │ rator    │  │              │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────┬───────┘ │
└─────────────────────────────────────────────────────┼─────────┘
                                                      ↓
┌─────────────────────────────────────────────────────┼─────────┐
│  Decision Layer                                      │         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────┴───────┐ │
│  │ Decision Engine  │→│ ROI Framework   │→│ Hermes       │ │
│  │ (Chapter 4)      │  │ (Chapter 5)      │  │ (Execution)  │ │
│  └────────┬─────────┘  └──────────────────┘  └──────────────┘ │
│           ↓                                                   │
│  ┌──────────────────┐                                         │
│  │ Planning Layer   │ (invoked by Engine)                     │
│  │ (Chapter 3)      │                                         │
│  │ 13 modules       │                                         │
│  └──────────────────┘                                         │
└───────────────────────────────────────────────────────────────┘
                      ↓
┌───────────────────────────────────────────────────────────────┐
│  Runtime Layer (Chapter 0)                                     │
│  ┌──────────────────┐                                          │
│  │ Response Builder │→ RuntimeResponse                        │
│  └──────────────────┘                                          │
└───────────────────────────────────────────────────────────────┘
```

## Dependency Graph

```
Chapter 3 (Planning) ────→ Chapter 4 (Engine) ────→ Chapter 5 (ROI) ────→ Runtime (Chapter 0)
       │                         │                         │                      │
       │ Provides modules        │ Provides EngineResponse  │ Provides             │ Orchestrates all
       │ for execution           │ for context             │ OptimizationResult   │ layers
       ↓                         ↓                         ↓                      ↓
  Context Object          Runtime Context            Runtime Context        RuntimeResponse
  (Chapter 4.3)           (Chapter 0.2)              (Chapter 0.2)          (Chapter 0.5)
```

**Dependency direction:** Strictly one-way: Chapter 3 → Chapter 4 → Chapter 5 → Chapter 0

**No circular dependencies.**

**No reverse dependencies.**

## Responsibility Matrix

| Responsibility | Owner | Chapter |
|---------------|-------|---------|
| Define purpose | Purpose Module | 3.1 |
| Define problem | Problem Module | 3.2 |
| Define target outcome | Target Outcome Module | 3.3 |
| Define success criteria | Success Criteria Module | 3.4 |
| Define scope | Scope Module | 3.5 |
| Define anti-goals | Anti-Goals Module | 3.6 |
| Define constraints | Constraints Module | 3.7 |
| Define assumptions | Assumptions Module | 3.8 |
| Collect evidence | Evidence Module | 3.9 |
| Identify open questions | Open Questions Module | 3.10 |
| Define validation strategy | Validation Strategy Module | 3.11 |
| Identify decision risks | Decision Risks Module | 3.12 |
| Define sunset conditions | Sunset Conditions Module | 3.13 |
| Engine architecture | Engine Architecture | 4.1 |
| Module interface contract | Standard Module Interface | 4.2 |
| Shared state container | Context Object | 4.3 |
| Module execution | Runner | 4.4 |
| Output aggregation | Decision Output | 4.5 |
| Error classification | Error Handling | 4.6 |
| Output envelope | Engine Response | 4.7 |
| Engine lifecycle | Engine Lifecycle | 4.8 |
| Execution Layer scope | Purpose | 5.1 |
| Optimization goals | Optimization Objectives | 5.2 |
| Optimization boundaries | Optimization Constraints | 5.3 |
| Evaluation criteria | Optimization Factors | 5.4 |
| Selection process | Optimization Process | 5.5 |
| Output format | Optimization Result | 5.6 |
| Architectural governance | Framework Principles | 5.7 |
| Evolution policy | Extension Model | 5.8 |
| Runtime architecture | Runtime Foundation | 0.0 |
| Request reception | Input Handler | 0.1 |
| Execution state | Runtime Context | 0.2 |
| Pipeline coordination | Orchestrator | 0.3 |
| Decision Layer invocation | Dispatcher | 0.4 |
| Response construction | Response Builder | 0.5 |
| Error management | Error Handling | 0.6 |

**Every responsibility has exactly one owner. No overlaps. No gaps.**

## Architectural Consistency Review

| Check | Status | Notes |
|-------|--------|-------|
| Terminology consistency | ✅ Pass | "Decision Blueprint", "RuntimeContext", "RuntimeResponse" used consistently |
| Naming consistency | ✅ Pass | Chapter numbering, file naming, section headers consistent |
| Responsibility consistency | ✅ Pass | Each responsibility owned by exactly one chapter |
| Execution consistency | ✅ Pass | Pipeline flow is deterministic and documented |
| Dependency consistency | ✅ Pass | One-way dependencies, no circular dependencies |

**Minor inconsistency identified:** "Optimisation" vs "Optimization" spelling varies across documents (British vs American English). Does not affect architecture.

## Missing Architecture

| Chapter | Classification | Reason |
|---------|---------------|--------|
| Chapter 1 — Framework Overview | Critical | Required to define foundational concepts, terminology, and system context |
| Chapter 2 — Governance Layer | Critical | Required to define governance policies, rules engine, and compliance |
| Chapter 6 — Hermes Execution | Critical | Required to define the execution agent that Runtime Dispatcher invokes |
| Chapter 7 — Memory Layer | Recommended | Required for persistent state across sessions |
| Chapter 8 — Knowledge Layer | Recommended | Required for knowledge base integration |
| Chapter 9 — Tooling Layer | Future | Required for tool integration and management |

## Blueprint Completion Assessment

| Metric | Value | Rationale |
|--------|-------|-----------|
| Overall completion | ~45% | 4 of ~10 chapters completed |
| Architecture maturity | High (completed chapters) | Completed chapters have been reviewed, refined, and frozen |
| Implementation readiness | Ready (completed chapters) | Architecture is stable and ready for implementation |
| Maintainability | High | Single Responsibility, modular design, clear boundaries |
| Scalability | High | Stateless, deterministic, horizontally scalable |
| Extensibility | High | Extension points documented in every chapter |

## Gap Analysis

| Gap | Status | Notes |
|-----|--------|-------|
| Missing contracts | None | All interfaces defined (Module Interface, Context Object, RuntimeRequest, RuntimeResponse, RuntimeErrorInfo) |
| Missing execution flow | None | Complete pipeline documented (0.7) |
| Missing interfaces | None | Standard Module Interface (4.2), Dispatcher contracts (0.4) |
| Missing lifecycle definitions | None | Engine Lifecycle (4.8), Runtime Context Lifecycle (0.2), Runtime States (0.2) |
| Missing ownership | None | Responsibility matrix complete |

## Freeze Status

| Chapter | Status | Justification |
|---------|--------|---------------|
| Chapter 3 — Planning Layer | **Freeze** | 13 modules complete, reviewed, integrated with Engine |
| Chapter 4 — Decision Engine | **Freeze** | 8 chapters complete, architecture reviewed, consistent |
| Chapter 5 — ROI Optimization Framework | **Freeze** (minor fixes) | Minor terminology refinements identified but no architectural changes needed |
| Runtime Layer (Chapter 0) | **Freeze** | 8 chapters complete, responsibility overlap resolved, reviewed |

---

# Part III: Remaining Work

## Roadmap

```
Completed
✅ Runtime Layer (Chapter 0) — 8 sections
✅ Planning Layer (Chapter 3) — 13 modules
✅ Decision Engine (Chapter 4) — 8 sections
✅ ROI Optimization Framework (Chapter 5) — 8 sections

Remaining
□ Chapter 1 — Framework Overview
□ Chapter 2 — Governance Layer
□ Chapter 6 — Hermes Execution
□ Chapter 7 — Memory Layer
□ Chapter 8 — Knowledge Layer
□ Chapter 9 — Tooling Layer
```

## Remaining Chapters

### Chapter 1 — Framework Overview

| Field | Value |
|-------|-------|
| Purpose | Define foundational concepts, terminology, and system context |
| Why needed | Required before any other chapter can be fully understood |
| Dependencies | None |
| Complexity | Low |
| Order | 1st |

### Chapter 2 — Governance Layer

| Field | Value |
|-------|-------|
| Purpose | Define governance policies, rules engine, compliance, and oversight |
| Why needed | Required to ensure system operates within defined boundaries |
| Dependencies | Chapter 1 |
| Complexity | Medium |
| Order | 2nd |

### Chapter 6 — Hermes Execution

| Field | Value |
|-------|-------|
| Purpose | Define the execution agent that Runtime Dispatcher invokes |
| Why needed | Required to complete the pipeline (Dispatcher → Hermes) |
| Dependencies | Chapter 0 (Runtime), Chapter 4, Chapter 5 |
| Complexity | High |
| Order | 3rd |

### Chapter 7 — Memory Layer

| Field | Value |
|-------|-------|
| Purpose | Define memory management and persistence across sessions |
| Why needed | Required for stateful interactions |
| Dependencies | Chapter 0, Chapter 6 |
| Complexity | Medium |
| Order | 4th |

### Chapter 8 — Knowledge Layer

| Field | Value |
|-------|-------|
| Purpose | Define knowledge base integration and retrieval |
| Why needed | Required for knowledge-augmented execution |
| Dependencies | Chapter 0, Chapter 6, Chapter 7 |
| Complexity | Medium |
| Order | 5th |

### Chapter 9 — Tooling Layer

| Field | Value |
|-------|-------|
| Purpose | Define tool integration and management |
| Why needed | Required for external tool execution |
| Dependencies | Chapter 0, Chapter 6 |
| Complexity | Medium |
| Order | 6th |

---

# Part IV: Executive Summary

## Key Metrics

| Metric | Value |
|--------|-------|
| Total completed chapters | 4 |
| Total completed sections | 37 |
| Blueprint maturity | ~45% complete |
| Frozen chapters | 4 of 4 completed |
| Remaining chapters | 6 |
| Critical gaps | 3 (Chapters 1, 2, 6) |

## Core Architectural Strengths

1. **Strict Single Responsibility:** Every component owns exactly one concern. No overlaps.
2. **Deterministic Pipeline:** Same inputs always produce same outputs. Predictable and auditable.
3. **Clear Layer Boundaries:** Planning, Decision, Optimization, and Runtime are strictly separated.
4. **Stateless Runtime:** No state between requests. Horizontally scalable.
5. **Standardised Interfaces:** Module Interface, Context Object, RuntimeRequest, RuntimeResponse, RuntimeErrorInfo — all standardised.
6. **Explicit Non-Responsibilities:** Every chapter documents what it does NOT do.
7. **Extensibility by Design:** Extension points documented in every chapter.

## Architectural Risks

1. **Hermes undefined:** The pipeline depends on Hermes (Execution Agent) which has not been designed yet. This is the highest-priority risk.
2. **Governance undefined:** No governance policies defined. System operates without oversight rules.
3. **Framework Overview missing:** No single document defines foundational concepts and terminology.

## Recommended Next Milestone

**Complete Chapter 6 — Hermes Execution.**

Rationale: The Runtime Dispatcher (0.4) already references Hermes as the execution agent. Without Hermes, the pipeline is incomplete. All other remaining chapters (Memory, Knowledge, Tooling) depend on Hermes being defined first.

## Overall Recommendation

The Blueprint Foundation (Chapters 0, 3, 4, 5) is **stable, consistent, and ready for implementation.**

The next phase should focus on:

1. **Chapter 1 — Framework Overview** (foundational concepts)
2. **Chapter 2 — Governance Layer** (governance policies)
3. **Chapter 6 — Hermes Execution** (execution agent — highest priority)

After these three chapters are complete, the core pipeline will be fully defined and implementation can begin.