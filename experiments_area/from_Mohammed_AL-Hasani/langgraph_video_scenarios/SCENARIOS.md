# LangGraph Video Scenarios

## Video

- Tutorial: https://www.youtube.com/watch?v=jGg_1h0qzaM
- Required section: 1:30:00 to the end
- Reference code: https://github.com/iamvaibhavmehra/LangGraph-Course-freeCodeCamp
- Approach: Rebuild the main agent examples using simple Python and LangGraph.
- Main concepts: State, nodes, edges, conditional routing, loops, and retrieval.

## Scenario Log

| # | Video timestamp | Scenario | File | State keys | Nodes | Workflow | Local result |
|---|---|---|---|---|---:|---|---|
| 1 | 1:32:49 | AI Agent 1 - Simple Bot | `scenario_04_ai_agent_1.py` | `message`, `response` | 1 | Sequential | Passed |
| 2 | 1:43:58 | AI Agent 2 - Chatbot | `scenario_05_ai_agent_2.py` | `message`, `history`, `response` | 1 | Sequential | History updated |
| 3 | 2:12:28 | AI Agent 3 - ReAct Agent concepts | `scenario_06_ai_agent_3.py` | `message`, `numbers`, `result` | 3 | Conditional routing | Calculation and normal paths passed |
| 4 | 2:30:59 | AI Agent 4 - Drafter concepts | `scenario_07_ai_agent_4.py` | `topic`, `draft`, `feedback`, `revision_count`, `saved` | 4 | Review and revision loop | Revision and save flag passed |
| 5 | 2:53:01 | RAG Agent concepts | `scenario_08_rag_agent.py` | `question`, `documents`, `context`, `answer` | 2 | Sequential | Relevant sample document retrieved |

The timestamps identify the published code chapter starts. The scripts are simplified learning implementations, not exact copies of the original agents.

## Additional Practice Examples

These files practise graph fundamentals separately from the five main agent examples.

| File | Purpose |
|---|---|
| `scenario_01_two_nodes.py` | Two sequential nodes |
| `scenario_02_conditional_message.py` | Conditional routing |
| `scenario_03_three_nodes.py` | Three-node workflow |

## Simplifications and Limitations

- **AI Agent 1:** Uses a fixed Python response instead of an LLM.
- **AI Agent 2:** Demonstrates conversation history in the state; it does not maintain persistent memory between independent runs.
- **AI Agent 3:** Demonstrates conditional routing and calculates the sum of numbers in the state. It is not a complete ReAct agent and does not call external tools.
- **AI Agent 4:** Uses sample review feedback, revises the draft once, and marks it as saved in the state. It does not use an LLM, human reviewer, or save the draft to a separate file.
- **RAG Agent:** Uses keyword matching on sample documents instead of PDF loading, embeddings, or a vector database.
- All examples are simplified to practise LangGraph concepts using basic Python.

## Verification Checklist

- [x] All eight scripts have been run successfully.
- [x] Agent 3 calculation and normal paths tested after its latest changes.
- [x] Agent 4 revision loop and save flag tested after its latest changes.
- [x] Ruff formatting and lint checks passed after the latest changes.
- [x] RAG retrieval returned the relevant sample document.
- [x] All eight scripts rerun after the latest changes.
- [ ] Every distinct scenario in the assigned video section compared with the implementation.
- [ ] Final documentation checked against the video.

Do not mark the remaining unchecked items complete until they have been verified.
