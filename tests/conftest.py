import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.dependencies import get_db
from main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def override_get_db():
    db = _TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=_engine)
    yield
    Base.metadata.drop_all(bind=_engine)


@pytest.fixture(scope="session")
def client(create_tables):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def registered_user(client):
    resp = client.post("/api/v1/auth/register", json={
        "email": "tester@example.com",
        "password": "testpassword123",
    })
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture(scope="session")
def auth_headers(client, registered_user):
    resp = client.post("/api/v1/auth/login", data={
        "username": "tester@example.com",
        "password": "testpassword123",
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
