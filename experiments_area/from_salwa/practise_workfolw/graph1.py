from typing import  TypedDict
from langgraph.graph import StateGraph, START, END
from pathlib import Path

class AgntState(TypedDict):
    message: str

def greeting_message(state: AgntState) -> AgntState:
    message =  state["message"]   
    return {"message": f"Hello! How can I assist you today? You said: '{message}'"}


graph1=StateGraph(AgntState)

graph1.add_node("greeting_message", greeting_message)
graph1.add_edge(START, "greeting_message")
graph1.add_edge("greeting_message", END)

app= graph1.compile()

result =app.invoke({"message": "hello my dear , I need your help!"})
print(result["message"])  # Output: "Hello! How can I assist you today?"



print(app.get_graph().draw_mermaid())
png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(app.get_graph().draw_mermaid_png())
print(f"Graph saved to: {png_path.resolve()}")