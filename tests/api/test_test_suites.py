import pytest


@pytest.fixture(scope="module")
def suite(client, auth_headers):
    resp = client.post("/api/v1/test-suites/", json={"name": "Login Tests"}, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()


def test_create_suite(client, auth_headers):
    resp = client.post("/api/v1/test-suites/", json={"name": "My Suite"}, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["name"] == "My Suite"


def test_create_suite_requires_auth(client):
    resp = client.post("/api/v1/test-suites/", json={"name": "No Auth Suite"})
    assert resp.status_code == 401


def test_list_suites(client, auth_headers, suite):
    resp = client.get("/api/v1/test-suites/", headers=auth_headers)
    assert resp.status_code == 200
    ids = [s["id"] for s in resp.json()]
    assert suite["id"] in ids


def test_get_suite_not_found(client, auth_headers):
    resp = client.get("/api/v1/test-suites/99999", headers=auth_headers)
    assert resp.status_code == 404


def test_delete_suite(client, auth_headers):
    create = client.post("/api/v1/test-suites/", json={"name": "To Delete"}, headers=auth_headers)
    suite_id = create.json()["id"]

    resp = client.delete(f"/api/v1/test-suites/{suite_id}", headers=auth_headers)
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/test-suites/{suite_id}", headers=auth_headers)
    assert resp.status_code == 404
