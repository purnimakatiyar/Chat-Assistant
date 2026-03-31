"""
Logging configuration for the Chat Assistant API.

Sets up:
  - Console handler  — coloured, human-readable
  - Rotating file handler — JSON-structured lines for log aggregators
  - Per-module log levels so third-party noise is suppressed
"""

import logging
import logging.handlers
from pathlib import Path

from app.core.config import settings
from app.core.constants import (
    LOG_COLOUR_RESET,
    LOG_CONSOLE_FORMAT,
    LOG_DATE_FORMAT,
    LOG_FILE_FORMAT,
    LOG_LEVEL_COLOURS,
    LOG_NOISY_LOGGERS,
)


class _ColourFormatter(logging.Formatter):
    """Adds ANSI colour codes to levelname in console output."""

    def format(self, record: logging.LogRecord) -> str:
        colour = LOG_LEVEL_COLOURS.get(record.levelno, LOG_COLOUR_RESET)
        record.levelname = f"{colour}{record.levelname:<8}{LOG_COLOUR_RESET}"
        return super().format(record)


def setup_logging() -> None:
    """Call once at application startup."""
    level = logging.getLevelName(settings.log_level.upper())

    handlers: list[logging.Handler] = [_build_console_handler(level)]
    if settings.log_to_file:
        handlers.append(_build_file_handler(level))

    logging.basicConfig(level=level, handlers=handlers, force=True)

    for noisy in LOG_NOISY_LOGGERS:
        logging.getLogger(noisy).setLevel(logging.WARNING)

    logging.getLogger(__name__).info(
        "Logging initialised (level=%s, file=%s)",
        settings.log_level.upper(),
        settings.log_file_path if settings.log_to_file else "disabled",
    )


def _build_console_handler(level: int) -> logging.StreamHandler:
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(_ColourFormatter(fmt=LOG_CONSOLE_FORMAT, datefmt=LOG_DATE_FORMAT))
    return handler


def _build_file_handler(level: int) -> logging.handlers.RotatingFileHandler:
    log_path = Path(settings.log_file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    handler = logging.handlers.RotatingFileHandler(
        filename=log_path,
        maxBytes=settings.log_max_bytes,
        backupCount=settings.log_backup_count,
        encoding="utf-8",
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt=LOG_FILE_FORMAT, datefmt=LOG_DATE_FORMAT))
    return handler
