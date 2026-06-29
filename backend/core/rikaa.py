from prompts.identity import get_identity
from rules.rules import get_rules
from decision.decision import make_decision


def _build_system_content() -> str:
    """Combine identity and rules into the system message content."""
    identity = get_identity()
    rules = "\n".join(f"- {rule}" for rule in get_rules())
    return f"{identity}\n\nRules:\n{rules}"


def process_user_request(message: str) -> list:
    """Core RIKAA processing layer.

    Returns a messages list ready for Ollama:
    - System message (identity + rules)
    - User message (trimmed, validated, decided)

    This layer is the single entry point for all user input,
    allowing future AI orchestration logic to be added here without
    modifying routes or services.
    """
    cleaned = message.strip()

    if not cleaned:
        raise ValueError("Message cannot be empty")

    # Pass through decision layer
    decided = make_decision(cleaned)

    return [
        {
            "role": "system",
            "content": _build_system_content()
        },
        {
            "role": "user",
            "content": decided
        }
    ]