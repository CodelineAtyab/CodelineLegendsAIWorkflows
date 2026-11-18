from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ChatState(TypedDict):
    messages: list[str]


def reply_with_memory(state: ChatState) -> ChatState:
    first_message = state["messages"][0]
    last_message = state["messages"][-1]
    state["messages"].append(f"AI: You said '{last_message}'. Your first message was '{first_message}'")
    return state



graph = StateGraph(ChatState)
graph.add_node("reply_node", reply_with_memory)
graph.add_edge(START, "reply_node")
graph.add_edge("reply_node", END)

workflow = graph.compile()


conversation_history = ["Hi, Im Louai"]
result = workflow.invoke({"messages": conversation_history})
print(result)



conversation_history = result["messages"] + ["What's my name?"]
result = workflow.invoke({"messages": conversation_history})
print(result)

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")




