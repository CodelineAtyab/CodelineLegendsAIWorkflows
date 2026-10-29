
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


DOCUMENTS = {
    "python": "Python is a programming language.",
    "langgraph": "LangGraph builds workflows using nodes and edges.",
}


class State(TypedDict):
    question: str
    passage: str
    answer: str


def retrieve_passage(state: State) -> dict:
    question = state["question"].lower()

    for keyword, passage in DOCUMENTS.items():
        if keyword in question:
            return {"passage": passage}

    return {"passage": ""}


def choose_path(state: State) -> str:
    if state["passage"]:
        return "found"

    return "missing"


def answer_from_passage(state: State) -> dict:
    return {"answer": state["passage"]}


def answer_no_match(state: State) -> dict:
    return {"answer": "No relevant document found."}


builder = StateGraph(State)

builder.add_node("retrieve_passage", retrieve_passage)
builder.add_node("answer_from_passage", answer_from_passage)
builder.add_node("answer_no_match", answer_no_match)

builder.add_edge(START, "retrieve_passage")

builder.add_conditional_edges(
    "retrieve_passage",
    choose_path,
    {
        "found": "answer_from_passage",
        "missing": "answer_no_match",
    },
)

builder.add_edge("answer_from_passage", END)
builder.add_edge("answer_no_match", END)

workflow = builder.compile()


if __name__ == "__main__":
    result1 = workflow.invoke({
        "question": "What is Python?",
        "passage": "",
        "answer": "",
    })

    print(result1)

    result2 = workflow.invoke({
        "question": "What is Java?",
        "passage": "",
        "answer": "",
    })

    print(result2)

    image = workflow.get_graph().draw_mermaid_png()
    Path(__file__).with_suffix(".png").write_bytes(image)
