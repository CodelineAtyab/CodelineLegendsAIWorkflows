from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class SharedState(TypedDict):
    message: str


def update_greeting_message_node(state: SharedState) -> SharedState:
    state["message"] = "Hello World!"
    return state


graph = StateGraph(SharedState)

graph.add_node("greeting_node", update_greeting_message_node)

graph.add_edge(START, "greeting_node")
graph.add_edge("greeting_node", END)

workflow = graph.compile()

result = workflow.invoke({"message": ""})

print(result)
