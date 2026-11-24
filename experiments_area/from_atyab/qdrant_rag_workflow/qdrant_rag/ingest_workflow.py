"""Workflow 1: PDF files -> text chunks -> OpenAI embeddings -> Qdrant.

The filesystem doubles as the progress ledger. A PDF that was embedded
successfully is renamed with a leading underscore (`report.pdf` ->
`_report.pdf`), so the next run skips it. Files that fail stay untouched and
are retried next time.

Graph shape:

    prepare_collection -> discover -> next_file -+-> load_and_chunk -> upsert
         ^                                    |            |
         |                                    |            v
         +------------------------------------+----- mark_processed
                                              |
                                              +-> report -> END
"""

import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from pypdf import PdfReader

from qdrant_rag.clients import WorkflowDeps
from qdrant_rag.config import Settings

WORKFLOW_NAME = "ingest_workflow"
PROCESSED_PREFIX = "_"


class IngestState(TypedDict, total=False):
    pending: list[Path]
    current: Path | None
    chunks: list[Document]
    stored_chunks: int
    processed: list[str]
    failed: list[str]
    skipped: int
    total_pdfs: int
    chunks_written: int


@dataclass(frozen=True)
class IngestOptions:
    recreate: bool = False
    include_processed: bool = False


def _processed_name(path: Path) -> Path:
    """`report.pdf` -> `_report.pdf`, avoiding collisions with existing names."""
    target = path.with_name(PROCESSED_PREFIX + path.name)
    if not target.exists():
        return target

    index = 1
    while True:
        candidate = path.with_name(f"{PROCESSED_PREFIX}{path.stem}-{index}{path.suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def _point_id(collection: str, chunk: Document) -> str:
    """Deterministic id, so re-ingesting the same chunk overwrites instead of duplicating."""
    metadata = chunk.metadata
    key = "{}:{}:{}:{}".format(
        collection,
        metadata.get("source", "unknown"),
        metadata.get("page", 0),
        metadata.get("chunk_index", 0),
    )
    return str(uuid.uuid5(uuid.NAMESPACE_URL, key))


def build_ingest_workflow(
    settings: Settings,
    options: IngestOptions | None = None,
) -> CompiledStateGraph:
    """Compile workflow 1. No network calls happen until it is invoked."""
    options = options or IngestOptions()
    deps = WorkflowDeps(settings)

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=settings.chunk_size_tokens,
        chunk_overlap=settings.chunk_overlap_tokens,
        add_start_index=True,
    )

    def prepare_collection_node(state: IngestState) -> dict[str, object]:
        deps.ping()
        deps.ensure_collection(recreate=options.recreate)
        return {}

    def discover_node(state: IngestState) -> dict[str, object]:
        directory = settings.pdf_dir
        directory.mkdir(parents=True, exist_ok=True)

        all_pdfs = sorted(path for path in directory.glob("*.pdf") if path.is_file())
        # Rebuilding the collection must re-read the files already marked with
        # an underscore, otherwise "reset the database" would silently lose them.
        include_processed = options.include_processed or options.recreate
        if include_processed:
            pending = all_pdfs
        else:
            pending = [path for path in all_pdfs if not path.name.startswith(PROCESSED_PREFIX)]
        skipped = len(all_pdfs) - len(pending)

        print(f"\nIngest from {directory}")
        print(
            f"  found {len(all_pdfs)} PDF(s), {len(pending)} to process, {skipped} already marked"
        )
        return {
            "pending": pending,
            "total_pdfs": len(all_pdfs),
            "skipped": skipped,
            "processed": [],
            "failed": [],
            "chunks_written": 0,
            "chunks": [],
            "current": None,
            "stored_chunks": 0,
        }

    def next_file_node(state: IngestState) -> dict[str, object]:
        pending = state.get("pending") or []
        if not pending:
            return {"current": None, "chunks": [], "stored_chunks": 0}

        current, remaining = pending[0], pending[1:]
        position = (state.get("total_pdfs") or 0) - len(remaining)
        print(f"\n[{position}] {current.name}")
        return {
            "pending": remaining,
            "current": current,
            "chunks": [],
            "stored_chunks": 0,
        }

    def load_and_chunk_node(state: IngestState) -> dict[str, object]:
        current = state.get("current")
        if current is None:
            return {}

        try:
            reader = PdfReader(str(current))
            total_pages = len(reader.pages)
            pages: list[Document] = []
            for page_number, page in enumerate(reader.pages, start=1):
                text = (page.extract_text() or "").strip()
                if not text:
                    continue
                pages.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": current.name,
                            "page": page_number,
                            "total_pages": total_pages,
                        },
                    )
                )

            if not pages:
                raise ValueError("no extractable text (is it a scanned PDF?)")

            chunks: list[Document] = []
            for page_document in pages:
                page_chunks = splitter.split_documents([page_document])
                for chunk_index, chunk in enumerate(page_chunks):
                    chunk.metadata["chunk_index"] = chunk_index
                chunks.extend(page_chunks)
        except Exception as error:  # noqa: BLE001 - one bad PDF must not stop the batch
            failure = f"{current.name}: {error}"
            print(f"  ! {failure}")
            return {
                "failed": [*(state.get("failed") or []), failure],
                "chunks": [],
                "stored_chunks": 0,
                "current": None,
            }

        print(f"  {len(pages)} page(s) -> {len(chunks)} chunk(s)")
        return {"chunks": chunks}

    def upsert_node(state: IngestState) -> dict[str, object]:
        current = state.get("current")
        chunks = state.get("chunks") or []
        if current is None or not chunks:
            return {"stored_chunks": 0}

        ids = [_point_id(settings.collection_name, chunk) for chunk in chunks]
        try:
            deps.store().add_documents(chunks, ids=ids)
        except Exception as error:  # noqa: BLE001 - reported per file, batch continues
            failure = f"{current.name}: embedding/upsert failed ({error})"
            print(f"  ! {failure}")
            return {
                "failed": [*(state.get("failed") or []), failure],
                "stored_chunks": 0,
            }

        stored = len(chunks)
        print(f"  stored {stored} chunk(s) in {settings.collection_name!r}")
        return {
            "stored_chunks": stored,
            "chunks_written": (state.get("chunks_written") or 0) + stored,
        }

    def mark_processed_node(state: IngestState) -> dict[str, object]:
        current = state.get("current")
        if current is None or (state.get("stored_chunks") or 0) == 0:
            return {}

        # Files pulled in by --include-processed are already marked; renaming
        # them again would pile up `_file-1.pdf`, `_file-2.pdf`, ...
        if current.name.startswith(PROCESSED_PREFIX):
            print("  already marked, name left as is")
            return {
                "processed": [*(state.get("processed") or []), current.name],
                "current": None,
            }

        try:
            target = _processed_name(current)
            current.rename(target)
        except OSError as error:
            # Chunks are already stored, so the deterministic ids make a retry safe.
            failure = f"{current.name}: stored but could not be marked ({error})"
            print(f"  ! {failure}")
            return {
                "failed": [*(state.get("failed") or []), failure],
                "current": None,
            }

        print(f"  marked as {target.name}")
        return {
            "processed": [*(state.get("processed") or []), target.name],
            "current": None,
        }

    def report_node(state: IngestState) -> dict[str, object]:
        processed = state.get("processed") or []
        failed = state.get("failed") or []
        skipped = state.get("skipped") or 0
        chunks_written = state.get("chunks_written") or 0

        print("\nIngest summary")
        print(f"  processed: {len(processed)} PDF(s), {chunks_written} chunk(s)")
        print(f"  skipped (already marked): {skipped}")
        print(f"  failed: {len(failed)}")
        for failure in failed:
            print(f"    - {failure}")
        if failed:
            print("  failed files were left unmarked and will be retried next run")
        print(f"  collection: {settings.collection_name!r} at {settings.qdrant_url}")
        return {}

    def route_after_next_file(state: IngestState) -> str:
        return "load_and_chunk" if state.get("current") is not None else "report"

    graph = StateGraph(IngestState)
    graph.add_node("prepare_collection", prepare_collection_node)
    graph.add_node("discover", discover_node)
    graph.add_node("next_file", next_file_node)
    graph.add_node("load_and_chunk", load_and_chunk_node)
    graph.add_node("upsert", upsert_node)
    graph.add_node("mark_processed", mark_processed_node)
    graph.add_node("report", report_node)

    graph.add_edge(START, "prepare_collection")
    graph.add_edge("prepare_collection", "discover")
    graph.add_edge("discover", "next_file")
    graph.add_conditional_edges(
        "next_file",
        route_after_next_file,
        {"load_and_chunk": "load_and_chunk", "report": "report"},
    )
    graph.add_edge("load_and_chunk", "upsert")
    graph.add_edge("upsert", "mark_processed")
    graph.add_edge("mark_processed", "next_file")
    graph.add_edge("report", END)

    return graph.compile()
