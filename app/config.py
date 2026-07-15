"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    app_debug: bool = False
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    database_url: str = "postgresql+asyncpg://registry:registry@localhost:5432/jol_registry"

    admin_api_key: str = "change-me-in-production"
    allowed_origins: str = "http://localhost:3000"

    rate_limit_requests_per_minute: int = 60

    log_level: str = "INFO"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
