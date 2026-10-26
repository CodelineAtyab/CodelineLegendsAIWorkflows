from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class ChatState(TypedDict):
    incoming_message: str
    history: list[str]
    processed_message: str
    
#Node 1: store_message_node  
def store_message_node(state: ChatState) -> ChatState:
    state["history"].append(state["incoming_message"].strip())
    return state

#Node 2: process_message_node
def process_message_node(state: ChatState) -> ChatState:
    current_msg = state["history"][-1] # Get the latest message from history (or clean incoming_message)
    
    upper_msg = current_msg.upper()
    word_count = len(current_msg.split())
    
    state["processed_message"] = f"{upper_msg} ({word_count} words)"
    return state

def main():
#Graph
    graph = StateGraph(ChatState)

    graph.add_node("store_message_node", store_message_node)
    graph.add_node("process_message_node", process_message_node)

    graph.add_edge(START, "store_message_node")
    graph.add_edge("store_message_node", "process_message_node")
    graph.add_edge("process_message_node", END)

    workflow = graph.compile()


if __name__ == "__main__":
    main()