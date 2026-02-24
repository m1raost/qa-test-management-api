import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


def configure_logging(level: str = "INFO") -> None:
    """
    Set up root logger with a consistent format.
    Call once at app startup — after this every `logging.getLogger(__name__)`
    across the codebase inherits the same handler and format.
    """
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Quieten noisy third-party loggers
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs one line per request showing method, path, status code, and duration.

    Example output:
        2026-02-24 21:00:00 | INFO     | app.core.logging | POST /api/v1/auth/login → 200 (34ms)
        2026-02-24 21:00:01 | INFO     | app.core.logging | GET  /api/v1/test-suites/ → 200 (8ms)
        2026-02-24 21:00:02 | WARNING  | app.core.logging | GET  /api/v1/test-suites/999 → 404 (3ms)
    """

    _logger = logging.getLogger(__name__)

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = int((time.perf_counter() - start) * 1000)

        log = self._logger.info if response.status_code < 400 else self._logger.warning
        log(
            "%-5s %s → %d (%dms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
