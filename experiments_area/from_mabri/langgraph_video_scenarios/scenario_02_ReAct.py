from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import (
    BaseMessage,
)  # The foundational class for all message types in LangGraph
from langchain_core.messages import (
    ToolMessage,
)  # Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import (
    SystemMessage,
)  # Message for providing instructions to the LLM
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
)  # Messages from the LLM and from the user
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from pathlib import Path


load_dotenv()  # Load environment variables from .env file


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a: int, b: int):
    """Adds two numbers."""
    return a + b


@tool
def subtract(a: int, b: int):
    """Subtracts two numbers."""
    return a - b


@tool
def multiply(a: int, b: int):
    """Multiplies two numbers."""
    return a * b


@tool
def divide(a: int, b: int):
    """Divides two numbers."""
    if b == 0:
        return "Error: Division by zero"
    return a / b


tools = [add, subtract, multiply, divide]

model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)


def model_node(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        content="You are my AI assistant, please answer my query to the best of your ability."
    )
    response = model.invoke([system_prompt, *state["messages"]])
    return {"messages": [response]}


def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        return "end"
    else:
        return "continue"


graph = StateGraph(AgentState)

graph.add_node("our_agent", model_node)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent", should_continue, {"continue": "tools", "end": END}
)

graph.add_edge("tools", "our_agent")

workflow = graph.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs: AgentState = {
    "messages": [
        HumanMessage(
            content="Add 40 + 12 and then multiply the result by 6. Also tell me a joke please."
        )
    ]
}
print_stream(workflow.stream(inputs, stream_mode="values"))

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")
