# Exploration: login and chat forms with Playwright MCP

App under test: `http://localhost:8000` (FastAPI, see `app/`).
Playwright MCP: `@playwright/mcp@0.0.85`, started over stdio with `npx` (see `.mcp.json`).
The real password of `demo_user` lives only in the git-ignored `.env`, so it is written here as `<DEMO_USER_PASSWORD>`.

## How the pages look to Playwright MCP

`browser_snapshot` returns the page as an accessibility tree. Every element gets a `ref`, which the
other tools use as their `target`:

```yaml
- heading "Clinic login" [level=1] [ref=e2]
- textbox "Username" [ref=e5]
- textbox "Password" [ref=e7]
- button "Log in" [ref=e8] [cursor=pointer]
- status [ref=e9]: Invalid username or password      # this is #login-result
```

On the chat page the log items show up as `listitem` (`#chat-log`) and the error as `alert` (`#chat-error`).

## Login form (6 inputs)

Tools used, in order, for every login attempt:
`browser_navigate` → `browser_snapshot` → `browser_type` (username) → `browser_type` (password) → `browser_click` (Log in) → `browser_wait_for` → `browser_snapshot`.
When a field was meant to stay empty, its `browser_type` call was skipped.

| # | Username | Password | Message shown in `#login-result` | Valid? |
|---|---|---|---|---|
| 1 | `demo_user` | `<DEMO_USER_PASSWORD>` | Welcome, demo_user | valid |
| 2 | `demo_user` | `wrong-pass` | Invalid username or password | invalid |
| 3 | `ghost_user` | `wrong-pass` | Invalid username or password | invalid |
| 4 | *(empty)* | `<DEMO_USER_PASSWORD>` | Username and password are required | invalid |
| 5 | `demo_user` | *(empty)* | Username and password are required | invalid |
| 6 | `' OR '1'='1` | `anything` | Invalid username or password | invalid |

Wrong password (2) and unknown username (3) show the same message, so the page does not reveal
which usernames exist. The injection attempt (6) is treated as a normal (unknown) username because
the server uses a parameterized query (`WHERE username = ?`).

## Chat form (4 inputs)

Tools used, in order: the 7 login steps above with the correct password, then
`browser_click` (Go to chat) → `browser_snapshot` → `browser_type` (message) → `browser_click` (Send) → `browser_wait_for` → `browser_snapshot`.
For the empty message the `browser_type` call was skipped.

| # | Message | Result on the page | Valid? |
|---|---|---|---|
| 1 | `Hello, is Dr. Salim available tomorrow?` | appears in `#chat-log` as `demo_user: Hello, is Dr. Salim available tomorrow?` | valid |
| 2 | *(empty)* | `#chat-error`: Message cannot be empty | invalid |
| 3 | `a` × 200 | appears in `#chat-log` (exactly at the limit) | valid |
| 4 | `a` × 201 | `#chat-error`: Message too long | invalid |

## Things I noticed

- Refs are only valid for the snapshot they came from. After a new navigation they changed from `e5` to `f1e5`,
  so a new `browser_snapshot` is needed before every click or type.
- The form inputs have no `required` or `maxlength` attributes, so the browser does not block the submit
  and the server's message is always shown. A `maxlength="200"` would have made the 201-character case impossible to type.
- The chat page only works after logging in in the same tab: the login stores the basic auth header in
  `sessionStorage`, and every chat request sends it again.

## Questions

<!-- Draft answers: reword them in your own words before submitting. -->

**What does the basic auth header contain?**
It contains the word `Basic`, a space, and the Base64 encoding of `username:password`, for example
`Authorization: Basic ZGVtb191c2VyOnNlY3JldA==`. Base64 is only an encoding, not encryption, so anyone
who sees the header can decode the password; that is why basic auth must only be used over HTTPS.

**Why must hashed passwords be salted?**
A salt is a random value stored with each hash and mixed into it, so two users with the same password
get different hashes. Without a salt an attacker can use precomputed tables of common password hashes
and crack every user who shares a password at once; with a salt every hash must be attacked separately,
and a slow algorithm like bcrypt makes each attempt expensive.
