# Temporal + PostgreSQL (Docker Compose)

A small, reliable single-host Temporal setup: PostgreSQL persistence, schema
migrations run by a one-shot job, healthchecked server, and the Temporal Web UI.
No Elasticsearch and no Prometheus — just the pieces you need for a demo.

## What runs

| Service | Image | Purpose |
| --- | --- | --- |
| `postgres` | `postgres:17-alpine` | Persistence for both databases (`temporal`, `temporal_visibility`) |
| `temporal-schema-setup` | `temporalio/admin-tools:1.32.2` | One-shot: creates databases and applies/updates the schema (idempotent) |
| `temporal` | `temporalio/server:1.32.2` | Temporal server: frontend, history, matching, worker in one process |
| `temporal-namespace-setup` | `temporalio/admin-tools:1.32.2` | One-shot: creates the `default` namespace with retention (idempotent) |
| `temporal-ui` | `temporalio/ui:2.56.4` | Web UI |

The two `*-setup` containers exit `0` after finishing. That is expected.

## Quick start

```bash
cp sample.env .env
# edit .env and set a real POSTGRES_PASSWORD
docker compose up -d
```

| Endpoint | URL |
| --- | --- |
| Web UI | http://localhost:8080 |
| gRPC frontend (SDKs) | `localhost:7233` |
| PostgreSQL | inside the compose network at `postgres:5432` (not published) |

Both published ports are bound to `127.0.0.1` on purpose.

Check status:

```bash
docker compose ps
docker compose logs -f temporal
```

Stop / start / wipe:

```bash
docker compose down          # keep data
docker compose down -v       # delete the postgres volume
```

## Connecting a worker

From the host, point the SDK at `localhost:7233`. From another container in
this compose network, use `temporal:7233`.

The CLI is available through a throwaway admin-tools container:

```bash
docker run --rm -it --network temporal_temporal temporalio/admin-tools:1.32.2 \
  temporal --address temporal:7233 operator cluster health
```

Or run the CLI on your host: https://docs.temporal.io/cli

## Python worker (uv)

The project is managed by [uv](https://docs.astral.sh/uv/) and pinned to
Python 3.14 in `.python-version`.

```bash
uv sync                        # create .venv and install temporalio
uv run python worker.py        # terminal 1 - polls the "hello-world" task queue
uv run python starter.py       # terminal 2 - prints "Hello, World!"
uv run python starter.py Temporal
```

| File | Purpose |
| --- | --- |
| `workflow.py` | `HelloWorldWorkflow` definition |
| `worker.py` | Worker that hosts the workflow and polls the task queue |
| `starter.py` | Client that starts one execution and prints the result |

Connection settings come from the environment:
`TEMPORAL_ADDRESS` (default `localhost:7233`), `TEMPORAL_NAMESPACE`
(default `default`), `TEMPORAL_TASK_QUEUE` (default `hello-world`).

Results are also visible in the Web UI at http://localhost:8080 under the
`default` namespace.

## Configuration

Everything is driven by `.env` (see `sample.env` for the full list):

- `POSTGRES_PASSWORD` — required, change it.
- `TEMPORAL_VERSION` / `TEMPORAL_ADMINTOOLS_VERSION` — must match each other.
- `TEMPORAL_NUM_HISTORY_SHARDS` — 512 by default; do **not** change it after the
  database has been initialized.
- `TEMPORAL_DEFAULT_NAMESPACE`, `TEMPORAL_NAMESPACE_RETENTION`,
  `TEMPORAL_EXTRA_NAMESPACES` — namespace bootstrap.
- `TEMPORAL_GRPC_PORT`, `TEMPORAL_UI_PORT` — host ports.
- `POSTGRES_SHARED_BUFFERS`, `POSTGRES_MAX_CONNECTIONS` — light tuning; raise
  `shared_buffers` to roughly 25% of host RAM for real workloads.

Extra namespaces are created on start, e.g. `TEMPORAL_EXTRA_NAMESPACES=staging,sandbox`.
Existing namespaces are never modified, so changing retention later is done with
the CLI, not this stack.

## Operations

### Backup and restore

```bash
# Backup (custom format)
docker compose exec -T postgres pg_dump -U temporal -Fc -d temporal \
  > temporal-$(date -u +%Y%m%dT%H%M%SZ).dump
docker compose exec -T postgres pg_dump -U temporal -Fc -d temporal_visibility \
  > temporal_visibility-$(date -u +%Y%m%dT%H%M%SZ).dump

# Restore (stop the server first)
docker compose stop temporal temporal-ui temporal-namespace-setup
docker compose exec -T postgres pg_restore -U temporal --clean --if-exists \
  -d temporal < temporal-YYYYMMDDTHHMMSSZ.dump
docker compose up -d
```

Back up both databases; the server needs the visibility database too.

### Upgrading Temporal

1. Bump `TEMPORAL_VERSION` and `TEMPORAL_ADMINTOOLS_VERSION` together, one minor
   version at a time (e.g. 1.32.x → 1.33.x), and keep the UI on a compatible tag.
2. `docker compose pull && docker compose up -d`

The schema job runs `update-schema` before the server starts, so migrations are
applied automatically. Never skip minor versions.

### Where the data lives

The named volume `temporal-postgres-data` (prefixed by `COMPOSE_PROJECT_NAME`).
Deleting it destroys history and visibility data.

## Production notes

This compose file is a reliable demo/small deployment, not a hardened
internet-facing service:

- Keep `7233` and `8080` on localhost/private networks; Temporal must not be
  exposed to the public internet. If remote clients need access, put a
  TLS-terminating proxy in front of the frontend (Temporal TLS itself is
  configured in the server's static config, not via this compose file).
- Postgres has no TLS here because it is only reachable on the internal compose
  network. Use a managed/HA database with TLS for anything critical, and set
  `SQL_TLS_ENABLED=true` with certificates mounted into both the schema job and
  the server.
- For horizontal scale, run history/matching/frontend/worker as separate
  replicas (or move to the Temporal Helm charts) instead of the all-in-one
  server.
