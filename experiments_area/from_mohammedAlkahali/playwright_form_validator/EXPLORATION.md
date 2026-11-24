# Exploring the login and chat forms with Playwright MCP

Tool used: Claude Code with the Playwright MCP server (head mode), app running on http://localhost:8000.

## Login form

| # | Username | Password | Message shown in `#login-result` | MCP tools used (in order) |
|---|----------|----------|----------------------------------|---------------------------|
| 1 | demo_user | (correct password) | Welcome, demo_user | browser_navigate, browser_snapshot, browser_fill_form, browser_click, browser_snapshot |
| 2 | demo_user | wrong-password | Invalid username or password | browser_navigate, browser_snapshot, browser_fill_form, browser_click, browser_snapshot |
| 3 | ghost_user | (correct password) | Invalid username or password | browser_navigate, browser_snapshot, browser_fill_form, browser_click, browser_snapshot |
| 4 | (empty) | (correct password) | Username and password are required | browser_navigate, browser_snapshot, browser_fill_form, browser_click, browser_snapshot |
| 5 | demo_user | (empty) | Username and password are required | browser_navigate, browser_snapshot, browser_fill_form, browser_click, browser_snapshot |
| 6 | ' OR '1'='1 | anything | Invalid username or password | browser_navigate, browser_snapshot, browser_fill_form, browser_click, browser_snapshot |

## Chat form (after logging in as demo_user)

| # | Message | Result shown (`#chat-log` or `#chat-error`) | MCP tools used (in order) |
|---|---------|---------------------------------------------|---------------------------|
| 1 | Hello, I would like to book an appointment | `#chat-log`: Hello, I would like to book an appointment | browser_navigate, browser_snapshot, browser_fill_form, browser_click, browser_snapshot, browser_navigate, browser_snapshot, browser_fill_form, browser_click, browser_snapshot |
| 2 | (empty) | `#chat-error`: Message cannot be empty | browser_navigate, browser_snapshot, browser_fill_form, browser_click, browser_snapshot, browser_navigate, browser_snapshot, browser_click, browser_snapshot |
| 3 | 201-character sentence | `#chat-error`: Message too long | browser_navigate, browser_snapshot, browser_fill_form, browser_click, browser_snapshot, browser_navigate, browser_snapshot, browser_fill_form, browser_click, browser_snapshot |

## What does the basic auth header contain?

The browser sends `Authorization: Basic <text>`, where `<text>` is `username:password` encoded in Base64. Base64 only changes how the text looks; anyone who sees the header can decode it straight back to the username and password. That is why basic auth must only be used over HTTPS.

## Why must hashed passwords be salted?

A salt is a random value stored with each user and mixed into the password before hashing, so two users with the same password get different hashes. Without a salt, an attacker could use a ready-made table of common passwords and their hashes (a rainbow table) to crack every user at once. With a salt they must attack each user separately, and a slow method like scrypt makes each guess expensive.
