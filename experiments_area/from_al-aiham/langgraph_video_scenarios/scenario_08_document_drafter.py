from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class DraftState(TypedDict):
    actions: list[dict[str, str]]
    action_index: int
    action: str
    document: str
    filename: str
    saved: bool


def select_action(state: DraftState) -> DraftState:
    state["action"] = state["actions"][state["action_index"]]["action"]
    return state


def choose_next(state: DraftState) -> str:
    return state["action"]


def update_document(state: DraftState) -> DraftState:
    action = state["actions"][state["action_index"]]
    state["document"] = action["content"]
    state["action_index"] += 1
    return state


def save_document(state: DraftState) -> DraftState:
    if not state["filename"].endswith(".txt"):
        state["filename"] += ".txt"
    Path(state["filename"]).write_text(state["document"], encoding="utf-8")
    state["saved"] = True
    return state


graph = StateGraph(DraftState)
graph.add_node("select_action", select_action)
graph.add_node("update_document", update_document)
graph.add_node("save_document", save_document)
graph.add_edge(START, "select_action")
graph.add_conditional_edges(
    "select_action",
    choose_next,
    {"update": "update_document", "save": "save_document"},
)
graph.add_edge("update_document", "select_action")
graph.add_edge("save_document", END)
workflow = graph.compile()

print(workflow.invoke({
    "actions": [
        {"action": "update", "content": "I cannot attend the meeting today."},
        {"action": "update", "content": "I cannot attend today. Please share the notes."},
        {"action": "save"},
    ],
    "action_index": 0,
    "action": "",
    "document": "",
    "filename": str(Path(__file__).with_name("draft_one")),
    "saved": False,
}))
print(workflow.invoke({
    "actions": [{"action": "save"}],
    "action_index": 0,
    "action": "",
    "document": "This document is already ready to save.",
    "filename": str(Path(__file__).with_name("draft_two.txt")),
    "saved": False,
}))

Path(__file__).with_suffix(".png").write_bytes(workflow.get_graph().draw_mermaid_png())
