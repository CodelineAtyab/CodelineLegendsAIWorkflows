import re
from pathlib import Path
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class SourceDocument(TypedDict):
    title: str
    content: str


class RagState(TypedDict):
    question: str
    documents: list[SourceDocument]
    retrieved_documents: list[SourceDocument]
    retrieval_done: bool
    next_step: Literal["retrieve", "answer"]
    answer: str


STOP_WORDS = {
    "a",
    "an",
    "and",
    "according",
    "did",
    "for",
    "how",
    "in",
    "is",
    "of",
    "on",
    "the",
    "to",
    "was",
    "what",
    "2024",
}


def choose_rag_step(state: RagState) -> RagState:
    state["next_step"] = "answer" if state["retrieval_done"] else "retrieve"
    return state


def retrieve_relevant_documents(state: RagState) -> RagState:
    query_terms = {
        term
        for term in re.findall(r"[a-z0-9]+", state["question"].casefold())
        if term not in STOP_WORDS
    }
    ranked_documents: list[tuple[int, SourceDocument]] = []

    for document in state["documents"]:
        document_terms = set(
            re.findall(
                r"[a-z0-9]+", f"{document['title']} {document['content']}".casefold()
            )
        )
        overlap = len(query_terms & document_terms)
        if overlap:
            ranked_documents.append((overlap, document))

    ranked_documents.sort(key=lambda item: item[0], reverse=True)
    state["retrieved_documents"] = [document for _, document in ranked_documents[:3]]
    state["retrieval_done"] = True
    return state


def compose_answer_from_sources(state: RagState) -> RagState:
    if not state["retrieved_documents"]:
        state["answer"] = "No matching passage was found in the local report."
    else:
        passages = " ".join(
            document["content"] for document in state["retrieved_documents"]
        )
        state["answer"] = f"Based on the local report: {passages}"
    return state


def route_rag_step(state: RagState) -> str:
    return state["next_step"]


graph = StateGraph(RagState)
graph.add_node("choose_rag_step", choose_rag_step)
graph.add_node("retrieve_relevant_documents", retrieve_relevant_documents)
graph.add_node("compose_answer_from_sources", compose_answer_from_sources)
graph.add_edge(START, "choose_rag_step")
graph.add_conditional_edges(
    "choose_rag_step",
    route_rag_step,
    {
        "retrieve": "retrieve_relevant_documents",
        "answer": "compose_answer_from_sources",
    },
)
graph.add_edge("retrieve_relevant_documents", "choose_rag_step")
graph.add_edge("compose_answer_from_sources", END)

workflow = graph.compile()
sample_documents: list[SourceDocument] = [
    {
        "title": "2024 market summary",
        "content": "The S&P 500 total return for 2024 was 25.02%.",
    },
    {
        "title": "Technology sector summary",
        "content": "The information technology sector returned 36.6% in 2024.",
    },
]

for question in (
    "What was the S&P 500 total return in 2024?",
    "What was the rainfall in Sydney in 2024?",
):
    result = workflow.invoke(
        {
            "question": question,
            "documents": sample_documents,
            "retrieved_documents": [],
            "retrieval_done": False,
            "next_step": "retrieve",
            "answer": "",
        }
    )
    print(result)

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(
    workflow.get_graph().draw_mermaid_png(max_retries=5, retry_delay=2.0)
)
print(f"Graph saved to {png_path}")
