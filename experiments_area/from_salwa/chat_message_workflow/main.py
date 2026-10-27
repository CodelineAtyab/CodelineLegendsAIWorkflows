
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from pathlib import Path

class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str


def store_message_node(state: ChatState) -> ChatState:
    message = state["incoming_message"]
    clean_message = message.strip()
    state["history"].append(clean_message)
    return state


def process_message_node(state: ChatState) -> ChatState:
    message = state["incoming_message"]
    clean_message = message.strip()
    upper_message = clean_message.upper()
    word_count = len(clean_message.split())

    state["processed_message"] = (
        f"{upper_message} ({word_count} words)"
    )

    return state


def main():
    graph = StateGraph(ChatState)

    graph.add_node("store_message_node", store_message_node)
    graph.add_node("process_message_node", process_message_node)

    graph.add_edge(START, "store_message_node")
    graph.add_edge("store_message_node", "process_message_node")
    graph.add_edge("process_message_node", END)

    workflow = graph.compile()

    messages = [
        "  hello team codeline  ",
        "how are you",
        "good",
    ]

    history = []

    for message in messages:
        initial_state = {
            "incoming_message": message,
            "history": history,
            "processed_message": "",
        }

        result = workflow.invoke(initial_state)

        print(result["processed_message"])
        print(result["history"])

        history = result["history"]

    print(workflow.get_graph().draw_mermaid())

    png_path = Path(__file__).with_suffix(".png")
    png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
    print(f"Graph saved to {png_path}")

if __name__ == "__main__":
    main()

