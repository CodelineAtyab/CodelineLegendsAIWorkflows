from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class ChatState(TypedDict):
  incoming_message: str
  history: list[str]
  processed_message: str


def store_message_node(state: ChatState) -> ChatState:
  state["history"].append(state["incoming_message"].strip())
  return state


def process_message_node(state: ChatState) -> ChatState:
  message = state["incoming_message"].strip()
  word_count = len(message.split())
  state["processed_message"] = f"{message.upper()} ({word_count} words)"
  return state


graph = StateGraph(ChatState)
graph.add_node("store_message_node", store_message_node)
graph.add_node("process_message_node", process_message_node)
graph.add_edge(START, "store_message_node")
graph.add_edge("store_message_node", "process_message_node")
graph.add_edge("process_message_node", END)

workflow = graph.compile()


def main():
  messages = ["  hello team codeline  ", "how are you", "good"]
  history = []

  for message in messages:
    state = {
      "incoming_message": message,
      "history": history,
      "processed_message": "",
    }
    result = workflow.invoke(state)
    history = result["history"]

    print(result["processed_message"])
    print(result["history"])

  print(workflow.get_graph().draw_mermaid())


if __name__ == "__main__":
  main()
