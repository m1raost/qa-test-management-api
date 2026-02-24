from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# ── Load app config and models ─────────────────────────────────────────────────
# These imports must happen before we reference `Base.metadata` so that all
# ORM models are registered on Base and Alembic can detect their tables.
from app.config import settings
import app.models  # noqa: F401 — registers User, TestSuite, TestCase, TestRun, TestResult
from app.database import Base

# Alembic Config object — gives access to values in alembic.ini
config = context.config

# Wire up Python logging from the [loggers] section in alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The metadata Alembic diffs against to generate migrations
target_metadata = Base.metadata

# Override the sqlalchemy.url from alembic.ini with the value from our Settings.
# This means DATABASE_URL in .env is the single source of truth.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """
    Run migrations without a live DB connection ('offline' mode).
    Generates SQL script output instead of executing against the DB.
    Useful for previewing SQL or deploying via DBA review.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Emit BEGIN/COMMIT around each migration step
        transaction_per_migration=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations with a live DB connection ('online' mode).
    This is the default when you run `alembic upgrade head`.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        # NullPool avoids connection reuse — important for migrations which
        # often ALTER tables and need a clean connection state.
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # compare_type=True tells Alembic to detect column type changes
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
