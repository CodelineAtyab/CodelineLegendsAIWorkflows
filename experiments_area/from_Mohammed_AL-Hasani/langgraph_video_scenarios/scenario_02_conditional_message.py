from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class MessageState(TypedDict):
    question: str
    is_processed: bool


def check_question(state: MessageState) -> MessageState:
    """Keep the state unchanged before routing."""
    return state


def process_question(state: MessageState) -> MessageState:
    """Mark the question as processed."""
    state["is_processed"] = True
    return state


def choose_next_step(state: MessageState) -> str:
    """Choose whether to process the question or exit."""
    if "exit" in state["question"].lower():
        return "exit"
    return "process"


builder = StateGraph(MessageState)

builder.add_node("check_question", check_question)
builder.add_node("process_question", process_question)

builder.add_edge(START, "check_question")
builder.add_conditional_edges(
    "check_question",
    choose_next_step,
    {
        "process": "process_question",
        "exit": END,
    },
)
builder.add_edge("process_question", END)

workflow = builder.compile()

test_inputs: list[MessageState] = [
    {"question": "Who are you?", "is_processed": False},
    {"question": "Please exit!", "is_processed": False},
]

for test_input in test_inputs:
    print(workflow.invoke(test_input))

diagram = workflow.get_graph().draw_mermaid_png()
diagram_path = Path(__file__).with_suffix(".png")
diagram_path.write_bytes(diagram)
