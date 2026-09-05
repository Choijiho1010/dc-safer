import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { placeholderDispatches, placeholderOperators } from "./api";
import { TheaterGrid } from "./TheaterGrid";

describe("TheaterGrid", () => {
  it("4인의 패널을 동시에 렌더링한다", () => {
    render(<TheaterGrid operators={placeholderOperators()} dispatches={placeholderDispatches()} />);
    const panels = screen.getAllByRole("article");
    expect(panels).toHaveLength(4);
  });

  it("역할별로 서로 다른 SOP 절을 표시한다", () => {
    render(<TheaterGrid operators={placeholderOperators()} dispatches={placeholderDispatches()} />);
    const sections = screen
      .getAllByText(/SOP 4\./)
      .map((el) => el.textContent?.match(/SOP (4\.\d)/)?.[1]);
    expect(new Set(sections).size).toBe(4);
  });

  it("지시가 없는 담당자는 '전파된 지시 없음'으로 표시한다", () => {
    render(<TheaterGrid operators={placeholderOperators()} dispatches={[]} />);
    expect(screen.getAllByText("전파된 지시 없음")).toHaveLength(4);
  });
});
