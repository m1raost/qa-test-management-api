import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def _error_body(status_code: int, message: str, details=None) -> dict:
    """Single consistent error envelope returned by every error response."""
    body = {"error": {"status": status_code, "message": message}}
    if details:
        body["error"]["details"] = details
    return body


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handles all HTTPException instances (404, 401, 403, etc.).
    Replaces FastAPI's default plain-string detail with the standard envelope.
    """
    logger.warning("HTTP %s — %s %s", exc.status_code, request.method, request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(exc.status_code, str(exc.detail)),
        headers=getattr(exc, "headers", None),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handles Pydantic validation errors (422 Unprocessable Entity).
    Extracts the field-level errors into a readable list.
    """
    field_errors = [
        {"field": " → ".join(str(loc) for loc in err["loc"]), "message": err["msg"]}
        for err in exc.errors()
    ]
    logger.info("Validation error — %s %s — %d field(s)", request.method, request.url.path, len(field_errors))
    return JSONResponse(
        status_code=422,
        content=_error_body(422, "Request validation failed", field_errors),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all for any exception that wasn't handled elsewhere.
    Logs the full traceback but returns a safe generic message to the client —
    never leak internal details in a 500 response.
    """
    logger.exception("Unhandled exception — %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_error_body(500, "An internal server error occurred"),
    )
