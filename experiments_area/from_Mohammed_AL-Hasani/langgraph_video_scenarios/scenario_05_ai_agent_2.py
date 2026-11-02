from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ChatState(TypedDict):
    message: str
    history: list[str]
    response: str


def reply_to_message(state: ChatState) -> ChatState:
    """Save the message and create a simple reply."""
    state["history"].append(state["message"])
    state["response"] = f"You said: {state['message']}"
    return state


builder = StateGraph(ChatState)

builder.add_node("reply_to_message", reply_to_message)

builder.add_edge(START, "reply_to_message")
builder.add_edge("reply_to_message", END)

workflow = builder.compile()

result = workflow.invoke(
    {
        "message": "Hello again!",
        "history": ["Hello!"],
        "response": "",
    }
)

print(result)

diagram = workflow.get_graph().draw_mermaid_png()
Path(__file__).with_suffix(".png").write_bytes(diagram)
