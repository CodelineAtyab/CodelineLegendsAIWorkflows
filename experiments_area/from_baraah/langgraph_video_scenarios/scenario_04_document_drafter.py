
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    topic: str
    feedback: str
    draft: str
    status: str


def create_draft(state: State) -> dict:
    return {
        "draft": f"Document about {state['topic']}."
    }


def choose_revision(state: State) -> str:
    if state["feedback"].strip():
        return "revise"

    return "finish"


def revise_draft(state: State) -> dict:
    return {
        "draft": state["draft"] + " " + state["feedback"],
        "status": "revised",
    }


def finalize_draft(state: State) -> dict:
    return {"status": "complete"}


builder = StateGraph(State)

builder.add_node("create_draft", create_draft)
builder.add_node("revise_draft", revise_draft)
builder.add_node("finalize_draft", finalize_draft)

builder.add_edge(START, "create_draft")

builder.add_conditional_edges(
    "create_draft",
    choose_revision,
    {
        "revise": "revise_draft",
        "finish": "finalize_draft",
    },
)

builder.add_edge("revise_draft", "finalize_draft")
builder.add_edge("finalize_draft", END)

workflow = builder.compile()


if __name__ == "__main__":
    result1 = workflow.invoke({
        "topic": "Python",
        "feedback": "",
        "draft": "",
        "status": "",
    })
    print(result1)

    result2 = workflow.invoke({
        "topic": "Python",
        "feedback": "Add an example.",
        "draft": "",
        "status": "",
    })
    print(result2)

    image = workflow.get_graph().draw_mermaid_png()
    Path(__file__).with_suffix(".png").write_bytes(image)
