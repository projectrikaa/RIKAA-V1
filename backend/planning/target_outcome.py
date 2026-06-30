"""Blueprint Module 3.3 — Target Outcome Module.

Uses Hermes for semantic understanding of the desired future state.
Owns the Blueprint boundary: JSON deserialization, validation, and structured output.
"""

import json

from models.chat import PlanningContext, TargetOutcomeResult
from prompts.target_outcome_prompt import get_target_outcome_system_prompt
from services.ollama_service import send_messages_to_ollama

_EXPECTED_KEYS = {
    "target_outcome_statement",
    "desired_future_state",
    "expected_business_outcome",
    "expected_user_outcome",
    "outcome_boundaries",
}


def identify_target_outcome(context: PlanningContext) -> TargetOutcomeResult:
    """Identify the target outcome by instructing Hermes.

    Consumes PlanningContext.purpose and PlanningContext.problem
    to construct the analysis.
    Hermes owns semantic reasoning and returns JSON.
    This module owns deserialization, validation, and Blueprint boundaries.
    """
    p = context.purpose
    pr = context.problem
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
        "Based on the purpose and problem above, define the desired target outcome."
    )
    messages = [
        {"role": "system", "content": get_target_outcome_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    raw_response = send_messages_to_ollama(messages)

    return _parse_target_outcome_json(raw_response)


def _parse_target_outcome_json(raw: str) -> TargetOutcomeResult:
    """Deserialize Hermes JSON response into a TargetOutcomeResult.

    If JSON is invalid or fields are missing, missing fields default
    to 'Not Specified'. No inference is performed.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return TargetOutcomeResult()

    # Extract only known fields, ignore any extras Hermes might return
    return TargetOutcomeResult(
        target_outcome_statement=str(data.get("target_outcome_statement", "Not Specified")),
        desired_future_state=str(data.get("desired_future_state", "Not Specified")),
        expected_business_outcome=str(data.get("expected_business_outcome", "Not Specified")),
        expected_user_outcome=str(data.get("expected_user_outcome", "Not Specified")),
        outcome_boundaries=str(data.get("outcome_boundaries", "Not Specified")),
    )