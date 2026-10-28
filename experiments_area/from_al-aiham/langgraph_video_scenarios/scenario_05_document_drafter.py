from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class DraftState(TypedDict):
    drafts: list[str]
    draft_index: int
    document: str
    filename: str
    saved: bool


def decide_action(state: DraftState) -> DraftState:
    return state


def choose_next(state: DraftState) -> str:
    if state["draft_index"] < len(state["drafts"]):
        return "update"
    return "save"


def update_document(state: DraftState) -> DraftState:
    state["document"] = state["drafts"][state["draft_index"]]
    state["draft_index"] += 1
    return state


def save_document(state: DraftState) -> DraftState:
    with open(state["filename"], "w", encoding="utf-8") as file:
        file.write(state["document"])
    state["saved"] = True
    return state


graph = StateGraph(DraftState)
graph.add_node("decide_action", decide_action)
graph.add_node("update_document", update_document)
graph.add_node("save_document", save_document)

graph.add_edge(START, "decide_action")
graph.add_conditional_edges(
    "decide_action",
    choose_next,
    {"update": "update_document", "save": "save_document"},
)
graph.add_edge("update_document", "decide_action")
graph.add_edge("save_document", END)

workflow = graph.compile()

print(
    workflow.invoke(
        {
            "drafts": [
                "I cannot attend the meeting today.",
                "I cannot attend today. Please share the meeting notes.",
            ],
            "draft_index": 0,
            "document": "",
            "filename": str(Path(__file__).with_name("draft_one.txt")),
            "saved": False,
        }
    )
)

print(
    workflow.invoke(
        {
            "drafts": [],
            "draft_index": 0,
            "document": "This document is ready to save.",
            "filename": str(Path(__file__).with_name("draft_two.txt")),
            "saved": False,
        }
    )
)

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
