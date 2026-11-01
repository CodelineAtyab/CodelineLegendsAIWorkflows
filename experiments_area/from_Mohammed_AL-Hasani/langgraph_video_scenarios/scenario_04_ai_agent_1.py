from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    message: str
    response: str


def process_message(state: AgentState) -> AgentState:
    """Process the user's message."""
    state["response"] = f"You said: {state['message']}"
    return state


builder = StateGraph(AgentState)

builder.add_node("process_message", process_message)

builder.add_edge(START, "process_message")
builder.add_edge("process_message", END)

workflow = builder.compile()

result = workflow.invoke(
    {
        "message": "Hello, LangGraph!",
        "response": "",
    }
)

print(result)

diagram = workflow.get_graph().draw_mermaid_png()
Path(__file__).with_suffix(".png").write_bytes(diagram)
