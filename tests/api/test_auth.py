"""Tests for /api/v1/auth endpoints."""


def test_register_success(client):
    resp = client.post("/api/v1/auth/register", json={
        "email": "newuser@example.com",
        "password": "securepassword",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "newuser@example.com"
    assert data["is_active"] is True
    assert "hashed_password" not in data   # never leak the hash


def test_register_duplicate_email(client, registered_user):
    """Registering with an already-used email returns 400."""
    resp = client.post("/api/v1/auth/register", json={
        "email": "tester@example.com",
        "password": "anything",
    })
    assert resp.status_code == 400
    assert "already registered" in resp.json()["error"]["message"]


def test_login_success(client):
    resp = client.post("/api/v1/auth/login", data={
        "username": "tester@example.com",
        "password": "testpassword123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    resp = client.post("/api/v1/auth/login", data={
        "username": "tester@example.com",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401


def test_login_unknown_email(client):
    resp = client.post("/api/v1/auth/login", data={
        "username": "nobody@example.com",
        "password": "anything",
    })
    assert resp.status_code == 401


def test_me_authenticated(client, auth_headers, registered_user):
    resp = client.get("/api/v1/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == registered_user["email"]


def test_me_no_token(client):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401


def test_me_invalid_token(client):
    resp = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer notavalidtoken"})
    assert resp.status_code == 401
