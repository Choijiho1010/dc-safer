#!/usr/bin/env python3
"""PreToolUse 훅 — 금칙어가 담긴 파일 쓰기를 차단한다.

한계(헌법에 명시): 스크립트가 실행 중에 생성하는 파일, 바이너리 메타데이터,
Bash 리다이렉션은 이 훅으로 못 막는다. 최종 판정은 scripts/validate_repo.py.
exit 2 = 차단(stderr가 모델에게 전달됨), exit 0 = 통과.
"""
import json
import re
import sys

PATTERNS = [
    r"SKALA|skala-ai|스칼라\s?아카데미",
    r"\bSK\s?(?:AX|C&C|텔레콤)\b",
    r"애커튼|Ackerton",
    r"amdp-registry|skala\d{2}[a-z]\b|\bsk\d{3}\b",
    r"qkrqudwn2|@A\d{4}\b",
    r"sk-proj-[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}",
    r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b",
]

def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    tool = payload.get("tool_name", "")
    if tool not in {"Write", "Edit", "NotebookEdit"}:
        return 0
    ti = payload.get("tool_input", {}) or {}
    path = str(ti.get("file_path", ""))
    if path.endswith(("validate_repo.py", "block_leak.py", "CLAUDE.md")):
        return 0
    haystack = "\n".join(
        str(ti.get(k, "")) for k in ("content", "new_string", "new_source")
    )
    for pattern in PATTERNS:
        m = re.search(pattern, haystack, re.IGNORECASE)
        if m:
            sys.stderr.write(
                f"차단: 공개 레포 금칙어 '{m.group(0)[:4]}***'가 {path} 쓰기에 포함됐다. "
                "제네릭 플레이스홀더(my-registry.example.com, my-namespace 등)로 바꿔 다시 시도할 것.\n"
            )
            return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
