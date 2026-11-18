from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


# Define the shared state
class SharedState(TypedDict):
    message: str
    all_validated: bool


# First node: add [USER] before the message
def process_question(state: SharedState) -> SharedState:
    state["message"] = f'[USER] {state["message"]}'
    return state


# Second node: check whether [USER] exists
def validate_answer(state: SharedState) -> SharedState:
    state["all_validated"] = "[USER]" in state["message"]
    return state


# Create the graph
graph = StateGraph(SharedState)

# Register nodes
graph.add_node("process_question_node", process_question)
graph.add_node("validate_answer_node", validate_answer)

# Connect nodes in order
graph.add_edge(START, "process_question_node")
graph.add_edge("process_question_node", "validate_answer_node")
graph.add_edge("validate_answer_node", END)

# Prepare the workflow
workflow = graph.compile()

# Run with the initial state
result = workflow.invoke({
    "message": "Who are you?",
    "all_validated": False,
})

# Print the final state
print(result)

# Save the graph as a PNG image
image_path = Path(__file__).with_suffix(".png")
image_path.write_bytes(workflow.get_graph().draw_mermaid_png())

print(f"Graph saved to: {image_path}")