from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root:
# ai-interview-coach/
BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "AI Interview Coach"
    app_env: str = "development"
    debug: bool = True

    # PostgreSQL
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    database_url: str

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Gemini
    gemini_api_key: str = ""

    # LLM Provider
    llm_provider: str = "openai"

    # VAPI
    vapi_api_key: str = ""
    vapi_assistant_id: str = ""

    # Hugging Face
    hf_token: str = ""

    # ChromaDB
    chroma_db_path: str = str(BASE_DIR / "chroma_db")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()