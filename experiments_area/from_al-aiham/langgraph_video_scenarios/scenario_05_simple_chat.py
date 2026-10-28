from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ChatState(TypedDict):
    question: str
    reply: str


def respond(state: ChatState) -> ChatState:
    state["reply"] = f"You asked: {state['question']}"
    return state


graph = StateGraph(ChatState)
graph.add_node("respond", respond)
graph.add_edge(START, "respond")
graph.add_edge("respond", END)
workflow = graph.compile()

print(workflow.invoke({"question": "Hello", "reply": ""}))
print(workflow.invoke({"question": "What is LangGraph?", "reply": ""}))

Path(__file__).with_suffix(".png").write_bytes(workflow.get_graph().draw_mermaid_png())
