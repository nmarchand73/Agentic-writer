"""Console logging (loguru) for CLI and pipeline."""

from __future__ import annotations

import logging
import os
import sys

from loguru import logger

_CONFIGURED = False

_FORMAT = (
    "<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{extra[name]}</cyan> - "
    "<level>{message}</level>"
)


def _patch_record_name(record: dict) -> None:
    """stdlib / uvicorn logs have no bind(name=…) — use logger name as fallback."""
    record["extra"].setdefault("name", record["name"])


def setup_logging(
    *,
    verbose: bool = False,
    quiet: bool = False,
    level: str | None = None,
) -> None:
    """Configure loguru on stderr (idempotent)."""
    global _CONFIGURED

    if quiet:
        resolved = "WARNING"
    elif verbose:
        resolved = "DEBUG"
    else:
        resolved = (level or os.environ.get("LOG_LEVEL", "INFO")).upper()

    logger.configure(patcher=_patch_record_name)
    logger.remove()
    logger.add(
        sys.stderr,
        level=resolved,
        format=_FORMAT,
        colorize=sys.stderr.isatty(),
        enqueue=False,
    )
    _intercept_stdlib_logging()
    _CONFIGURED = True
    logger.bind(name="agentic_writer").debug("Logging level={}", resolved)


def _intercept_stdlib_logging() -> None:
    """Route uvicorn / third-party stdlib logs through loguru."""

    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            try:
                lvl = logger.level(record.levelname).name
            except ValueError:
                lvl = record.levelno
            # record.name e.g. "uvicorn.server" — évite KeyError sur extra[name]
            logger.bind(name=record.name).opt(
                depth=6, exception=record.exc_info
            ).log(lvl, record.getMessage())

    handler = InterceptHandler()
    logging.basicConfig(handlers=[handler], level=0, force=True)
    for lib in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        lib_logger = logging.getLogger(lib)
        lib_logger.handlers = [handler]
        lib_logger.propagate = False


def get_logger(name: str):
    """Module-scoped logger (shows in extra[name])."""
    return logger.bind(name=name)


__all__ = ["get_logger", "logger", "setup_logging"]
