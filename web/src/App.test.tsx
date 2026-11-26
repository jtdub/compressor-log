import { act, cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import App from "./App";

function jsonResponse(body: unknown, status: number): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function stubFetch(implementation: (request: Request) => Promise<Response>) {
  vi.stubGlobal("fetch", vi.fn(implementation));
}

describe("App", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.useRealTimers();
  });

  it("shows the app name", () => {
    stubFetch(() => new Promise<Response>(() => {}));
    render(<App />);
    expect(
      screen.getByRole("heading", { name: "compressor-log" }),
    ).toBeTruthy();
    expect(screen.getByText("API: checking")).toBeTruthy();
  });

  it("shows API: ok when the health request succeeds", async () => {
    stubFetch(async () => jsonResponse({ status: "ok" }, 200));
    render(<App />);
    expect(await screen.findByText("API: ok")).toBeTruthy();
  });

  it("shows API: not available when the API returns 503", async () => {
    stubFetch(async () => jsonResponse({ status: "unavailable" }, 503));
    render(<App />);
    expect(await screen.findByText("API: not available")).toBeTruthy();
  });

  it("shows API: not available when the request fails", async () => {
    stubFetch(async () => {
      throw new TypeError("Failed to fetch");
    });
    render(<App />);
    expect(await screen.findByText("API: not available")).toBeTruthy();
  });

  it("shows API: not available when the API does not answer in 5 seconds", async () => {
    vi.useFakeTimers();
    stubFetch(
      (request) =>
        new Promise<Response>((_resolve, reject) => {
          request.signal.addEventListener("abort", () =>
            reject(new DOMException("Aborted", "AbortError")),
          );
        }),
    );
    render(<App />);
    expect(screen.getByText("API: checking")).toBeTruthy();
    await act(() => vi.advanceTimersByTimeAsync(5000));
    expect(screen.getByText("API: not available")).toBeTruthy();
  });
});
