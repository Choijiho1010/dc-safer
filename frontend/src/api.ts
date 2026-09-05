import type { Dispatch, Operator } from "./types";

const BASE = import.meta.env.VITE_API_BASE ?? "/api";

export async function fetchHealth(): Promise<{ status: string; version: string }> {
  const res = await fetch(`${BASE}/healthz`);
  if (!res.ok) throw new Error(`healthz ${res.status}`);
  return res.json();
}

/** P5에서 실제 오케스트레이터에 연결한다. 그 전까지 화면 골격 확인용 고정 데이터. */
export function placeholderOperators(): Operator[] {
  return [
    { id: "op-pwr", name: "전력설비 담당", role: "전력설비", assignedSystems: ["UPS", "발전기"] },
    { id: "op-srv", name: "서버·GPU 담당", role: "서버운영", assignedSystems: ["GPU 랙"] },
    { id: "op-net", name: "네트워크 담당", role: "네트워크", assignedSystems: ["코어스위치"] },
    { id: "op-fac", name: "시설안전 담당", role: "시설안전", assignedSystems: ["냉각", "소방"] },
  ];
}

export function placeholderDispatches(): Dispatch[] {
  return placeholderOperators().map((op, i) => ({
    operatorId: op.id,
    step: 1,
    sopSection: `4.${i + 1}`,
    instruction: "시나리오 연결 전 — 표시 골격 확인용",
    status: "대기" as const,
    evidenceType: "text" as const,
  }));
}
