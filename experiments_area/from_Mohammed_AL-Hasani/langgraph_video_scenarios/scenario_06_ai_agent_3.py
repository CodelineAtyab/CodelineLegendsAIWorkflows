from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    message: str
    numbers: list[int]
    result: str


def check_message(state: AgentState) -> AgentState:
    """Check the user's message before choosing a path."""
    state["result"] = ""
    return state


def calculate_answer(state: AgentState) -> AgentState:
    """Calculate the sum of the numbers in the state."""
    total = sum(state["numbers"])
    state["result"] = f"The answer is {total}."
    return state


def reply_normally(state: AgentState) -> AgentState:
    """Reply when the user did not request a calculation."""
    state["result"] = "No calculation requested."
    return state


def choose_next_step(state: AgentState) -> str:
    """Choose the next node based on the user's message."""
    if "calculate" in state["message"].lower():
        return "calculate_answer"

    return "reply_normally"


builder = StateGraph(AgentState)

builder.add_node("check_message", check_message)
builder.add_node("calculate_answer", calculate_answer)
builder.add_node("reply_normally", reply_normally)

builder.add_edge(START, "check_message")
builder.add_conditional_edges(
    "check_message",
    choose_next_step,
    {
        "calculate_answer": "calculate_answer",
        "reply_normally": "reply_normally",
    },
)
builder.add_edge("calculate_answer", END)
builder.add_edge("reply_normally", END)

workflow = builder.compile()

calculation_result = workflow.invoke(
    {
        "message": "Please calculate the answer",
        "numbers": [10, 5, 3],
        "result": "",
    }
)
print(calculation_result)

normal_result = workflow.invoke(
    {
        "message": "Hello there",
        "numbers": [],
        "result": "",
    }
)
print(normal_result)

diagram = workflow.get_graph().draw_mermaid_png()
Path(__file__).with_suffix(".png").write_bytes(diagram)
