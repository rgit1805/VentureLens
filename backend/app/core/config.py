
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = "VentureLens API"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True

    database_url: str

    # Embedding configuration
    embedding_provider: str = "gemini"
    embedding_model: str = "gemini-embedding-2"
    embedding_dimension: int = 768

    # Gemini API configuration
    gemini_api_key: str | None = None

    # Document storage configuration
    document_storage_dir: Path = BASE_DIR / "storage"
    max_upload_size_bytes: int = Field(
        default=25 * 1024 * 1024,
        gt=0,
    )
        # Document chunking configuration
    document_chunk_size_chars: int = Field(
        default=1200,
        gt=0,
    )

    document_chunk_overlap_chars: int = Field(
        default=200,
        ge=0,
    )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
