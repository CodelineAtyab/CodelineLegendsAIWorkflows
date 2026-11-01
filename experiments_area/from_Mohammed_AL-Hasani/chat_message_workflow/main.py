from chat_workflow import ChatState, workflow

messages = [
    "  hello team codeline  ",
    "how are you",
    "good",
]

history: list[str] = []

for message in messages:
    initial_state: ChatState = {
        "incoming_message": message,
        "history": history,
        "processed_message": "",
    }

    result = workflow.invoke(initial_state)

    history = result["history"]

    print(result["processed_message"])
    print(history)

print(workflow.get_graph().draw_mermaid())
