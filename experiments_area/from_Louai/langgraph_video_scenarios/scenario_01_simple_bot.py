from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class BotState(TypedDict):
    messages: list[str]


def reply_to_user(state: BotState) -> BotState:
    last_message = state["messages"][-1]
    state["messages"].append(f"AI: You said '{last_message}'")
    return state


graph = StateGraph(BotState)
graph.add_node("reply_node", reply_to_user)
graph.add_edge(START,"reply_node")
graph.add_edge("reply_node", END)


workflow = graph.compile()

print(workflow.invoke({"messages": ["Hi, Im Louai"]}))
print(workflow.invoke({"messages":["what is my name"]}))

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")



