"""기동·상태 엔드포인트 계약 테스트."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz_returns_ok():
    res = client.get("/healthz")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert body["app"] == "dc-safer"


def test_readyz_reports_vector_backend():
    res = client.get("/readyz")
    assert res.status_code == 200
    assert res.json()["vector_backend"] in {"pgvector", "qdrant"}


def test_openapi_is_served():
    assert client.get("/openapi.json").status_code == 200
