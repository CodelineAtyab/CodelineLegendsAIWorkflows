"""Command line entry point for the two RAG workflows.

uv run python main.py ingest                 # PDFs -> Qdrant
uv run python main.py ingest --recreate      # rebuild the collection
uv run python main.py query "your question"  # Qdrant -> answer
uv run python main.py query --interactive
uv run python main.py graphs                 # refresh the workflow diagrams
"""

import argparse
import sys
from typing import Any, Sequence

from qdrant_rag.config import Settings, load_settings
from qdrant_rag.graph_utils import ensure_graph_artifacts, save_graph_artifacts
from qdrant_rag.ingest_workflow import (
    WORKFLOW_NAME as INGEST_WORKFLOW_NAME,
)
from qdrant_rag.ingest_workflow import (
    IngestOptions,
    build_ingest_workflow,
)
from qdrant_rag.query_workflow import (
    WORKFLOW_NAME as QUERY_WORKFLOW_NAME,
)
from qdrant_rag.query_workflow import build_query_workflow

# One PDF costs a handful of graph steps; the loop is bounded by the number of
# files, so a generous limit only prevents LangGraph's default of 25 from
# stopping a normal multi-file ingest.
INGEST_RECURSION_LIMIT = 1000


def ingest(settings: Settings, options: IngestOptions) -> int:
    workflow = build_ingest_workflow(settings, options)
    ensure_graph_artifacts(workflow, INGEST_WORKFLOW_NAME)

    result: dict[str, Any] = workflow.invoke(
        {},
        config={"recursion_limit": INGEST_RECURSION_LIMIT},
    )
    failed = result.get("failed") or []
    return 1 if failed else 0


def ask_once(settings: Settings, question: str, top_k: int | None) -> int:
    workflow = build_query_workflow(settings, top_k=top_k)
    ensure_graph_artifacts(workflow, QUERY_WORKFLOW_NAME)

    result: dict[str, Any] = workflow.invoke({"question": question})
    print_answer(result)
    return 0


def query(settings: Settings, question: str | None, top_k: int | None, interactive: bool) -> int:
    if not interactive and not question:
        print("Error: pass a question or use --interactive", file=sys.stderr)
        return 2

    if not interactive:
        return ask_once(settings, question or "", top_k)

    workflow = build_query_workflow(settings, top_k=top_k)
    ensure_graph_artifacts(workflow, QUERY_WORKFLOW_NAME)
    print("Interactive mode. Press Enter on an empty line to quit.")

    while True:
        try:
            typed = input("\nQuestion: ").strip()
        except EOFError, KeyboardInterrupt:
            print()
            return 0
        if not typed:
            return 0
        result: dict[str, Any] = workflow.invoke({"question": typed})
        print_answer(result)


def print_answer(result: dict[str, Any]) -> None:
    print("\nAnswer")
    print("------")
    print(result.get("answer", "").strip() or "(no answer)")

    sources = result.get("sources") or []
    if sources:
        print("\nSources")
        for source in sources:
            print(f"  - {source}")


def graphs(settings: Settings) -> int:
    print("Compiling workflows (no network calls needed)")
    ingest_workflow = build_ingest_workflow(settings)
    query_workflow = build_query_workflow(settings)

    for workflow, name in (
        (ingest_workflow, INGEST_WORKFLOW_NAME),
        (query_workflow, QUERY_WORKFLOW_NAME),
    ):
        png_path, mermaid_path = save_graph_artifacts(workflow, name)
        print(f"  {name}: {png_path.name}, {mermaid_path.name}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qdrant-rag-workflow",
        description=(
            "Two LangGraph demos over Qdrant: ingest PDFs, then answer questions from them."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser(
        "ingest",
        help="embed every unprocessed PDF in PDF_DIR into Qdrant",
    )
    ingest_parser.add_argument(
        "--recreate",
        action="store_true",
        help="drop and rebuild the collection (implies --include-processed)",
    )
    ingest_parser.add_argument(
        "--include-processed",
        action="store_true",
        help="also ingest files already renamed with a leading underscore",
    )

    query_parser = subparsers.add_parser(
        "query",
        help="answer a question from the ingested PDFs",
    )
    query_parser.add_argument("question", nargs="?", help="the customer question")
    query_parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="number of chunks to retrieve (default: RETRIEVAL_TOP_K)",
    )
    query_parser.add_argument(
        "--interactive",
        action="store_true",
        help="keep asking questions until an empty line is entered",
    )

    subparsers.add_parser("graphs", help="rewrite the workflow .png/.mmd files")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = load_settings()

    try:
        if args.command == "ingest":
            options = IngestOptions(
                recreate=args.recreate,
                include_processed=args.include_processed,
            )
            return ingest(settings, options)
        if args.command == "query":
            return query(settings, args.question, args.top_k, args.interactive)
        return graphs(settings)
    except (RuntimeError, ValueError) as error:
        print(f"\nError: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
