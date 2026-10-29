# LangGraph Video Scenarios (#257)

Video: https://www.youtube.com/watch?v=jGg_1h0qzaM (watched from 1:30:00 to the end)

| # | Timestamp | Scenario name | File | State keys | Nodes | Edges (plain / conditional) | Result matches video? |
|---|---|---|---|---|---|---|---|
| 1 | 1:31:01 | Simple bot (no memory) | scenario_01_simple_bot.py | messages | 1 | plain | Yes, same graph. LLM replaced with an echo reply |
| 2 | 1:42:54 | Chatbot with memory | scenario_02_chatbot_memory.py | messages | 1 | plain | Yes, same graph. LLM replaced with a reply that quotes the first message; logging.txt not written |
| 3 | 2:12:28 | ReAct agent (agent and tools loop) | scenario_03_react_agent.py | messages, pending_tools, result | 2 | plain + conditional (loop) | Yes, same graph. The LLM's tool choice is replaced by a pending_tools list; add and multiply are plain functions without @tool |
| 4 | 2:28:46 | Drafter (human in the loop) | scenario_04_drafter.py | user_commands, current_command, document, saved_as, messages | 2 | plain + conditional (loop) | Yes, same graph. input() replaced by a user_commands list; save records the file name instead of writing a .txt |
| 5 | 2:52:09 | RAG agent | scenario_05_rag_agent.py | question, keyword, documents, searched, retrieved, answer | 2 | plain + conditional (loop) | Yes, same graph. PDF, embeddings and Chroma replaced by a list of sentences and a keyword search |

## Branches tested

- Scenario 3: a question that needs tools (40 + 12, then × 6 = 312) and one that needs none (goes straight to END).
- Scenario 4: ends after a save, and ends when the commands run out without a save.
- Scenario 5: keyword found in the documents, and keyword not found.

## Parts of the video without a scenario

- 2:05:00 AI Agent 3 Prerequisite: theory only (Annotated, Sequence, add_messages, message types).
- 3:06:15 RAG Agent Testing: more questions against scenario 5, covered by its two inputs.

## Notes

- No LLM, async, decorators or databases, as the task requires. Each replacement is listed in the table above.
