# compressor-log

compressor-log is a multi-tenant app, hosted or self-hosted, that tracks
high-pressure breathing-gas equipment: compressors, booster pumps, and nitrox
membrane systems. It records hour meters, filtration stacks, filter cartridges,
maintenance, fills, and the cost of each fill. An organization that operates 2 to
10 compressors is the typical user.

## Backend

Before you start, install Docker, Python 3.13, and uv.

Start the database and the API on your host:

```bash
cp .env.example .env
docker compose up -d db
cd backend
uv sync
uv run --env-file ../.env python manage.py migrate
uv run --env-file ../.env python manage.py runserver
```

The API answers at `http://localhost:8000/api/v1/health/`.

The settings read the process environment only. The option `uv run --env-file`
loads `.env` for a host command.

Run the tests and the checks in `backend/`:

```bash
uv run --env-file ../.env pytest
uv run --env-file ../.env mypy .
uv run ruff check . && uv run ruff format --check .
```

WARNING: This deletes the development database. The command `docker compose down -v`
removes the data volume.

## Changelog

Each pull request adds one fragment file to `changes/`. The name is
`<issue number>.<type>`, for example `30.added`. The file holds one line for an end
user. CI fails a pull request that has no fragment.
