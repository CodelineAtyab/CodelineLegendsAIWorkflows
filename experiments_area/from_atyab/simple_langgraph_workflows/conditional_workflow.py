from pathlib import Path
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class SharedState(TypedDict):
  question: str
  is_processed: bool


def the_decider(state: SharedState) -> SharedState:
  """
  This node decides if a user needs to exit or if their question needs
  to be processed
  """
  if "exit" in state["question"]:
    return "exit"
  else:
    return "process_question"


def process_question(state: SharedState) -> SharedState:
  state["is_processed"] = True
  print("Processed question successfully!")
  return state


graph = StateGraph(SharedState)

# Register Nodes
graph.add_node("process_question_node", process_question)
graph.add_node("decide_node", lambda state: state)

# Define Edges 
graph.add_conditional_edges("decide_node", the_decider, {"exit": END, "process_question": "process_question_node"})
graph.add_edge(START, "decide_node")
graph.add_edge("process_question_node", END)

workflow = graph.compile()

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")

# print(workflow.invoke({"question": "Please exit!", "is_processed": False}))
print(workflow.invoke({"question": "Who are you ???", "is_processed": False}))