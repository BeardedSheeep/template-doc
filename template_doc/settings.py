from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="template-doc", alias="APP_NAME")
    environment: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=False, alias="APP_DEBUG")

    model_config = SettingsConfigDict(extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings.

    Tests that mutate environment variables should call
    ``get_settings.cache_clear()`` before reading settings again.
    """
    return Settings()
