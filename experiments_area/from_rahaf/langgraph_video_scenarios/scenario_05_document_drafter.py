from pathlib import Path
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class DrafterState(TypedDict):
    draft: str
    feedback: list[str]
    feedback_index: int
    pending_feedback: str
    next_action: Literal["revise", "save"]
    output_path: str
    saved: bool
    saved_path: str


def choose_drafter_action(state: DrafterState) -> DrafterState:
    if state["feedback_index"] >= len(state["feedback"]):
        state["pending_feedback"] = ""
        state["next_action"] = "save"
        return state

    feedback = state["feedback"][state["feedback_index"]]
    state["pending_feedback"] = feedback
    save_phrases = ("save", "looks good", "approved")
    state["next_action"] = (
        "save"
        if any(phrase in feedback.casefold() for phrase in save_phrases)
        else "revise"
    )
    return state


def apply_draft_feedback(state: DrafterState) -> DrafterState:
    state["draft"] += f"\n\nRevision requested: {state['pending_feedback']}"
    state["feedback_index"] += 1
    return state


def save_draft(state: DrafterState) -> DrafterState:
    output_path = Path(state["output_path"])
    output_path.write_text(state["draft"] + "\n", encoding="utf-8")
    state["saved"] = True
    state["saved_path"] = str(output_path)
    return state


def route_drafter_action(state: DrafterState) -> str:
    return state["next_action"]


graph = StateGraph(DrafterState)
graph.add_node("choose_drafter_action", choose_drafter_action)
graph.add_node("apply_draft_feedback", apply_draft_feedback)
graph.add_node("save_draft", save_draft)
graph.add_edge(START, "choose_drafter_action")
graph.add_conditional_edges(
    "choose_drafter_action",
    route_drafter_action,
    {"revise": "apply_draft_feedback", "save": "save_draft"},
)
graph.add_edge("apply_draft_feedback", "choose_drafter_action")
graph.add_edge("save_draft", END)

workflow = graph.compile()
result = workflow.invoke(
    {
        "draft": "Hello team, our project is progressing.",
        "feedback": [
            "Add a sentence saying the first review is due Friday.",
            "Looks good; save this draft.",
        ],
        "feedback_index": 0,
        "pending_feedback": "",
        "next_action": "revise",
        "output_path": str(Path(__file__).with_name("draft_output.txt")),
        "saved": False,
        "saved_path": "",
    }
)
print(result)

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(
    workflow.get_graph().draw_mermaid_png(max_retries=5, retry_delay=2.0)
)
print(f"Graph saved to {png_path}")
