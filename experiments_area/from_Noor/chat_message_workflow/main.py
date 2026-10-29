'''
# defines the expected keys and value types in your state.
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


# defines the three values shared between nodes.
class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str


# strips the incoming message and appends it to history. It does not modify processed_message.
def store_message_node(state: ChatState) -> ChatState:
    """Store the cleaned incoming message in conversation history."""
    message = state["incoming_message"].strip()
    state["history"].append(message)
    return state # Returns the state so LangGraph can pass it to the next node.


# converts the incoming message to uppercase and calculates the word count. It does not modify history.
def process_message_node(state: ChatState) -> ChatState:
    """Uppercase the message and include its word count."""
    message = state["incoming_message"].strip()
    word_count = len(message.split())

    state["processed_message"] = f"{message.upper()} ({word_count} words)"
    return state

# Build the LangGraph workflow
# StateGraph registers the two nodes and connects them in the required order.
builder = StateGraph(ChatState)

builder.add_node("store_message_node", store_message_node)
builder.add_node("process_message_node", process_message_node)

builder.add_edge(START, "store_message_node")
builder.add_edge("store_message_node", "process_message_node")
builder.add_edge("process_message_node", END)

# builds the workflow once.
workflow = builder.compile()


def main():
    history = []

    messages = [
        " hello team codeline ",
        "how are you",
        "good",
    ]

    for message in messages:
        initial_state: ChatState = {
            "incoming_message": message,
            "history": history,
            "processed_message": "",
        }

        # executes it for each message, carrying history from the previous result into the next invocation.
        result = workflow.invoke(initial_state)
        history = result["history"]

        print(result["processed_message"])
        print(history)

    print(workflow.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
'''


from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str
    decision: str


def store_message_node(state: ChatState) -> ChatState:
    """Store the cleaned incoming message in conversation history."""
    message = state["incoming_message"].strip()
    state["history"].append(message)
    return state


def decide_node(state: ChatState) -> ChatState:
    """Decide whether to process the message or exit."""
    message = state["incoming_message"].strip().lower()

    if message in ("exit", "quit"):
        state["decision"] = "exit"
    else:
        state["decision"] = "process_question"

    return state


def process_question_node(state: ChatState) -> ChatState:
    """Uppercase the message and include its word count."""
    message = state["incoming_message"].strip()
    word_count = len(message.split())

    state["processed_message"] = (
        f"{message.upper()} ({word_count} words)"
    )
    return state


def route_decision(
    state: ChatState,
) -> Literal["process_question", "exit"]:
    """Route the workflow based on the decision."""
    return state["decision"]


builder = StateGraph(ChatState)

builder.add_node("store_message_node", store_message_node)
builder.add_node("decide_node", decide_node)
builder.add_node("process_question_node", process_question_node)

builder.add_edge(START, "store_message_node")
builder.add_edge("store_message_node", "decide_node")

builder.add_conditional_edges(
    "decide_node",
    route_decision,
    {
        "process_question": "process_question_node",
        "exit": END,
    },
)

builder.add_edge("process_question_node", END)

workflow = builder.compile()



def main():
    history = []

    while True:
        message = input("You: ").strip()

        initial_state: ChatState = {
            "incoming_message": message,
            "history": history,
            "processed_message": "",
            "decision": "",
        }

        result = workflow.invoke(initial_state)
        history = result["history"]

        if result["decision"] == "exit":
            print("Chat ended.")
            break

        print(result["processed_message"])
        print(history)

    print(workflow.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
