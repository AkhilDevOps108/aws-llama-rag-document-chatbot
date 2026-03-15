from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ROOT_DIR / ".env"), extra="ignore")

    app_name: str = "Document Knowledge AI"
    backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")
    frontend_origin: str = Field(default="http://localhost:5173", alias="FRONTEND_ORIGIN")

    aws_access_key: str = Field(default="", alias="AWS_ACCESS_KEY")
    aws_secret_key: str = Field(default="", alias="AWS_SECRET_KEY")
    aws_region: str = Field(default="us-east-1", alias="AWS_REGION")
    s3_bucket_name: str = Field(default="rag-documents-bucket", alias="S3_BUCKET_NAME")
    s3_document_prefix: str = Field(default="documents/", alias="S3_DOCUMENT_PREFIX")

    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    qdrant_collection: str = Field(default="documents", alias="QDRANT_COLLECTION")

    ollama_url: str = Field(default="http://localhost:11434", alias="OLLAMA_URL")
    ollama_model: str = Field(default="llama3", alias="OLLAMA_MODEL")

    embedding_model: str = Field(default="BAAI/bge-small-en", alias="EMBEDDING_MODEL")
    chunk_size: int = 2000
    chunk_overlap: int = 250
    top_k: int = 5

    @property
    def s3_prefix(self) -> str:
        prefix = self.s3_document_prefix.strip("/")
        return f"{prefix}/" if prefix else ""


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

