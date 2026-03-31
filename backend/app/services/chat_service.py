from app.core.config import settings
from app.core.constants import CHAT_SYSTEM_PROMPT
from app.schemas.chat import Message
from app.services.groq_client import get_groq_client


def build_messages(user_message: str, history: list[Message]) -> list[dict]:
    messages: list[dict] = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": user_message})
    return messages


def generate_response(user_message: str, history: list[Message]) -> str:
    client = get_groq_client()
    messages = build_messages(user_message, history)

    completion = client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        max_tokens=settings.groq_chat_max_tokens,
        temperature=settings.groq_chat_temperature,
    )
    return completion.choices[0].message.content
