from pathlib import Path
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class DrafterState(TypedDict):
    user_commands: list[str]
    current_command: str
    document: str
    saved_as: str
    messages: list[str]


def agent(state: DrafterState) -> DrafterState:
    state["current_command"] = state["user_commands"].pop(0)
    state["messages"].append(f"User: {state['current_command']}")
    return state


def run_tool(state: DrafterState) -> DrafterState:
    action, text = state["current_command"].split(" ", 1)
    if action == "update":
        state["document"] = text
        state["messages"].append(f"Tool: document updated to '{text}'")
    elif action == "save":
        state["saved_as"] = f"{text}.txt"
        state["messages"].append(f"Tool: document saved as '{state['saved_as']}'")
    return state


def should_continue(state: DrafterState) -> str:
    if state["saved_as"] or not state["user_commands"]:
        return "end"
    return "continue"


graph = StateGraph(DrafterState)
graph.add_node("agent_node", agent)
graph.add_node("tools_node", run_tool)
graph.add_edge(START, "agent_node")
graph.add_edge("agent_node", "tools_node")
graph.add_conditional_edges("tools_node", should_continue, {"continue": "agent_node", "end": END})

workflow = graph.compile()

print(workflow.invoke({
    "user_commands": ["update Hi Tom, the meeting moves to Friday", "update Hi Tom, the meeting moves to Friday at 3pm", "save meeting_email"],
    "current_command": "",
    "document": "",
    "saved_as": "",
    "messages": [],
}))
print(workflow.invoke({
    "user_commands": ["update First draft"],
    "current_command": "",
    "document": "",
    "saved_as": "",
    "messages": [],
}))

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")