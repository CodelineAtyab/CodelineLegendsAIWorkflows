from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class MemoryState(TypedDict):
    messages: list[dict[str, str]]


def respond_with_history(state: MemoryState) -> MemoryState:
    questions = []
    for message in state["messages"]:
        if message["role"] == "user":
            questions.append(message["content"])
    reply = "Questions so far: " + "; ".join(questions)
    state["messages"].append({"role": "assistant", "content": reply})
    return state


graph = StateGraph(MemoryState)
graph.add_node("respond_with_history", respond_with_history)
graph.add_edge(START, "respond_with_history")
graph.add_edge("respond_with_history", END)
workflow = graph.compile()

history: list[dict[str, str]] = []
for question in ["What is LangGraph?", "What did I ask before?"]:
    history.append({"role": "user", "content": question})
    result = workflow.invoke({"messages": history})
    history = result["messages"]
    print(result)

with open(Path(__file__).with_name("logging.txt"), "w", encoding="utf-8") as file:
    file.write("Your Conversation Log:\n")

    for message in history:
        label = "You" if message["role"] == "user" else "AI"
        file.write(f"{label}: {message['content']}\n")

    file.write("End of Conversation\n")

Path(__file__).with_suffix(".png").write_bytes(workflow.get_graph().draw_mermaid_png())
