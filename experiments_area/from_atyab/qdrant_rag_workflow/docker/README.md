# Qdrant in Docker

Single `qdrant/qdrant` service used by both workflows. Nothing else is needed:
the ingest workflow creates the collection on its first run.

## Start

```bash
# from the project root (experiments_area/from_atyab/qdrant_rag_workflow)
docker compose -f docker/docker-compose.yml up -d
```

Wait until `docker compose -f docker/docker-compose.yml ps` reports `healthy`
(usually a few seconds), then check the REST API:

```bash
curl http://localhost:6333/healthz
```

## Stop / clean up

```bash
# keep the vectors for the next session
docker compose -f docker/docker-compose.yml down

# delete the vectors as well (also removes docker/qdrant_storage)
docker compose -f docker/docker-compose.yml down
rm -rf docker/qdrant_storage
```

To wipe only the demo collection, keep the container running and use
`uv run python main.py ingest --recreate` instead.

## Ports and data

| What | Where |
| --- | --- |
| REST / web UI | http://localhost:6333 (dashboard at `/dashboard`) |
| gRPC | localhost:6334 (unused by the Python app, kept for parity) |
| On-disk data | `docker/qdrant_storage/` (gitignored) |

Both ports are bound to `127.0.0.1`, so they are not exposed to your network.

## Overrides

The compose file reads these optional variables from the shell or a `.env`
next to the compose file:

| Variable | Default | Meaning |
| --- | --- | --- |
| `QDRANT_VERSION` | `v1.20.2` | Image tag. Pin exactly; do not use `latest`. |
| `QDRANT_HTTP_PORT` | `6333` | Host port mapped to the REST API |
| `QDRANT_GRPC_PORT` | `6334` | Host port mapped to gRPC |
| `COMPOSE_PROJECT_NAME` | `qdrant-rag-workflow` | Container/network prefix |

If you change a host port, change `QDRANT_URL` in the project `sample.env` too.
