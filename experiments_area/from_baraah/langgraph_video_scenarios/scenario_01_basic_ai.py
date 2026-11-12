from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    question: str
    answer: str


# reads the question and creates an answer
def answer_question(state: State) -> dict:
    question = state["question"]
    return {"answer": f"You asked: {question}"}


# create  graph using the state
builder = StateGraph(State)

# Add the function as a node in the graph
builder.add_node("answer_question", answer_question)

# Connect START to the node, then the node to END
builder.add_edge(START, "answer_question")
builder.add_edge("answer_question", END)


workflow = builder.compile()


if __name__ == "__main__":
    # run the workflow with an initial question and empty answer
    result = workflow.invoke(
        {
            "question": "What is LangGraph?",
            "answer": "",
        }
    )

    print(result)

    # generate an image showing graph
    image = workflow.get_graph().draw_mermaid_png()

    # Save the graph image as a PNG
    Path(__file__).with_suffix(".png").write_bytes(image)
