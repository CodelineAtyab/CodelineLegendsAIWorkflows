from pathlib import Path
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class SharedState(TypedDict):
  message: str

"""
Defining Nodes
"""
def update_greeting_message_node(state: SharedState) -> SharedState:
  state["message"] = "Hello Team Codeline Legends!"
  return state


graph = StateGraph(SharedState)
graph.add_node("greeting_node", update_greeting_message_node)
graph.add_edge(START, "greeting_node")
graph.add_edge("greeting_node", END)

workflow = graph.compile()

result = workflow.invoke({"message": ""})
print(result)

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")