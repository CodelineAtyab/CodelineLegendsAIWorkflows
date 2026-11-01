
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str


def store_message_node(state: ChatState) -> dict:
    message = state["incoming_message"].strip()

    return {
        "history": state["history"] + [message],
    }


def process_message_node(state: ChatState) -> dict:
    message = state["incoming_message"].strip().upper()
    word_count = len(message.split())

    return {
        "processed_message": f"{message} ({word_count} words)"
    }


def main():
    graph = StateGraph(ChatState)

    graph.add_node("store_message_node", store_message_node)
    graph.add_node("process_message_node", process_message_node)

    graph.add_edge(START, "store_message_node")
    graph.add_edge("store_message_node", "process_message_node")
    graph.add_edge("process_message_node", END)

    workflow = graph.compile()

    state: ChatState = {
        "incoming_message": "",
        "history": [],
        "processed_message": "",
    }

    messages = [
        "  hello team codeline  ",
        "  how are you  ",
        "  good  ",
    ]

    for message in messages:
        state["incoming_message"] = message
        state = workflow.invoke(state)

        print(state["processed_message"])
        print(state["history"])

    png_path = Path(__file__).with_suffix(".png")
    png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
    print(f"Graph saved to {png_path}")


if __name__ == "__main__":
    main()
