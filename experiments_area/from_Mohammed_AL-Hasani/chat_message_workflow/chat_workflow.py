from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str


def store_message_node(state: ChatState) -> ChatState:
    message = state["incoming_message"].strip()
    state["history"].append(message)
    return state


def process_message_node(state: ChatState) -> ChatState:
    message = state["incoming_message"].strip()
    word_count = len(message.split())

    state["processed_message"] = f"{message.upper()} ({word_count} words)"
    return state


graph = StateGraph(ChatState)

graph.add_node("store_message_node", store_message_node)
graph.add_node("process_message_node", process_message_node)

graph.add_edge(START, "store_message_node")
graph.add_edge("store_message_node", "process_message_node")
graph.add_edge("process_message_node", END)

workflow = graph.compile()
