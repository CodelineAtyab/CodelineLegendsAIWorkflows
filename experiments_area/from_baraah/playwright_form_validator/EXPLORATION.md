# Issue #291 Part 1 Exploration

This document records the completed exploration of the FastAPI forms using the official Playwright MCP server. No passwords, secrets, or database contents are included.

## Login Tests

### Valid Login

- Input: Username `demo_user`; valid local training password.
- Exact displayed message: `Welcome, demo_user`
- Result: PASS
- Playwright MCP tools, in order: `browser_navigate` -> `browser_evaluate` -> `browser_navigate` -> `browser_evaluate`
- The protected `/chat` page opened successfully.

### Wrong Password

- Input: Known username with an incorrect password.
- Exact displayed message: `Invalid username or password`
- Result: PASS
- Playwright MCP tools, in order: `browser_navigate` -> `browser_snapshot` -> `browser_evaluate` -> `browser_snapshot`

### Unknown Username

- Input: Unknown username with a training password.
- Exact displayed message: `Invalid username or password`
- Result: PASS
- Playwright MCP tools, in order: `browser_navigate` -> `browser_snapshot` -> `browser_evaluate` -> `browser_snapshot`

### Empty Username

- Input: Empty username with a training password.
- Exact displayed message: `Username and password are required`
- Result: PASS
- Playwright MCP tools, in order: `browser_navigate` -> `browser_snapshot` -> `browser_evaluate` -> `browser_snapshot`

### Empty Password

- Input: Known username with an empty password.
- Exact displayed message: `Username and password are required`
- Result: PASS
- Playwright MCP tools, in order: `browser_navigate` -> `browser_snapshot` -> `browser_evaluate` -> `browser_snapshot`

## Chat Tests

The valid login was completed before opening the protected chat page. Each scenario used the recorded setup sequence followed by the scenario interaction.

### Valid Message

- Input: `Hello clinic`
- Exact displayed message: `Hello clinic` in `#chat-log`
- Result: PASS
- Playwright MCP tools, in order: `browser_navigate` -> `browser_evaluate` -> `browser_navigate` -> `browser_evaluate`

### Empty Message

- Input: Empty message.
- Exact displayed message: `Message cannot be empty` in `#chat-error`
- Result: PASS
- Playwright MCP tools, in order: `browser_navigate` -> `browser_evaluate` -> `browser_navigate` -> `browser_evaluate`

### Exactly 201 Characters

- Input: A message containing exactly 201 characters.
- Exact displayed message: `Message too long` in `#chat-error`
- Result: PASS
- Playwright MCP tools, in order: `browser_navigate` -> `browser_evaluate` -> `browser_navigate` -> `browser_evaluate`

## HTTP Basic Authorization

An HTTP Basic Authorization header contains the word `Basic` followed by a Base64-encoded `username:password` pair. Base64 is an encoding, not encryption, so HTTPS is needed to protect those credentials while they are sent.

## Salted Password Hashes

A salt is a unique random value combined with a password before hashing. Salting makes identical passwords produce different hashes and makes precomputed hash or rainbow-table attacks much harder.

## How Playwright MCP Was Used

Playwright MCP opened the local website in a browser, filled the login and chat forms, clicked the relevant buttons, and evaluated the displayed result text. Browser navigation and snapshots/evaluations were used to confirm both visible validation messages and access to the protected `/chat` page.
