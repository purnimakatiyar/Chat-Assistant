from groq import Groq

from app.core.config import settings

# Module-level singleton — created once on first import
_client: Groq | None = None


def get_groq_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=settings.groq_api_key)
    return _client
