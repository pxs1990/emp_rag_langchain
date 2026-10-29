from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_url: str | None = None
    google_api_key: str
    embedding_model: str = "models/gemini-embedding-001"
    llm_model: str = "gemini-2.5-flash"

    postgres_user: str | None = None
    postgres_password: str | None = None
    postgres_host: str | None = None
    postgres_port: str | None = None
    postgres_db: str | None = None

    # Tell Pydantic to automatically load from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def build_postgres_url(cls, data):
        if isinstance(data, dict) and not data.get("postgres_url"):
            user = data.get("postgres_user")
            password = data.get("postgres_password")
            host = data.get("postgres_host")
            port = data.get("postgres_port")
            db = data.get("postgres_db")
            if all([user, password, host, port, db]):
                data["postgres_url"] = f"postgresql://{user}:{password}@{host}:{port}/{db}"
        return data


settings = Settings()