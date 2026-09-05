import { useEffect, useState } from "react";

import { fetchHealth, placeholderDispatches, placeholderOperators } from "./api";
import { TheaterGrid } from "./TheaterGrid";

export function App() {
  const [backend, setBackend] = useState<string>("확인 중");

  useEffect(() => {
    fetchHealth()
      .then((h) => setBackend(`정상 (v${h.version})`))
      .catch(() => setBackend("연결 실패"));
  }, []);

  return (
    <main>
      <header className="app-header">
        <h1>dc-safer 관제 콘솔</h1>
        <p className="backend-status">백엔드: {backend}</p>
      </header>
      <TheaterGrid operators={placeholderOperators()} dispatches={placeholderDispatches()} />
    </main>
  );
}
