from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    message: str

def node_a(state: State) -> State:
    print("--- Running Node A ---")
    return {"message": state["message"] + " -> processed by Node A"}

def node_b(state: State) -> State:
    print("--- Running Node B ---")
    return {"message": state["message"] + " -> processed by Node B"}

workflow = StateGraph(State)

workflow.add_node("node_a", node_a)
workflow.add_node("node_b", node_b)

workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

app = workflow.compile()

try:
    with open("graph_01.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
except Exception:
    pass

if __name__ == "__main__":
    initial_input = {"message": "Hello LangGraph"}
    result = app.invoke(initial_input)
    print("Final State:", result)