
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    question: str
    answer: str
    needs_calculator: bool


def classify_question(state: State) -> dict:
    needs_calculator = state["question"].startswith("add ")
    return {"needs_calculator": needs_calculator}


def choose_path(state: State) -> str:
    if state["needs_calculator"]:
        return "calculator"

    return "plain_reply"


def calculator(state: State) -> dict:
    parts = state["question"].split()[1:]

    try:
        numbers = [int(number) for number in parts]
        result = sum(numbers)
        return {"answer": str(result)}
    except ValueError:
        return {"answer": "Please enter valid numbers."}


def plain_reply(state: State) -> dict:
    return {
        "answer": "This question does not need a calculator."
    }


builder = StateGraph(State)

builder.add_node("classify_question", classify_question)
builder.add_node("calculator", calculator)
builder.add_node("plain_reply", plain_reply)

builder.add_edge(START, "classify_question")

builder.add_conditional_edges(
    "classify_question",
    choose_path,
    {
        "calculator": "calculator",
        "plain_reply": "plain_reply",
    },
)

builder.add_edge("calculator", END)
builder.add_edge("plain_reply", END)

workflow = builder.compile()


if __name__ == "__main__":
    result1 = workflow.invoke({
        "question": "add 25 15",
        "answer": "",
        "needs_calculator": False,
    })

    print(result1)

    result2 = workflow.invoke({
        "question": "Say hello",
        "answer": "",
        "needs_calculator": False,
    })

    print(result2)

    image = workflow.get_graph().draw_mermaid_png()
    Path(__file__).with_suffix(".png").write_bytes(image)
