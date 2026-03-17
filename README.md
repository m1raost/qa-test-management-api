# QA Test Management API

A REST API for managing QA test suites, test cases, runs, and results — similar to tools like TestRail or Qase.
Built as a portfolio project to demonstrate API testing skills and clean backend structure.

## What it does

Teams use this API to organize their testing work:

- **Test Suites** — groups of related test cases (e.g. "Login feature tests")
- **Test Cases** — individual scenarios with steps and expected results
- **Test Runs** — when you execute a suite (e.g. "Sprint 12 regression")
- **Test Results** — the outcome of each test case in a run (passed / failed / blocked)

## Highlights

- **JWT authentication** — register, login, protected routes with Bearer tokens
- **Full CRUD** — test suites, cases, runs, and results with ownership checks
- **52 automated tests** — full API coverage with pytest and in-memory SQLite
- **Postman collection** — ready-to-import collection with all 21 endpoints
- **Formal test cases** — documented in `docs/test-cases.md`
- **SQL verification queries** — in `sql/verify.sql`

## Tech Stack

`FastAPI` `SQLAlchemy` `Pydantic` `JWT` `bcrypt` `pytest` `SQLite`

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env        # set SECRET_KEY
uvicorn main:app --reload   # tables are created automatically on startup
```

Interactive docs → `http://localhost:8000/docs`

## API Endpoints

```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
GET    /api/v1/auth/me

GET    POST              /api/v1/test-suites/
GET    PATCH   DELETE    /api/v1/test-suites/{id}

GET    POST              /api/v1/test-cases/
GET    PATCH   DELETE    /api/v1/test-cases/{id}

GET    POST              /api/v1/test-runs/
GET    PATCH   DELETE    /api/v1/test-runs/{id}

GET    POST              /api/v1/test-results/
GET    PATCH   DELETE    /api/v1/test-results/{id}
```

## Testing

```bash
pytest              # run all 52 tests
pytest -v           # verbose output
```

## Postman

Import `postman/qa-api.postman_collection.json` into Postman.
See `postman/README.md` for setup instructions.

## SQL Verification

After running the API and creating some data:

```bash
sqlite3 qa.db < sql/verify.sql
```

See `sql/verify.sql` for queries that verify data integrity across tables.

## Project Structure

```
app/
  routers/      API endpoints (what the API does)
  crud/         Database operations (plain functions)
  models/       Database table definitions
  schemas/      Request/response data shapes
  core/         Auth, logging, error handling
tests/
  api/          52 API tests covering all endpoints
postman/        Postman collection + import guide
docs/           Formal test cases (15 test cases)
sql/            SQL verification queries
```
