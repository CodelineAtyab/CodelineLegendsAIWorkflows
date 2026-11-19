# AGENTS.md

Project memory for AI coding agents (and humans) working on
`experiments_area/from_atyab/qdrant_rag_workflow`.

## What this project is

A teaching demo of two LangGraph workflows over a containerised Qdrant vector
database:

1. **Ingest** - read `.pdf` files from `data/pdfs/`, split them into 1000-token
   chunks with 200-token overlap, embed them with `text-embedding-3-small`, and
   store them in Qdrant.
2. **Query** - embed a customer question, retrieve the closest chunks, and
   answer with `gpt-4.1-mini` using only those chunks, with citations.

It lives inside the `CodelineLegendsAIWorkflows` monorepo, so it must stay a
self-contained uv project (`pyproject.toml` + committed `uv.lock`).

Stack: Python 3.14, uv, LangGraph 1.x, langchain-openai, langchain-qdrant,
pypdf, Qdrant `v1.20.2` in Docker.

## Run order (never reorder)

```bash
uv sync
docker compose -f docker/docker-compose.yml up -d     # Qdrant must be up first
uv run python main.py ingest                          # then load PDFs
uv run python main.py query "your question"           # then ask
```

The app never starts Qdrant itself. If Qdrant is down, `ingest` and `query`
print the exact compose command to run and exit non-zero.

## Commands

| Command | Meaning |
| --- | --- |
| `uv sync` | Install from `uv.lock` |
| `docker compose -f docker/docker-compose.yml up -d` | Start Qdrant (pinned image) |
| `docker compose -f docker/docker-compose.yml down` | Stop it, keep vectors |
| `uv run python main.py ingest` | Ingest new PDFs; exit 1 if any file failed |
| `... ingest --include-processed` | Also re-ingest `_`-marked files |
| `... ingest --recreate` | Drop collection, rebuild from **all** PDFs |
| `... query "q"` / `query --interactive` / `query "q" --top-k 8` | Ask |
| `... graphs` | Rewrite the four diagram files |
| `uvx ruff@0.16.10 check .` | Lint, same version as CI |
| `uv run --frozen --with 'mypy==2.4.0' mypy --ignore-missing-imports .` | Type check, same as CI |
| `uvx ruff@0.16.10 format .` | Format (line length 100) |

## Invariants - do not break these

- **Chunking is token-based**: `RecursiveCharacterTextSplitter.from_tiktoken_encoder`
  with `cl100k_base`, `CHUNK_SIZE_TOKENS=1000`, `CHUNK_OVERLAP_TOKENS=200`.
  Do not switch to character counts.
- **Vector size is fixed by the embedding model** (`text-embedding-3-small` ->
  1536). Changing the model or dimensions requires `ingest --recreate`; the
  code checks for a mismatch and refuses to continue with a clear message.
- **The filesystem is the ingest ledger.** A successfully embedded PDF is
  renamed `name.pdf` -> `_name.pdf`. Never rename marked files back by hand
  unless you intend to re-ingest them.
- **Rename only after a successful upsert** (`mark_processed` runs after
  `upsert`, and skips files whose `stored_chunks` is 0). A failed file must
  remain unmarked so the next run retries it.
- **`--recreate` implies `--include-processed`** (implemented in
  `discover_node`). Without it, rebuilding would silently drop every PDF that
  had already been marked.
- **Point ids are deterministic**: `uuid5(collection:source:page:chunk_index)`.
  Re-ingest must overwrite, never duplicate.
- **Never answer without context**: the `no_context` branch exists to stop
  hallucinated answers. Keep the refusal in `prompts.NO_CONTEXT_ANSWER`.
- **No network calls at import or graph-compile time.** `WorkflowDeps` keeps
  clients lazy so `main.py graphs` works without Docker or an OpenAI key.
- **Graph diagrams are committed artifacts.** If you change a graph's nodes or
  edges, run `uv run python main.py graphs` and commit the `.png` and `.mmd`.

## Code map

| File | Responsibility |
| --- | --- |
| `main.py` | argparse CLI, printing, exit codes |
| `qdrant_rag/config.py` | `Settings` dataclass from env + `.env`, validation |
| `qdrant_rag/clients.py` | lazy Qdrant/OpenAI clients, collection creation, connectivity checks |
| `qdrant_rag/ingest_workflow.py` | workflow 1 (prepare -> discover -> per-file loop -> report) |
| `qdrant_rag/query_workflow.py` | workflow 2 (retrieve -> answer / no_context) |
| `qdrant_rag/prompts.py` | grounded-answer prompt and the no-context refusal |
| `qdrant_rag/graph_utils.py` | writes `<workflow>.png` and `.mmd` |
| `docker/docker-compose.yml` | Qdrant service, pinned image, `127.0.0.1` ports |

## Gotchas discovered the hard way

- **LangGraph introspects node closures at compile time.** `get_function_nonlocals`
  walks every `LOAD_ATTR` a node performs and calls `getattr` on it. A `@property`
  that creates a client therefore runs during `graph.compile()`, which is why
  `WorkflowDeps` exposes **methods** (`deps.store()`, `deps.chat()`), not
  properties. Do not turn them back into properties.
- **`QdrantVectorStore(...)` validates the collection on construction** and
  therefore needs a reachable server. Build it inside a node, never in
  `build_*_workflow`.
- **LangGraph's default recursion limit is 25.** A multi-file ingest would stop
  early, so `main.py` invokes with `recursion_limit=1000`.
- **`QdrantClient(check_compatibility=False)`** is deliberate: it avoids a
  background version-check thread (and a warning) when Qdrant is not running.
- **`draw_mermaid_png()` uses the mermaid.ink web service.** Normal runs only
  render the diagram when the `.png` is missing; `main.py graphs` forces a
  refresh and reports failures but still writes the `.mmd`.
- **Scanned PDFs yield no text**, so `load_and_chunk_node` raises
  "no extractable text" and leaves the file unmarked (visible in the summary).
- **`data/` is gitignored at the repo root**, so `data/pdfs/` is created at
  runtime and nothing inside it should ever be committed.

## Conventions

- One `StateGraph` + `TypedDict` state per workflow; nodes named `*_node` and
  wired explicitly with `START`/`END` (no hidden LCEL chains doing the flow).
- 4-space indentation, line length 100, ruff `select = ["E4", "E7", "E9", "F", "I"]`.
- Type hints everywhere; mypy runs with `--ignore-missing-imports` because some
  third-party packages ship no stubs.
- User-facing failures raise `RuntimeError`/`ValueError` with a concrete fix
  (exact command to run); `main()` turns those into `Error: ...` + exit 1.
- Keep README, `sample.env`, and `Settings` in sync when adding a setting.

## Environment

`sample.env` is the contract; `.env` is never committed. A relative `PDF_DIR`
resolves against the project root, not the current working directory.

## Repository workflow

- Branch: `feature/<ticket-id>-<your-id>-<ticket-title>` cut from `main`.
- CI (`/.github/workflows/lint.yml`) auto-discovers this project and runs ruff
  and mypy in it; no workflow edits needed.
- PR needs two approvals, then squash merge.
- `.env`, `data/`, and `docker/qdrant_storage/` must never be committed.
