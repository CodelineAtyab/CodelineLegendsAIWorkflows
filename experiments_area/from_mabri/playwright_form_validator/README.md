# Playwright Form Validator (issue #291)

An AI agent (Gemini) gets the Playwright MCP browser tools and tests a small login + chat app,
driven by a LangGraph workflow and the cases in `test_plan.json`.

You need **two terminals**: one keeps the app running, the other runs the tests.

## One-time setup

```bash
cd experiments_area/from_mabri/playwright_form_validator
cp .env.example .env            # then fill in GOOGLE_API_KEY and two fake passwords
uv run python app/seed_db.py    # creates users.db with bcrypt hashes
```

Port 8000 must be free. If a Docker container uses it, stop that first
(for example `docker stop clinic-assistant-api-1`).

## Terminal 1: start the app (keeps running on purpose)

```bash
uv run uvicorn app.server:app --port 8000
```

This is a web server, so it **never finishes by itself**. Leave it open while you test,
and press **Ctrl+C** in this terminal to stop it. You can log in by hand at http://localhost:8000.

## Terminal 2: run the tests (finishes by itself)

```bash
uv run main.py
```

It prints one `PASS`, `FAIL` or `ERROR` line per case, plus a `tools used:` line, and ends with
`<passed>/<total> passed`. A full run takes a few minutes.

- A Chrome window opens and the agent clicks through it. **Do not close it**: the next
  browser tool call just opens a new one. To stop a run early, press **Ctrl+C** in this terminal.
- Set `HEADLESS=true` in `.env` to run Chrome without a visible window.
- `deliberate_fail_demo` is meant to print `FAIL`, so a good run shows `9/10 passed`.

## When something goes wrong

| What you see | Why | What to do |
|---|---|---|
| `ERROR \| … \| GoogleRateLimitError … 429` and "remaining cases are skipped" | Free Gemini quota used up | Wait for the reset, or set another model, e.g. `GEMINI_MODEL=gemini-3.1-flash-lite` in `.env` |
| `ERROR \| … \| GoogleAPIError … 503` | Gemini is overloaded right now | Run again later |
| Every case fails with `Invalid username or password` | `.env` passwords and `users.db` differ | Run `uv run python app/seed_db.py` again |
| The agent sees a 404 page | Something else answers on port 8000 | Free the port (see setup) |
