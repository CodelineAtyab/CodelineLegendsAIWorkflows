from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class RetrievalState(TypedDict):
    question: str
    documents: list[str]
    context: str
    searched: bool
    answer: str


def answer_question(state: RetrievalState) -> RetrievalState:
    if state["searched"]:
        if state["context"]:
            state["answer"] = state["context"]
        else:
            state["answer"] = "No matching document."
    return state


def choose_next(state: RetrievalState) -> str:
    if state["searched"]:
        return "finish"
    return "search"


def search_documents(state: RetrievalState) -> RetrievalState:
    matches = []
    for document in state["documents"]:
        if state["question"].lower() in document.lower():
            matches.append(document)
    state["context"] = "\n".join(matches)
    state["searched"] = True
    return state


graph = StateGraph(RetrievalState)
graph.add_node("answer_question", answer_question)
graph.add_node("search_documents", search_documents)

graph.add_edge(START, "answer_question")
graph.add_conditional_edges(
    "answer_question", choose_next,
    {"search": "search_documents", "finish": END},
)
graph.add_edge("search_documents", "answer_question")

workflow = graph.compile()

documents = [
    "LangGraph connects processing steps using nodes and edges.",
    "TypedDict describes the keys and value types in a dictionary.",
]

for question in ["LangGraph", "unknown"]:
    print(workflow.invoke({
        "question": question,
        "documents": documents,
        "context": "",
        "searched": False,
        "answer": "",
    }))

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
