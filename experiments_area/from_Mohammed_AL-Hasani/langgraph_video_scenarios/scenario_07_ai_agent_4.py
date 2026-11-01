from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class DraftState(TypedDict):
    topic: str
    draft: str
    feedback: str
    revision_count: int
    saved: bool


def write_draft(state: DraftState) -> DraftState:
    """Create the first draft."""
    state["draft"] = f"This is a first draft about {state['topic']}."
    state["feedback"] = ""
    state["revision_count"] = 0
    state["saved"] = False
    return state


def review_draft(state: DraftState) -> DraftState:
    """Review the draft and provide feedback."""
    if state["revision_count"] == 0:
        state["feedback"] = "Add more detail."
    else:
        state["feedback"] = "The draft is ready."
    return state


def revise_draft(state: DraftState) -> DraftState:
    """Improve the draft using the review feedback."""
    state["draft"] += " It explains the topic in more detail."
    state["revision_count"] += 1
    return state


def choose_next_step(state: DraftState) -> str:
    """Decide whether the draft needs revision or can be saved."""
    if state["feedback"] == "Add more detail.":
        return "revise_draft"

    return "save_draft"


def save_draft(state: DraftState) -> DraftState:
    """Mark the finished draft as saved."""
    state["saved"] = True
    return state


builder = StateGraph(DraftState)

builder.add_node("write_draft", write_draft)
builder.add_node("review_draft", review_draft)
builder.add_node("revise_draft", revise_draft)
builder.add_node("save_draft", save_draft)

builder.add_edge(START, "write_draft")
builder.add_edge("write_draft", "review_draft")
builder.add_conditional_edges(
    "review_draft",
    choose_next_step,
    {
        "revise_draft": "revise_draft",
        "save_draft": "save_draft",
    },
)
builder.add_edge("revise_draft", "review_draft")
builder.add_edge("save_draft", END)

workflow = builder.compile()

result = workflow.invoke(
    {
        "topic": "LangGraph",
        "draft": "",
        "feedback": "",
        "revision_count": 0,
        "saved": False,
    }
)

print(result)

diagram = workflow.get_graph().draw_mermaid_png()
Path(__file__).with_suffix(".png").write_bytes(diagram)
