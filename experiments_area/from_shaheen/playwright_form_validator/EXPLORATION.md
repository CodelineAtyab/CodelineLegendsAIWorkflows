# Login and chat form exploration

Explored on 2026-11-18 with Playwright MCP in Claude Code, against the app from `app.py` running on `http://localhost:8000`. The two training users were seeded with throwaway passwords from environment variables; below, `<demo password>` stands for demo_user's password, which is not written down here.

## Login form (`/`)

Each input started from a fresh `browser_navigate` to `http://localhost:8000/`. Elements used: `#username`, `#password`, `#login-button`, and the message in `#login-result`.

| # | Username | Password | Message shown | MCP tools in order |
|---|---|---|---|---|
| 1 | demo_user | `<demo password>` | Welcome, demo_user (and a "Go to chat" link appeared) | browser_navigate, browser_snapshot, browser_type, browser_type, browser_click, browser_snapshot |
| 2 | demo_user | wrong-pass-123 | Invalid username or password | browser_navigate, browser_type, browser_type, browser_click, browser_snapshot |
| 3 | ghost_user | `<demo password>` | Invalid username or password | browser_navigate, browser_type, browser_type, browser_click, browser_snapshot |
| 4 | (empty) | `<demo password>` | Username and password are required | browser_navigate, browser_type, browser_click, browser_snapshot |
| 5 | demo_user | (empty) | Username and password are required | browser_navigate, browser_type, browser_click, browser_snapshot |
| 6 | `' OR '1'='1` | anything | Invalid username or password | browser_navigate, browser_type, browser_type, browser_click, browser_snapshot |

## Chat form (`/chat`)

First logged in as demo_user (browser_navigate, browser_type, browser_type, browser_click), then followed the "Go to chat" link (browser_click on `#chat-link`) and took a browser_snapshot of the chat page. Elements used: `#chat-message`, `#send-button`, `#chat-log` and `#chat-error`.

| # | Message | Result shown | MCP tools in order |
|---|---|---|---|
| 1 | Is Dr. Salim available tomorrow? | Appeared in `#chat-log` | browser_type, browser_click, browser_snapshot |
| 2 | (empty) | Message cannot be empty | browser_click, browser_snapshot |
| 3 | A 201-character sentence ("Good morning, my name is Huda and I need to move my Thursday dental check-up ...") | Message too long | browser_type, browser_click, browser_snapshot |

## What I noticed

- The login never says whether the username or the password was wrong: a wrong password and an unknown username both show `Invalid username or password`.
- The injection-style username `' OR '1'='1` is treated as an ordinary unknown username, because the app uses a parameterised SQL query.
- The "Go to chat" link only appears after a successful login, and `/chat` sends you back to the login page without one.
- A snapshot shows the page as text with a `ref` for each element; typing and clicking can use those refs or a CSS selector such as `#username`.

## What does the basic auth header contain?

The browser sends `Authorization: Basic <value>`, where the value is the Base64 encoding of `username:password`; for example `demo_user:secret` becomes `ZGVtb191c2VyOnNlY3JldA==`. Base64 is only an encoding, not encryption, so anyone who can see the request can decode the password. That is why basic auth is only safe over HTTPS.

## Why must hashed passwords be salted?

A salt is a random value stored next to each user's hash and mixed into the password before hashing, so two users with the same password get different hashes. Without it, an attacker who steals the database could look hashes up in precomputed tables (rainbow tables) or crack every user with that password at once. With a salt, every hash has to be attacked separately, and a slow method like scrypt makes each guess expensive.
