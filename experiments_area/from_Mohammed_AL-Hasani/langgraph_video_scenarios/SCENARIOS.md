
# LangGraph Video Scenarios

## Video

- Tutorial: https://www.youtube.com/watch?v=jGg_1h0qzaM
- Required start time: 1:30:00
- Required end time: end of video
- Approach: Rebuild each distinct scenario using plain Python and LangGraph.
- Scope: State, nodes, chaining, edges, and conditional routing.
- Simplifications: Replace LLM calls, tools, async code, decorators,
  generators, FastAPI, Temporal, and Qdrant with plain Python where needed.

## Scenario Log

| # | Timestamp | Scenario name | File | State keys | Nodes | Edges (plain / conditional) | Result matches video? |
|---|---|---|---|---|---:|---|---|
| 1 | 1:30:xx | Replace with actual scenario | `scenario_01_two_nodes.py` | `message`, `processed_message` | 2 | plain | Pending verification |
| 2 | Actual timestamp | Replace with actual scenario | `scenario_02_conditional_message.py` | `question`, `is_processed` | 2 | conditional + plain | Pending verification |

## Testing

- [ ] Each scenario runs with `uv run`.
- [ ] Each scenario prints the final state as a plain dictionary.
- [ ] Each scenario saves its own PNG graph diagram.
- [ ] Every conditional branch has been tested.
- [ ] Results have been compared with the video.
- [ ] Simplifications from the original video have been documented.

## Notes and Simplifications

Document the actual simplifications made for each scenario here.
Do not mark a scenario complete until it has been run and checked.
