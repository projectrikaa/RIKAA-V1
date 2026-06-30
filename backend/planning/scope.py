"""Blueprint Module 3.5 — Scope Definition Module.

Uses Hermes for semantic understanding of scope.
Owns the Blueprint boundary: JSON deserialization, validation, and structured output.
"""

import json

from models.chat import PlanningContext, ScopeResult
from prompts.scope_prompt import get_scope_system_prompt
from services.ollama_service import send_messages_to_ollama

_EXPECTED_KEYS = {"scope_statement", "in_scope_items", "out_of_scope_items", "scope_boundary"}


def define_scope(context: PlanningContext) -> ScopeResult:
    """Define scope by instructing Hermes.

    Consumes PlanningContext.purpose, PlanningContext.problem,
    PlanningContext.target_outcome, and PlanningContext.success_criteria
    to construct the analysis.
    Hermes owns semantic reasoning and returns JSON.
    This module owns deserialization, validation, and Blueprint boundaries.
    """
    p = context.purpose
    pr = context.problem
    t = context.target_outcome
    s = context.success_criteria
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
        "Based on the purpose, problem, target outcome, and success criteria above, "
        "define the scope."
    )
    messages = [
        {"role": "system", "content": get_scope_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    raw_response = send_messages_to_ollama(messages)

    return _parse_scope_json(raw_response)


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


def _parse_scope_json(raw: str) -> ScopeResult:
    """Deserialize Hermes JSON response into a ScopeResult.

    If JSON is invalid or fields are missing, missing fields default
    to 'Not Specified'. No inference is performed.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return ScopeResult()

    # Extract only known fields, ignore any extras Hermes might return
    return ScopeResult(
        scope_statement=_normalize_missing(data.get("scope_statement", "Not Specified")),
        in_scope_items=_normalize_missing(data.get("in_scope_items", "Not Specified")),
        out_of_scope_items=_normalize_missing(data.get("out_of_scope_items", "Not Specified")),
        scope_boundary=_normalize_missing(data.get("scope_boundary", "Not Specified")),
    )