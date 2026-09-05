#!/usr/bin/env python3
"""공개 레포 유출 게이트.

커밋·푸시 전 최종 방어선. 훅(PreToolUse)이 1차 차단하지만 훅은 스크립트가
직접 쓴 파일·바이너리 메타데이터를 못 막으므로 이 게이트가 최종 판정을 한다.

exit 0 = 통과 / exit 1 = 유출 의심. CI에서도 동일하게 실행된다.
"""
from __future__ import annotations

import re
import subprocess
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 이 파일들은 금칙어를 '정의'하므로 검사 대상에서 제외한다.
SELF_EXEMPT = {
    "scripts/validate_repo.py",
    "CLAUDE.md",
    ".claude/hooks/block_leak.py",
    ".claude/hooks/test_block_leak.py",
    ".claude/settings.json",
}

# (라벨, 정규식) — 대소문자 무시
FORBIDDEN = [
    ("조직식별", r"\bSK\s?(?:AX|C&C|텔레콤|하이닉스)\b"),
    ("조직식별", r"SKALA|스칼라(?:\s?아카데미)?|skala-ai"),
    ("조직식별", r"애커튼|Ackerton|ATS\s*\(.*테크놀로지"),
    ("코스식별", r"\bsk\d{3}\b|skala\d{2}[a-z]\b|amdp-registry"),
    ("코스식별", r"namespace:\s*class-\d"),
    ("호스트/계정", r"qkrqudwn2|@A\d{4}\b"),
    ("자격증명", r"sk-proj-[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"),
    # 값이 셸/컴포즈 치환(${..})이거나 플레이스홀더면 유출이 아니다.
    ("자격증명", r"(?i)(password|passwd|secret|api_key)\s*[:=]\s*['\"]?(?!your_|change_me|placeholder|[-$<{])[A-Za-z0-9!@#$%^&*_-]{8,}"),
    ("내부IP", r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b"),
    ("개인정보", r"01[016-9]-?\d{3,4}-?\d{4}"),
    ("개인정보", r"\b\d{6}-[1-4]\d{6}\b"),
]

TEXT_SUFFIXES = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".yaml", ".yml", ".md",
    ".sql", ".sh", ".toml", ".cfg", ".ini", ".txt", ".env.example", ".html",
    ".css", ".dockerfile", ".conf",
}
BINARY_META_SUFFIXES = {".png", ".jpg", ".jpeg", ".pdf", ".mp4", ".webp"}


def tracked_files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if out.returncode != 0:  # git 저장소가 아직 아니면 전체 워킹트리
        return [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    return [ROOT / line for line in out.stdout.splitlines() if line]


def scan_text(path: Path, rel: str, findings: list[str]) -> None:
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return
    for lineno, line in enumerate(content.splitlines(), 1):
        for label, pattern in FORBIDDEN:
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                hit = m.group(0)
                masked = hit[:3] + "*" * max(0, len(hit) - 3)
                findings.append(f"[{label}] {rel}:{lineno} → {masked}")


def scan_binary_metadata(path: Path, rel: str, findings: list[str]) -> None:
    """PDF의 Author/Producer, PNG의 tEXt 청크처럼 눈에 안 보이는 메타를 본다."""
    try:
        blob = path.read_bytes()
    except OSError:
        return
    chunks = [blob]
    if path.suffix.lower() == ".png":
        # zTXt/iTXt 압축 청크는 풀어서 본다
        for match in re.finditer(rb"(zTXt|iTXt)", blob):
            tail = blob[match.end(): match.end() + 4096]
            try:
                chunks.append(zlib.decompressobj().decompress(tail))
            except zlib.error:
                pass
    for chunk in chunks:
        text = chunk.decode("latin-1", errors="ignore")
        for label, pattern in FORBIDDEN:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                findings.append(f"[{label}/메타데이터] {rel} → {m.group(0)[:3]}***")
                return


def main() -> int:
    findings: list[str] = []
    checked = 0
    for path in tracked_files():
        rel = str(path.relative_to(ROOT))
        if rel in SELF_EXEMPT or not path.is_file():
            continue
        if rel == ".env" or rel.endswith("/.env"):
            findings.append(f"[자격증명] {rel} → .env 파일이 트래킹되고 있다")
            continue
        suffix = path.suffix.lower()
        if suffix in TEXT_SUFFIXES or path.name in {"Dockerfile", "Makefile", ".env.example"}:
            scan_text(path, rel, findings)
            checked += 1
        elif suffix in BINARY_META_SUFFIXES:
            scan_binary_metadata(path, rel, findings)
            checked += 1

    if findings:
        print(f"유출 게이트 실패 — {len(findings)}건 (검사 {checked}개 파일)", file=sys.stderr)
        for f in findings:
            print("  " + f, file=sys.stderr)
        print("\n조치: 해당 값을 제네릭 플레이스홀더로 치환한 뒤 다시 실행한다.", file=sys.stderr)
        return 1

    print(f"유출 게이트 통과 — 검사 {checked}개 파일, 위반 0건")
    return 0


if __name__ == "__main__":
    sys.exit(main())
