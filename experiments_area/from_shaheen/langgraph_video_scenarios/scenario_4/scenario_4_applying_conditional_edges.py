from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from pathlib import Path


class AgentState(TypedDict):
    number1: int
    number2: int
    number3: int
    number4: int
    operation1: str
    operation2: str
    final_number1: int
    final_number2: int


def add_node(state: AgentState) -> AgentState:
    """This node add 2 numbers"""
    state["final_number1"] = state["number1"] + state["number2"]
    return state


def subtract_node(state: AgentState) -> AgentState:
    """This node subtract 2 numbers"""
    state["final_number1"] = state["number1"] - state["number2"]
    return state


def add_node2(state: AgentState) -> AgentState:
    """This node add 2 numbers"""
    state["final_number2"] = state["number3"] + state["number4"]
    return state


def subtract_node2(state: AgentState) -> AgentState:
    """This node subtract 2 numbers"""
    state["final_number2"] = state["number3"] - state["number4"]
    return state


def router(state: AgentState) -> AgentState:
    """This is a router node to navigate the next node"""
    if state["operation1"] == "+":
        return "addition_operation"
    if state["operation1"] == "-":
        return "subtraction_operation"


def router2(state: AgentState) -> AgentState:
    """This is a router node to navigate the next node"""
    if state["operation2"] == "+":
        return "addition_operation2"
    if state["operation2"] == "-":
        return "subtraction_operation2"


graph = StateGraph(AgentState)

graph.add_node("add_node", add_node)
graph.add_node("add_node2", add_node2)
graph.add_node("subtract_node", subtract_node)
graph.add_node("subtract_node2", subtract_node2)
graph.add_node("router", lambda state: state)
graph.add_node("router2", lambda state: state)

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    router,
    {"addition_operation": "add_node", "subtraction_operation": "subtract_node"},
)

graph.add_edge("add_node", "router2")
graph.add_edge("subtract_node", "router2")

graph.add_conditional_edges(
    "router2",
    router2,
    {"addition_operation2": "add_node2", "subtraction_operation2": "subtract_node2"},
)

graph.add_edge("add_node2", END)
graph.add_edge("subtract_node2", END)

app = graph.compile()

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(app.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")

initial_state = AgentState(
    number1=10,
    operation1="-",
    number2=5,
    number3=7,
    number4=2,
    operation2="+",
    final_number1=0,
    final_number2=0,
)

print(app.invoke(initial_state))
