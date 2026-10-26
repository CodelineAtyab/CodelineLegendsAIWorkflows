from typing import TypedDict


class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str