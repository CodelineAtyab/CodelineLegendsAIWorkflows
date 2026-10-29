from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ReActState(TypedDict):
    messages: list[str]
    pending_tools: list[str]
    result: int


def add(a: int, b: int) -> int:
    return a + b


def multiply(a: int, b: int) -> int:
    return a * b


def agent(state: ReActState) -> ReActState:
    if state["pending_tools"]:
        state["messages"].append(f"AI: I will call the tool '{state['pending_tools'][0]}'")
    else:
        state["messages"].append(f"AI: Final answer is {state['result']}")
    return state


def run_tool(state: ReActState) -> ReActState:
    tool_call = state["pending_tools"].pop(0)
    tool_name, number = tool_call.split()
    if tool_name == "add":
        state["result"] = add(state["result"], int(number))
    elif tool_name == "multiply":
        state["result"] = multiply(state["result"], int(number))
    state["messages"].append(f"Tool: {tool_call} -> {state['result']}")
    return state


def should_continue(state: ReActState) -> str:
    if state["pending_tools"]:
        return "continue"
    return "end"


graph = StateGraph(ReActState)
graph.add_node("agent_node", agent)
graph.add_node("tools_node", run_tool)
graph.add_edge(START, "agent_node")
graph.add_conditional_edges("agent_node", should_continue, {"continue": "tools_node", "end": END})
graph.add_edge("tools_node", "agent_node")

workflow = graph.compile()

print(workflow.invoke({"messages": ["Add 40 + 12, then multiply by 6"], "pending_tools": ["add 12", "multiply 6"], "result": 40}))
print(workflow.invoke({"messages": ["What is 7?"], "pending_tools": [], "result": 7}))

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")