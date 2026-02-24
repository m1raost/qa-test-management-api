from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.core.exceptions import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import RequestLoggingMiddleware, configure_logging
from app.routers import auth, test_cases, test_results, test_runs, test_suites

# Configure logging before anything else so all startup messages are captured
configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Schema is managed by Alembic migrations (`alembic upgrade head`).
    # Run that command before starting the server for the first time or after
    # pulling new model changes. Nothing to do here at runtime.
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="Manage test suites, test cases, runs, and results.",
    lifespan=lifespan,
)

# ── Middleware ─────────────────────────────────────────────────────────────────
# Order matters — middleware is applied bottom-up (last added = outermost).
app.add_middleware(RequestLoggingMiddleware)   # logs every request + duration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Lock down to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Exception handlers ─────────────────────────────────────────────────────────
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# ── Routers ───────────────────────────────────────────────────────────────────
_PREFIX = settings.API_V1_STR

app.include_router(auth.router,         prefix=_PREFIX)
app.include_router(test_suites.router,  prefix=_PREFIX)
app.include_router(test_cases.router,   prefix=_PREFIX)
app.include_router(test_runs.router,    prefix=_PREFIX)
app.include_router(test_results.router, prefix=_PREFIX)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def root():
    return {"message": settings.PROJECT_NAME, "docs": "/docs"}
