"""Tests for /api/v1/test-cases endpoints."""
import pytest


@pytest.fixture(scope="module")
def suite_id(client, auth_headers):
    """Create a suite to own all test cases in this module."""
    resp = client.post("/api/v1/test-suites/", json={"name": "Cases Suite"}, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()["id"]


@pytest.fixture(scope="module")
def case(client, auth_headers, suite_id):
    """Create one test case reused across this module's tests."""
    resp = client.post("/api/v1/test-cases/", json={
        "title": "Verify login with valid credentials",
        "description": "Checks the happy-path login flow",
        "steps": "1. Open /login\n2. Enter valid email and password\n3. Click Submit",
        "expected_result": "Redirected to dashboard",
        "priority": "high",
        "severity": "critical",
        "status": "active",
        "suite_id": suite_id,
    }, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()


# ── CREATE ─────────────────────────────────────────────────────────────────────

def test_create_case_minimal(client, auth_headers, suite_id):
    """Only required fields — defaults should fill the rest."""
    resp = client.post("/api/v1/test-cases/", json={
        "title": "Minimal case",
        "suite_id": suite_id,
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Minimal case"
    assert data["priority"] == "medium"     # default
    assert data["severity"] == "major"      # default
    assert data["status"] == "draft"        # default
    assert data["description"] is None


def test_create_case_invalid_priority(client, auth_headers, suite_id):
    resp = client.post("/api/v1/test-cases/", json={
        "title": "Bad priority",
        "suite_id": suite_id,
        "priority": "urgent",               # not a valid enum value
    }, headers=auth_headers)
    assert resp.status_code == 422


def test_create_case_invalid_severity(client, auth_headers, suite_id):
    resp = client.post("/api/v1/test-cases/", json={
        "title": "Bad severity",
        "suite_id": suite_id,
        "severity": "catastrophic",         # not a valid enum value
    }, headers=auth_headers)
    assert resp.status_code == 422


def test_create_case_requires_auth(client, suite_id):
    resp = client.post("/api/v1/test-cases/", json={"title": "No auth", "suite_id": suite_id})
    assert resp.status_code == 401


# ── LIST ───────────────────────────────────────────────────────────────────────

def test_list_cases(client, auth_headers, suite_id, case):
    resp = client.get("/api/v1/test-cases/", params={"suite_id": suite_id}, headers=auth_headers)
    assert resp.status_code == 200
    ids = [c["id"] for c in resp.json()]
    assert case["id"] in ids


def test_list_cases_unknown_suite(client, auth_headers):
    resp = client.get("/api/v1/test-cases/", params={"suite_id": 99999}, headers=auth_headers)
    assert resp.status_code == 404


# ── GET ────────────────────────────────────────────────────────────────────────

def test_get_case(client, auth_headers, case):
    resp = client.get(f"/api/v1/test-cases/{case['id']}", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == case["id"]
    assert data["title"] == case["title"]
    assert data["severity"] == "critical"


def test_get_case_not_found(client, auth_headers):
    resp = client.get("/api/v1/test-cases/99999", headers=auth_headers)
    assert resp.status_code == 404


# ── UPDATE ─────────────────────────────────────────────────────────────────────

def test_update_case_partial(client, auth_headers, case):
    """PATCH only changes the provided fields; others stay untouched."""
    resp = client.patch(f"/api/v1/test-cases/{case['id']}", json={
        "status": "active",
        "priority": "critical",
    }, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "active"
    assert data["priority"] == "critical"
    assert data["title"] == case["title"]   # untouched


def test_update_case_not_found(client, auth_headers):
    resp = client.patch("/api/v1/test-cases/99999", json={"title": "x"}, headers=auth_headers)
    assert resp.status_code == 404


# ── DELETE ─────────────────────────────────────────────────────────────────────

def test_delete_case(client, auth_headers, suite_id):
    create = client.post("/api/v1/test-cases/", json={
        "title": "To Delete", "suite_id": suite_id,
    }, headers=auth_headers)
    case_id = create.json()["id"]

    resp = client.delete(f"/api/v1/test-cases/{case_id}", headers=auth_headers)
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/test-cases/{case_id}", headers=auth_headers)
    assert resp.status_code == 404


def test_delete_case_not_found(client, auth_headers):
    resp = client.delete("/api/v1/test-cases/99999", headers=auth_headers)
    assert resp.status_code == 404
