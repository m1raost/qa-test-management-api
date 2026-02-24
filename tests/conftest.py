import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.dependencies import get_db
from main import app

# ── In-memory SQLite for tests ─────────────────────────────────────────────────
# StaticPool makes every SessionLocal() reuse the SAME underlying connection.
# Without it, each new connection gets its own blank in-memory database — tables
# created by the fixture wouldn't be visible to sessions opened by the app.
TEST_DATABASE_URL = "sqlite:///:memory:"

_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,   # <-- single shared connection for all sessions
)
_TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def override_get_db():
    """Replace the real DB session with the in-memory one for every request."""
    db = _TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the dependency globally before any test runs
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create all tables once for the entire test session, drop them at the end."""
    import app.models  # noqa: F401 — register models on Base
    Base.metadata.create_all(bind=_engine)
    yield
    Base.metadata.drop_all(bind=_engine)


@pytest.fixture(scope="session")
def client(create_tables):
    """Shared TestClient — reused across all tests in the session."""
    with TestClient(app) as c:
        yield c


# ── Auth helpers ───────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def registered_user(client):
    """Register a test user once and return the response JSON."""
    resp = client.post("/api/v1/auth/register", json={
        "email": "tester@example.com",
        "password": "testpassword123",
    })
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture(scope="session")
def auth_headers(client, registered_user):
    """Log in and return headers with a valid Bearer token."""
    resp = client.post("/api/v1/auth/login", data={
        "username": "tester@example.com",   # OAuth2 form field is 'username'
        "password": "testpassword123",
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
