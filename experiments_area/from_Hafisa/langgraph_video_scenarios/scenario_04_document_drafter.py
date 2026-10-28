from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    request: str
    document: str
    action: str
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
        state["request"] = "save document"
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

result = workflow.invoke(
    {
        "request": "A short note about state graphs.",
        "document": "",
        "action": "",
        "complete": False,
    }
)
print(result)

diagram_path = Path(__file__).with_suffix(".png")
diagram_path.write_bytes(workflow.get_graph().draw_mermaid_png())
