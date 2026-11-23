from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    messages: list[str]


def answer_question(state: AgentState) -> AgentState:
    question = state["messages"][-1]
    state["messages"].append(f"I can help with: {question}")
    return state


graph = StateGraph(AgentState)
graph.add_node("answer_question", answer_question)
graph.add_edge(START, "answer_question")
graph.add_edge("answer_question", END)
workflow = graph.compile()

result = workflow.invoke({"messages": ["What is LangGraph?"]})
print(result)

diagram_path = __file__.replace(".py", ".png")
with open(diagram_path, "wb") as diagram_file:
    diagram_file.write(workflow.get_graph().draw_mermaid_png())
