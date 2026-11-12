Overview:
Chatbot Upgrade is a Python-based chatbot that uses the OpenAI API to answer user questions. It supports both interactive and non-interactive modes and allows users to save and resume previous conversations.

The project also includes command-line argument handling, session management, and unit tests to ensure the application works as expected.
--------------------------------------

Features:

1- Interactive mode: Chat with the assistant continuously until you enter exit or quit.

2- Non-interactive mode: Ask one question directly from the terminal and exit after receiving the response.

3- Session management: Automatically generate session names for new conversations.

4- Resume conversations: Continue an existing session using its name and previous conversation history.

5- Persistent storage: Save session information and conversation history as JSON files.

6- Error handling: Handle invalid session names and API or file-related errors.

7- Unit testing: Test command-line argument parsing, session name cleaning, and exit commands.
----------------------------------------
Usage:

- Interactive Mode:

Run the application without arguments:

uv run app.py

You can resume an existing session by entering its name or press Enter to start a new conversation. Continue chatting until you enter exit or quit.

- Non-Interactive Mode: New Session:

Pass a question as the only argument:

uv run app.py "What is the capital of Oman?"

The application generates a session name, answers the question, saves the conversation, and exits.

Example output:

Session: oman_capital
Assistant: The capital of Oman is Muscat.

The session name and assistant response are examples; the actual response and generated name may differ.

- Non-Interactive Mode: Resume a Session

Provide an existing session name followed by your question:

uv run app.py oman_capital "What is its population?"

The chatbot loads the previous conversation history, answers the follow-up question, saves the updated history, and exits.

- Invalid Session:

If the specified session does not exist:

uv run app.py unknown_session "Hello"

The application displays an error and exits without prompting for input.
----------------------------------

Session Storage:

Session information is stored in the sessions/ directory.

index.json stores session names and their corresponding IDs.

Individual JSON files store conversation messages, including user questions and assistant responses.

This allows the chatbot to maintain conversation history between application runs.
-------------------------------------

Testing:

Run the unit tests:

uv run pytest

The tests cover the command-line argument helper functions in utils/cli_args.py.
----------------------------------------

Error Handling:

The application handles situations such as:

Missing or invalid session names.

Missing API configuration.

OpenAI API errors.

File access and JSON parsing errors.

Invalid command-line arguments.
-------------------------------------------

