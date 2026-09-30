from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    llm_mode: str = "mock"  # mock | openai
    llm_base_url: str = "http://127.0.0.1:11434/v1"
    llm_model: str = "llama3.1"
    llm_api_key: str = "not-needed-for-local"
    company_seed: int = 42
    ai_server_host: str = "127.0.0.1"
    ai_server_port: int = 8000


@lru_cache
def get_settings() -> Settings:
    return Settings()
