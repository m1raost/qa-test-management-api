from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# ── Engine ────────────────────────────────────────────────────────────────────
# connect_args is SQLite-specific: allows the same connection to be used
# across threads (FastAPI handles requests in a thread pool).
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)

# ── Session factory ───────────────────────────────────────────────────────────
# Each request gets its own session (opened/closed by the get_db dependency).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ── Declarative base ──────────────────────────────────────────────────────────
# All ORM models inherit from this. SQLAlchemy uses it to track the schema.
class Base(DeclarativeBase):
    pass
