"""API 응답 스키마."""
from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(description="ok 고정")
    app: str
    version: str


class ReadyResponse(BaseModel):
    status: str
    vector_backend: str
    dependencies: dict[str, str] = Field(description="의존 서비스별 상태")
