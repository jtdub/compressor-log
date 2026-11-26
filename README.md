# compressor-log

## Backend

Run these commands from the repository root. Docker must run on your machine.

```bash
cp .env.example .env
docker compose up -d db redis
cd backend
uv sync
uv run --env-file ../.env python manage.py migrate
uv run --env-file ../.env python manage.py runserver
uv run --env-file ../.env pytest
uv run --env-file ../.env mypy .
uv run ruff check . && uv run ruff format --check .
```

The settings read the process environment only. The `uv run --env-file` option loads `.env` for a host command.

### API schema

The API schema is at `http://localhost:8000/api/schema/`. The API documentation page is at `http://localhost:8000/api/docs/`. The page loads Swagger UI from `cdn.jsdelivr.net`, so it needs internet access.

The file `openapi/schema.yaml` holds the schema. After you change an endpoint, run this command. Then commit the file. CI fails when the file is not current.

```bash
cd backend
uv run --env-file ../.env python manage.py spectacular --file ../openapi/schema.yaml --validate --fail-on-warn
```

`SAAS_MODE` is `false` by default. `GET /api/v1/config/` returns its value.

### Worker

Start the Celery worker in a second terminal. The `redis` service must run.

```bash
cd backend
uv run --env-file ../.env celery -A config worker -l info
```

If you change `REDIS_PORT`, change the port in `CELERY_BROKER_URL` to the same value.

## Web

Run these commands from the repository root. Node 24 and pnpm must be on your machine.

```bash
cd web
pnpm install
pnpm dev
pnpm test
pnpm lint && pnpm format:check && pnpm typecheck
```

`pnpm dev` starts the web app at `http://localhost:5173`. The API must run at `http://localhost:8000`.

Vite forwards each request for `/api` to the API. To use another API address, set `VITE_API_PROXY_TARGET` before you run `pnpm dev`.

The web app calls the API through a typed client. The file `web/src/api/schema.d.ts` holds the types. After you change `openapi/schema.yaml`, run this command. Then commit the file. CI fails when the file is not current.

```bash
cd web
pnpm generate:api
```
