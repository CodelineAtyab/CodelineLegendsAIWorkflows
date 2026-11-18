# Playwright Form Validator

A LangGraph workflow where an AI agent, given the Playwright MCP tools by an MCP client, tests a
login form and a chat form from instructions in `test_plan.json`.

## Setup

Node.js (`npx`) must be installed. Copy `.env.example` to `.env` and set your own fake training
passwords and your OpenAI API key (`.env` is git-ignored).

## Run

Terminal 1, the app (creates `webapp/users.db` with salted password hashes):

```
uv run webapp/server.py
```

Terminal 2, the workflow:

```
uv run main.py
```

Each case prints `PASS`, `FAIL` or `ERROR`, an indented line with the tools the agent used, and the
run ends with `<passed>/<total> passed`.

See `EXPLORATION.md` for the manual exploration notes.
