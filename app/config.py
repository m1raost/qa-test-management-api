from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── API ───────────────────────────────────────────────────────────────────
    PROJECT_NAME: str = "QA Test Management API"
    API_V1_STR: str = "/api/v1"

    # ── Database ──────────────────────────────────────────────────────────────
    # SQLite by default; swap for postgresql+psycopg2://... in .env for prod
    DATABASE_URL: str = "sqlite:///./qa_test_management.db"

    # ── JWT ───────────────────────────────────────────────────────────────────
    # Generate a strong secret in prod: python -c "import secrets; print(secrets.token_hex(32))"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Reads from a .env file automatically (values there override the defaults above)
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


# Single shared instance imported everywhere:  `from app.config import settings`
settings = Settings()
