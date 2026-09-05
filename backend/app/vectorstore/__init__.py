"""벡터스토어 구현 선택."""
from __future__ import annotations

from app.vectorstore.base import Chunk, SearchHit, VectorStore

_BACKENDS = ("pgvector", "qdrant")


def build_store(backend: str, **kwargs: object) -> VectorStore:
    """설정값으로 구현체를 고른다. 실제 구현은 P2에서 채운다."""
    if backend not in _BACKENDS:
        raise ValueError(f"알 수 없는 vector_backend: {backend!r} (가능: {', '.join(_BACKENDS)})")
    if backend == "pgvector":
        from app.vectorstore.pg import PgVectorStore

        return PgVectorStore(**kwargs)  # type: ignore[arg-type]
    from app.vectorstore.qdrant import QdrantStore

    return QdrantStore(**kwargs)  # type: ignore[arg-type]


__all__ = ["Chunk", "SearchHit", "VectorStore", "build_store"]
