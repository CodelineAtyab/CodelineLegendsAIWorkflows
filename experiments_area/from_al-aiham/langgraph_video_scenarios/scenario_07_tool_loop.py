from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ToolState(TypedDict):
    steps: list[dict]
    step_index: int
    result: int
    answer: str


def decide_action(state: ToolState) -> ToolState:
    if state["step_index"] == len(state["steps"]) and state["steps"]:
        state["answer"] = f"{state['result']} {state['answer']}".strip()
    return state


def choose_next(state: ToolState) -> str:
    if state["step_index"] < len(state["steps"]):
        return "tool"
    return "finish"


def execute_tool(state: ToolState) -> ToolState:
    step = state["steps"][state["step_index"]]
    left = state["result"] if step["left"] is None else step["left"]
    right = step["right"]

    if step["operation"] == "add":
        state["result"] = left + right
    elif step["operation"] == "subtract":
        state["result"] = left - right
    elif step["operation"] == "multiply":
        state["result"] = left * right

    state["step_index"] += 1
    return state


graph = StateGraph(ToolState)
graph.add_node("decide_action", decide_action)
graph.add_node("execute_tool", execute_tool)
graph.add_edge(START, "decide_action")
graph.add_conditional_edges(
    "decide_action", choose_next, {"tool": "execute_tool", "finish": END}
)
graph.add_edge("execute_tool", "decide_action")
workflow = graph.compile()

print(workflow.invoke({
    "steps": [{"operation": "add", "left": 10, "right": 4}],
    "step_index": 0,
    "result": 0,
    "answer": "",
}))

print(workflow.invoke({
    "steps": [
        {"operation": "add", "left": 10, "right": 5},
        {"operation": "add", "left": None, "right": 3},
    ],
    "step_index": 0,
    "result": 0,
    "answer": "",
}))

print(workflow.invoke({
    "steps": [
        {"operation": "add", "left": 40, "right": 12},
        {"operation": "multiply", "left": None, "right": 6},
    ],
    "step_index": 0,
    "result": 0,
    "answer": "Canned joke: the computer was cold because it left its Windows open.",
}))

print(workflow.invoke({
    "steps": [{"operation": "subtract", "left": 10, "right": 3}],
    "step_index": 0,
    "result": 0,
    "answer": "",
}))

print(workflow.invoke({
    "steps": [],
    "step_index": 0,
    "result": 0,
    "answer": "Hello! This is a plain-Python reply without a tool call.",
}))

Path(__file__).with_suffix(".png").write_bytes(workflow.get_graph().draw_mermaid_png())
