import createClient from "openapi-fetch";

import type { paths } from "./schema";

/** Typed client for the compressor-log API. */
export const api = createClient<paths>({
  baseUrl: window.location.origin,
  fetch: (request) => globalThis.fetch(request),
});
