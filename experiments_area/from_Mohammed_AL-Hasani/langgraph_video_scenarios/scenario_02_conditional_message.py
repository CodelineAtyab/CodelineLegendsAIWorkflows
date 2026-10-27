from pathlib import Path
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class MessageState(TypedDict):
    question: str
    is_processed: bool


def process_question(state: MessageState) -> MessageState:
    """Mark a question as processed."""
    return {
        **state,
        "is_processed": True,
    }


def choose_next_step(
    state: MessageState,
) -> Literal["process", "exit"]:
    """Choose whether to process or exit."""
    if "exit" in state["question"].lower():
        return "exit"

    return "process"


builder = StateGraph(MessageState)

builder.add_node("process_question", process_question)

builder.add_edge(START, "check_question")


# This node decides which path to take.
def check_question(state: MessageState) -> MessageState:
    """Keep the state unchanged before routing."""
    return state


builder.add_node("check_question", check_question)

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

test_inputs = [
    {
        "question": "Who are you?",
        "is_processed": False,
    },
    {
        "question": "Please exit!",
        "is_processed": False,
    },
]

for test_input in test_inputs:
    print(workflow.invoke(test_input))

diagram = workflow.get_graph().draw_mermaid_png()
diagram_path = Path(__file__).with_suffix(".png")
diagram_path.write_bytes(diagram)
