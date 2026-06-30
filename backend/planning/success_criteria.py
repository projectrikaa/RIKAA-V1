"""Blueprint Module 3.4 — Success Criteria Module.

Uses Hermes for semantic understanding of success criteria.
Owns the Blueprint boundary: JSON deserialization, validation, and structured output.
"""

import json

from models.chat import PlanningContext, SuccessCriteriaResult
from prompts.success_criteria_prompt import get_success_criteria_system_prompt
from services.ollama_service import send_messages_to_ollama

_EXPECTED_KEYS = {"success_criteria", "acceptance_rules", "measurement_rules"}


def identify_success_criteria(context: PlanningContext) -> SuccessCriteriaResult:
    """Identify success criteria by instructing Hermes.

    Consumes PlanningContext.purpose, PlanningContext.problem, and
    PlanningContext.target_outcome to construct the analysis.
    Hermes owns semantic reasoning and returns JSON.
    This module owns deserialization, validation, and Blueprint boundaries.
    """
    p = context.purpose
    pr = context.problem
    t = context.target_outcome
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
        "Based on the purpose, problem, and target outcome above, "
        "define the success criteria."
    )
    messages = [
        {"role": "system", "content": get_success_criteria_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    raw_response = send_messages_to_ollama(messages)

    return _parse_success_criteria_json(raw_response)


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


def _parse_success_criteria_json(raw: str) -> SuccessCriteriaResult:
    """Deserialize Hermes JSON response into a SuccessCriteriaResult.

    If JSON is invalid or fields are missing, missing fields default
    to 'Not Specified'. No inference is performed.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return SuccessCriteriaResult()

    # Extract only known fields, ignore any extras Hermes might return
    return SuccessCriteriaResult(
        success_criteria=_normalize_missing(data.get("success_criteria", "Not Specified")),
        acceptance_rules=_normalize_missing(data.get("acceptance_rules", "Not Specified")),
        measurement_rules=_normalize_missing(data.get("measurement_rules", "Not Specified")),
    )