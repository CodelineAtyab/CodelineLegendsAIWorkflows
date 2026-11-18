from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    question: str
    context: str
    answer: str
    searched: bool


DOCUMENTS = [
    "LangGraph models workflows as a graph of stateful nodes.",
    "A StateGraph shares a TypedDict state between nodes.",
]


def answer_question(state: AgentState) -> AgentState:
    if state["searched"]:
        state["answer"] = state["context"]
    return state


def retrieve_context(state: AgentState) -> AgentState:
    words = state["question"].lower().split()
    matches = [document for document in DOCUMENTS if any(word in document.lower() for word in words)]
    state["context"] = " ".join(matches) or "No matching document was found."
    state["searched"] = True
    return state


def choose_next_step(state: AgentState) -> str:
    return "finish" if state["searched"] else "retrieve"


graph = StateGraph(AgentState)
graph.add_node("answer", answer_question)
graph.add_node("retrieve", retrieve_context)
graph.add_edge(START, "answer")
graph.add_conditional_edges("answer", choose_next_step, {"retrieve": "retrieve", "finish": END})
graph.add_edge("retrieve", "answer")
workflow = graph.compile()

inputs = [
    {"question": "How does a StateGraph share state?", "context": "", "answer": "", "searched": False},
    {"question": "What does a retriever do?", "context": "", "answer": "", "searched": False},
]
for input_state in inputs:
    print(workflow.invoke(input_state))

diagram_path = __file__.replace(".py", ".png")
with open(diagram_path, "wb") as diagram_file:
    diagram_file.write(workflow.get_graph().draw_mermaid_png())
