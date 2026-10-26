from chat_workflow import workflow

messages = [
    "  hello team codeline  ",
    "how are you",
    "good",
]

history = []

for message in messages:
    initial_state = {
        "incoming_message": message,
        "history": history,
        "processed_message": "",
    }

    result = workflow.invoke(initial_state)

    history = result["history"]

    print(result["processed_message"])
    print(history)

print(workflow.get_graph().draw_mermaid())
