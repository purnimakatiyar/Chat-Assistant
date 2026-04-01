import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.core.config import settings
from app.core.exceptions import (
    ServiceUnavailableError,
    service_unavailable_handler,
    unhandled_exception_handler,
)
from app.core.logging import setup_logging
from app.middleware.logging import RequestLoggingMiddleware

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title=settings.app_title,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    app.add_exception_handler(ServiceUnavailableError, service_unavailable_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Routers
    app.include_router(health_router)
    app.include_router(chat_router)

    logger.info("Application '%s' v%s ready.", settings.app_title, settings.app_version)
    return app
