import type { Dispatch, Operator } from "./types";

interface Props {
  operators: Operator[];
  dispatches: Dispatch[];
}

/** Operator Theater — 4인의 수신 지시와 대응 상태를 한 화면에 동시 렌더링한다. */
export function TheaterGrid({ operators, dispatches }: Props) {
  return (
    <section aria-label="Operator Theater" className="theater-grid">
      {operators.map((op) => {
        const d = dispatches.find((x) => x.operatorId === op.id);
        return (
          <article key={op.id} className="theater-panel" aria-label={`${op.role} 패널`}>
            <header>
              <h2>{op.role}</h2>
              <span className="status" data-status={d?.status ?? "대기"}>
                {d?.status ?? "대기"}
              </span>
            </header>
            <p className="systems">담당 설비: {op.assignedSystems.join(", ")}</p>
            <p className="instruction">
              {d ? `[SOP ${d.sopSection}] ${d.instruction}` : "전파된 지시 없음"}
            </p>
          </article>
        );
      })}
    </section>
  );
}
