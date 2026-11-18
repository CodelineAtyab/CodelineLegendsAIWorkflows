from pathlib import Path
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class ToolCall(TypedDict):
    name: Literal["add", "subtract", "multiply"]
    left: int | None
    right: int


class ReActState(TypedDict):
    tool_plan: list[ToolCall]
    next_tool_index: int
    pending_call: ToolCall | None
    result: int | None
    route: Literal["", "tool", "done"]
    messages: list[str]


def choose_next_action(state: ReActState) -> ReActState:
    if state["next_tool_index"] < len(state["tool_plan"]):
        call = state["tool_plan"][state["next_tool_index"]]
        state["pending_call"] = call
        state["route"] = "tool"
        state["messages"].append(f"Requesting calculator tool: {call['name']}.")
    else:
        state["pending_call"] = None
        state["route"] = "done"
        state["messages"].append(f"Calculation complete: {state['result']}.")
    return state


def execute_requested_tool(state: ReActState) -> ReActState:
    call = state["pending_call"]
    if call is None:
        raise ValueError("There is no pending calculator tool call.")

    left = call["left"] if call["left"] is not None else state["result"]
    if left is None:
        raise ValueError("A first calculator operation must provide its left operand.")

    if call["name"] == "add":
        state["result"] = left + call["right"]
    elif call["name"] == "subtract":
        state["result"] = left - call["right"]
    else:
        state["result"] = left * call["right"]

    state["messages"].append(f"Tool result: {state['result']}.")
    state["next_tool_index"] += 1
    state["pending_call"] = None
    return state


def route_after_agent(state: ReActState) -> str:
    return state["route"]


graph = StateGraph(ReActState)
graph.add_node("choose_next_action", choose_next_action)
graph.add_node("execute_requested_tool", execute_requested_tool)
graph.add_edge(START, "choose_next_action")
graph.add_conditional_edges(
    "choose_next_action",
    route_after_agent,
    {"tool": "execute_requested_tool", "done": END},
)
graph.add_edge("execute_requested_tool", "choose_next_action")

workflow = graph.compile()
result = workflow.invoke(
    {
        "tool_plan": [
            {"name": "add", "left": 40, "right": 12},
            {"name": "multiply", "left": None, "right": 6},
        ],
        "next_tool_index": 0,
        "pending_call": None,
        "result": None,
        "route": "",
        "messages": [],
    }
)
print(result)

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(
    workflow.get_graph().draw_mermaid_png(max_retries=5, retry_delay=2.0)
)
print(f"Graph saved to {png_path}")
