from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class RetrievalState(TypedDict):
    query: str
    documents: list[str]
    context: str
    retrieval_done: bool
    answer: str


def prepare_answer(state: RetrievalState) -> RetrievalState:
    if state["retrieval_done"]:
        state["answer"] = state["context"] or "No matching document."
    return state


def choose_next(state: RetrievalState) -> str:
    if state["retrieval_done"]:
        return "finish"
    return "retrieve"


def retrieve(state: RetrievalState) -> RetrievalState:
    matching_documents = []
    for document in state["documents"]:
        if state["query"].lower() in document.lower():
            matching_documents.append(document)
    state["context"] = "\n".join(matching_documents)
    state["retrieval_done"] = True
    return state


graph = StateGraph(RetrievalState)
graph.add_node("prepare_answer", prepare_answer)
graph.add_node("retrieve", retrieve)
graph.add_edge(START, "prepare_answer")
graph.add_conditional_edges(
    "prepare_answer", choose_next, {"retrieve": "retrieve", "finish": END}
)
graph.add_edge("retrieve", "prepare_answer")
workflow = graph.compile()

documents = [
    "LangGraph connects processing steps using nodes and edges.",
    "TypedDict describes the keys and value types expected in a dictionary.",
]
for query in ["LangGraph", "unknown"]:
    print(workflow.invoke({
        "query": query,
        "documents": documents,
        "context": "",
        "retrieval_done": False,
        "answer": "",
    }))

Path(__file__).with_suffix(".png").write_bytes(workflow.get_graph().draw_mermaid_png())
