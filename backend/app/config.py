"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Relevance Engine application settings."""

    APP_NAME: str = "Relevance Engine"
    API_PREFIX: str = "/api"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./relevance_engine.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    SECRET_KEY: str = "change-me-in-production"
    JWT_SECRET_KEY: str = "change-me-jwt-secret"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # ConsentHub integration (B2B_Consent_Personalization)
    CONSENTHUB_API_URL: str | None = None
    CONSENTHUB_API_KEY: str | None = None

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
