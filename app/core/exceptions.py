import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def _error_body(status_code: int, message: str, details=None) -> dict:
    body = {"error": {"status": status_code, "message": message}}
    if details:
        body["error"]["details"] = details
    return body


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    logger.warning("HTTP %s — %s %s", exc.status_code, request.method, request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(exc.status_code, str(exc.detail)),
        headers=getattr(exc, "headers", None),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    field_errors = [
        {"field": " → ".join(str(loc) for loc in err["loc"]), "message": err["msg"]}
        for err in exc.errors()
    ]
    logger.info("Validation error — %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=422,
        content=_error_body(422, "Request validation failed", field_errors),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception — %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=_error_body(500, "An internal server error occurred"),
    )
