from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Rural Weaver API"
    environment: str = "development"
    api_prefix: str = "/api"
    secret_key: str
    access_token_expire_minutes: int = 1440
    database_url: str
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @cached_property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


settings = Settings()  # type: ignore[call-arg]
