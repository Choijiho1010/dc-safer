.PHONY: up down logs test lint validate eval fmt

DATA_ROOT ?= ./.data

up:            ## 원커맨드 데모 기동
	docker compose up -d --build
	@echo "frontend http://localhost:5173  |  backend http://localhost:8000/docs"

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

test:          ## 백엔드 + 프론트 테스트
	cd backend && uv run pytest
	cd frontend && npm test

lint:
	cd backend && uv run ruff check .
	cd frontend && npm run lint

validate:      ## 공개 레포 유출 게이트 (커밋 전 필수)
	python3 scripts/validate_repo.py
	python3 .claude/hooks/test_block_leak.py
	cd backend && uv run --with pyyaml python ../scripts/validate_corpus.py

eval:          ## RAG 평가셋 실행 → docs/BENCHMARKS.md 갱신 (P3에서 구현)
	@echo "P3 단계에서 구현한다"

fmt:
	cd backend && uv run ruff format .
