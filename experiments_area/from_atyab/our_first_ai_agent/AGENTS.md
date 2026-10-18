# AGENTS.md — our_first_ai_agent

A minimal command-line chat agent: a Python REPL loop that talks to OpenAI and
persists each conversation to its own JSON file.

## Stack

- Python 3.14, pinned in `.python-version`
- `uv` for the environment and dependencies — do not use `pip` directly
- `openai` SDK and `python-dotenv`

## Commands

```sh
uv run main.py               # start a new session
uv run main.py <session_id>  # resume an existing session
uv add <package>             # add a dependency (updates pyproject.toml + uv.lock)
```

The chat loop exits on `exit` or `quit`.

## Layout

| Path | Purpose |
| --- | --- |
| `main.py` | Entry point; wires the modules together and runs the chat loop |
| `utils/config.py` | Env loading, model settings, shared paths, `require_api_key()` |
| `utils/client.py` | OpenAI client creation, payload shaping, reply extraction |
| `utils/session.py` | Load, save, and resolve session IDs |
| `tests/` | pytest unit tests, named `test_*.py`, one file per module under test |
| `sessions/` | Generated JSON history, one file per session — gitignored |

## Conventions

- Keep the one-module-per-concern split: config, client, session. Do not collapse them.
- Each module opens with a short comment describing its responsibility.
- Inside functions, use short numbered step comments (`# 1. ...`) to narrate the flow.
- Keep functions small, with type hints and one-line docstrings.
- Use relative imports inside the package (`from .config import ...`).
- Bound the model context with `MAX_HISTORY_MESSAGES` in `utils/config.py`; never send
  the full history.
- Model name, exit words, and the system prompt live in `utils/config.py`. Change them
  there, not inline in the call sites.

## Gotchas

- `OPENAI_API_KEY` is read from `.env` via `load_dotenv()`. `require_api_key()` fails fast
  with a clear message when it is missing.
- `.env` is gitignored by the repository root. Never commit real keys.
- `sessions/` is gitignored. Never commit conversation history.
- `resolve_session_id()` always starts a new session when no argument is given.
- Session files are rewritten in full on every turn; there is no append path.
- A corrupt or unreadable session file is treated as empty after a warning, not an error.

## Verification

After any change, run `uv run main.py`, send one message, then exit. Confirm the reply
comes back and a new file appears in `sessions/`.

## Note on tooling

GitHub and Slack MCP servers used during development are configured in the **global**
OpenCode config (`~/.config/opencode/opencode.json`), not in this project. Nothing
project-specific depends on them.
