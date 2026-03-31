import json
import logging

from app.core.config import settings
from app.core.constants import (
    INSIGHT_FALLBACK_INTENT,
    INSIGHT_FALLBACK_SENTIMENT,
    INSIGHT_PROMPT_TEMPLATE,
    VALID_INTENTS,
    VALID_SENTIMENTS,
)
from app.schemas.chat import Insights
from app.services.groq_client import get_groq_client

logger = logging.getLogger(__name__)

_FALLBACK_INSIGHTS = Insights(
    intent=INSIGHT_FALLBACK_INTENT,
    sentiment=INSIGHT_FALLBACK_SENTIMENT,
)


def _parse_raw(raw: str) -> dict:
    """Strip markdown fences then parse JSON."""
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.startswith("json"):
            text = text[4:].strip()
    return json.loads(text)


def extract_insights(user_message: str) -> Insights:
    client = get_groq_client()
    prompt = INSIGHT_PROMPT_TEMPLATE.format(message=user_message)

    try:
        completion = client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.groq_insight_max_tokens,
            temperature=settings.groq_insight_temperature,
        )
        raw = completion.choices[0].message.content
        data = _parse_raw(raw)

        intent = data.get("intent", "").lower().strip()
        sentiment = data.get("sentiment", "").lower().strip()

        # Guard against values outside the defined vocabulary
        if intent not in VALID_INTENTS:
            logger.warning("Unexpected intent %r from model — falling back.", intent)
            intent = INSIGHT_FALLBACK_INTENT
        if sentiment not in VALID_SENTIMENTS:
            logger.warning("Unexpected sentiment %r from model — falling back.", sentiment)
            sentiment = INSIGHT_FALLBACK_SENTIMENT

        return Insights(intent=intent, sentiment=sentiment)
    except (json.JSONDecodeError, KeyError, ValueError) as exc:
        logger.warning("Insight parsing failed, using fallback. Reason: %s", exc)
        return _FALLBACK_INSIGHTS
    except Exception as exc:
        logger.error("Unexpected error during insight extraction: %s", exc)
        return _FALLBACK_INSIGHTS
