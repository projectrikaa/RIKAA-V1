"""Blueprint Module 3.1 — Purpose Module.

Uses Hermes for semantic understanding of the user's purpose.
Owns the Blueprint boundary: JSON deserialization, validation, and structured output.
"""

import json

from models.chat import PurposeResult
from prompts.purpose_prompt import get_purpose_system_prompt
from services.ollama_service import send_messages_to_ollama

_EXPECTED_KEYS = {"primary_purpose", "secondary_purpose", "expected_value"}


def identify_purpose(user_request: str) -> PurposeResult:
    """Identify the user's purpose by instructing Hermes.

    Hermes owns semantic understanding and returns JSON.
    This module owns deserialization, validation, and Blueprint boundaries.
    """
    messages = [
        {"role": "system", "content": get_purpose_system_prompt()},
        {"role": "user", "content": user_request},
    ]

    raw_response = send_messages_to_ollama(messages)

    return _parse_purpose_json(raw_response)


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


def _parse_purpose_json(raw: str) -> PurposeResult:
    """Deserialize Hermes JSON response into a PurposeResult.

    If JSON is invalid or fields are missing, missing fields default
    to 'Not Specified'. No inference is performed.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return PurposeResult()

    # Extract only known fields, ignore any extras Hermes might return
    return PurposeResult(
        primary_purpose=_normalize_missing(data.get("primary_purpose", "Not Specified")),
        secondary_purpose=_normalize_missing(data.get("secondary_purpose", "Not Specified")),
        expected_value=_normalize_missing(data.get("expected_value", "Not Specified")),
    )
