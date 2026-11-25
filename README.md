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

The file `openapi/schema.yaml` holds the schema. Run this command after you change an endpoint, then commit the file. CI fails when the file is not current.

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
