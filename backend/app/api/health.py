import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.constants import GROQ_HEALTH_PROBE_MAX_TOKENS, GROQ_HEALTH_PROBE_MESSAGE
from app.schemas.health import DependencyStatus, HealthResponse
from app.services.groq_client import get_groq_client

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Liveness + dependency check")
async def health_check() -> JSONResponse:
    """
    Returns overall service health.

    - **ok** — all dependencies reachable.
    - **degraded** — service is up but at least one dependency is unhealthy.
    """
    groq_status = await _check_groq()

    all_ok = groq_status.status == "ok"
    overall = "ok" if all_ok else "degraded"
    http_status = 200 if all_ok else 503

    body = HealthResponse(
        status=overall,
        version=settings.app_version,
        dependencies={"groq": groq_status},
    )

    logger.info("Health check — overall=%s groq=%s", overall, groq_status.status)
    return JSONResponse(content=body.model_dump(), status_code=http_status)


# ── Dependency probes ─────────────────────────────────────────────────────────

async def _check_groq() -> DependencyStatus:
    """Send a minimal request to Groq to confirm the API key and network are valid."""
    try:
        client = get_groq_client()
        client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": GROQ_HEALTH_PROBE_MESSAGE}],
            max_tokens=GROQ_HEALTH_PROBE_MAX_TOKENS,
        )
        return DependencyStatus(status="ok")
    except Exception as exc:
        logger.warning("Groq health probe failed: %s", exc)
        return DependencyStatus(status="error", detail=str(exc))
