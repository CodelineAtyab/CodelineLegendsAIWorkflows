from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    user_message: str
    history: list[str]
    reply: str


def add_user_message(state: State) -> dict:
    new_history = state["history"] + [f"User: {state['user_message']}"]
    return {"history": new_history}


def reply_to_user(state: State) -> dict:
    count = len(state["history"])
    message = state["user_message"]

    return {"reply": f"Message {count}: {message}"}


def save_reply(state: State) -> dict:
    new_history = state["history"] + [f"Bot: {state['reply']}"]
    return {"history": new_history}


builder = StateGraph(State)

builder.add_node("add_user_message", add_user_message)
builder.add_node("reply_to_user", reply_to_user)
builder.add_node("save_reply", save_reply)

builder.add_edge(START, "add_user_message")
builder.add_edge("add_user_message", "reply_to_user")
builder.add_edge("reply_to_user", "save_reply")
builder.add_edge("save_reply", END)

workflow = builder.compile()


if __name__ == "__main__":
    first = workflow.invoke(
        {
            "user_message": "Hello",
            "history": [],
            "reply": "",
        }
    )

    print(first)

    second = workflow.invoke(
        {
            "user_message": "How are you?",
            "history": first["history"],
            "reply": "",
        }
    )

    print(second)

    image = workflow.get_graph().draw_mermaid_png()
    Path(__file__).with_suffix(".png").write_bytes(image)
