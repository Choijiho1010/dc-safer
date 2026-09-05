# CLAUDE.md — dc-safer 헌법

## 불변 블록 (변경 금지)

### 프로젝트
데이터센터 이상탐지 → 역할별 SOP 전파 → 순차 대응 → 관제(Operator Theater) 시스템. **공개 포트폴리오 레포**(MIT).

### 보안 원칙 — 최우선
- **모든 데이터·문서·이미지는 가상이다.** 실존 기업·기관·인물·설비·도메인·레지스트리 주소를 넣지 않는다.
- 금칙어(대소문자 무시): `SK`, `SKALA`, `skala-ai`, `sk0\d\d`, `SK AX`, `SK C&C`, `애커튼`, `Ackerton`, `amdp-registry`, `class-2` 네임스페이스, 실명 `최지호` 외 개인정보.
- 커밋 전 **반드시** `python scripts/validate_repo.py` 통과(exit 0). PreToolUse 훅이 1차 차단하지만 훅은 스크립트 stdout·바이너리를 못 막으므로 게이트가 최종 방어선이다.
- 스크린샷·PDF는 **메타데이터(EXIF·Author)까지** 세척한 것만 커밋한다.
- 실제 자격증명은 어떤 형태로도 커밋하지 않는다. `.env.example`에는 플레이스홀더만.

### 데이터 함정 (실측으로 확인된 것만 기록)
- (비어 있음 — 실측 즉시 여기에 1줄로 추가)

### 재현 명령
```bash
make up        # docker compose up (postgres+pgvector, qdrant, backend, frontend)
make test      # pytest + vitest
make lint      # ruff + eslint
make validate  # 유출 게이트
make eval      # RAG 평가셋 실행 → docs/BENCHMARKS.md 갱신
```

### 저장소 정책
- 코드는 이 레포(텍스트만). **데이터셋·임베딩 모델·Qdrant/PG 볼륨·미디어는 `/Volumes/T7/data/dc-safer/`**. 내장 SSD에 무거운 산출물을 두지 않는다.
- T7 미마운트면 compose·평가가 실패한다. 착수 전 `ls /Volumes/T7` 확인.

## 가변 블록

### 다음 세션 진입점
1. 이 파일 → 2. `phases/index.json`(진행 상태) → 3. `docs/ADR.md`(결정과 버린 대안) → 4. 해당 phase 작업.

### 운용 규칙
- 검증기(`validate` → 테스트 → judge) 없이 작성기부터 만들지 않는다.
- 새 수치를 문서에 쓰기 전에 `eval/` 산출물로 먼저 만든다. 파이프라인을 고치면 하위 수치 전부 재생성.
- 버린 대안은 반드시 `docs/ADR.md`에 이유와 함께 남긴다 — 이 레포의 차별점은 "검증·실패 기록"이다.
- 벡터스토어는 `VectorStore` 인터페이스 뒤에만 둔다. pgvector/Qdrant 중 하나에 직접 결합하지 않는다.

### 실수 → 규칙
- 게이트 정규식을 고칠 때는 반드시 **오탐 제거 + 진짜 유출 리허설**을 한 쌍으로 돌린다. 오탐만 없애면 게이트가 조용히 무력화된다.
- 컨테이너 이미지는 **로컬에서 build + run + 엔드포인트 확인까지** 하고 푸시한다. lint·테스트가 초록이어도 Dockerfile 레이어 순서(소스 COPY 전 `pip install .`)는 CI에서만 터진다.
- 빌드 산출물(`*.egg-info/`, `dist/`, `.data/`)은 만들어지는 즉시 `.gitignore`에 넣는다 — 스테이징에 섞이면 게이트 검사 대상이 불필요하게 늘어난다.
