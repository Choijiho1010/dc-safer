#!/usr/bin/env python3
"""훅 회귀 테스트 — 훅이 실제로 막는지 검증한다. `python3 .claude/hooks/test_block_leak.py`"""
import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).parent / "block_leak.py"
CASES = [
    ({"tool_name": "Write", "tool_input": {"file_path": "k8s/a.yaml", "content": "image: amdp-registry.example/x"}}, 2, "레지스트리"),
    ({"tool_name": "Write", "tool_input": {"file_path": "a.md", "content": "SKALA 과정에서"}}, 2, "코스명"),
    ({"tool_name": "Edit", "tool_input": {"file_path": "a.py", "new_string": "host='10.1.2.3'"}}, 2, "내부IP"),
    ({"tool_name": "Write", "tool_input": {"file_path": "a.md", "content": "한빛 IDC 전력 계통"}}, 0, "정상 통과"),
    ({"tool_name": "Bash", "tool_input": {"command": "echo SKALA"}}, 0, "Write 아님(훅 범위 밖)"),
]

def main() -> int:
    failed = 0
    for payload, expected, label in CASES:
        proc = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), text=True, capture_output=True)
        ok = proc.returncode == expected
        print(f"{'PASS' if ok else 'FAIL'}  {label}: exit={proc.returncode} (기대 {expected})")
        failed += 0 if ok else 1
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
