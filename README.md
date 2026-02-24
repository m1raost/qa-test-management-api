# QA Test Management API

Production-ready REST API for managing QA test suites, test cases, runs, and results.
Built as a portfolio project to demonstrate clean FastAPI architecture with real-world patterns.

## Highlights

- **JWT authentication** — register, login, protected routes with Bearer tokens
- **Full CRUD** — test suites, cases, runs, and results with ownership checks
- **Layered architecture** — models → schemas → CRUD → routers, no business logic leaking between layers
- **Alembic migrations** — versioned schema changes, not `create_all()`
- **52 tests** — full API coverage with in-memory SQLite and session fixtures
- **Consistent error responses** — custom exception handlers, structured logging middleware

## Tech Stack

`FastAPI` `SQLAlchemy 2` `Alembic` `Pydantic v2` `JWT` `bcrypt` `pytest` `SQLite`

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env        # set SECRET_KEY
alembic upgrade head
uvicorn main:app --reload
```

Interactive docs → `http://localhost:8000/docs`

## API

```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
GET    /api/v1/auth/me

GET    POST   /api/v1/test-suites/
GET    PATCH  DELETE  /api/v1/test-suites/{id}

GET    POST   /api/v1/test-cases/
GET    PATCH  DELETE  /api/v1/test-cases/{id}

GET    POST   /api/v1/test-runs/
GET    PATCH  DELETE  /api/v1/test-runs/{id}

GET    POST   /api/v1/test-results/
GET    PATCH  DELETE  /api/v1/test-results/{id}
```
