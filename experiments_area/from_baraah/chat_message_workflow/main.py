from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str


# Save the cleaned message in history.
def store_message_node(state: ChatState) -> ChatState:
    state["history"].append(state["incoming_message"].strip())
    return state


# Convert the message to uppercase and count words.
def process_message_node(state: ChatState) -> ChatState:
    message = state["incoming_message"].strip()
    state["processed_message"] = f"{message.upper()} ({len(message.split())} words)"
    return state


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

history: list[str] = []

for message in messages:
    state: ChatState = {
        "incoming_message": message,
        "history": history.copy(),
        "processed_message": "",
    }

    result = workflow.invoke(state)

    history = result["history"]

    print(result["processed_message"])
    print(history)

print(workflow.get_graph().draw_mermaid())
