"""
Central configuration for the GPR backend.

Everything here is read from environment variables (or a local .env file
during development). Nothing sensitive is hardcoded, so the same codebase
runs unchanged in local, CI, and production environments — only the
environment variables differ.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://gpr_user:gpr_password@localhost:5432/gpr_db"
    secret_key: str = "change-me-before-deploying"
    access_token_expire_minutes: int = 60
    jwt_algorithm: str = "HS256"
    sql_echo: bool = False

    project_name: str = "Global Prediction Repository"


@lru_cache
def get_settings() -> Settings:
    # Cached so we're not re-parsing environment variables on every request.
    return Settings()
