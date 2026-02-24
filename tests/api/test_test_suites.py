"""Tests for /api/v1/test-suites endpoints."""
import pytest


@pytest.fixture(scope="module")
def suite(client, auth_headers):
    """Create one suite reused across this module's tests."""
    resp = client.post("/api/v1/test-suites/", json={
        "name": "Login Tests",
        "description": "All login-related test cases",
    }, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()


# ── CREATE ─────────────────────────────────────────────────────────────────────

def test_create_suite(client, auth_headers):
    resp = client.post("/api/v1/test-suites/", json={"name": "Signup Tests"}, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Signup Tests"
    assert data["description"] is None
    assert "id" in data and "owner_id" in data


def test_create_suite_requires_auth(client):
    resp = client.post("/api/v1/test-suites/", json={"name": "No Auth"})
    assert resp.status_code == 401


# ── LIST ───────────────────────────────────────────────────────────────────────

def test_list_suites(client, auth_headers, suite):
    resp = client.get("/api/v1/test-suites/", headers=auth_headers)
    assert resp.status_code == 200
    ids = [s["id"] for s in resp.json()]
    assert suite["id"] in ids


def test_list_suites_requires_auth(client):
    resp = client.get("/api/v1/test-suites/")
    assert resp.status_code == 401


# ── GET ────────────────────────────────────────────────────────────────────────

def test_get_suite(client, auth_headers, suite):
    resp = client.get(f"/api/v1/test-suites/{suite['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == suite["id"]


def test_get_suite_not_found(client, auth_headers):
    resp = client.get("/api/v1/test-suites/99999", headers=auth_headers)
    assert resp.status_code == 404


# ── UPDATE ─────────────────────────────────────────────────────────────────────

def test_update_suite(client, auth_headers, suite):
    resp = client.patch(f"/api/v1/test-suites/{suite['id']}", json={
        "description": "Updated description",
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["description"] == "Updated description"
    assert resp.json()["name"] == suite["name"]   # unchanged field stays intact


def test_update_suite_not_found(client, auth_headers):
    resp = client.patch("/api/v1/test-suites/99999", json={"name": "x"}, headers=auth_headers)
    assert resp.status_code == 404


# ── DELETE ─────────────────────────────────────────────────────────────────────

def test_delete_suite(client, auth_headers):
    create = client.post("/api/v1/test-suites/", json={"name": "To Delete"}, headers=auth_headers)
    suite_id = create.json()["id"]

    resp = client.delete(f"/api/v1/test-suites/{suite_id}", headers=auth_headers)
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/test-suites/{suite_id}", headers=auth_headers)
    assert resp.status_code == 404


def test_delete_suite_not_found(client, auth_headers):
    resp = client.delete("/api/v1/test-suites/99999", headers=auth_headers)
    assert resp.status_code == 404
