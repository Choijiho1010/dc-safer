"""pgvector 기반 VectorStore 구현. 스키마·검색은 P2에서 채운다."""
from __future__ import annotations

from app.vectorstore.base import Chunk, SearchHit


class PgVectorStore:
    backend = "pgvector"

    def __init__(self, **options: object) -> None:
        self.options = options

    def ensure_schema(self, dim: int) -> None:
        raise NotImplementedError("P2에서 구현")

    def upsert(self, chunks: list[Chunk], vectors: list[list[float]]) -> int:
        raise NotImplementedError("P2에서 구현")

    def search(
        self, vector: list[float], top_k: int = 5, roles: tuple[str, ...] | None = None
    ) -> list[SearchHit]:
        raise NotImplementedError("P2에서 구현")

    def count(self) -> int:
        raise NotImplementedError("P2에서 구현")
