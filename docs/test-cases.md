# Test Cases — QA Test Management API

These are formal test cases for the API endpoints. Each test case follows the standard format used in QA test management tools.

---

## Auth

### TC-001 — Register a new user successfully
| Field | Value |
|---|---|
| **Preconditions** | The email `newuser@example.com` is not already registered |
| **Steps** | POST `/api/v1/auth/register` with `{"email": "newuser@example.com", "password": "securepass123"}` |
| **Expected Result** | Response status 201; body contains `id` and `email`; `hashed_password` is NOT in the response |
| **Priority** | High |

---

### TC-002 — Register with an already-used email
| Field | Value |
|---|---|
| **Preconditions** | `tester@example.com` is already registered |
| **Steps** | POST `/api/v1/auth/register` with `{"email": "tester@example.com", "password": "anypassword"}` |
| **Expected Result** | Response status 400; body contains `"Email already registered"` |
| **Priority** | High |

---

### TC-003 — Login with valid credentials
| Field | Value |
|---|---|
| **Preconditions** | User `tester@example.com` is registered |
| **Steps** | POST `/api/v1/auth/login` with form data `username=tester@example.com&password=testpassword123` |
| **Expected Result** | Response status 200; body contains `access_token` and `token_type: "bearer"` |
| **Priority** | High |

---

### TC-004 — Login with wrong password
| Field | Value |
|---|---|
| **Preconditions** | User `tester@example.com` is registered |
| **Steps** | POST `/api/v1/auth/login` with `password=wrongpassword` |
| **Expected Result** | Response status 401; body contains `"Incorrect email or password"` |
| **Priority** | High |

---

### TC-005 — Access protected route without token
| Field | Value |
|---|---|
| **Preconditions** | None |
| **Steps** | GET `/api/v1/auth/me` with no Authorization header |
| **Expected Result** | Response status 401 |
| **Priority** | High |

---

## Test Suites

### TC-006 — Create a test suite
| Field | Value |
|---|---|
| **Preconditions** | User is logged in and has a valid Bearer token |
| **Steps** | POST `/api/v1/test-suites/` with `{"name": "Login Tests"}` and `Authorization: Bearer <token>` header |
| **Expected Result** | Response status 201; body contains `id`, `name: "Login Tests"`, `owner_id` matching the logged-in user |
| **Priority** | High |

---

### TC-007 — Create a test suite without authentication
| Field | Value |
|---|---|
| **Preconditions** | None |
| **Steps** | POST `/api/v1/test-suites/` with `{"name": "Unauthorized Suite"}` — no Authorization header |
| **Expected Result** | Response status 401 |
| **Priority** | High |

---

### TC-008 — Get a test suite that does not exist
| Field | Value |
|---|---|
| **Preconditions** | User is logged in |
| **Steps** | GET `/api/v1/test-suites/99999` with valid token |
| **Expected Result** | Response status 404; body contains `"Test suite not found"` |
| **Priority** | Medium |

---

## Test Cases

### TC-009 — Create a test case with all required fields
| Field | Value |
|---|---|
| **Preconditions** | User is logged in; a test suite with `id=1` exists and belongs to this user |
| **Steps** | POST `/api/v1/test-cases/` with `{"title": "Verify login", "suite_id": 1}` |
| **Expected Result** | Response status 201; `priority` defaults to `"medium"`, `severity` to `"major"`, `status` to `"draft"` |
| **Priority** | High |

---

### TC-010 — Create a test case with an invalid priority value
| Field | Value |
|---|---|
| **Preconditions** | User is logged in; suite exists |
| **Steps** | POST `/api/v1/test-cases/` with `{"title": "Bad case", "suite_id": 1, "priority": "urgent"}` |
| **Expected Result** | Response status 422; body explains `priority` must be one of: `low`, `medium`, `high`, `critical` |
| **Priority** | Medium |

---

### TC-011 — Partially update a test case (PATCH)
| Field | Value |
|---|---|
| **Preconditions** | A test case with `id=1` exists |
| **Steps** | PATCH `/api/v1/test-cases/1` with `{"status": "active"}` |
| **Expected Result** | Response status 200; `status` is `"active"`; all other fields are unchanged |
| **Priority** | Medium |

---

### TC-012 — Delete a test case and verify it is gone
| Field | Value |
|---|---|
| **Preconditions** | A test case with `id=5` exists |
| **Steps** | 1. DELETE `/api/v1/test-cases/5` — expect 204. 2. GET `/api/v1/test-cases/5` — expect 404 |
| **Expected Result** | First call returns 204 (no body); second call returns 404 |
| **Priority** | Medium |

---

## Test Results

### TC-013 — Record a passed test result
| Field | Value |
|---|---|
| **Preconditions** | A test run with `id=1` and a test case with `id=1` both exist |
| **Steps** | POST `/api/v1/test-results/` with `{"run_id": 1, "test_case_id": 1, "status": "passed"}` |
| **Expected Result** | Response status 201; body contains `status: "passed"` and correct `run_id` / `test_case_id` |
| **Priority** | High |

---

### TC-014 — Record a result with an invalid status
| Field | Value |
|---|---|
| **Preconditions** | Run and test case exist |
| **Steps** | POST `/api/v1/test-results/` with `{"run_id": 1, "test_case_id": 1, "status": "pending"}` |
| **Expected Result** | Response status 422; `status` must be one of: `passed`, `failed`, `skipped`, `blocked`, `error` |
| **Priority** | Medium |

---

### TC-015 — List results filtered by run
| Field | Value |
|---|---|
| **Preconditions** | Test run with `id=1` has 3 results recorded |
| **Steps** | GET `/api/v1/test-results/?run_id=1` with valid token |
| **Expected Result** | Response status 200; array of 3 result objects, all with `run_id: 1` |
| **Priority** | Medium |
