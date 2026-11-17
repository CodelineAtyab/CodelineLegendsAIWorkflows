from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class MemoryState(TypedDict):
    messages: list[str]


def respond_with_history(state: MemoryState) -> MemoryState:
    reply = "Bot: Your first message was: " + state["messages"][0]
    state["messages"].append(reply)
    return state


graph = StateGraph(MemoryState)
graph.add_node("respond_with_history", respond_with_history)
graph.add_edge(START, "respond_with_history")
graph.add_edge("respond_with_history", END)

workflow = graph.compile()

history: list[str] = []

for question in ["My name is Aiham.", "What was my first message?"]:
    history.append("You: " + question)
    result = workflow.invoke({"messages": history})
    history = result["messages"]
    print(result)

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
