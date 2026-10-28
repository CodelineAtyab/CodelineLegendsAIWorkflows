from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from pathlib import Path

class SharedState(TypedDict):
    name: str
    age: int
    skills: list
    final_output: str

def greeting_message(state: SharedState) -> SharedState:
    state["final_output"] = f"{state["name"]}, welcome to the system!"
    return state

def describes_user_age(state: SharedState) -> SharedState:
    state["final_output"] = state["final_output"] + f" You are {state["age"]} years old!"
    return state

def lists_user_skills(state: SharedState) -> SharedState:
    state["final_output"] = state["final_output"] + f" You have skills in: {', '.join(state["skills"])}" 
    return state

graph = StateGraph(SharedState)

graph.add_node("greeting_message_node", greeting_message)
graph.add_node("describes_user_age_node", describes_user_age)
graph.add_node("lists_user_skills_node", lists_user_skills)

graph.add_edge(START, "greeting_message_node")
graph.add_edge("greeting_message_node","describes_user_age_node")
graph.add_edge("describes_user_age_node","lists_user_skills_node")
graph.add_edge("lists_user_skills_node", END)



app = graph.compile()

result = app.invoke({"name":"Linda", "age":31, "skills":["Python","Machine Learning","LangGraph"]})

print(result["final_output"])

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(app.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")