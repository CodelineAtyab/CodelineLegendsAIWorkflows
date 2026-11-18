## Playwright MCP and LangGraph training app

Create a local `.env` from `.env.example` and replace both values with fake training passwords. Do not commit `.env`.

Run the app with uv:

```powershell
uv run --env-file .env uvicorn app:app --host 127.0.0.1 --port 8000
```

Open <http://localhost:8000>. The database is created as `training_users.db` on first startup. User passwords are stored only as salted Argon2 hashes.

Run the sequential LangGraph browser test suite in a second terminal:

```powershell
uv run --env-file .env python main.py
```

The workflow starts Playwright MCP with the Windows-safe `npx.cmd` command. It creates one explicit MCP session and agent for the sequential test suite, requires the exact observed visible message, and reports browser failures with a specific error as `actual=error`.

Run quality checks with:

```powershell
uv run ruff check .
uv run ruff format --check .
```

Files added for this small app:

- `app.py`: FastAPI routes, dotenv loading, SQLite setup, Basic-auth login, and protected chat API.
- `main.py`: LangGraph workflow that asks an AI agent to perform browser actions through Playwright MCP.
- `test_plan.json`: Ten sequential login and chat test cases, including one deliberate failure.
- `templates/login.html`: Login form and result display.
- `templates/chat.html`: Protected chat form and log.
- `.env.example`: Names of the local password variables without real secrets.
- `.gitignore`: Ignores environment files, SQLite files, and Python caches.
