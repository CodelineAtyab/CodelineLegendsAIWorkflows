#1:47:27 - 2:03:42

from typing import TypedDict

from langgraph.graph import START, END, StateGraph


class Message(TypedDict):
    role: str
    content: str


class AgentState(TypedDict):
    messages: list[Message]


def process_message(state: AgentState) -> AgentState:
    #Generate a simple response and preserve conversation history.
    messages = state["messages"]
    user_message = messages[-1]["content"].strip()

    if user_message.lower() in ("hi", "hello", "hey"):
        response = "Hello! How can I help you?"
    elif "langgraph" in user_message.lower():
        response = "LangGraph helps you build stateful workflows using nodes and edges."
    else:
        response = f"I received your message: {user_message}"

    updated_messages = messages + [
        {"role": "assistant", "content": response}
    ]

    return {"messages": updated_messages}


builder = StateGraph(AgentState)

builder.add_node("process_message", process_message)
builder.add_edge(START, "process_message")
builder.add_edge("process_message", END)

workflow = builder.compile()


def main() -> None:
    conversation_history: list[Message] = []

    while True:
        user_input = input(
            "\nEnter your message (or type 'exit' to quit): "
        ).strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        conversation_history.append(
            {"role": "user", "content": user_input}
        )

        result = workflow.invoke({
            "messages": conversation_history
        })

        conversation_history = result["messages"]

        print("\nFinal state:")
        print(result)

        print("\nAI:", conversation_history[-1]["content"])

    with open("logging.txt", "w", encoding="utf-8") as file:
        file.write("Your Conversation Log:\n")

        for message in conversation_history:
            if message["role"] == "user":
                file.write(f"Human: {message['content']}\n")
            else:
                file.write(f"AI: {message['content']}\n")

        file.write("\nEnd of Conversation\n")

    diagram = workflow.get_graph().draw_mermaid_png()

    with open(
        "scenario_02_conversation_memory.png", "wb"
    ) as file:
        file.write(diagram)

    print("\nConversation log saved to logging.txt")
    print("Graph diagram saved to scenario_02_conversation_memory.png")


if __name__ == "__main__":
    main()
