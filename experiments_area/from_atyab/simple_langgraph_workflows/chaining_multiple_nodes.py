from pathlib import Path
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class SharedState(TypedDict):
  message: str
  all_validated: bool


def process_question(state: SharedState) -> SharedState:
  state["message"] = f'[USER] {state["message"]}'
  return state

def validate_answer(state: SharedState) -> SharedState:
  if "[USER]" in state["message"]:
    state["all_validated"] = True
  return state

graph = StateGraph(SharedState)

# Register Nodes
graph.add_node("process_question_node", process_question)
graph.add_node("validate_answer_node", validate_answer)

# Connect them using Edges
graph.add_edge(START, "process_question_node")
graph.add_edge("process_question_node", "validate_answer_node")
graph.add_edge("validate_answer_node", END)

workflow = graph.compile()
print(workflow.invoke({"message": "Who are you ?", "all_validated": False}))

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")