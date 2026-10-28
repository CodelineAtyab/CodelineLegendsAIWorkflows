from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ToolState(TypedDict):
    number1: int
    number2: int
    operation: str
    next_operation: str
    next_number: int
    result: int
    reply: str


def decide_action(state: ToolState) -> ToolState:
    return state


def choose_next(state: ToolState) -> str:
    if state["operation"] == "finish":
        return "finish"
    return "calculate"


def calculate(state: ToolState) -> ToolState:
    if state["operation"] == "add":
        state["result"] = state["number1"] + state["number2"]
    elif state["operation"] == "subtract":
        state["result"] = state["number1"] - state["number2"]
    elif state["operation"] == "multiply":
        state["result"] = state["number1"] * state["number2"]

    state["reply"] = "The result is " + str(state["result"])
    state["number1"] = state["result"]
    state["number2"] = state["next_number"]
    state["operation"] = state["next_operation"]
    state["next_operation"] = "finish"
    return state


graph = StateGraph(ToolState)
graph.add_node("decide_action", decide_action)
graph.add_node("calculate", calculate)

graph.add_edge(START, "decide_action")
graph.add_conditional_edges(
    "decide_action", choose_next, {"calculate": "calculate", "finish": END}
)
graph.add_edge("calculate", "decide_action")

workflow = graph.compile()

print(
    workflow.invoke(
        {
            "number1": 10,
            "number2": 4,
            "operation": "add",
            "next_operation": "finish",
            "next_number": 0,
            "result": 0,
            "reply": "",
        }
    )
)

print(
    workflow.invoke(
        {
            "number1": 10,
            "number2": 5,
            "operation": "add",
            "next_operation": "add",
            "next_number": 3,
            "result": 0,
            "reply": "",
        }
    )
)

print(
    workflow.invoke(
        {
            "number1": 40,
            "number2": 12,
            "operation": "add",
            "next_operation": "multiply",
            "next_number": 6,
            "result": 0,
            "reply": "",
        }
    )
)

print(
    workflow.invoke(
        {
            "number1": 10,
            "number2": 3,
            "operation": "subtract",
            "next_operation": "finish",
            "next_number": 0,
            "result": 0,
            "reply": "",
        }
    )
)

print(
    workflow.invoke(
        {
            "number1": 0,
            "number2": 0,
            "operation": "finish",
            "next_operation": "finish",
            "next_number": 0,
            "result": 0,
            "reply": "Hello! No calculation was requested.",
        }
    )
)

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
