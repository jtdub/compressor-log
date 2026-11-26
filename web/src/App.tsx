import { useEffect, useState } from "react";

import { api } from "./api/client";

const HEALTH_TIMEOUT_MS = 5000;

type ApiStatus = "checking" | "ok" | "not available";

async function readApiStatus(signal: AbortSignal): Promise<ApiStatus> {
  try {
    const { data } = await api.GET("/api/v1/health/", { signal });
    return data?.status === "ok" ? "ok" : "not available";
  } catch {
    return "not available";
  }
}

/** Show the name of the app and the state of the API. */
export default function App() {
  const [status, setStatus] = useState<ApiStatus>("checking");

  useEffect(() => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), HEALTH_TIMEOUT_MS);
    let active = true;
    readApiStatus(controller.signal).then((result) => {
      if (active) {
        setStatus(result);
      }
    });
    return () => {
      active = false;
      clearTimeout(timer);
      controller.abort();
    };
  }, []);

  return (
    <main>
      <h1>compressor-log</h1>
      <p>API: {status}</p>
    </main>
  );
}
