import re
from pathlib import Path
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class ChatMessage(TypedDict):
    role: Literal["user", "assistant"]
    content: str


class ConversationState(TypedDict):
    messages: list[ChatMessage]
    reply: str


def find_name(message: str) -> str | None:
    match = re.search(
        r"\b(?:my name is|i am|i'm)\s+([A-Za-z][A-Za-z'-]*)", message, re.IGNORECASE
    )
    if match is None:
        return None
    return match.group(1)


def respond_using_history(state: ConversationState) -> ConversationState:
    latest_user_index = next(
        (
            index
            for index in range(len(state["messages"]) - 1, -1, -1)
            if state["messages"][index]["role"] == "user"
        ),
        None,
    )
    if latest_user_index is None:
        raise ValueError("The conversation needs at least one user message.")

    latest_message = state["messages"][latest_user_index]["content"]
    name = find_name(latest_message)
    if name is not None:
        reply = f"Nice to meet you, {name}."
    elif "name" in latest_message.casefold():
        previous_user_messages = state["messages"][:latest_user_index]
        remembered_name = next(
            (
                found_name
                for message in reversed(previous_user_messages)
                if message["role"] == "user"
                if (found_name := find_name(message["content"])) is not None
            ),
            None,
        )
        if remembered_name is None:
            reply = "I don't know your name yet."
        else:
            reply = f"Your name is {remembered_name}."
    else:
        reply = f"I heard you say, '{latest_message}'."

    state["reply"] = reply
    state["messages"].append({"role": "assistant", "content": reply})
    return state


graph = StateGraph(ConversationState)
graph.add_node("respond_using_history", respond_using_history)
graph.add_edge(START, "respond_using_history")
graph.add_edge("respond_using_history", END)

workflow = graph.compile()
conversation = workflow.invoke(
    {
        "messages": [{"role": "user", "content": "Hi, I'm Steve."}],
        "reply": "",
    }
)
conversation["messages"].append({"role": "user", "content": "What is my name?"})
result = workflow.invoke(conversation)
print(result)

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(
    workflow.get_graph().draw_mermaid_png(max_retries=5, retry_delay=2.0)
)
print(f"Graph saved to {png_path}")
