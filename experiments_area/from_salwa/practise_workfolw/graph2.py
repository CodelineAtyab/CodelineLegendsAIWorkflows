
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from pathlib import Path


class ComplimentState(TypedDict):
    name: str
    message: str

def compliment_node(state: ComplimentState) -> ComplimentState:
    name = state["name"]

    state["message"] = ( f"{name}, you're doing an amazing job learning LangGraph!")

    return state

graph = StateGraph(ComplimentState)
graph.add_node("compliment", compliment_node)
graph.add_edge(START, "compliment")
graph.add_edge("compliment", END)

app = graph.compile()
result = app.invoke({
    "name": "salwa",
    "message": ""
})

print(result["message"])

print(app.get_graph().draw_mermaid())

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(app.get_graph().draw_mermaid_png())
print(f"Graph saved to: {png_path.resolve()}")