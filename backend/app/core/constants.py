"""
Application-wide constants.

All magic strings, prompt templates, format strings, and fixed values live
here so they have a single source of truth and are easy to find and update.
"""

# ── AI / Groq ─────────────────────────────────────────────────────────────────

CHAT_SYSTEM_PROMPT = (
    "You are a helpful, friendly AI assistant. "
    "Respond naturally and conversationally. "
    "Keep replies clear and concise."
)

INSIGHT_PROMPT_TEMPLATE = """\
Analyze the user message below and extract two fields.

1. intent — choose the single best match from this list:
   - greeting       : opening hello, hi, hey
   - farewell       : goodbye, see you, bye
   - query          : asking for information or an explanation
   - request        : asking the assistant to do or produce something
   - complaint      : expressing dissatisfaction with a product, service, or experience
   - praise         : complimenting or expressing appreciation
   - feedback       : giving an opinion or suggestion about something
   - clarification  : asking for more detail or to rephrase something already said
   - confirmation   : verifying or agreeing with something
   - denial         : disagreeing, refusing, or correcting something
   - troubleshooting: reporting a technical problem and seeking a fix
   - small_talk     : casual conversation with no specific goal
   - opinion        : sharing a personal view or preference
   - urgent         : conveying urgency, emergency, or time-sensitive need
   - other          : anything that does not fit the above

2. sentiment — choose the single best match from this list:
   - very_positive  : enthusiastic, excited, delighted
   - positive       : happy, satisfied, pleased
   - slightly_positive : mildly happy or content
   - neutral        : no emotional tone, purely informational
   - slightly_negative : mildly unhappy or disappointed
   - negative       : frustrated, unhappy, upset
   - very_negative  : angry, furious, extremely distressed

User message: "{message}"

Respond ONLY with valid JSON, nothing else:
{{"intent": "...", "sentiment": "..."}}"""

INSIGHT_FALLBACK_INTENT = "query"
INSIGHT_FALLBACK_SENTIMENT = "neutral"

# Canonical value sets — kept in sync with schemas/chat.py Literals
VALID_INTENTS = frozenset({
    "greeting", "farewell", "query", "request", "complaint", "praise",
    "feedback", "clarification", "confirmation", "denial",
    "troubleshooting", "small_talk", "opinion", "urgent", "other",
})

VALID_SENTIMENTS = frozenset({
    "very_positive", "positive", "slightly_positive",
    "neutral",
    "slightly_negative", "negative", "very_negative",
})

GROQ_HEALTH_PROBE_MESSAGE = "ping"
GROQ_HEALTH_PROBE_MAX_TOKENS = 1

# ── Logging formats ───────────────────────────────────────────────────────────

LOG_CONSOLE_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_FILE_FORMAT = (
    '{"time": "%(asctime)s", "level": "%(levelname)s", '
    '"logger": "%(name)s", "message": %(message)r}'
)
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ANSI colour codes keyed by logging level integer
LOG_LEVEL_COLOURS: dict[int, str] = {
    10: "\033[36m",   # DEBUG   → cyan
    20: "\033[32m",   # INFO    → green
    30: "\033[33m",   # WARNING → yellow
    40: "\033[31m",   # ERROR   → red
    50: "\033[35m",   # CRITICAL→ magenta
}
LOG_COLOUR_RESET = "\033[0m"

# Third-party loggers
LOG_NOISY_LOGGERS = ("httpx", "httpcore", "groq", "uvicorn.access")
