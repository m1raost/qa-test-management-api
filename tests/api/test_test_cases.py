import pytest


@pytest.fixture(scope="module")
def suite_id(client, auth_headers):
    resp = client.post("/api/v1/test-suites/", json={"name": "Cases Suite"}, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()["id"]


@pytest.fixture(scope="module")
def case(client, auth_headers, suite_id):
    resp = client.post("/api/v1/test-cases/", json={
        "title": "Verify login with valid credentials",
        "suite_id": suite_id,
    }, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()


def test_create_case(client, auth_headers, suite_id):
    resp = client.post("/api/v1/test-cases/", json={
        "title": "Minimal case",
        "suite_id": suite_id,
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Minimal case"
    assert data["priority"] == "medium"
    assert data["status"] == "draft"


def test_create_case_invalid_priority(client, auth_headers, suite_id):
    resp = client.post("/api/v1/test-cases/", json={
        "title": "Bad priority",
        "suite_id": suite_id,
        "priority": "urgent",
    }, headers=auth_headers)
    assert resp.status_code == 422


def test_get_case(client, auth_headers, case):
    resp = client.get(f"/api/v1/test-cases/{case['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == case["id"]


def test_delete_case(client, auth_headers, suite_id):
    create = client.post("/api/v1/test-cases/", json={
        "title": "To Delete",
        "suite_id": suite_id,
    }, headers=auth_headers)
    case_id = create.json()["id"]

    resp = client.delete(f"/api/v1/test-cases/{case_id}", headers=auth_headers)
    assert resp.status_code == 204
