# Exploration with Playwright MCP

App under test: `http://localhost:8000` (started with `uv run app/server.py`).
Playwright MCP server: `npx @playwright/mcp@latest --headless --isolated` (version 0.0.85).

The real passwords of the two training users live only in the git-ignored `.env`
file, so below they are written as `<demo password>` and `<nurse password>`.

## MCP tools used, in order

For every **login** attempt:

1. `browser_navigate` → `http://localhost:8000/`
2. `browser_snapshot` → read the page as text and find the refs of the `Username` textbox, the `Password` textbox and the `Log in` button
3. `browser_type` → type into `Username` (argument `target` = the ref from the snapshot)
4. `browser_type` → type into `Password`
5. `browser_click` → click `Log in`
6. `browser_wait_for` (1 second) → give the `fetch` call time to finish
7. `browser_snapshot` → read the text of the `status` element (`#login-result`)

For every **chat** attempt (after logging in as `demo_user`):

1. `browser_navigate` → `http://localhost:8000/chat`
2. `browser_snapshot` → find the `Message` textbox and the `Send` button
3. `browser_type` → type the message
4. `browser_click` → click `Send`
5. `browser_wait_for` (1 second)
6. `browser_snapshot` → read the `alert` element (`#chat-error`) and the `list` items (`#chat-log`)

Things I learned while exploring:

- The first snapshot right after the click still showed an empty `status`, because the page sends the
  credentials with `fetch` and the answer had not come back yet. A short `browser_wait_for` fixed it.
- In this Playwright MCP version the element argument of `browser_type` / `browser_click` is called
  `target` (older versions called it `ref`).
- Refs change after each navigation (`e4` on the first page load, `f1e4` later), so a fresh
  `browser_snapshot` is needed after every `browser_navigate`.
- A failed login leaves `Console: 1 errors` in the page info: that is the browser logging the
  `401 Unauthorized` response, not a bug in the page.

## Login form (`#username`, `#password`, `#login-button` → `#login-result`)

| # | Username | Password | Message shown in `#login-result` | Valid? |
|---|----------|----------|----------------------------------|--------|
| 1 | `demo_user` | `wrong-password` | Invalid username or password | invalid |
| 2 | `ghost_user` (does not exist) | `<demo password>` | Invalid username or password | invalid |
| 3 | *(empty)* | `<demo password>` | Username and password are required | invalid |
| 4 | `demo_user` | *(empty)* | Username and password are required | invalid |
| 5 | `' OR '1'='1` | `' OR '1'='1` | Invalid username or password | invalid |
| 6 | `nurse_user` | `<nurse password>` | Welcome, nurse_user | valid |
| 7 | `demo_user` | `<demo password>` | Welcome, demo_user | valid |

Rows 1 and 2 show the same message, so the page never says whether the username or the password
was the wrong part. Row 5 is rejected because the server uses a parameterised SQL query
(`WHERE username = ?`), so the quote characters are just part of a username that does not exist.

## Chat form (`#chat-message`, `#send-button` → `#chat-log` / `#chat-error`)

| # | Message typed | `#chat-error` | `#chat-log` | Valid? |
|---|---------------|---------------|-------------|--------|
| 1 | `Hello, I need an appointment on Monday` | *(empty)* | the message appears as a new item | valid |
| 2 | *(empty)* | Message cannot be empty | unchanged | invalid |
| 3 | the letter `a` 201 times | Message too long | unchanged | invalid |
| 4 | the letter `a` 200 times (boundary) | *(empty)* | the message appears as a new item | valid |

Opening `/chat` without logging in redirects back to the login page (`303 See Other` → `/`).

## Short answers

**What does the basic auth header contain?**
It contains the word `Basic`, a space, and then `username:password` encoded with Base64, for example
`Authorization: Basic ZGVtb191c2VyOnNlY3JldA==`. Base64 is only an encoding, not encryption: anyone
who sees the header can decode it straight back to the username and password, which is why basic
auth is only safe over HTTPS.

**Why must hashed passwords be salted?**
A salt is a random value stored next to each hash and mixed into the password before hashing, so two
users with the same password get completely different hashes. Without a salt an attacker who steals
the database can look hashes up in precomputed (rainbow) tables or crack every user with the same
password at once; with a salt they have to attack each hash separately. This app uses `scrypt`, a
deliberately slow hashing method, with a 16-byte random salt per user.
