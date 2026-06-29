from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


# Simple in-memory conversation history (single user, MVP)
conversation_history: list = []