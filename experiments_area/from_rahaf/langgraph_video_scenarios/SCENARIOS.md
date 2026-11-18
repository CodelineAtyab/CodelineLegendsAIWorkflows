# Scenario log

The course moves from the automatic higher/lower guessing exercise into five
agent examples. The exercise prompt starts at **1:29:25**, just before the
requested 1:30:00 start, and its description continues past 1:30.

| # | Timestamp | Scenario name | File | State keys | Nodes | Edges (plain / conditional) | Result matches video? |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | 1:29:25–1:31:05 | Automatic higher/lower guessing loop | `scenario_01_number_guessing_loop.py` | `player_name`, `secret_number`, `guesses`, `attempts`, `lower_bound`, `upper_bound`, `current_guess`, `max_attempts`, `greeting`, `hint`, `status` | 3 | 3 / 2 labels (`guess_again`, `finish`) | Partial: the bounded loop and default 7-attempt cap are represented; the target is supplied in state and midpoint guesses keep the run deterministic. Both hint directions are exercised, plus a 2-attempt run to test the cap. |
| 2 | 1:31:01 | Stateless chatbot | `scenario_02_stateless_chatbot.py` | `messages`, `reply` | 1 | 2 / none | Partial: same single-turn graph shape; a deterministic echo replaces the LLM response. |
| 3 | 1:42:54 | Chatbot with conversation history | `scenario_03_conversation_memory.py` | `messages`, `reply` | 1 | 2 / none | Partial: conversation history is carried between invocations; deterministic name recall replaces the LLM. |
| 4 | 2:03:20 | ReAct calculator and tool loop | `scenario_04_react_calculator.py` | `tool_plan`, `next_tool_index`, `pending_call`, `result`, `route`, `messages` | 2 | 2 / 2 labels (`tool`, `done`) | Partial: the agent/tool/agent loop and conditional finish are preserved; tool selection is supplied as a structured plan instead of an LLM call. |
| 5 | 2:28:46 | Drafter with feedback and save | `scenario_05_document_drafter.py` | `draft`, `feedback`, `feedback_index`, `pending_feedback`, `next_action`, `output_path`, `saved`, `saved_path` | 3 | 3 / 2 labels (`revise`, `save`) | Partial: feedback, revision, and save branches are modeled; scripted feedback and plain file I/O replace the LLM and tools. |
| 6 | 2:52:09 | Retrieval-augmented stock report Q&A | `scenario_06_local_rag.py` | `question`, `documents`, `retrieved_documents`, `retrieval_done`, `next_step`, `answer` | 3 | 3 / 2 labels (`retrieve`, `answer`) | Partial: retrieval and answer routing are exercised with matching and non-matching questions; local keyword matching replaces embeddings, vector storage, and the LLM. |

## Adaptations and practice note

- All examples use plain Python and local data; they need no API keys, model
  calls, interactive input, embeddings, or vector database.
- Each script prints the final `workflow.invoke(...)` state and writes a
  Mermaid PNG beside the script. The drafter also saves its demonstration
  output to `draft_output.txt`.
- The replies and retrieval behavior intentionally differ from model output,
  so the rows above are marked partial rather than claiming exact output
  parity.
- The course transcript and reference examples were reviewed, but the full
  video was not personally watched end-to-end; the viewing checklist remains
  incomplete.
- This implementation was prepared with coding assistance. It does not satisfy
  the issue's personal requirement to hand-type the basic syntax without AI;
  manually retype and review the examples before marking that learning
  checklist item complete.
