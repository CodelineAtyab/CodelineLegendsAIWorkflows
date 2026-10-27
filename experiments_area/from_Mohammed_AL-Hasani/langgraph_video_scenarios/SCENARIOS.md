# LangGraph Video Scenarios

## Video

- Tutorial: https://www.youtube.com/watch?v=jGg_1h0qzaM
- Required start time: 1:30:00
- Required end time: End of video
- Approach: Rebuild each distinct scenario using plain Python and LangGraph.
- Scope: State, nodes, chaining, edges, and conditional routing.

## Scenario Log

| # | Timestamp | Scenario name | File | State keys | Nodes | Edges | Result verified |
|---|---|---|---|---|---:|---|---|
| 1 | TODO | Two-node message workflow | `scenario_01_two_nodes.py` | `message`, `processed_message` | 2 | Plain | Code runs; comparison pending |
| 2 | TODO | Conditional message workflow | `scenario_02_conditional_message.py` | `question`, `is_processed` | Verify | Conditional + plain | Both branches tested; comparison pending |
| 3 | TODO | Three-node message workflow | `scenario_03_three_nodes.py` | `message` | 3 | Plain | Code runs; comparison pending |

## Testing

- [x] All three current scripts run with `uv run`.
- [x] All three current scripts print the final state as a plain dictionary.
- [x] All three current scripts generate PNG graph diagrams.
- [x] Both branches of the current conditional workflow have been tested.
- [ ] Every scenario from the video has been identified and implemented.
- [ ] Results have been compared with the video.
- [ ] Simplifications from the original video have been documented.

## Notes and Simplifications

The current scripts use simple Python string operations to practise LangGraph state, nodes, chaining, and conditional routing. Confirm which examples correspond to the tutorial and document any differences. Add a separate Python file and PNG for each additional distinct scenario found in the required video section.

Do not mark full video coverage as complete until it has been verified.