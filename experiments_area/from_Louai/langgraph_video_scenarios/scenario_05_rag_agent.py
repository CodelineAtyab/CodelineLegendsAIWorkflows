from pathlib import Path
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class RagState(TypedDict):
    question: str
    keyword: str
    documents: list[str]
    searched: bool
    retrieved: list[str]
    answer: str


def call_llm(state: RagState) -> RagState:
    if state["searched"] and state["retrieved"]:
        state["answer"] = " ".join(state["retrieved"])
    elif state["searched"]:
        state["answer"] = "I found no relevant information in the document."
    return state


def retrieve(state: RagState) -> RagState:
    for chunk in state["documents"]:
        if state["keyword"] in chunk.lower():
            state["retrieved"].append(chunk)
    state["searched"] = True
    return state


def should_search(state: RagState) -> str:
    if state["searched"]:
        return "finish"
    return "search"


graph = StateGraph(RagState)
graph.add_node("llm_node", call_llm)
graph.add_node("retriever_node", retrieve)
graph.add_edge(START, "llm_node")
graph.add_conditional_edges("llm_node", should_search, {"search": "retriever_node", "finish": END})
graph.add_edge("retriever_node", "llm_node")

workflow = graph.compile()

documents = [
    "LangGraph uses a shared state that every node can read and write.",
    "Conditional edges pick the next node using a decider function.",
    "A loop happens when an edge points back to an earlier node.",
]

print(workflow.invoke({"question": "What is a conditional edge?", "keyword": "conditional", "documents": documents, "searched": False, "retrieved": [], "answer": ""}))
print(workflow.invoke({"question": "What is Docker?", "keyword": "docker", "documents": documents, "searched": False, "retrieved": [], "answer": ""}))

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")