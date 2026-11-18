# Exploration notes

The app in `webapp/` runs on `http://localhost:8000` (`uv run webapp/server.py`). I explored it
through the Playwright MCP server (`@playwright/mcp`, headless), calling its tools through a small
throwaway client script. Every input below was typed into the real page and the text shown was
read back from a snapshot.

Tool order for one login attempt: `browser_navigate` -> `browser_snapshot` -> `browser_type`
(username) -> `browser_type` (password) -> `browser_click` (Log in) -> `browser_wait_for` (1 s)
-> `browser_snapshot`. The snapshot is needed first because it gives the `ref` of each element.
The wait is needed because the result is written after the `fetch` call finishes.

## Login form

| # | Username | Password | Message shown in `#login-result` | MCP tools used (in order) |
|---|---|---|---|---|
| 1 | `demo_user` | correct password | `Welcome, demo_user` (and a "Go to chat" link appears) | navigate, snapshot, type, type, click, wait_for, snapshot |
| 2 | `demo_user` | `wrongpass` | `Invalid username or password` | navigate, snapshot, type, type, click, wait_for, snapshot |
| 3 | `ghost_user` | `whatever` | `Invalid username or password` | navigate, snapshot, type, type, click, wait_for, snapshot |
| 4 | empty | `something` | `Username and password are required` | navigate, snapshot, type, click, wait_for, snapshot |
| 5 | `demo_user` | empty | `Username and password are required` | navigate, snapshot, type, click, wait_for, snapshot |
| 6 | `' OR '1'='1` | `' OR '1'='1` | `Invalid username or password` | navigate, snapshot, type, type, click, wait_for, snapshot |

Rows 2 and 3 show the same message, so the page never tells which of the two was wrong. Row 6
shows the SQL injection attempt is rejected because the user lookup is a parameterised query.

## Chat form

Tool order for one chat message: log in as above, then `browser_click` (Go to chat link) ->
`browser_snapshot` -> `browser_type` (message) -> `browser_click` (Send) -> `browser_wait_for`
-> `browser_snapshot`.

| # | Message | What the page showed | Element |
|---|---|---|---|
| 1 | `Hello nurse` | the message was added to the chat log | `#chat-log` |
| 2 | 201 times the letter `a` | `Message too long` | `#chat-error` |
| 3 | 200 times the letter `a` | accepted, added to the chat log (200 is the limit) | `#chat-log` |
| 4 | nothing typed, Send clicked | `Message cannot be empty` | `#chat-error` |

## What does the basic auth header contain?

The header is `Authorization: Basic <base64 of "username:password">`. The browser joins the
username and password with a colon and base64-encodes the result, and the server decodes it and
splits it again. Base64 is only an encoding, not encryption, so anyone who can see the header can
read the password; basic auth must be used over HTTPS.

## Why must hashed passwords be salted?

A salt is a random value stored next to each hash and mixed into the password before hashing. Without
a salt, two users with the same password get the same hash, and an attacker can use ready-made
tables of hashes of common passwords to reverse many of them at once. With a unique salt per user
every hash is different, so the attacker must attack each password separately. This app uses
`hashlib.scrypt` (a slow hash) with a random 16-byte salt per user.

## One thing I learned about the MCP client

`MultiServerMCPClient.get_tools()` opens a new MCP session for every tool call, so the browser
restarts and the page is lost between calls. The workflow therefore opens one session with
`client.session("playwright")` and loads the tools with `load_mcp_tools(session)`, so the agent
keeps the same browser for the whole run.
