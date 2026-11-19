"""Workflow 2: customer question -> Qdrant retrieval -> grounded answer.

Graph shape:

    retrieve -+-> answer -> END          (chunks found)
              |
              +-> no_context -> END      (nothing relevant in the knowledge base)
"""

from typing import TypedDict

from langchain_core.documents import Document
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from qdrant_rag.clients import WorkflowDeps
from qdrant_rag.config import Settings
from qdrant_rag.prompts import ANSWER_PROMPT, NO_CONTEXT_ANSWER

WORKFLOW_NAME = "query_workflow"


class QueryState(TypedDict, total=False):
    question: str
    top_k: int
    documents: list[Document]
    scores: list[float]
    answer: str
    sources: list[str]


def _source_label(document: Document) -> str:
    source = document.metadata.get("source", "unknown")
    page = document.metadata.get("page")
    return f"{source} p.{page}" if page is not None else str(source)


def _format_context(documents: list[Document]) -> str:
    passages = []
    for index, document in enumerate(documents, start=1):
        passages.append(f"[{index}] {_source_label(document)}\n{document.page_content.strip()}")
    return "\n\n".join(passages)


def build_query_workflow(
    settings: Settings,
    *,
    top_k: int | None = None,
) -> CompiledStateGraph:
    """Compile workflow 2. No network calls happen until it is invoked."""
    deps = WorkflowDeps(settings)
    retrieval_k = top_k or settings.retrieval_top_k

    def retrieve_node(state: QueryState) -> dict[str, object]:
        question = state.get("question", "")
        # Fail with the real reason (missing key, Qdrant down) before wrapping
        # search errors; QdrantVectorStore also validates the collection on init.
        settings.require_openai_key()
        deps.ping()
        try:
            hits = deps.store().similarity_search_with_score(
                question,
                k=retrieval_k,
                score_threshold=settings.retrieval_score_threshold,
            )
        except Exception as error:  # noqa: BLE001 - surfaced with hints below
            raise RuntimeError(
                f"Could not search collection {settings.collection_name!r} at "
                f"{settings.qdrant_url}.\n"
                "Has the ingest workflow run (uv run python main.py ingest)?\n"
                f"Underlying error: {error}"
            ) from error

        documents = [document for document, _score in hits]
        scores = [score for _document, score in hits]
        print(f"\nRetrieved {len(documents)} chunk(s) for: {question!r}")
        for document, score in hits:
            print(f"  {score:.3f}  {_source_label(document)}")
        return {"documents": documents, "scores": scores, "top_k": retrieval_k}

    def answer_node(state: QueryState) -> dict[str, object]:
        documents = state.get("documents") or []
        question = state.get("question", "")

        messages = ANSWER_PROMPT.format_messages(
            context=_format_context(documents),
            question=question,
        )
        response = deps.chat().invoke(messages)

        sources: list[str] = []
        for document in documents:
            label = _source_label(document)
            if label not in sources:
                sources.append(label)

        return {"answer": response.text.strip(), "sources": sources}

    def no_context_node(state: QueryState) -> dict[str, object]:
        return {"answer": NO_CONTEXT_ANSWER, "sources": []}

    def route_after_retrieve(state: QueryState) -> str:
        return "answer" if state.get("documents") else "no_context"

    graph = StateGraph(QueryState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("answer", answer_node)
    graph.add_node("no_context", no_context_node)

    graph.add_edge(START, "retrieve")
    graph.add_conditional_edges(
        "retrieve",
        route_after_retrieve,
        {"answer": "answer", "no_context": "no_context"},
    )
    graph.add_edge("answer", END)
    graph.add_edge("no_context", END)

    return graph.compile()
