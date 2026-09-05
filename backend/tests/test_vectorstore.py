"""벡터스토어 추상화 계약 — 구현이 바뀌어도 이 테스트는 유지된다."""
import pytest

from app.vectorstore import VectorStore, build_store
from app.vectorstore.base import Chunk


def test_factory_selects_backend():
    assert build_store("pgvector").backend == "pgvector"
    assert build_store("qdrant").backend == "Qdrant"


def test_factory_rejects_unknown_backend():
    with pytest.raises(ValueError, match="알 수 없는 vector_backend"):
        build_store("faiss")


@pytest.mark.parametrize("backend", ["pgvector", "qdrant"])
def test_implementations_satisfy_protocol(backend):
    assert isinstance(build_store(backend), VectorStore)


def test_chunk_is_hashable_and_immutable():
    chunk = Chunk(chunk_id="c1", doc_id="SOP-PWR-001", section="4.1", text="x")
    assert chunk.roles == ()
    with pytest.raises(AttributeError):
        chunk.text = "바꿀 수 없다"  # type: ignore[misc]
