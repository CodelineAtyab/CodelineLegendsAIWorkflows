# Scenario Log

Video: [LangGraph Complete Course for Beginners](https://www.youtube.com/watch?v=jGg_1h0qzaM)

The timestamps below are the chapter start times. The video uses OpenAI,
interactive input, file tools, and Chroma. Those runtime dependencies are
represented by deterministic local functions so every exercise runs without
credentials or external services.

| # | Timestamp | Scenario name | File | State keys | Nodes | Edges (plain / conditional) | Result matches video? |
|---|---|---|---|---|---:|---|---|
| 1 | 1:32:49 | Basic AI agent | `scenario_01_basic_agent.py` | `messages` | 1 | Plain | Yes: one response is added |
| 2 | 1:43:58 | Conversational memory agent | `scenario_02_memory_agent.py` | `messages` | 1 | Plain | Yes: prior turns are retained |
| 3 | 2:12:28 | ReAct tool agent | `scenario_03_react_tools.py` | `question`, `first_number`, `second_number`, `answer`, `tool_calls`, `complete` | 2 | Conditional + plain | Yes: tool loop and final answer are exercised with two inputs |
| 4 | 2:30:59 | Document drafting agent | `scenario_04_document_drafter.py` | `request`, `document`, `action`, `save_request`, `complete` | 2 | Conditional + plain | Yes: update and save paths are exercised with two inputs |
| 5 | 2:53:01 | Retrieval-augmented agent | `scenario_05_rag_agent.py` | `question`, `context`, `answer`, `searched` | 2 | Conditional + plain | Yes: retrieval and final response are exercised with two inputs |

## Simplifications

- The chat model is replaced by named Python functions with fixed responses.
- User input is represented by explicit test inputs rather than `input()`.
- The document save tool returns a filename instead of writing outside this project.
- The RAG retriever searches a small in-memory document list instead of using a PDF and Chroma.
