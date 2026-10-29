from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    messages: list[str]


def respond_with_memory(state: AgentState) -> AgentState:
    user_message = state["messages"][-1]
    turn_number = sum(message.startswith("User:") for message in state["messages"])
    if user_message.lower().endswith("what is my name?"):
        remembered_name = ""
        for message in state["messages"]:
            if message.startswith("User: My name is "):
                remembered_name = message[len("User: My name is "):].rstrip(".")
                break
        response = f"Assistant: Your name is {remembered_name}."
    else:
        response = f"Assistant: Turn {turn_number}; I remember that you said '{user_message[6:]}'."
    state["messages"].append(response)
    return state


graph = StateGraph(AgentState)
graph.add_node("respond_with_memory", respond_with_memory)
graph.add_edge(START, "respond_with_memory")
graph.add_edge("respond_with_memory", END)
workflow = graph.compile()

conversation = ["User: My name is Hafisa.", "Assistant: Nice to meet you, Hafisa.", "User: What is my name?"]
result = workflow.invoke({"messages": conversation})
print(result)

diagram_path = __file__.replace(".py", ".png")
with open(diagram_path, "wb") as diagram_file:
    diagram_file.write(workflow.get_graph().draw_mermaid_png())
