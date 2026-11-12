# Playwright MCP + LangGraph

Give AI agents a real, **visible** (headed) browser through the Playwright MCP
server, first in Claude Code, then in a LangGraph workflow driven by Gemini.

## What is what

| Tool | What it is | Who decides the clicks |
|---|---|---|
| **Playwright** | Library that controls Chromium / Firefox / WebKit (tests, automation, scraping) | You, in code |
| **Playwright CLI** (`npx playwright`) | `install`, `codegen <url>` (records clicks into code), `test --headed`, `show-trace` | You (or the recorder) |
| **`@playwright/cli`** | Same browser actions as shell commands (`open`, `snapshot`, `click`, `fill`) for coding agents | An AI agent, via the terminal |
| **Playwright MCP** (`@playwright/mcp`) | MCP server exposing ~25 browser tools (`browser_navigate`, `browser_snapshot`, `browser_fill_form`, ...) | An AI agent, via MCP |

Playwright MCP sends the model the page's **accessibility snapshot** (e.g.
`textbox "Email" [ref=e7]`), not screenshots, so a text-only LLM can act on
elements by `ref`. It is headed by default (`--headless` to hide the browser).

## Steps

| Step | File | Idea |
|---|---|---|
| 1 | `step1_playwright_basics.py` | Plain Playwright: you write every step (role/label locators, `expect`) |
| 2 | `.mcp.json` | Claude Code drives the browser through Playwright MCP |
| 3 | `step3_deterministic_graph.py` | LangGraph calls MCP tools in a fixed order, no LLM |
| 4 | `step4_agent_graph.py` | LangGraph ReAct agent: Gemini chooses the MCP tool calls |

```
step 3:  open_page -> read_snapshot -> fill_form -> submit -> verify -> save_evidence
step 4:  agent <-> tools (12 allowed browser tools)  ->  report (JSON)
```

## Setup

```bash
uv sync
uv run playwright install chromium
cp .env.example .env            # add a free key from https://aistudio.google.com/apikey (step 4 only)
uv run python -m http.server 8000 --bind 127.0.0.1 --directory demo_site   # keep running
```

`demo_site/index.html` is a small registration form with validation, used as
the test target. It is served over HTTP because Playwright MCP blocks
`file://` URLs by default.

## Run

```bash
uv run python step1_playwright_basics.py
claude                                   # step 2: run inside this folder, approve the "playwright" server
uv run python step3_deterministic_graph.py [--headless]
uv run python step4_agent_graph.py --preset form-test
uv run python step4_agent_graph.py --preset hotels --city Muscat
uv run python step4_agent_graph.py --task "any browser task"
```

Step 2 example prompt: *"Open http://localhost:8000, register a civil engineer
named Sara, submit, and take a screenshot."*

Screenshots, snapshots and JSON reports go to `outputs/` (git-ignored).

### Sharing one MCP server between Claude Code and LangGraph

```bash
npx @playwright/mcp@0.0.85 --port 8931
claude mcp add --transport http playwright-shared http://localhost:8931/mcp
PLAYWRIGHT_MCP_MODE=http uv run python step3_deterministic_graph.py
```

## Findings

- **Deterministic tests found the real bug, the AI did not.** An empty
  "Years of experience" is accepted (`Number("") === 0`). Step 1/3 scripts
  expose it; the `flash-lite` agent instead reported bugs it *expected* (e.g.
  "-5 accepted") although its own snapshots showed `Years must be 0-60.`
  Use AI to explore, scripts to confirm.
- **Context, not the model, caused the first hallucination.** History
  trimming kept only the *head* of old snapshots, while the result text is at
  the *end*. It now keeps head + tail. Snapshot `.yml` files in `outputs/`
  show exactly what the agent saw.
- **Free-tier Gemini limits shape the design:** ~20 requests/day on
  `gemini-3.8-flash`, 250k input tokens/minute, frequent 503/504 under load.
  Hence: model fallback chain (`GEMINI_MODEL=a,b`), 60 s timeout, tool output
  capped at ~6k tokens with a hint to use `browser_find`, step limit.
- **Least privilege:** the agent gets 12 of 25 tools; `browser_evaluate` and
  `browser_run_code_unsafe` are withheld so injected page text cannot make it
  run arbitrary JavaScript. It is told to decline cookies and stop at CAPTCHAs.
- **Booking.com** loaded real results (prices visible, a sign-in popup, no
  CAPTCHA) but the hotels run did not finish because of Gemini timeouts.
- **"Browser is already in use":** two Playwright MCP instances share one
  Chrome profile by default; the Python client uses `--isolated`.
- On Windows, stdio MCP servers launched with `npx` need `cmd /c`.
