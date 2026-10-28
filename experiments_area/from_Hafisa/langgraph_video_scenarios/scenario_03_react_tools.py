from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    question: str
    answer: str
    tool_calls: list[str]
    complete: bool


def call_agent(state: AgentState) -> AgentState:
    if state["tool_calls"]:
        state["answer"] = f"The result is {state['answer']}."
        state["complete"] = True
    else:
        state["tool_calls"].append("add(40, 12)")
    return state


def run_tools(state: AgentState) -> AgentState:
    state["answer"] = str(40 + 12)
    return state


def choose_next_step(state: AgentState) -> str:
    return "finish" if state["complete"] else "use_tool"


graph = StateGraph(AgentState)
graph.add_node("agent", call_agent)
graph.add_node("tools", run_tools)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", choose_next_step, {"use_tool": "tools", "finish": END})
graph.add_edge("tools", "agent")
workflow = graph.compile()

result = workflow.invoke(
    {"question": "Add 40 and 12.", "answer": "", "tool_calls": [], "complete": False}
)
print(result)

diagram_path = Path(__file__).with_suffix(".png")
diagram_path.write_bytes(workflow.get_graph().draw_mermaid_png())
