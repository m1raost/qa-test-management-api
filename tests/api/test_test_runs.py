"""Tests for /api/v1/test-runs endpoints."""
import pytest


@pytest.fixture(scope="module")
def suite_id(client, auth_headers):
    resp = client.post("/api/v1/test-suites/", json={"name": "Runs Suite"}, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()["id"]


@pytest.fixture(scope="module")
def run(client, auth_headers, suite_id):
    """Create one run reused across this module's tests."""
    resp = client.post("/api/v1/test-runs/", json={
        "name": "Sprint 42 Regression",
        "suite_id": suite_id,
    }, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()


# ── CREATE ─────────────────────────────────────────────────────────────────────

def test_create_run_with_suite(client, auth_headers, suite_id):
    resp = client.post("/api/v1/test-runs/", json={
        "name": "Smoke Run",
        "suite_id": suite_id,
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Smoke Run"
    assert data["status"] == "pending"      # default
    assert data["suite_id"] == suite_id


def test_create_run_without_suite(client, auth_headers):
    """Ad-hoc run not linked to any suite."""
    resp = client.post("/api/v1/test-runs/", json={"name": "Ad-hoc Run"}, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["suite_id"] is None


def test_create_run_requires_auth(client):
    resp = client.post("/api/v1/test-runs/", json={"name": "No Auth"})
    assert resp.status_code == 401


# ── LIST ───────────────────────────────────────────────────────────────────────

def test_list_runs(client, auth_headers, run):
    resp = client.get("/api/v1/test-runs/", headers=auth_headers)
    assert resp.status_code == 200
    ids = [r["id"] for r in resp.json()]
    assert run["id"] in ids


# ── GET ────────────────────────────────────────────────────────────────────────

def test_get_run(client, auth_headers, run):
    resp = client.get(f"/api/v1/test-runs/{run['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == run["id"]


def test_get_run_not_found(client, auth_headers):
    resp = client.get("/api/v1/test-runs/99999", headers=auth_headers)
    assert resp.status_code == 404


# ── UPDATE ─────────────────────────────────────────────────────────────────────

def test_update_run_status(client, auth_headers, run):
    resp = client.patch(f"/api/v1/test-runs/{run['id']}", json={
        "status": "running",
        "started_at": "2026-02-24T10:00:00Z",
    }, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "running"
    assert data["started_at"] is not None


def test_complete_run(client, auth_headers, run):
    resp = client.patch(f"/api/v1/test-runs/{run['id']}", json={
        "status": "completed",
        "completed_at": "2026-02-24T11:00:00Z",
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"


def test_update_run_not_found(client, auth_headers):
    resp = client.patch("/api/v1/test-runs/99999", json={"status": "aborted"}, headers=auth_headers)
    assert resp.status_code == 404


# ── DELETE ─────────────────────────────────────────────────────────────────────

def test_delete_run(client, auth_headers):
    create = client.post("/api/v1/test-runs/", json={"name": "To Delete"}, headers=auth_headers)
    run_id = create.json()["id"]

    resp = client.delete(f"/api/v1/test-runs/{run_id}", headers=auth_headers)
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/test-runs/{run_id}", headers=auth_headers)
    assert resp.status_code == 404


def test_delete_run_not_found(client, auth_headers):
    resp = client.delete("/api/v1/test-runs/99999", headers=auth_headers)
    assert resp.status_code == 404
