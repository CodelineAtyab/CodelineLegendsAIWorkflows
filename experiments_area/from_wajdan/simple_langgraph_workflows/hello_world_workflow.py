from typing import TypedDict
from pathlib import Path
from langgraph.graph import END, START, StateGraph


# Define the shared data structure
class SharedState(TypedDict):
    message: str


# Define a node that updates the message
def update_greeting_message_node(state: SharedState) -> SharedState:
    state["message"] = "Hello Team Codeline Legends!"
    return state


# Create the graph
graph = StateGraph(SharedState)

# Register the node
graph.add_node("greeting_node", update_greeting_message_node)

# Connect the steps
graph.add_edge(START, "greeting_node")
graph.add_edge("greeting_node", END)

# Prepare the workflow
workflow = graph.compile()

# Run with an initial state
result = workflow.invoke({"message": ""})

# Print the final state
print(result)

print(workflow.get_graph().draw_ascii())

image_path = Path(__file__).with_suffix(".png")

image_path.write_bytes(
    workflow.get_graph().draw_mermaid_png()
)

print(f"Graph saved to: {image_path}")