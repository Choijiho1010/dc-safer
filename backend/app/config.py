"""환경 설정. 실제 값은 .env(커밋 금지), 예시는 .env.example."""
from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "dc-safer"
    environment: Literal["local", "ci", "prod"] = "local"

    database_url: str = "postgresql+psycopg://safer:change_me@localhost:5432/safer"

    # 벡터스토어: 두 구현을 같은 인터페이스 뒤에 두고 벤치마크로 기본값을 정한다(ADR-002).
    vector_backend: Literal["pgvector", "qdrant"] = "pgvector"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "sop_chunks"

    # 임베딩 모델은 벤치마크 결과로 확정한다(ADR-004). 그 전까지는 후보 기본값.
    embedding_model: str = "BAAI/bge-m3"
    embedding_dim: int = 1024

    # LLM은 LiteLLM 추상화 뒤. 키가 없으면 규칙 기반 목 응답으로 폴백한다.
    llm_model: str = "ollama/qwen2.5:7b"
    llm_base_url: str = "http://localhost:11434"


@lru_cache
def get_settings() -> Settings:
    return Settings()
