from typing import TypedDict
from pathlib import Path
from langgraph.graph import StateGraph, START, END


class SharedState(TypedDict):
    message: str


def print_greeting_message(state: SharedState):
    state["message"] = (
        f"{state['message']}, you're doing an amazing job learning LangGraph!"
    )

    return state


graph = StateGraph(SharedState)

graph.add_node("print_greeting_message_node", print_greeting_message)

graph.add_edge(START, "print_greeting_message_node")
graph.add_edge("print_greeting_message_node", END)

app = graph.compile()

result = app.invoke({"message": "Shaheen"})
print(result["message"])

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(app.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")
