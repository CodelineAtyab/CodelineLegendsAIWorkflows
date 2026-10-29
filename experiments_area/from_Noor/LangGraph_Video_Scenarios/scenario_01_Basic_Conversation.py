
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph

load_dotenv()


class AgentState(TypedDict):
    messages: list[HumanMessage]


llm = ChatOpenAI(model="gpt-4.1-mini")


def process(state: AgentState) -> dict:
    response = llm.invoke(state["messages"])

    print(f"\nAI: {response.content}")

    return {"messages": state["messages"]}


graph = StateGraph(AgentState)

graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()


def main():
    user_input = input("Enter your message: ")
    while user_input.lower() != "exit":
        agent.invoke({
            "messages": [HumanMessage(content=user_input)]
        })
        user_input = input("\nEnter your message (or type 'exit' to quit): ")



if __name__ == "__main__":
    main()
