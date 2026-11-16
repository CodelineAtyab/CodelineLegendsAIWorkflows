# Exploring the login and chat forms with Playwright MCP

Tool used: Claude Code with the Playwright MCP server (head mode), app running on http://localhost:8000.

## Login form

| # | Username | Password | Message shown in `#login-result` | MCP tools used (in order) |
|---|----------|----------|----------------------------------|---------------------------|
| 1 | demo_user | (correct password) | | |
| 2 | demo_user | wrong-password | | |
| 3 | ghost_user | (correct password) | | |
| 4 | (empty) | (correct password) | | |
| 5 | demo_user | (empty) | | |
| 6 | ' OR '1'='1 | anything | | |

## Chat form (after logging in as demo_user)

| # | Message | Result shown (`#chat-log` or `#chat-error`) | MCP tools used (in order) |
|---|---------|---------------------------------------------|---------------------------|
| 1 | Hello, I would like to book an appointment | | |
| 2 | (empty) | | |
| 3 | 201 times the letter a | | |

## What does the basic auth header contain?

The browser sends `Authorization: Basic <text>`, where `<text>` is `username:password` encoded in Base64. Base64 only changes how the text looks; anyone who sees the header can decode it straight back to the username and password. That is why basic auth must only be used over HTTPS.

## Why must hashed passwords be salted?

A salt is a random value stored with each user and mixed into the password before hashing, so two users with the same password get different hashes. Without a salt, an attacker could use a ready-made table of common passwords and their hashes (a rainbow table) to crack every user at once. With a salt they must attack each user separately, and a slow method like scrypt makes each guess expensive.
