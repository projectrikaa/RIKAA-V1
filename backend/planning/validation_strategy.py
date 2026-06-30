"""Blueprint Module 3.11 — Validation Strategy Module.

Uses Hermes for semantic understanding of validation strategy.
Owns the Blueprint boundary: JSON deserialization, validation, and structured output.
"""

import json

from models.chat import ValidationStrategyResult, PlanningContext
from prompts.validation_strategy_prompt import get_validation_strategy_system_prompt
from services.ollama_service import send_messages_to_ollama

_EXPECTED_KEYS = {"validation_plan", "validation_method", "validation_checklist", "validation_schedule", "acceptance_decision"}


def identify_validation_strategy(context: PlanningContext) -> ValidationStrategyResult:
    """Identify validation strategy by instructing Hermes.

    Consumes all previous PlanningContext fields to construct the analysis.
    Hermes owns semantic reasoning and returns JSON.
    This module owns deserialization, validation, and Blueprint boundaries.
    """
    p = context.purpose
    pr = context.problem
    t = context.target_outcome
    s = context.success_criteria
    sc = context.scope
    a = context.anti_goals
    c = context.constraints
    asm = context.assumptions
    ev = context.evidence
    oq = context.open_questions
    user_message = (
        f"Primary Purpose: {p.primary_purpose}\n"
        f"Secondary Purpose: {p.secondary_purpose}\n"
        f"Expected Value: {p.expected_value}\n"
        "\n"
        "Problem:\n"
        f"Problem Statement: {pr.problem_statement}\n"
        f"Root Cause: {pr.root_cause}\n"
        f"Impact: {pr.impact}\n"
        f"Stakeholders Affected: {pr.stakeholders_affected}\n"
        "\n"
        "Target Outcome:\n"
        f"Target Outcome Statement: {t.target_outcome_statement}\n"
        f"Desired Future State: {t.desired_future_state}\n"
        f"Expected Business Outcome: {t.expected_business_outcome}\n"
        f"Expected User Outcome: {t.expected_user_outcome}\n"
        f"Outcome Boundaries: {t.outcome_boundaries}\n"
        "\n"
        "Success Criteria:\n"
        f"Success Criteria: {s.success_criteria}\n"
        f"Acceptance Rules: {s.acceptance_rules}\n"
        f"Measurement Rules: {s.measurement_rules}\n"
        "\n"
        "Scope:\n"
        f"Scope Statement: {sc.scope_statement}\n"
        f"In-Scope Items: {sc.in_scope_items}\n"
        f"Out-of-Scope Items: {sc.out_of_scope_items}\n"
        f"Scope Boundary: {sc.scope_boundary}\n"
        "\n"
        "Anti-Goals:\n"
        f"Anti-Goals: {a.anti_goals}\n"
        f"Non-Targeted Objectives: {a.non_targeted_objectives}\n"
        f"Optimization Exclusions: {a.optimization_exclusions}\n"
        "\n"
        "Constraints:\n"
        f"Constraint List: {c.constraint_list}\n"
        f"Constraint Categories: {c.constraint_categories}\n"
        f"Constraint Boundaries: {c.constraint_boundaries}\n"
        "\n"
        "Assumptions:\n"
        f"Assumption List: {asm.assumption_list}\n"
        f"Confidence Rating: {asm.confidence_rating}\n"
        f"Validation Priority: {asm.validation_priority}\n"
        f"Review Conditions: {asm.review_conditions}\n"
        "\n"
        "Evidence:\n"
        f"Evidence List: {ev.evidence_list}\n"
        f"Evidence Classification: {ev.evidence_classification}\n"
        f"Source References: {ev.source_references}\n"
        f"Evidence Coverage: {ev.evidence_coverage}\n"
        "\n"
        "Open Questions:\n"
        f"Open Question List: {oq.open_question_list}\n"
        f"Question Priority: {oq.question_priority}\n"
        f"Required Action: {oq.required_action}\n"
        f"Target Resolution Point: {oq.target_resolution_point}\n"
        "\n"
        "Based on all the above, define the validation strategy."
    )
    messages = [
        {"role": "system", "content": get_validation_strategy_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    raw_response = send_messages_to_ollama(messages)

    return _parse_validation_strategy_json(raw_response)


def _normalize_missing(value) -> str:
    """Normalize missing/null/empty values to 'Not Specified'.

    Rules:
      None        → "Not Specified"
      ""          → "Not Specified"
      "None"      → "Not Specified"
      "null"      → "Not Specified"
      whitespace  → "Not Specified"
    Otherwise returns the original value unchanged.
    """
    if value is None:
        return "Not Specified"
    s = str(value).strip()
    if s in ("", "None", "null"):
        return "Not Specified"
    return value


def _parse_validation_strategy_json(raw: str) -> ValidationStrategyResult:
    """Deserialize Hermes JSON response into a ValidationStrategyResult.

    If JSON is invalid or fields are missing, missing fields default
    to 'Not Specified'. No inference is performed.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return ValidationStrategyResult()

    # Extract only known fields, ignore any extras Hermes might return
    return ValidationStrategyResult(
        validation_plan=_normalize_missing(data.get("validation_plan", "Not Specified")),
        validation_method=_normalize_missing(data.get("validation_method", "Not Specified")),
        validation_checklist=_normalize_missing(data.get("validation_checklist", "Not Specified")),
        validation_schedule=_normalize_missing(data.get("validation_schedule", "Not Specified")),
        acceptance_decision=_normalize_missing(data.get("acceptance_decision", "Not Specified")),
    )