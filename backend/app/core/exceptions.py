from fastapi import Request
from fastapi.responses import JSONResponse


class ServiceUnavailableError(Exception):
    """Raised when an external service (e.g. Groq) cannot be reached."""


class InsightExtractionError(Exception):
    """Raised when insight parsing fails and no fallback is acceptable."""


# ── FastAPI exception handlers ──────────────────────────────────────────────

async def service_unavailable_handler(
    request: Request, exc: ServiceUnavailableError
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again."},
    )
