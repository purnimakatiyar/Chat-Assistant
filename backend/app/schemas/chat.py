from typing import Literal

from pydantic import BaseModel, field_validator


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[Message] = []

    @field_validator("message")
    @classmethod
    def message_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Message must not be empty.")
        return value.strip()


class Insights(BaseModel):
    intent: Literal[
        "greeting", "farewell", "query", "request", "complaint", "praise",
        "feedback", "clarification", "confirmation", "denial",
        "troubleshooting", "small_talk", "opinion", "urgent", "other",
    ]
    sentiment: Literal[
        "very_positive", "positive", "slightly_positive",
        "neutral",
        "slightly_negative", "negative", "very_negative",
    ]


class ChatResponse(BaseModel):
    response: str
    insights: Insights
