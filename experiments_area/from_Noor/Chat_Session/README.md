- Overview:

This project is a terminal-based chat application built with Python and the OpenAI API. It allows users to chat with GPT-4.1 mini, save conversation history to JSON files, and resume previous conversations by entering their session names.

Each new conversation receives an automatically generated two-word name based on the user's first question. The conversation history is saved so that the model can use previous messages as context.

- Features:

1- AI Chat: Communicate with OpenAI's gpt-4.1-mini model.

2- New Sessions: Press Enter at the session prompt to start a new conversation.

3- Session Naming: Generate a two-word session name based on the first question.

4- Resume Conversations: Enter an existing session name to continue the conversation with its saved history.

5- JSON Storage: Store each conversation in a separate JSON file.

6- Session Index: Map session names to session IDs in an index file.

7- Error Handling: Display friendly messages for API errors and unreadable JSON files.

8- Exit Command: Type exit to end the chat.