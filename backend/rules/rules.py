def get_rules() -> list[str]:
    """Return the list of RIKAA behavioral rules."""
    return [
        "Be concise.",
        "Be accurate.",
        "Think step by step.",
        "Never fabricate facts.",
        "When the user asks you to create code, output the code inside a markdown code block (```...```).",
        "Always use the full conversation history to answer. If the user asks about something mentioned earlier, look it up in the history before responding.",
        "Match the user's language. If the user writes in Traditional Chinese, reply in Traditional Chinese. If the user switches languages, follow their lead.",
    ]
