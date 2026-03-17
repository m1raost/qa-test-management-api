def test_register(client):
    resp = client.post("/api/v1/auth/register", json={
        "email": "newuser@example.com",
        "password": "securepassword",
    })
    assert resp.status_code == 201
    assert resp.json()["email"] == "newuser@example.com"


def test_register_duplicate_email(client, registered_user):
    resp = client.post("/api/v1/auth/register", json={
        "email": "tester@example.com",
        "password": "anything",
    })
    assert resp.status_code == 400


def test_login_success(client, registered_user):
    resp = client.post("/api/v1/auth/login", data={
        "username": "tester@example.com",
        "password": "testpassword123",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client, registered_user):
    resp = client.post("/api/v1/auth/login", data={
        "username": "tester@example.com",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401
