from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str


def store_message_node(state: ChatState) -> ChatState:
    """Append the stripped incoming message to the history."""
    state["history"].append(state["incoming_message"].strip())
    return state


def process_message_node(state: ChatState) -> ChatState:
    """Uppercase the message and append its word count."""
    message = state["incoming_message"].strip()
    word_count = len(message.split())
    state["processed_message"] = f"{message.upper()} ({word_count} words)"
    return state


def main() -> None:
    """Process three messages and print the results and graph diagram."""
    graph = StateGraph(ChatState)
    graph.add_node("store_message_node", store_message_node)
    graph.add_node("process_message_node", process_message_node)

    graph.add_edge(START, "store_message_node")
    graph.add_edge("store_message_node", "process_message_node")
    graph.add_edge("process_message_node", END)

    workflow = graph.compile()

    history: list[str] = []
    messages = ["  hello team codeline  ", "  how are you  ", "good"]

    for message in messages:
        initial_state: ChatState = {
            "incoming_message": message,
            "history": history,
            "processed_message": "",
        }

        result = workflow.invoke(initial_state)
        history = result["history"]

        print(result["processed_message"])
        print(history)

    print(workflow.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
