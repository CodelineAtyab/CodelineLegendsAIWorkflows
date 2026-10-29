
from typing import TypedDict

from langgraph.graph import START, END, StateGraph


class AgentState(TypedDict):
    question: str
    is_processed: bool


def process_question(state: AgentState) -> AgentState:
    question = state["question"].strip()

    return {
        "question": question,
        "is_processed": bool(question),
    }


builder = StateGraph(AgentState)

builder.add_node("process_question", process_question)
builder.add_edge(START, "process_question")
builder.add_edge("process_question", END)

workflow = builder.compile()


def main() -> None:
    while True:
        user_input = input("\nEnter your question (or type 'exit' to quit): ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        initial_state: AgentState = {
            "question": user_input,
            "is_processed": False,
        }

        result = workflow.invoke(initial_state)

        print(result)

    diagram = workflow.get_graph().draw_mermaid_png()

    with open("scenario_01_basic_agent.png", "wb") as file:
        file.write(diagram)

    print("Graph diagram saved to scenario_01_basic_agent.png")


if __name__ == "__main__":
    main()
