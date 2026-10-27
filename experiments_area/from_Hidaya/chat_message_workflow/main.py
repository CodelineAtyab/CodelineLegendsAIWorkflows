from typing import TypedDict
from pathlib import Path

from langgraph.graph import END, START, StateGraph


class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str


def store_message_node(state: ChatState) -> ChatState:
    """Add the cleaned message to history."""
    state["history"].append(state["incoming_message"].strip())
    return state


def process_message_node(state: ChatState) -> ChatState:
    """Uppercase the message and count its words."""
    message = state["incoming_message"].strip()
    state["processed_message"] = (
        f"{message.upper()} ({len(message.split())} words)"
    )
    return state


graph = StateGraph(ChatState)

graph.add_node("store_message_node", store_message_node)
graph.add_node("process_message_node", process_message_node)

graph.add_edge(START, "store_message_node")
graph.add_edge("store_message_node", "process_message_node")
graph.add_edge("process_message_node", END)

workflow = graph.compile()

history: list[str] = []

for message in ["  hello team codeline  ", "how are you", "good"]:
    result = workflow.invoke(
        {
            "incoming_message": message,
            "history": history,
            "processed_message": "",
        }
    )

    history = result["history"]
    print(result["processed_message"])
    print(history)

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")