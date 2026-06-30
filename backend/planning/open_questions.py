"""Blueprint Module 3.10 — Open Questions Module.

Uses Hermes for semantic understanding of open questions.
Owns the Blueprint boundary: JSON deserialization, validation, and structured output.
"""

import json

from models.chat import OpenQuestionsResult, PlanningContext
from prompts.open_questions_prompt import get_open_questions_system_prompt
from services.ollama_service import send_messages_to_ollama

_EXPECTED_KEYS = {"open_question_list", "question_priority", "required_action", "target_resolution_point"}


def identify_open_questions(context: PlanningContext) -> OpenQuestionsResult:
    """Identify open questions by instructing Hermes.

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
        "Based on all the above, record the open questions."
    )
    messages = [
        {"role": "system", "content": get_open_questions_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    raw_response = send_messages_to_ollama(messages)

    return _parse_open_questions_json(raw_response)


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


def _parse_open_questions_json(raw: str) -> OpenQuestionsResult:
    """Deserialize Hermes JSON response into an OpenQuestionsResult.

    If JSON is invalid or fields are missing, missing fields default
    to 'Not Specified'. No inference is performed.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return OpenQuestionsResult()

    # Extract only known fields, ignore any extras Hermes might return
    return OpenQuestionsResult(
        open_question_list=_normalize_missing(data.get("open_question_list", "Not Specified")),
        question_priority=_normalize_missing(data.get("question_priority", "Not Specified")),
        required_action=_normalize_missing(data.get("required_action", "Not Specified")),
        target_resolution_point=_normalize_missing(data.get("target_resolution_point", "Not Specified")),
    )