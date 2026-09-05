#!/usr/bin/env python3
"""SOP 코퍼스 구조 게이트.

문서가 지켜야 할 계약을 기계가 검사한다. 사람이나 에이전트에게 "형식 맞나
봐줘"를 시키지 않기 위한 것 — 판정이 가능한 것은 전부 여기서 끝낸다.

검사 항목
  1. frontmatter 필수 키와 fictional 플래그, 가상 문서 고지
  2. '## 4. 대응절차'의 모든 하위 절에 담당역할·예상소요·완료판정 3줄
  3. 골드셋의 gold_doc_id가 실존 문서를 가리키는지, 문서별 분포
  4. 인물 역할 중복 없음, 시나리오의 expected_sop 유효성

exit 0 = 통과 / exit 1 = 계약 위반.
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data/sop/sop-corpus"
GOLDSET = ROOT / "eval/rag-goldset.yaml"
PERSONAS = ROOT / "data/sop/personas.yaml"
SCENARIOS = ROOT / "data/sop/incident-scenarios.yaml"

REQUIRED_FM = {"doc_id", "title", "version", "roles", "systems", "fictional"}
STEP_KEYS = ("담당역할:", "예상소요:", "완료판정:")


def _load(path: Path, *keys: str) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    for key in keys:
        if key in data:
            return data[key]
    raise SystemExit(f"{path.name}: 리스트 또는 {keys} 키가 필요하다")


def main() -> int:
    problems: list[str] = []
    docs: dict[str, dict] = {}

    for path in sorted(CORPUS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not fm:
            problems.append(f"{path.name}: frontmatter 없음")
            continue
        meta = yaml.safe_load(fm.group(1))
        missing = REQUIRED_FM - set(meta)
        if missing:
            problems.append(f"{path.name}: frontmatter 키 누락 {sorted(missing)}")
        if not meta.get("fictional"):
            problems.append(f"{path.name}: fictional 플래그가 참이 아니다")
        if "가상 문서" not in text[:900]:
            problems.append(f"{path.name}: 가상 문서 고지 누락")
        docs[meta.get("doc_id", path.stem)] = meta

        body = text[fm.end():]
        section = re.search(r"^## 4\..*?(?=^## 5\.|\Z)", body, re.S | re.M)
        if not section:
            problems.append(f"{path.name}: '## 4. 대응절차' 절 없음")
            continue
        subsections = re.split(r"^### ", section.group(0), flags=re.M)[1:]
        if not subsections:
            problems.append(f"{path.name}: 4.x 하위 절이 없다")
        for sub in subsections:
            title = sub.splitlines()[0].strip()[:30]
            for key in STEP_KEYS:
                if key not in sub:
                    problems.append(f"{path.name} §{title}: '{key}' 누락")

    if not docs:
        problems.append("SOP 문서가 하나도 없다")

    gold = _load(GOLDSET, "queries", "goldset")
    unknown = [q["qid"] for q in gold if q.get("gold_doc_id") not in docs]
    if unknown:
        problems.append(f"골드셋이 존재하지 않는 doc_id 참조: {unknown}")
    dist = collections.Counter(q.get("gold_doc_id") for q in gold)
    empty = [d for d in docs if dist[d] == 0]
    if empty:
        problems.append(f"골드셋 질의가 하나도 없는 문서: {empty}")

    personas = _load(PERSONAS, "personas", "operators")
    roles = [p.get("role") for p in personas]
    if len(set(roles)) != len(roles):
        problems.append(f"인물 역할이 중복된다: {roles}")

    for scenario in _load(SCENARIOS, "scenarios"):
        expected = scenario.get("expected_sop")
        refs = expected if isinstance(expected, list) else [expected]
        for ref in refs:
            if ref not in docs:
                problems.append(f"{scenario.get('scenario_id')}: expected_sop {ref!r} 미존재")
        for step in scenario.get("steps", []):
            if not step.get("completion_criteria"):
                problems.append(f"{scenario.get('scenario_id')}: completion_criteria 없는 단계")

    if problems:
        print(f"코퍼스 게이트 실패 — {len(problems)}건", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1

    print(
        f"코퍼스 게이트 통과 — 문서 {len(docs)}종, 골드셋 {len(gold)}건 "
        f"(문서별 {min(dist.values())}-{max(dist.values())}건), 인물 {len(personas)}명"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
