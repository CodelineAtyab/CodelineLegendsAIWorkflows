# Chat Sessions

This project creates a terminal chat using `gpt-4.1-mini`.

Each conversation is saved in a JSON file and can be continued later by entering the session name.

This project practises:

- OpenAI API
- Functions
- While loops
- JSON files
- try/except
- Environment variables
# Chat Sessions Chatbot

A simple Python chatbot using OpenAI GPT-4.1-mini that saves conversations and supports interactive and non-interactive modes.

## Features

- Chat with GPT-4.1-mini.
- Save and resume previous conversations.
- Run interactively or with command-line arguments.
- Automatically generate session names.
- Handle invalid arguments.
- Test CLI helper functions using pytest.

## Technologies

Python, OpenAI API, uv, python-dotenv, pytest.

## Installation

Install dependencies:

```bash
uv sync
```

Create a `.env` file and add your API key:

```env
OPENAI_API_KEY=your_api_key_here
```

Keep `.env` out of Git.

## How to Run

**Interactive mode:**

```bash
uv run app.py
```

**Non-interactive mode (new session):**

```bash
uv run app.py "What is the capital of Oman?"
```

**Non-interactive mode (resume session):**

```bash
uv run app.py oman_capital "And its population?"
```

## Run Tests

```bash
uv run pytest
```

## Project Structure

```text
chat_sessions/
├── app.py
├── utils/
│   ├── __init__.py
│   └── cli_args.py
├── tests/
│   ├── __init__.py
│   └── test_cli_args.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Note

Chat history is saved locally, and API keys should never be committed to GitHub.