"""
Load all application configuration from environment variables once via pydantic-settings,
 validate it, and make it available everywhere in the application by exposing as a single `settings` instance.
 See .env.example for the full list of variables.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_env: str = "local"
    log_level: str = "INFO"

    database_url: str
    test_database_url: str | None = None

    jwt_algorithm: str = "RS256"
    jwt_private_key_path: str = "keys/private.pem"
    jwt_public_key_path: str = "keys/public.pem"
    access_token_expire_minutes: int = 15


@lru_cache
def get_settings() -> Settings:
    """Cached so env vars are parsed once (at first import), not for every request."""
    return Settings()


settings = get_settings()
