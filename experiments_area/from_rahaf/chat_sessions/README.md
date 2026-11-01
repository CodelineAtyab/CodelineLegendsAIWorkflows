# Chat Sessions

A terminal chat app using `gpt-4.1-mini`. Each conversation is saved as JSON and
can be resumed later by entering its generated session name.

## Setup

1. Create a `.env` file in this directory with your OpenAI API key:

   ```text
   OPENAI_API_KEY=your_api_key_here
   ```

2. Run the application:

   ```sh
   uv run app.py
   ```

Press Enter at the session prompt to start a new conversation, or enter a saved
session name to resume it. Type `exit` to quit.

The app stores the name-to-ID mapping in `sessions_index.json` and each chat in
its own file under `sessions/`. These runtime files and `.env` are ignored by
Git.
