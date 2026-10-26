# Chat REST API

A simple REST API built with Python and FastAPI to manage users, bots, conversations, and messages.

## Features
- Add and view users.
- Add and view bots.
- Start and view conversations.
- Send user messages and receive random bot replies.
- Filter conversations and messages.
- Handle missing fields, invalid IDs, and duplicate replies.

## Technologies
- Python 3.14
- FastAPI
- Uvicorn
- uv

## Project Structure
```text
chat_rest_api/
├── main.py
├── chat_data.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Installation
Install dependencies:

```bash
uv sync
```

## Run the Project
Start the server:

```bash
uv run main.py
```

Open the API documentation:

http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/add` | Add a user |
| GET | `/users` | View users |
| POST | `/bots/add` | Add a bot |
| GET | `/bots` | View bots |
| POST | `/conversations/start` | Start a conversation |
| GET | `/conversations` | View conversations |
| GET | `/conversations/show` | Show conversation messages |
| POST | `/messages/ask` | Send a user query |
| POST | `/messages/reply` | Generate a bot reply |
| GET | `/messages` | View and filter messages |

## Notes
- Data is stored in Python lists, without a database.
- Bot replies are randomly selected from predefined responses.
- Data resets when the server restarts.
- No real AI API is used.
