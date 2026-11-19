"""Environment configuration for both workflows.

Everything comes from environment variables, with sane defaults for a local
demo. `.env` in the project root is loaded automatically (see `sample.env`).
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Loaded once at import time. Real environment variables always win.
load_dotenv(PROJECT_ROOT / ".env")


def _text(name: str, default: str) -> str:
    value = os.getenv(name)
    return default if value is None or value.strip() == "" else value.strip()


def _optional_text(name: str) -> str | None:
    value = os.getenv(name)
    return None if value is None or value.strip() == "" else value.strip()


def _number(name: str, default: int) -> int:
    raw = _optional_text(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer, got {raw!r}") from error


def _decimal(name: str, default: float) -> float:
    raw = _optional_text(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError as error:
        raise ValueError(f"{name} must be a number, got {raw!r}") from error


@dataclass(frozen=True)
class Settings:
    """Resolved configuration shared by the ingest and query workflows."""

    openai_api_key: str
    chat_model: str
    embedding_model: str
    embedding_dimensions: int
    qdrant_url: str
    qdrant_api_key: str | None
    collection_name: str
    pdf_dir: Path
    chunk_size_tokens: int
    chunk_overlap_tokens: int
    retrieval_top_k: int
    retrieval_score_threshold: float

    @classmethod
    def from_env(cls) -> "Settings":
        # A relative PDF_DIR is resolved against the project root, so the
        # workflows behave the same no matter which directory you run them from.
        pdf_dir = Path(_text("PDF_DIR", "data/pdfs")).expanduser()
        if not pdf_dir.is_absolute():
            pdf_dir = PROJECT_ROOT / pdf_dir

        return cls(
            openai_api_key=_text("OPENAI_API_KEY", ""),
            chat_model=_text("OPENAI_CHAT_MODEL", "gpt-4.1-mini"),
            embedding_model=_text("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
            embedding_dimensions=_number("OPENAI_EMBEDDING_DIMENSIONS", 1536),
            qdrant_url=_text("QDRANT_URL", "http://localhost:6333"),
            qdrant_api_key=_optional_text("QDRANT_API_KEY"),
            collection_name=_text("QDRANT_COLLECTION", "pdf_knowledge"),
            pdf_dir=pdf_dir,
            chunk_size_tokens=_number("CHUNK_SIZE_TOKENS", 1000),
            chunk_overlap_tokens=_number("CHUNK_OVERLAP_TOKENS", 200),
            retrieval_top_k=_number("RETRIEVAL_TOP_K", 4),
            retrieval_score_threshold=_decimal("RETRIEVAL_SCORE_THRESHOLD", 0.2),
        )

    def require_openai_key(self) -> str:
        """Return the API key or fail with an actionable message."""
        if not self.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Copy sample.env to .env "
                "(`cp sample.env .env`) and add your key."
            )
        return self.openai_api_key

    def validate_splitter(self) -> None:
        if self.chunk_size_tokens <= 0:
            raise ValueError("CHUNK_SIZE_TOKENS must be greater than 0")
        if self.chunk_overlap_tokens < 0:
            raise ValueError("CHUNK_OVERLAP_TOKENS cannot be negative")
        if self.chunk_overlap_tokens >= self.chunk_size_tokens:
            raise ValueError("CHUNK_OVERLAP_TOKENS must be smaller than CHUNK_SIZE_TOKENS")


def load_settings() -> Settings:
    settings = Settings.from_env()
    settings.validate_splitter()
    return settings
