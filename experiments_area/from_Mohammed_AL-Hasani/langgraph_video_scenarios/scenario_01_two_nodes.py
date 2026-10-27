from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class MessageState(TypedDict):
    message: str
    processed_message: str


def prepare_message(state: MessageState) -> MessageState:
    """Prepare the message for processing."""
    return {
        **state,
        "processed_message": state["message"].strip(),
    }


def add_greeting(state: MessageState) -> MessageState:
    """Add a greeting to the processed message."""
    return {
        **state,
        "processed_message": f"Hello, {state['processed_message']}!",
    }


builder = StateGraph(MessageState)

builder.add_node("prepare_message", prepare_message)
builder.add_node("add_greeting", add_greeting)

builder.add_edge(START, "prepare_message")
builder.add_edge("prepare_message", "add_greeting")
builder.add_edge("add_greeting", END)

workflow = builder.compile()

result = workflow.invoke(
    {
        "message": "Mohammed",
        "processed_message": "",
    }
)

print(result)

diagram = workflow.get_graph().draw_mermaid_png()
diagram_path = Path(__file__).with_suffix(".png")
diagram_path.write_bytes(diagram)
