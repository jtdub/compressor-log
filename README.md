# compressor-log

compressor-log is a multi-tenant app, hosted or self-hosted, that tracks high-pressure breathing-gas equipment: compressors, booster pumps, and nitrox membrane systems. It records hour meters, filtration stacks, filter cartridges, maintenance, fills, and the cost of each fill. An organization that operates 2 to 10 compressors is the typical user.

## Prerequisites

- Docker with Docker Compose v5.7.1. This is the version that the first start used.
- uv, to run the backend commands on your host.
- Node 24 and pnpm, to run the web commands on your host.

## First start

Run these commands from the repository root.

```bash
cp .env.example .env
docker compose up --build --wait
```

The command starts the database, Redis, the API, the worker, and the web app. The service `migrate` runs the database migrations and then exits with code 0.

| Address | Content |
| --- | --- |
| `http://localhost:5173` | The web app. It shows "API: ok" when the API works. |
| `http://localhost:8000/api/v1/health/` | The health check of the API. |
| `http://localhost:8000/api/docs/` | The API documentation page. |

To stop the stack, run `docker compose down`.

WARNING: This deletes the development database. Use `docker compose down -v` only when you want to remove the data volume.

```bash
docker compose down -v
```

## Tests in compose

Start the stack first. Then run these commands.

```bash
docker compose run --rm api pytest
docker compose run --rm web pnpm test
```

## Variables

Compose reads the file `.env`. Compose publishes each port on `127.0.0.1` only.

| Variable | Default | Use |
| --- | --- | --- |
| `DJANGO_DEBUG` | `true` | Turns on the Django debug mode. |
| `DJANGO_SECRET_KEY` | empty | The Django secret key. An empty value is permitted only when `DJANGO_DEBUG` is `true`. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | The host names that the API accepts. |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | `compressor_log` | The database name, user, and password. |
| `POSTGRES_HOST` | `localhost` | The database host. Compose sets `db` for the containers. |
| `POSTGRES_PORT` | `5432` | The database port on your host. |
| `REDIS_PORT` | `6379` | The Redis port on your host. |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | The Redis address of the worker. Compose sets `redis://redis:6379/0` for the containers. |
| `SAAS_MODE` | `false` | Turns on the features of the hosted service. |
| `API_PORT` | `8000` | The API port on your host. |
| `WEB_PORT` | `5173` | The web app port on your host. |

If a port is busy, set another value for the port variable in `.env`. Then run `docker compose up --build --wait` again.

If you change `API_PORT`, set `VITE_API_PROXY_TARGET` to the new address for the host commands of the Web section. If you change `REDIS_PORT`, change the port in `CELERY_BROKER_URL`.

## Changelog

Each pull request needs a towncrier fragment in `changes/`. Name the file `<number>.<type>`, for example `34.added`. Write one item on one line. CI fails when the fragment is missing.

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
```

`pnpm dev` starts the web app at `http://localhost:5173`. The API must run at `http://localhost:8000`.

To run the tests and the checks, use a second terminal.

```bash
cd web
pnpm test
pnpm lint && pnpm format:check && pnpm typecheck
```

Vite forwards each request for `/api` to the API. To use another API address, set `VITE_API_PROXY_TARGET` before you run `pnpm dev`.

The web app calls the API through a typed client. The file `web/src/api/schema.d.ts` holds the types. After you change `openapi/schema.yaml`, run this command. Then commit the file. CI fails when the file is not current.

```bash
cd web
pnpm generate:api
```
