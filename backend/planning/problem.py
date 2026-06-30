"""Blueprint Module 3.2 — Problem Definition Module.

Uses Hermes for semantic understanding of the problem.
Owns the Blueprint boundary: JSON deserialization, validation, and structured output.
"""

import json

from models.chat import PlanningContext, ProblemResult
from prompts.problem_prompt import get_problem_system_prompt
from services.ollama_service import send_messages_to_ollama

_EXPECTED_KEYS = {"problem_statement", "root_cause", "impact", "stakeholders_affected"}


def define_problem(context: PlanningContext) -> ProblemResult:
    """Define the problem by instructing Hermes.

    Consumes PlanningContext.purpose to construct the analysis.
    Hermes owns semantic reasoning and returns JSON.
    This module owns deserialization, validation, and Blueprint boundaries.
    """
    p = context.purpose
    user_message = (
        f"Primary Purpose: {p.primary_purpose}\n"
        f"Secondary Purpose: {p.secondary_purpose}\n"
        f"Expected Value: {p.expected_value}\n"
        "\n"
        "Based on the purpose above, define the problem that prevents this purpose from being achieved."
    )
    messages = [
        {"role": "system", "content": get_problem_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    raw_response = send_messages_to_ollama(messages)

    return _parse_problem_json(raw_response)


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


def _parse_problem_json(raw: str) -> ProblemResult:
    """Deserialize Hermes JSON response into a ProblemResult.

    If JSON is invalid or fields are missing, missing fields default
    to 'Not Specified'. No inference is performed.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return ProblemResult()

    # Extract only known fields, ignore any extras Hermes might return
    return ProblemResult(
        problem_statement=_normalize_missing(data.get("problem_statement", "Not Specified")),
        root_cause=_normalize_missing(data.get("root_cause", "Not Specified")),
        impact=_normalize_missing(data.get("impact", "Not Specified")),
        stakeholders_affected=_normalize_missing(data.get("stakeholders_affected", "Not Specified")),
    )