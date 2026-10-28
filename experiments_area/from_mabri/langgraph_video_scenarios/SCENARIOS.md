# LangGraph Video Scenarios (#257)

Video: https://www.youtube.com/watch?v=jGg_1h0qzaM (watched from 1:30:00)

| # | Timestamp | Scenario name | File | State keys | Nodes | Edges (plain / conditional) | Result matches video? |
|---|---|---|---|---|---|---|---|
| 01 | ~1:30:00 | Automatic Higher or Lower game (Graph V exercise) | [scenario_01_higher_lower_game.py](scenario_01_higher_lower_game.py) | `player_name`, `guesses`, `attempts`, `lower_bound`, `upper_bound`, `target` | `setup`, `guess`, `hint` | Plain: `START→setup`, `setup→guess`, `guess→hint` / Conditional: `hint→decider→{continue: guess, end: END}` | Yes: both runs guessed the target in 6 attempts (limit is 7) |
| 02 | ~2:03:00 | ReAct agent with math tools | [scenario_02_ReAct.py](scenario_02_ReAct.py) | `messages` (`Sequence[BaseMessage]` with `add_messages` reducer) | `our_agent` (LLM `gpt-4o-mini` with tools bound), `tools` (`ToolNode`: `add`, `subtract`, `multiply`, `divide`) | Plain: entry→`our_agent`, `tools→our_agent` / Conditional: `our_agent→should_continue→{continue: tools, end: END}` | Not verified yet (needs `OPENAI_API_KEY` in `.env`) |

## Notes

### Scenario 01: Higher or Lower
- **Bug hit:** `InvalidUpdateError: Expected dict, got continue`. `decider` was registered as a node with `add_node` *and* used as the router in `add_conditional_edges`. A node must return a state-update dict, but a router returns a branch label (`"continue"`/`"end"`).
- **Fix:** remove the `decider` node and attach the router directly to `hint` with `graph.add_conditional_edges("hint", decider, {"continue": "guess", "end": END})`.
- **Takeaway:** routers are not nodes. The first argument to `add_conditional_edges` is the node the branch starts from.
- **Typing:** `target` is `NotRequired[int]` because it's set by `setup`, not passed to `invoke`. Without that, mypy rejects the input dict.

### Scenario 02: ReAct agent
- **Loop:** `our_agent` calls the LLM. If the reply has `tool_calls`, it goes to `tools`, then back to `our_agent`. When there are no more tool calls, the run ends.
- **Typing fixes:**
  - `[system_prompt, *state["messages"]]` instead of `[system_prompt] + state["messages"]`. `list + Sequence` doesn't type-check because `list.__add__` only accepts a `list`, while `*` unpacks any iterable.
  - `should_continue` checks `isinstance(last_message, AIMessage)` before reading `.tool_calls`, since `BaseMessage` has no `tool_calls`.
  - Input uses `HumanMessage(...)` instead of a `("user", "...")` tuple so it matches `AgentState`.

## Checks

```powershell
uv run --frozen --with 'mypy==2.4.0' mypy --ignore-missing-imports .   # type check, same as CI
uvx ruff@0.16.10 check .                                               # lint, same as CI
```

- Use `uv run --with mypy`, not `uvx mypy`. `uvx` runs mypy in an isolated env that can't see langgraph etc. (`import-not-found`), while `uv run` uses the project's env.
- Don't set `python_executable` in `pyproject.toml`. A Windows path like `.venv\Scripts\python.exe` broke CI on Linux (`Invalid python executable`).
- CI failures fixed: `F401` (unused `ToolMessage`), `UP035` (`Sequence` from `collections.abc`), `I001` (import order), `SIM114` (merged `if` branches in `decider`).
