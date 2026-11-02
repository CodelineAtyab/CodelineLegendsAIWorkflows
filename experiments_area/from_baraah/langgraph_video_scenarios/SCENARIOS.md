# LangGraph Video Scenarios — Issue #257

## Description

I watched the LangGraph tutorial from 1:30:00 and practised five scenarios using Python and LangGraph.

I learned how to create workflows using State, Nodes, Edges, Chaining, Conditional Edges, and Loops.

## Scenarios

| # | Timestamp | Scenario Name | File | State Keys | Nodes | Edges | Result Matches Video? |
|---|---|---|---|---|---|---|---|
| 1 | 1:31:01 | Basic AI Agent | `scenario_01_basic_ai.py` | question, answer | 1 | Plain | Not verified |
| 2 | 1:42:54 | Chatbot Memory | `scenario_02_chatbot_memory.py` | user_message, history, reply | 3 | Plain | Not verified |
| 3 | 2:03:20 | Tool-Using Agent | `scenario_03_tool_routing.py` | question, tool_result, answer | 2 | Plain + Conditional + Loop | Not verified |
| 4 | 2:28:46 | Document Drafter | `scenario_04_document_drafter.py` | topic, feedback, draft, status | 3 | Plain + Conditional | Not verified |
| 5 | 2:52:09 | RAG Agent | `scenario_05_rag_retrieval.py` | question, passage, answer | 3 | Plain + Conditional | Not verified |

## What I Learned

- How to define shared state using `TypedDict`.
- How to create nodes using Python functions.
- How to connect nodes using `add_edge()`.
- How to use `add_conditional_edges()` to make decisions.
- How to create a loop between the agent and a tool.
- How to run a workflow using `compile()` and `invoke()`.

## Simplifications

- Used normal Python functions instead of AI model calls.
- Used a simple calculator instead of an AI-powered tool.
- Used a Python dictionary instead of a vector database for RAG.
- Focused on understanding LangGraph workflows without external APIs.

## Testing

- [ ] Ran all five scenarios successfully.
- [ ] Tested both paths in conditional workflows.
- [ ] Generated PNG diagrams for each scenario.
- [ ] Compared the scenario results with the video.

## Challenges

My main challenge was understanding how multiple nodes work together, how information is updated between nodes, and how a tool returns its result to the agent in a loop.