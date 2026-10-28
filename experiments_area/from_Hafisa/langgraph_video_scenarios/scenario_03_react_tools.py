from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    question: str
    first_number: int
    second_number: int
    answer: str
    tool_calls: list[str]
    complete: bool


def call_agent(state: AgentState) -> AgentState:
    if state["tool_calls"]:
        state["answer"] = f"The result is {state['answer']}."
        state["complete"] = True
    else:
        state["tool_calls"].append(
            f"add({state['first_number']}, {state['second_number']})"
        )
    return state


def run_tools(state: AgentState) -> AgentState:
    state["answer"] = str(state["first_number"] + state["second_number"])
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

inputs = [
    {
        "question": "Add 40 and 12.",
        "first_number": 40,
        "second_number": 12,
        "answer": "",
        "tool_calls": [],
        "complete": False,
    },
    {
        "question": "Add 7 and 5.",
        "first_number": 7,
        "second_number": 5,
        "answer": "",
        "tool_calls": [],
        "complete": False,
    },
]
for input_state in inputs:
    print(workflow.invoke(input_state))

diagram_path = __file__.replace(".py", ".png")
with open(diagram_path, "wb") as diagram_file:
    diagram_file.write(workflow.get_graph().draw_mermaid_png())
