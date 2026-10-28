from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    request: str
    document: str
    action: str
    save_request: str
    complete: bool


def draft_document(state: AgentState) -> AgentState:
    if state["request"].lower().startswith("save"):
        state["action"] = "save"
    else:
        state["document"] = state["request"]
        state["action"] = "update"
    return state


def apply_action(state: AgentState) -> AgentState:
    if state["action"] == "save":
        print(f"Saved document: {state['document']}")
        state["complete"] = True
    else:
        state["request"] = state["save_request"]
    return state


def choose_next_step(state: AgentState) -> str:
    return "finish" if state["complete"] else "draft"


graph = StateGraph(AgentState)
graph.add_node("draft", draft_document)
graph.add_node("action", apply_action)
graph.add_edge(START, "draft")
graph.add_edge("draft", "action")
graph.add_conditional_edges("action", choose_next_step, {"draft": "draft", "finish": END})
workflow = graph.compile()

inputs = [
    {
        "request": "A short note about state graphs.",
        "document": "",
        "action": "",
        "save_request": "save the document",
        "complete": False,
    },
    {
        "request": "save the document",
        "document": "An existing state graph note.",
        "action": "",
        "save_request": "save the document",
        "complete": False,
    },
]
for input_state in inputs:
    print(workflow.invoke(input_state))

diagram_path = __file__.replace(".py", ".png")
with open(diagram_path, "wb") as diagram_file:
    diagram_file.write(workflow.get_graph().draw_mermaid_png())
