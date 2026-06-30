"""
RIKAA V1.2 — Planning Engine Blueprint
Runtime 0.4: Dispatcher
=========================================

Defines the Runtime Dispatcher as the execution bridge between Runtime and
the Decision Layer.

This chapter specifies architectural contracts only. It does not introduce
implementation logic, algorithms, or executable code.

==============================================================================
0.4.1 Purpose
==============================================================================

The Dispatcher is the execution bridge between Runtime and the Decision
Layer. It is the only component responsible for invoking the Decision
Engine, ROI Framework, and Hermes in the correct order.

The Dispatcher coordinates execution only. It contains no business logic,
never makes decisions, never performs ROI optimisation, and never generates
responses. Its sole responsibility is to dispatch execution to the
appropriate layer and collect the results.

The Dispatcher exists to isolate the Runtime Orchestrator from the details
of layer invocation. The Orchestrator controls the pipeline sequence; the
Dispatcher handles the actual invocation of each layer.

Architecture Position
---------------------

Runtime Orchestrator
    ↓
Runtime Dispatcher
    ↓
Decision Engine → ROI Framework → Hermes
    ↓
DispatcherResult → Response Builder

==============================================================================
0.4.2 Responsibilities
==============================================================================

The Dispatcher is responsible for:

- Building the execution request for each layer based on the current
  RuntimeContext
- Invoking the Decision Engine (Chapter 4) with the appropriate inputs
- Invoking the ROI Optimization Framework (Chapter 5) with the decision
  outputs
- Invoking Hermes (Execution Agent) with the optimisation recommendation
- Maintaining the correct execution order across all invocations
- Collecting execution results from each layer
- Returning a DispatcherResult containing all layer outputs

The Dispatcher is NOT responsible for:

- Performing planning or decision making
- Performing ROI optimisation or analysis
- Performing Hermes logic or execution
- Generating responses
- Modifying layer outputs
- Interpreting or validating layer results
- Recovering from layer errors
- Maintaining state between invocations

The Dispatcher invokes, collects, and returns. It does not transform.

==============================================================================
0.4.3 Decision Dispatch
==============================================================================

The Dispatcher invokes the Decision Engine (Chapter 4) to produce a
decision based on the planning outputs stored in the RuntimeContext.

Input
-----

The Dispatcher extracts the following from the RuntimeContext:

- Planning Context: The outputs produced by the Planning Layer (Chapter 3),
  including goals, constraints, requirements, assumptions, risks, and
  related planning artifacts.

- Request Context: The original and normalized request data.

The Dispatcher does not modify or interpret these inputs. It passes them
to the Decision Engine as received.

Invocation
----------

The Dispatcher invokes the Decision Engine with the extracted inputs. The
Decision Engine executes its internal decision process and returns a
DecisionOutput.

The Dispatcher does not participate in any decision logic. It does not
influence, guide, or constrain the decision process. It only ensures that
the Decision Engine receives the correct inputs.

Output
------

The Dispatcher receives the DecisionOutput from the Decision Engine. The
DecisionOutput contains:

- Selected Strategy: The strategy selected by the Decision Engine.
- Alternatives: Alternative strategies that were evaluated.
- Decision Score: The score or ranking of the selected strategy.
- Confidence: The confidence level of the decision.
- Escalation Result: Any escalation outcome.

The Dispatcher stores the DecisionOutput for inclusion in the
DispatcherResult.

Decision Dispatch Flow
----------------------

RuntimeContext
    ↓
Dispatcher extracts Planning Context
    ↓
Dispatcher invokes Decision Engine
    ↓
Decision Engine returns DecisionOutput
    ↓
Dispatcher stores DecisionOutput

==============================================================================
0.4.4 ROI Dispatch
==============================================================================

The Dispatcher invokes the ROI Optimization Framework (Chapter 5) to
produce an optimized execution recommendation based on the decision
outputs.

Input
-----

The Dispatcher extracts the following from the RuntimeContext and the
DecisionOutput:

- Decision Context: The outputs produced by the Decision Engine, including
  the selected strategy and alternatives.

- Optimization Objectives: The goals defined by the ROI Framework
  (Chapter 5.2).

- Optimization Constraints: The boundaries defined by the ROI Framework
  (Chapter 5.3).

- Optimization Factors: The evaluation criteria defined by the ROI
  Framework (Chapter 5.4).

The Dispatcher does not modify or interpret these inputs. It passes them
to the ROI Framework as received.

Invocation
----------

The Dispatcher invokes the ROI Framework with the extracted inputs. The
ROI Framework executes its optimization process and returns an
OptimizationResult.

The Dispatcher never performs ROI calculations itself. It does not
evaluate costs, analyse trade-offs, or compute recommendations. It only
ensures that the ROI Framework receives the correct inputs.

Output
------

The Dispatcher receives the OptimizationResult from the ROI Framework. The
OptimizationResult contains:

- Recommended Strategy: The execution strategy recommended by the
  optimization process.
- Cost Analysis: The cost evaluation performed during optimization.
- Time Analysis: The time evaluation performed during optimization.
- Resource Analysis: The resource utilisation analysis.
- Trade-off Analysis: The trade-offs considered during optimization.
- Supporting Rationale: The reasoning that justifies the recommendation.

The Dispatcher stores the OptimizationResult for inclusion in the
DispatcherResult.

ROI Dispatch Flow
-----------------

DecisionOutput
    ↓
Dispatcher extracts Decision Context
    ↓
Dispatcher invokes ROI Framework
    ↓
ROI Framework returns OptimizationResult
    ↓
Dispatcher stores OptimizationResult

==============================================================================
0.4.5 Hermes Dispatch
==============================================================================

The Dispatcher invokes Hermes (Execution Agent) to execute the recommended
strategy. Hermes performs the actual execution work based on the
optimization recommendation.

Input
-----

The Dispatcher extracts the following from the OptimizationResult:

- DecisionOutput: The original decision output produced by the Decision
  Engine.

- ROIResult: The optimization result produced by the ROI Framework,
  including the recommended strategy and supporting analysis.

The Dispatcher does not modify or interpret these inputs. It passes them
to Hermes as received.

Invocation
----------

The Dispatcher invokes Hermes with the extracted inputs. Hermes executes
the recommended strategy and produces an ExecutionBlueprint.

The Dispatcher does not participate in execution. It does not generate
blueprints, execute tasks, or monitor execution progress. Blueprint
generation belongs entirely to Hermes.

Output
------

The Dispatcher receives the ExecutionBlueprint from Hermes. The
ExecutionBlueprint contains:

- Executed Modules: The modules that were executed.
- Execution Order: The order of execution.
- Tool Calls: Records of tool invocations.
- Generated Outputs: The outputs produced during execution.
- Execution Metadata: Timing, retry count, and related metadata.

The Dispatcher stores the ExecutionBlueprint for inclusion in the
DispatcherResult.

Hermes Dispatch Flow
--------------------

OptimizationResult
    ↓
Dispatcher extracts DecisionOutput + ROIResult
    ↓
Dispatcher invokes Hermes
    ↓
Hermes returns ExecutionBlueprint
    ↓
Dispatcher stores ExecutionBlueprint

==============================================================================
0.4.6 Result Collection
==============================================================================

After all layers have been invoked, the Dispatcher collects the outputs
from each layer into a single DispatcherResult.

The Dispatcher aggregates the following outputs:

- From Decision Engine: DecisionOutput
- From ROI Framework: OptimizationResult
- From Hermes: ExecutionBlueprint

The Dispatcher only aggregates outputs. It never modifies component
outputs, never reinterprets results, never reorders or filters data, and
never adds new information.

The DispatcherResult preserves the original structure of each layer's
output. Downstream components receive the outputs exactly as produced by
their originating layers.

Result Collection Flow
----------------------

DecisionOutput  ─┐
                  ├──→ DispatcherResult
OptimizationResult ─┤
                    │
ExecutionBlueprint ─┘

==============================================================================
0.4.7 Outputs
==============================================================================

The Dispatcher produces a single output:

DispatcherResult
---------------

The DispatcherResult contains all layer outputs collected during
execution:

- DecisionOutput: The output produced by the Decision Engine (Chapter 4),
  including the selected strategy, alternatives, scores, and confidence.

- OptimizationResult: The output produced by the ROI Optimization
  Framework (Chapter 5), including the recommended strategy, cost
  analysis, time analysis, resource analysis, and trade-off analysis.

- ExecutionBlueprint: The output produced by Hermes, including executed
  modules, execution order, tool calls, generated outputs, and execution
  metadata.

The DispatcherResult becomes the input for the Runtime Response Builder.
The Response Builder uses the DispatcherResult to construct the final
RuntimeResponse.

Overall Dispatcher Pipeline
---------------------------

Runtime Orchestrator
    ↓
Runtime Dispatcher
    ↓
├── Decision Dispatch  ──→  DecisionOutput
├── ROI Dispatch       ──→  OptimizationResult
├── Hermes Dispatch    ──→  ExecutionBlueprint
    ↓
DispatcherResult
    ↓
Response Builder