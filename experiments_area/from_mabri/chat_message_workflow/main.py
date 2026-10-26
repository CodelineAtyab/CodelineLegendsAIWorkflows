from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str


def store_message_node(state: ChatState) -> ChatState:
    state["history"].append(state["incoming_message"].strip())
    return state


def process_message_node(state: ChatState) -> ChatState:
    state["processed_message"] = state["incoming_message"].strip().upper() + " (" + str(len(state["incoming_message"].split())) + " words)"
    return state


graph = StateGraph(ChatState)


# Register nodes
graph.add_node("store_message_node", store_message_node)
graph.add_node("process_message_node", process_message_node)


# Connect nodes
graph.add_edge(START, "store_message_node")
graph.add_edge("store_message_node", "process_message_node")
graph.add_edge("process_message_node", END)


workflow = graph.compile()


messages = ["  hello team codeline  ", "how are you", "good"]
history: list[str] = []

for message in messages:
    result = workflow.invoke(
        {"incoming_message": message, "history": history, "processed_message": ""}
    )
    history = result["history"]
    print(result["processed_message"])
    print(history)

print(workflow.get_graph().draw_mermaid())
