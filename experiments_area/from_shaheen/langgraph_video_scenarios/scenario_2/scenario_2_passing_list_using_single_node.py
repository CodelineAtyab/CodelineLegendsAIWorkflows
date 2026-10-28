from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from pathlib import Path
from functools import reduce

class SharedState(TypedDict):
    values: list
    operation: str
    name: str
    final_output: str

def process(state: SharedState) -> SharedState:
    if state["operation"] == "+":
        total = reduce(lambda x, y: x + y, state["values"], 0)
    
    elif state["operation"] == "*":
        total = reduce(lambda x, y: x * y, state["values"], 1)


    state["final_output"] = f"Hi {state["name"]}, your answer is: {total}"
    return state


graph = StateGraph(SharedState)

graph.add_node("process_node" , process)

graph.add_edge(START, "process_node")
graph.add_edge("process_node", END)

app = graph.compile()

result = app.invoke({"name": "Jack Sparrow","values":[1,2,3,4],"operation": "*", "final_output" : "" })

print(result["final_output"])

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(app.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")