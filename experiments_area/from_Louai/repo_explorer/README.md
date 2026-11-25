# Repo Explorer: LangGraph Branching + GitHub MCP Server

Beginner practice for issue **#315**. A small workflow answers questions about a
public GitHub repository by calling the GitHub MCP server.

## What goes in this folder

| File | Purpose |
| --- | --- |
| `explore_tools.py` | Step 1: connect to the GitHub MCP server, list tools, call one |
| `github_tools.py` | Step 2: `get_open_issues` and `get_recent_commits` async helpers |
| `repo_graph.py` | Step 3: LangGraph workflow with classify + conditional branching |
| `repo_graph.png` | Diagram saved by `draw_mermaid_png()` |

The three `.py` files start empty on purpose. Type them yourself.

## Setup

Python 3.14, dependencies already installed with `uv`.

1. Put your token in `.env` (this file is git-ignored):

   ```env
   GITHUB_TOKEN=github_pat_...
   ```

   Use a fine-grained personal access token with **read-only** access to public
   repositories. `.env.example` shows the shape; never commit `.env`.

2. Sync the environment if you move to another machine:

   ```bash
   cd experiments_area/from_Louai/repo_explorer
   uv sync
   ```

3. Select `.venv/bin/python` as the interpreter in VS Code
   (`Python: Select Interpreter` -> `./.venv`).

## Run

```bash
uv run explore_tools.py
uv run repo_graph.py
```

## My four questions and answers

Fill this in after your first successful run.

| Question | Branch | Answer |
| --- | --- | --- |
| Show open issues | issues | |
| What are the latest commits? | commits | |
| Any new issue today? | issues | |
| Hello | help | |
