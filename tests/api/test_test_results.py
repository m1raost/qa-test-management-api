"""Tests for /api/v1/test-results endpoints."""
import pytest


@pytest.fixture(scope="module")
def run_and_case(client, auth_headers):
    """Create a suite, one test case, and one test run — all needed to record a result."""
    suite = client.post("/api/v1/test-suites/", json={"name": "Results Suite"}, headers=auth_headers).json()
    case = client.post("/api/v1/test-cases/", json={
        "title": "Check dashboard loads",
        "suite_id": suite["id"],
    }, headers=auth_headers).json()
    run = client.post("/api/v1/test-runs/", json={
        "name": "Results Run",
        "suite_id": suite["id"],
    }, headers=auth_headers).json()
    return {"run_id": run["id"], "case_id": case["id"]}


@pytest.fixture(scope="module")
def result(client, auth_headers, run_and_case):
    """Create one result reused across this module's tests."""
    resp = client.post("/api/v1/test-results/", json={
        "run_id": run_and_case["run_id"],
        "test_case_id": run_and_case["case_id"],
        "status": "passed",
        "duration_ms": 342,
    }, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()


# ── CREATE ─────────────────────────────────────────────────────────────────────

def test_create_result_passed(client, auth_headers, run_and_case):
    resp = client.post("/api/v1/test-results/", json={
        "run_id": run_and_case["run_id"],
        "test_case_id": run_and_case["case_id"],
        "status": "passed",
        "duration_ms": 150,
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "passed"
    assert data["duration_ms"] == 150
    assert data["notes"] is None


def test_create_result_failed_with_notes(client, auth_headers, run_and_case):
    resp = client.post("/api/v1/test-results/", json={
        "run_id": run_and_case["run_id"],
        "test_case_id": run_and_case["case_id"],
        "status": "failed",
        "notes": "Button unresponsive on mobile viewport",
        "duration_ms": 5200,
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "failed"
    assert "mobile viewport" in data["notes"]


def test_create_result_invalid_status(client, auth_headers, run_and_case):
    resp = client.post("/api/v1/test-results/", json={
        "run_id": run_and_case["run_id"],
        "test_case_id": run_and_case["case_id"],
        "status": "unknown",                # not a valid ResultStatus
    }, headers=auth_headers)
    assert resp.status_code == 422


def test_create_result_requires_auth(client, run_and_case):
    resp = client.post("/api/v1/test-results/", json={
        "run_id": run_and_case["run_id"],
        "test_case_id": run_and_case["case_id"],
        "status": "skipped",
    })
    assert resp.status_code == 401


# ── LIST ───────────────────────────────────────────────────────────────────────

def test_list_results_by_run(client, auth_headers, run_and_case, result):
    resp = client.get("/api/v1/test-results/",
                      params={"run_id": run_and_case["run_id"]},
                      headers=auth_headers)
    assert resp.status_code == 200
    ids = [r["id"] for r in resp.json()]
    assert result["id"] in ids


# ── GET ────────────────────────────────────────────────────────────────────────

def test_get_result(client, auth_headers, result):
    resp = client.get(f"/api/v1/test-results/{result['id']}", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == result["id"]
    assert data["status"] == result["status"]


def test_get_result_not_found(client, auth_headers):
    resp = client.get("/api/v1/test-results/99999", headers=auth_headers)
    assert resp.status_code == 404


# ── UPDATE ─────────────────────────────────────────────────────────────────────

def test_update_result(client, auth_headers, result):
    resp = client.patch(f"/api/v1/test-results/{result['id']}", json={
        "status": "failed",
        "notes": "Flaky — failed on retry",
    }, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "failed"
    assert data["notes"] == "Flaky — failed on retry"
    assert data["duration_ms"] == result["duration_ms"]   # unchanged


def test_update_result_not_found(client, auth_headers):
    resp = client.patch("/api/v1/test-results/99999", json={"status": "skipped"}, headers=auth_headers)
    assert resp.status_code == 404


# ── DELETE ─────────────────────────────────────────────────────────────────────

def test_delete_result(client, auth_headers, run_and_case):
    create = client.post("/api/v1/test-results/", json={
        "run_id": run_and_case["run_id"],
        "test_case_id": run_and_case["case_id"],
        "status": "skipped",
    }, headers=auth_headers)
    result_id = create.json()["id"]

    resp = client.delete(f"/api/v1/test-results/{result_id}", headers=auth_headers)
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/test-results/{result_id}", headers=auth_headers)
    assert resp.status_code == 404


def test_delete_result_not_found(client, auth_headers):
    resp = client.delete("/api/v1/test-results/99999", headers=auth_headers)
    assert resp.status_code == 404
