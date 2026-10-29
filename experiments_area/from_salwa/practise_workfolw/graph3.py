
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from pathlib import Path


class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str


def process_values(state: AgentState) -> AgentState:
    """This function handles multiple different inputs."""

    state["result"] = (
        f"Hi there {state['name']}! "
        f"Your sum = {sum(state['values'])}"
    )

    return state


graph = StateGraph(AgentState)

graph.add_node("processor", process_values)

graph.add_edge(START, "processor")
graph.add_edge("processor", END)

app = graph.compile()


# Send input values to the workflow
answers = app.invoke({
    "values": [1, 2, 3, 4],
    "name": "salwa",
    "result": ""
})

# Print the results
print(answers)
print(answers["result"])

# Display the workflow graph

print(app.get_graph().draw_mermaid())
png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(app.get_graph().draw_mermaid_png())
print(f"Graph saved to: {png_path.resolve()}")