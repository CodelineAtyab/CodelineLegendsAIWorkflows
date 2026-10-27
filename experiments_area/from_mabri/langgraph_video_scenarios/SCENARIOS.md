# LangGraph Video Scenarios (#257)

Video: https://www.youtube.com/watch?v=jGg_1h0qzaM (watched from 1:30:00)

| # | Timestamp | Scenario name | File | State keys | Nodes | Edges (plain / conditional) | Result matches video? |
|---|---|---|---|---|---|---|---|
| 01 | ~1:30:00 | Automatic Higher or Lower game (Graph V exercise) | [scenario_01_higher_lower_game.py](scenario_01_higher_lower_game.py) | `player_name`, `guesses`, `attempts`, `lower_bound`, `upper_bound`, `target` | `setup`, `guess`, `hint` | Plain: `START→setup`, `setup→guess`, `guess→hint` / Conditional: `hint→decider→{continue: guess, end: END}` | Yes: both runs guessed the target in 6 attempts (limit is 7) |

## Notes

### Scenario 01: Higher or Lower
- **Bug hit:** `InvalidUpdateError: Expected dict, got continue`. `decider` was registered as a node with `add_node` *and* used as the router in `add_conditional_edges`. A node must return a state-update dict, but a router returns a branch label (`"continue"`/`"end"`).
- **Fix:** remove the `decider` node and attach the router directly to `hint` with `graph.add_conditional_edges("hint", decider, {"continue": "guess", "end": END})`.
- **Takeaway:** routers are not nodes. The first argument to `add_conditional_edges` is the node the branch starts from.
