from typing import TypedDict


class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str
    
#Node 1: store_message_node  
def store_message_node(state: ChatState) -> ChatState:
    state["history"].append(state["incoming_message"].strip())
    return state