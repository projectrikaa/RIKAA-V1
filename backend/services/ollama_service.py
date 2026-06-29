from ollama import chat as ollama_chat


def send_messages_to_ollama(messages: list) -> str:
    """Send a list of messages to Ollama and return the assistant reply."""
    response = ollama_chat(
        model="hermes3:8b",
        messages=messages
    )
    return response["message"]["content"]