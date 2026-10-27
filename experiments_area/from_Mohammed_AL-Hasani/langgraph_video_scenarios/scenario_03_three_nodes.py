from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ScenarioState(TypedDict):
    message: str


def first_node(state: ScenarioState) -> ScenarioState:
    """Perform the first step."""
    return {
        **state,
        "message": state["message"].strip(),
    }


def second_node(state: ScenarioState) -> ScenarioState:
    """Perform the next step."""
    return {
        **state,
        "message": state["message"].upper(),
    }


builder = StateGraph(ScenarioState)

builder.add_node("first_node", first_node)
builder.add_node("second_node", second_node)

builder.add_edge(START, "first_node")
builder.add_edge("first_node", "second_node")
builder.add_edge("second_node", END)

workflow = builder.compile()

result = workflow.invoke({"message": "hello"})
print(result)

diagram = workflow.get_graph().draw_mermaid_png()
Path(__file__).with_suffix(".png").write_bytes(diagram)
