# backend/app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    google_api_key: str | None = None
    gemini_api_key: str | None = None
    serper_api_key: str | None = None
    port: int | None = None  

    # Pydantic v2 style config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  
    )

settings = Settings()
