# dc-safer — 데이터센터 이상탐지 대응 오케스트레이션

[![CI](https://github.com/Choijiho1010/dc-safer/actions/workflows/ci.yml/badge.svg)](https://github.com/Choijiho1010/dc-safer/actions/workflows/ci.yml)

> **문제**: 데이터센터 장애 대응은 "경보 발생 → 담당자가 매뉴얼 PDF를 뒤져 → 무전으로 지시 전파"에 의존한다. 야간·교대 상황에서 누가 어느 절차를 어디까지 했는지 관제에서 보이지 않는다.
> **방식**: 시계열 이상탐지가 경보를 띄우면, 인사정보(역할·근무조·자격)로 대상자를 고르고 SOP에서 **그 역할에 해당하는 절**만 검색해 4명에게 **서로 다른 지시**를 동시 전파한다. 각자 사진·영상으로 대응 결과를 보고하면 완료 판정 후 다음 단계를 순차 전파하고, 시니어 화면에서 4인의 진행률·SLA를 실시간으로 본다.
> **숫자**: 측정 예정 — 임베딩 모델 4종 x 벡터스토어 2종 검색 정확도, 이상탐지 3모델 F1·오탐률. 결과는 `docs/BENCHMARKS.md`에 재현 명령과 함께 게시한다. **측정 전까지 이 자리에 수치를 쓰지 않는다.**

> ⚠ **이 저장소의 모든 문서·인물·설비·데이터는 가상이다.** 실제 조직·고객사와 무관하며, RAG 원본 SOP는 공개 표준을 참고해 새로 집필했다(`data/sop/SOURCES.md`).

## 빠른 시작

```bash
cp .env.example .env
make up      # postgres(pgvector) + qdrant + backend + frontend
```
- 관제 콘솔 http://localhost:5173 · API 문서 http://localhost:8000/docs

```bash
make test        # 백엔드 pytest + 프론트 vitest
make lint        # ruff + eslint
make validate    # 공개 레포 유출 게이트 (커밋 전 필수)
```

## 구조

```
backend/    FastAPI · SQLAlchemy 2.0 · 벡터스토어 추상화(pgvector | Qdrant)
frontend/   React 19 + Vite + TS · Operator Theater(4분할 실시간 화면)
data/sop/   가상 데이터센터 SOP 코퍼스 + 인물·시나리오 정의
eval/       RAG 골드셋과 벤치마크 실행기
scripts/    유출 게이트 · 적재 파이프라인
docs/       RUBRIC(자체 채점표) · ADR(결정과 **버린 대안**) · BENCHMARKS
```

## 설계에서 의도적으로 고른 것들

- **벡터스토어를 하나로 안 골랐다.** `VectorStore` 인터페이스 뒤에 pgvector와 Qdrant 두 구현을 두고 같은 골드셋으로 hit@k·MRR·p95를 재서 운영 기본값을 정한다. 선택의 근거를 수치로 남기기 위해서다. → `docs/ADR.md` ADR-002
- **이상탐지는 공개 벤치마크로 검증한다.** 자체 합성 데이터로만 성능을 주장하면 "내가 만든 문제를 내가 푼" 자기충족이 된다. 임계치 기준선 → Isolation Forest → LSTM-AE 순으로 같은 조건에서 비교한다.
- **유출 방지를 프롬프트가 아니라 파이프라인으로 강제한다.** `scripts/validate_repo.py`가 금칙어·자격증명·**이미지 EXIF와 PDF 메타데이터**까지 검사하고, CI의 첫 잡으로 돌아 실패하면 나머지를 막는다.
- **실패도 기록한다.** `docs/ADR.md`에는 채택안뿐 아니라 **버린 대안과 그 이유**가 함께 있다.

## 진행 상태

`phases/index.json`이 단일 원천이다.

| 단계 | 내용 | 상태 |
|---|---|---|
| P0 | 하네스(유출 게이트·훅·채점표·ADR) | 완료 |
| P1 | 골격 + CI/CD 초록불 | 완료 |
| P2 | SOP 코퍼스 → 파싱·임베딩·적재 | 진행 중 |
| P3 | 임베딩·벡터스토어 벤치마크 | 예정 |
| P4 | 이상탐지 모델 사다리 | 예정 |
| P5 | 역할별 전파 + 순차 대응 루프 | 예정 |
| P6 | Operator Theater | 예정 |
| P7 | 포트폴리오 마감(자체 채점 80+) | 예정 |

## 라이선스
MIT. 자세한 내용은 [LICENSE](LICENSE).
