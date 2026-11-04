from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    question: str
    is_processed: bool

def decide_next_step(state: State) -> str:
    if "exit" in state["question"].lower():
        return "exit_node"
    return "process_node"

def process_node(state: State) -> State:
    print("--- Running Process Node ---")
    return {"question": state["question"], "is_processed": True}

def exit_node(state: State) -> State:
    print("--- Running Exit Node (No processing) ---")
    return {"question": state["question"], "is_processed": False}


workflow = StateGraph(State)

workflow.add_node("process_node", process_node)
workflow.add_node("exit_node", exit_node)


workflow.add_conditional_edges(
    START,
    decide_next_step,
    {
        "process_node": "process_node",
        "exit_node": "exit_node"
    }
)

workflow.add_edge("process_node", END)
workflow.add_edge("exit_node", END)

app = workflow.compile()

try:
    with open("graph_02.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
except Exception:
    pass

if __name__ == "__main__":
    print("--- Test Case 1: Normal Question ---")
    res1 = app.invoke({"question": "Who are you ???", "is_processed": False})
    print("Result 1:", res1)

    print("\n--- Test Case 2: Exit Question ---")
    res2 = app.invoke({"question": "Please exit!", "is_processed": False})
    print("Result 2:", res2)