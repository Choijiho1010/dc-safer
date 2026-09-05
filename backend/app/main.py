"""FastAPI 진입점. P1 단계에서는 기동·상태 확인까지만 책임진다."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.schemas import HealthResponse, ReadyResponse

settings = get_settings()

app = FastAPI(
    title="dc-safer",
    version="0.1.0",
    summary="데이터센터 이상탐지 → 역할별 SOP 전파 → 순차 대응 오케스트레이션",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz", response_model=HealthResponse, tags=["ops"])
def healthz() -> HealthResponse:
    """프로세스 생존 확인. 의존 서비스를 건드리지 않는다."""
    return HealthResponse(status="ok", app=settings.app_name, version=app.version)


@app.get("/readyz", response_model=ReadyResponse, tags=["ops"])
def readyz() -> ReadyResponse:
    """의존 서비스 준비 상태. P2에서 DB·벡터스토어 실제 핑으로 채운다."""
    return ReadyResponse(
        status="ok",
        vector_backend=settings.vector_backend,
        dependencies={"database": "unchecked", "vectorstore": "unchecked"},
    )
