# --------------------------------
# Pydantic Settings
# --------------------------------

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    environment: str = "development"

    # Database configuration
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "aurora"
    database_url: str = "postgresql://aurora:aurora@localhost:5432/aurora"

    # Embedding provider
    embedding_provider: str = "ollama"

    # LLM provider
    llm_provider: str = "ollama"
    ollama_host: str = "http://localhost:11434"

    # API Keys (optional)
    openai_api_key: str | None = None

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()