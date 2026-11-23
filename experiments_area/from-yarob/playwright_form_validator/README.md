# Playwright Form Validator (issue #291)

A LangGraph workflow where an AI agent gets the Playwright MCP tools through an MCP client
(`langchain-mcp-adapters`) and tests a login form (HTTP basic auth) and a chat form, following the
plain-language instructions in `test_plan.json`.

## Layout

| Path | What it is |
|------|------------|
| `app/server.py` | Tiny web app on `http://localhost:8000` (standard library only) |
| `app/seed_users.py` | Creates `app/users.db` with `demo_user` and `nurse_user` (salted `scrypt` hashes) |
| `app/password_hashing.py` | Salt + `scrypt` hashing and constant-time checking |
| `app/pages/` | Login page (`/`) and chat page (`/chat`) |
| `EXPLORATION.md` | Part 1 notes from exploring the forms with Playwright MCP |
| `test_plan.json` | Base URL, model, MCP server, system prompt and the test cases |
| `main.py` | The LangGraph workflow |

## Run it

Requires Node.js (`npx`) for Playwright MCP.

1. Copy `.env.example` to `.env` and fill in your OpenAI key and two made-up passwords.
   `.env` and `app/users.db` are git-ignored.
2. Seed the users and start the app (keep this terminal open):

   ```bash
   uv run app/seed_users.py
   uv run app/server.py
   ```

3. In a second terminal run the workflow:

   ```bash
   uv run main.py
   ```

Instructions in `test_plan.json` can use `${DEMO_USER_PASSWORD}`-style placeholders; `prepare_prompt`
fills them from environment variables whose names end in `_PASSWORD`, so no password is committed.

## Workflow

```
START → prepare_prompt → run_agent → parse_verdict ─┬─ "pass" → record_pass → END
                                                    └─ "fail" → record_fail → END
```
