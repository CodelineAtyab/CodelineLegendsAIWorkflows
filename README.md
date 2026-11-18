# ⚒️ Agent Foundry

### Team Codeline Legends

> A shared workshop where the team forges, breaks, and rebuilds real Python projects while learning to build Agentic AI.

---

## What Is This Repo?

**Agent Foundry** is the team's collective playground for Agentic AI development.

Every member learns the same way: by building. So instead of keeping experiments scattered across laptops and random gists, everyone pushes their working examples into this single repository. Each project is a real, runnable Python project — managed with [uv](https://docs.astral.sh/uv/), locked with a `uv.lock`, and self-contained in its own folder.

Think of it as a shared bench full of tools. Someone builds a small calculator agent, someone else wires up a LangGraph workflow, another spins up a Temporal worker or a Playwright form-filling agent. We all get to read it, run it, copy from it, and improve on it.

**The rule of thumb:** if it works, it belongs here. Rough edges are welcome — that's what a lab is for.

---

## What You'll Find Here

The repository grows with the team, but the common themes are:

- **Python fundamentals applied to AI** — small scripts, decorators, data classes, typing and testing
- **LLM API integrations** — chat clients, message handling, session state, token management
- **REST APIs around agents** — FastAPI services, request/response models, streaming endpoints
- **Agent workflows with LangGraph** — nodes, edges, state, conditional routing, multi-agent graphs
- **Durable workflows with Temporal** — activities, workers, retries, long-running agent tasks (often with Docker Compose)
- **Browser automation agents** — Playwright and Playwright MCP driving real forms and pages
- **Tooling and infrastructure** — Docker, n8n, environment configuration, CI linting

---

## Repository Layout

Every member gets their own folder under `experiments_area/`, and every project inside it is independently runnable:

```
experiments_area/
└── from_<your-name>/
    ├── README.md
    └── <project-name>/
        ├── pyproject.toml      # project metadata + dependencies
        ├── uv.lock             # locked, reproducible dependency set
        ├── README.md           # what it does and how to run it
        └── ...                 # source files, tests, data, docker-compose.yml
```

Because each project has its own `pyproject.toml` and lockfile, one member's experiments can never break another member's environment.

---

## Running Someone Else's Example

Every project in this repository runs with uv — no global installs, no virtualenv juggling.

```bash
# install uv once (if you don't have it)
pip install uv

cd experiments_area/from_<name>/<project-name>
uv sync                       # create .venv and install the locked dependencies
uv run python main.py         # or whatever entry point the project README names
```

Prefer to read before you run? Each project's own `README.md` explains what it does and what it needs (API keys, Docker services, sample data, and so on).

---

## Continuous Integration

The GitHub Actions workflow in `.github/workflows/lint.yml` runs on every pull request and is deliberately polite:

1. It walks `experiments_area/` and discovers the `pyproject.toml` projects touched by your PR.
2. It checks only those projects — each in its own directory, against its own locked environment.
3. It runs `ruff` for linting and `mypy` for type checking.

Untouched projects cost zero CI time, and adding a brand-new project folder needs no workflow changes.

---

## License

This repository is released into the public domain under the [**Unlicense**](https://unlicense.org/).

You are free to copy, modify, publish, use, compile, sell, or distribute any of this code, for any purpose, commercial or non-commercial, with no attribution and no warranty. For the full legal text, see the [LICENSE](LICENSE) file.

---

## Contribution Guidelines

### Step 1
Copy the issue ID (ticket-id) from GitHub issues

### Step 2
Goto the repo and git status (Make sure you are on main branch)

### Step 3
git pull (Make sure you are up to date)

### Step 4
Create a new branch (replica of main) from the main branch and check it out (switch to the new branch)
Example: `git branch feature/<ticket-id>-<your-id>-ticket-title`

### Step 5
Checkout the new branch using git checkout 
Example: `git checkout feature/<ticket-id>-<your-id>-ticket-title`

### Step 6
Now do your task

### Step 7
Push your changes (branch) to github by doing:
```
git add *
git commit -m "some-message"
git push 
```
NOTE: (if upstream bracnh is not there then run the --set-upstream command given by git only once)

### Step 8
Got GitHub and click on "Compare & pull request"

### Step 9
Add Reviewers and Click on "Create pull request"

### Step 10
Move the ticket to "Ready for Review"

### Step 11
Wait for atleast 2 approvals from the team

### Step 12
After approvals, Please "SQUASH MERGE"

### Step 13
Go back to the main branch
```
git checkout main
```

### Step 14
Pull the latest chages by doing
```
git pull
```

### Step 15
Repeat the same steps from Step 1 for a new task
