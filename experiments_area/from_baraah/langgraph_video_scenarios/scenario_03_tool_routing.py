from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


# Store the question, tool result, and final answer.
class State(TypedDict):
    question: str
    tool_result: str
    answer: str


# Decide whether to use the calculator or finish.
def agent(state: State) -> dict:
    if state["tool_result"]:
        return {"answer": f"The answer is {state['tool_result']}"}

    if state["question"].startswith("add "):
        return {"answer": ""}

    return {"answer": "No calculator needed."}


# Choose the next node based on the state.
def choose_next(state: State) -> str:
    if state["answer"]:
        return "finish"

    return "use_tool"


# Calculate the sum of the numbers in the question.
def calculator(state: State) -> dict:
    parts = state["question"].split()[1:]

    try:
        numbers = [int(number) for number in parts]

        if not numbers:
            return {"tool_result": "No numbers provided"}

        return {"tool_result": str(sum(numbers))}
    except ValueError:
        return {"tool_result": "Invalid numbers"}


# Create the graph.
builder = StateGraph(State)

# Add the agent and calculator nodes.
builder.add_node("agent", agent)
builder.add_node("calculator", calculator)

# Start with the agent.
builder.add_edge(START, "agent")

# The agent chooses whether to use the tool or finish.
builder.add_conditional_edges(
    "agent",
    choose_next,
    {
        "use_tool": "calculator",
        "finish": END,
    },
)

# Return the tool result to the agent.
builder.add_edge("calculator", "agent")

# Compile the workflow.
workflow = builder.compile()


if __name__ == "__main__":
    # Test a question that needs the calculator.
    result1 = workflow.invoke(
        {
            "question": "add 25 15",
            "tool_result": "",
            "answer": "",
        }
    )
    print(result1)

    # Test a question that does not need the calculator.
    result2 = workflow.invoke(
        {
            "question": "Hello",
            "tool_result": "",
            "answer": "",
        }
    )
    print(result2)

    # Save the graph diagram.
    image = workflow.get_graph().draw_mermaid_png()
    Path(__file__).with_suffix(".png").write_bytes(image)
