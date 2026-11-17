from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class RAGState(TypedDict):
    question: str
    documents: list[str]
    context: str
    answer: str


def retrieve_documents(state: RAGState) -> RAGState:
    """Find sample documents related to the question."""
    common_words = {
        "what",
        "is",
        "a",
        "an",
        "the",
        "of",
        "in",
        "to",
        "for",
        "and",
        "does",
        "how",
    }

    question_words = [
        word.strip("?!.,").lower()
        for word in state["question"].split()
        if word.strip("?!.,").lower() not in common_words
    ]

    matches = [
        document
        for document in state["documents"]
        if any(word in document.lower() for word in question_words)
    ]

    state["context"] = " ".join(matches)
    return state


def generate_answer(state: RAGState) -> RAGState:
    """Create a simple answer using the retrieved context."""
    if state["context"]:
        state["answer"] = state["context"]
    else:
        state["answer"] = "No relevant information found."

    return state


builder = StateGraph(RAGState)

builder.add_node("retrieve_documents", retrieve_documents)
builder.add_node("generate_answer", generate_answer)

builder.add_edge(START, "retrieve_documents")
builder.add_edge("retrieve_documents", "generate_answer")
builder.add_edge("generate_answer", END)

workflow = builder.compile()

result = workflow.invoke(
    {
        "question": "What is LangGraph?",
        "documents": [
            "LangGraph helps build stateful AI workflows.",
            "Python is a programming language.",
        ],
        "context": "",
        "answer": "",
    }
)

print(result)

diagram = workflow.get_graph().draw_mermaid_png()
Path(__file__).with_suffix(".png").write_bytes(diagram)
