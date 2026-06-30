from models.chat import PlanningContext
from planning.purpose import identify_purpose
from planning.problem import define_problem
from planning.target_outcome import identify_target_outcome
from planning.success_criteria import identify_success_criteria
from planning.scope import define_scope
from planning.anti_goals import identify_anti_goals
from planning.constraints import identify_constraints
from planning.assumptions import identify_assumptions
from planning.evidence import identify_evidence
from planning.open_questions import identify_open_questions
from planning.validation_strategy import identify_validation_strategy
from planning.decision_risks import identify_decision_risks
from planning.sunset_conditions import identify_sunset_conditions


def create_plan(message: str) -> PlanningContext:
    """Planning layer for RIKAA Core.

    Orchestrates planning modules in strict Blueprint order:

      1. Purpose Module — identify user's purpose (receives raw user_request)
      2. Problem Definition Module — define the problem (receives PlanningContext)
      3. Target Outcome Module — identify desired future state (receives PlanningContext)
      4. Success Criteria Module — define success criteria (receives PlanningContext)
      5. Scope Module — define scope (receives PlanningContext)
      6. Anti-Goals Module — define anti-goals (receives PlanningContext)
      7. Constraints Module — define constraints (receives PlanningContext)
      8. Assumptions Module — define assumptions (receives PlanningContext)
      9. Evidence Module — record evidence (receives PlanningContext)
     10. Open Questions Module — record open questions (receives PlanningContext)
     11. Validation Strategy Module — define validation strategy (receives PlanningContext)
     12. Decision Risks Module — identify decision risks (receives PlanningContext)
     13. Sunset Conditions Module — determine sunset conditions (receives PlanningContext)

    Each module after 3.1 consumes the accumulated PlanningContext.
    No module after 3.1 analyses the original user request independently.

    Returns:
        PlanningContext with purpose, problem, target_outcome, success_criteria,
        scope, anti_goals, constraints, assumptions, evidence, open_questions,
        validation_strategy, decision_risks, and sunset_conditions populated.
    """
    context = PlanningContext()

    # Module 3.1: receives raw user_request
    context.purpose = identify_purpose(message)

    # Module 3.2: receives PlanningContext, consumes context.purpose
    context.problem = define_problem(context)

    # Module 3.3: receives PlanningContext, consumes context.purpose + context.problem
    context.target_outcome = identify_target_outcome(context)

    # Module 3.4: receives PlanningContext, consumes context.purpose + context.problem + context.target_outcome
    context.success_criteria = identify_success_criteria(context)

    # Module 3.5: receives PlanningContext, consumes context.purpose + context.problem + context.target_outcome + context.success_criteria
    context.scope = define_scope(context)

    # Module 3.6: receives PlanningContext, consumes all previous module outputs
    context.anti_goals = identify_anti_goals(context)

    # Module 3.7: receives PlanningContext, consumes all previous module outputs
    context.constraints = identify_constraints(context)

    # Module 3.8: receives PlanningContext, consumes all previous module outputs
    context.assumptions = identify_assumptions(context)

    # Module 3.9: receives PlanningContext, consumes all previous module outputs
    context.evidence = identify_evidence(context)

    # Module 3.10: receives PlanningContext, consumes all previous module outputs
    context.open_questions = identify_open_questions(context)

    # Module 3.11: receives PlanningContext, consumes all previous module outputs
    context.validation_strategy = identify_validation_strategy(context)

    # Module 3.12: receives PlanningContext, consumes all previous module outputs
    context.decision_risks = identify_decision_risks(context)

    # Module 3.13: receives PlanningContext, consumes all previous module outputs
    context.sunset_conditions = identify_sunset_conditions(context)

    return context
