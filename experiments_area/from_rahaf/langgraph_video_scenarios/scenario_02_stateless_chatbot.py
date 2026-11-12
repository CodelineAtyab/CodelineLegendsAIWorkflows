from pathlib import Path
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class ChatMessage(TypedDict):
    role: Literal["user", "assistant"]
    content: str


class ChatbotState(TypedDict):
    messages: list[ChatMessage]
    reply: str


def reply_to_latest_message(state: ChatbotState) -> ChatbotState:
    latest_user_message = next(
        (
            message["content"]
            for message in reversed(state["messages"])
            if message["role"] == "user"
        ),
        None,
    )
    if latest_user_message is None:
        raise ValueError("The chatbot needs at least one user message.")

    reply = f"Deterministic demo reply: I heard you say, '{latest_user_message}'"
    state["reply"] = reply
    state["messages"].append({"role": "assistant", "content": reply})
    return state


graph = StateGraph(ChatbotState)
graph.add_node("reply_to_message", reply_to_latest_message)
graph.add_edge(START, "reply_to_message")
graph.add_edge("reply_to_message", END)

workflow = graph.compile()
result = workflow.invoke(
    {
        "messages": [
            {"role": "user", "content": "Hi, I'm Steve. Can you say hello?"},
        ],
        "reply": "",
    }
)
print(result)

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(
    workflow.get_graph().draw_mermaid_png(max_retries=5, retry_delay=2.0)
)
print(f"Graph saved to {png_path}")
