"""벡터스토어 추상화.

pgvector와 Qdrant 두 구현을 같은 인터페이스 뒤에 두고, 동일 평가셋으로
비교한 뒤 운영 기본값을 정한다(docs/ADR.md ADR-002). 애플리케이션 코드는
어느 쪽에도 직접 결합하지 않는다.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class Chunk:
    """SOP 문서에서 잘라낸 검색 단위."""

    chunk_id: str
    doc_id: str
    section: str
    text: str
    roles: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SearchHit:
    chunk: Chunk
    score: float


@runtime_checkable
class VectorStore(Protocol):
    """구현체가 지켜야 할 계약."""

    def ensure_schema(self, dim: int) -> None:
        """컬렉션·테이블·인덱스를 멱등하게 준비한다."""

    def upsert(self, chunks: list[Chunk], vectors: list[list[float]]) -> int:
        """청크와 임베딩을 적재하고 처리 건수를 돌려준다."""

    def search(
        self, vector: list[float], top_k: int = 5, roles: tuple[str, ...] | None = None
    ) -> list[SearchHit]:
        """유사도 상위 top_k를 돌려준다. roles가 주어지면 역할로 필터링한다."""

    def count(self) -> int:
        """적재된 청크 수."""
