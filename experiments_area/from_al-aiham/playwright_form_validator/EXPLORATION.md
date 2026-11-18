# Login and chat exploration

Explored on 17 November 2026 through the real Playwright MCP server using an
MCP client in Codex. This exploration used `http://localhost:8001` because an
existing Godot MCP service occupied port 8000. The submitted app and test plan
retain the required `http://localhost:8000` default.

## Running locally

Use Python 3.14, uv, Node.js/npx, and Chrome. Create a local, ignored `.env` with
`DEMO_PASSWORD` and `NURSE_PASSWORD` set to two made-up training passwords and
`OPENAI_API_KEY` set to your model API key. No password values belong in the
submitted files. `test_plan.json` uses `${DEMO_PASSWORD}`, expanded from the
environment when preparing each case's prompt.

From this directory, start `uv run --env-file .env app.py` in one terminal and
`uv run --env-file .env main.py` in another. With those environment variables
already exported, the commands are simply `uv run app.py` and `uv run main.py`.
The first app start seeds `demo_user` and `nurse_user` in the ignored `users.db`;
keep using the same fake passwords on subsequent runs. The workflow loads the
Playwright MCP tools once in a persistent session and builds one agent and graph.

## Login inputs and observations

For each row, the tools were called in this order:
`browser_navigate` (login page) → `browser_fill_form` (both fields) →
`browser_click` (Log in) → `browser_snapshot` (read the visible status).
An initial `browser_navigate` → `browser_snapshot` inspected the form before
these trials. The fake passwords below refer to local environment variables;
their values are intentionally omitted.

| Username input | Password input | Message observed | Result |
|---|---|---|---|
| `demo_user` | Local `DEMO_PASSWORD` | `Welcome, demo_user` | Accepted; Open chat link appeared |
| `demo_user` | Deliberately wrong value | `Invalid username or password` | Rejected |
| `unknown_user` | Local `DEMO_PASSWORD` | `Invalid username or password` | Rejected without identifying which field was wrong |
| Empty | Local `DEMO_PASSWORD` | `Username and password are required` | Rejected |
| `demo_user` | Empty | `Username and password are required` | Rejected |
| `' OR '1'='1` | Local `DEMO_PASSWORD` | `Invalid username or password` | Rejected |
| `nurse_user` | Local `NURSE_PASSWORD` | `Welcome, nurse_user` | Accepted; Open chat link appeared |

## Chat inputs and observations

After the successful nurse login above, `browser_navigate` opened `/chat`.
For each row, the tools were called in this order:
`browser_type` (message field) → `browser_click` (Send) →
`browser_snapshot` (read the log and error).

| Message input | Message observed | Result |
|---|---|---|
| `Hello clinic` | `Hello clinic` in the chat log | Accepted; message field cleared |
| Empty | `Message cannot be empty` | Rejected; log unchanged |
| Exactly 201 lowercase `a` characters | `Message too long` | Rejected; log unchanged |
| Exactly 200 lowercase `a` characters | All 200 characters appeared in the log | Accepted; error cleared |

The browser was closed with `browser_close` after exploration. Server-side
HTTP checks also confirmed that unauthenticated chat access is blocked, invalid
login clears a previous session, whitespace-only chat is rejected, and the
database contains two distinct salts and scrypt hashes rather than passwords.

## Deliberately broken tool call

With `load_mcp_tools(..., handle_tool_errors=False)`, a `browser_click` targeting
the nonexistent `#deliberately-missing-control` raised
`_MCPToolExecutionError`. This is a subclass of `ToolException`, which the case
loop catches specifically so it can print `ERROR` and continue. This temporary
verification call is not part of the submitted generic workflow or test plan.

The actual compiled graph was also verified locally with controlled agent
responses: a matching verdict passed, the deliberately wrong expectation failed,
and missing or malformed verdicts became `unknown` and failed. A case raising
`ToolException` printed `ERROR` and the next case still ran; tool-call order,
the summary count, and friendly missing/invalid JSON messages were checked.
The subsequent end-to-end run used the real OpenAI model and Playwright MCP,
with only the verification base URL changed to port 8001. All six login and
three chat validation cases passed, `deliberate_fail_demo` failed as intended,
and the summary was `9/10 passed`, with no execution errors. The agent and graph
were each built once for that run. Browser tool calls are sequential, and MCP
execution errors are returned to the agent so it can recover from transient
browser failures itself.

A later local run exposed idle browser connections blocking the original
single-threaded server. The app now uses `ThreadingHTTPServer`; a regression
check held four idle connections open while the login page still returned
HTTP 200. Connection failures and incomplete tests now have the explicit
`VERDICT: unknown | <reason>` outcome, which always fails the case instead of
counting an unavailable app as a successful invalid-input test. The submitted
config runs the browser visibly; keep the app running in a separate terminal
while the agent runs. The test browser closes when the MCP session ends.

After those fixes, a fresh full run against `http://localhost:8000` completed
with the submitted visible-browser configuration. All nine validation cases
passed, `deliberate_fail_demo` produced its intended failure, and the final
summary was `9/10 passed`, with zero `ERROR` results.

At the user's request, the last case's expectation was subsequently changed
to `invalid`. It now passes when the wrong password is rejected, so the current
plan expects `10/10 passed` for correct behavior. This explicitly overrides the
issue's requirement to retain a deliberately failing expectation.

## What does the basic authentication header contain?

The header is `Authorization: Basic <base64(username:password)>`, containing
the username and password separated by a colon before encoding. Base64 is
reversible encoding, so real deployments must use HTTPS; the plain HTTP app
here is only for local training with fake credentials.

## Why must password hashes be salted?

A fresh random salt makes identical passwords produce different stored hashes
and prevents attackers from reusing precomputed hash tables across users.
Each salt is stored alongside its hash, and a slow password hashing function
such as scrypt makes each password guess more expensive.

## Learning requirements

The class recording was not available in this task. This implementation was
AI-assisted, so it does not claim to satisfy the issue's personal requirement
to review the recording and type the Python workflow without AI.
