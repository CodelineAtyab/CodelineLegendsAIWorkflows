# Scenario log — Issue #257

## Scope

Video: https://www.youtube.com/watch?v=jGg_1h0qzaM

Required interval: **1:30:00 to the end**. The issue's original URL has
`t=1919s` (31:59); follow the written 1:30:00 requirement.

This package covers the six main graph applications identified in the chapter
list and source-code review: the guessing exercise already in progress at
1:30:00, followed by five agent examples. Introduction, coding and testing
sections for one application are grouped in one row. This is not a claim that
every video frame or minor demonstration was independently viewed and verified.

Filenames 04–09 are retained from the earlier reference package. The earlier
conditional-arithmetic, two-decisions and random-loop files (01–03) precede
the required interval and are not included here.

## Scenarios

| # | Timestamp | Scenario name | File | State keys | Nodes | Edges (plain / conditional) | Result matches video? |
|---|---|---|---|---|---|---|---|
| 1 | Exercise begins 1:29:19 and continues after 1:30:00 | Automatic higher/lower guessing game | `scenario_04_guessing_game.py` | `player_name, target_number, guesses, attempts, hint, lower_bound, upper_bound` | 3 | Plain + conditional loop | Reproduces automatic guesses, bound updates, success and the seven-attempt limit. Fixed seeds make example runs repeatable; exact random values and wording are not a video-output match. Direct functions checked; actual graph/PNG pending. |
| 2 | Intro 1:31:01; code 1:32:49 | Simple chatbot without memory | `scenario_05_simple_chat.py` | `question, reply` | 1 | Plain | Model response replaced with an echo. Two independent invocations; not identical generated text. Direct functions checked; actual graph/PNG pending. |
| 3 | Intro 1:42:54; code 1:43:58 | Chatbot with conversation history and a log | `scenario_06_chat_memory.py` | `messages` | 1 | Plain | Earlier user/assistant messages are retained and written to `logging.txt`. Model response replaced with a summary of the questions. Direct functions and log write checked; actual graph/PNG pending. |
| 4 | Intro 2:03:20; code 2:12:28 | ReAct-style arithmetic tool loop | `scenario_07_tool_loop.py` | `steps, step_index, result, answer` | 2 | Plain + conditional loop | Model/tool selection replaced with operations in state. Cases cover single/repeated addition, addition then multiplication, subtraction, and no-tool text. Direct functions checked; actual graph/PNG pending. |
| 5 | Intro 2:28:46; code 2:30:59 | Document drafting and saving | `scenario_08_document_drafter.py` | `actions, action_index, action, document, filename, saved` | 3 | Plain + conditional loop | Model-directed editing replaced with update/save actions in state. Update twice then save; save existing content. Actual file writes checked directly; graph/PNG pending. |
| 6 | Intro 2:52:09; code 2:53:01; testing 3:06:15 | Retrieval and answer | `scenario_09_retrieval.py` | `query, documents, context, retrieval_done, answer` | 2 | Plain + conditional loop | PDF/embeddings/vector search/model replaced with supplied text and substring matching. Match/no-match cases checked directly; graph/PNG pending. Not semantic RAG or a reproduction of stock-document answers. |

## Example inputs and expected behavior

- **Guessing game:** two seeds are supplied outside the nodes. In the local
  Python 3.13.5 direct-function check, seed 0 found target 13 on attempt 5;
  seed 40 reached seven unsuccessful attempts for target 15. Both runs
  exercised `repeat` and `finish`. Verify outcomes in the required Python 3.14
  environment instead of assuming every Python version gives the same sequence.
- **Simple chat:** `Hello` and `What is LangGraph?` each receive an independent
  `You asked: ...` reply. No conversation memory is implied.
- **Memory:** the second response includes both supplied questions. Four messages
  remain after two turns. The final conversation is written to `logging.txt`.
- **Tool loop:** single addition gives 14; repeated additions give 18; the
  `(40 + 12) * 6` case gives 312 and includes supplied canned conversational
  text; subtraction gives 7; the no-tool case returns supplied text directly.
  `left: None` means reuse the preceding arithmetic result. All operations
  are supplied outside the nodes. Both `tool` and `finish` routes are exercised.
- **Drafter:** update/update/save creates `draft_one.txt`; saving supplied existing
  content creates `draft_two.txt`. The save function adds `.txt` when omitted.
  Both `update` and `save` routes are exercised.
- **Retrieval:** `LangGraph` returns the matching supplied passage; `unknown`
  returns `No matching document.` Each request follows `retrieve`, then `finish`.

All input cases above are demonstrations of the adapted code. They are not
claims that every model-generated answer or incidental video prompt was reproduced.

## Plain-Python substitutions

The issue excludes LLM calls, async code, decorators, generators, FastAPI,
Temporal and Qdrant. These scripts use no API key and make no LLM requests.

- Echo/history-based replies replace model responses.
- State-supplied operations and actions replace model-selected tool calls.
- Ordinary functions replace tool decorators and ToolNode.
- Full state is returned without message reducers or streaming.
- Supplied strings and substring matching replace PDF loading, embeddings,
  vector storage and model-generated answers.
- Scripted example inputs replace interactive prompts so each file prints final
  dictionaries and finishes. Multiple requests still demonstrate memory behavior.

## Runtime verification status

Checks performed on this revised package:

- Python syntax and static graph structure: passed on **Python 3.13.5**.
- Direct function execution: **15 input cases passed**.
- Conversation-log writing and both document writes: passed in a temporary folder.
- Actual LangGraph `compile()` / `invoke()` runs: **not verified here**.
- Python **3.14** runtime: **not verified here**.
- `draw_mermaid_png()` requests and PNG output: **not verified here**.

The checking environment could not resolve the download hosts for Python or PyPI.
No placeholder PNGs, fabricated lockfile, or simulated LangGraph run is included.
Install the declared dependencies, run all six scripts, inspect the PNGs, and
update each pending result with what was actually observed on your machine.

The default `draw_mermaid_png()` uses Mermaid.ink over the network. The message
processing does not call an LLM, but PNG generation still needs internet access.

## Complete before submission

- [ ] Run all six scripts with Python 3.14 and the real LangGraph package.
- [ ] Inspect the final dictionaries and verify every conditional route.
- [ ] Open all six generated PNGs and confirm their node/edge structure.
- [ ] Confirm `logging.txt`, `draft_one.txt`, and `draft_two.txt` are generated correctly.
- [ ] Finish watching the required interval and reconcile any additional demonstrations.
- [ ] Replace pending log entries with actual runtime and video-comparison findings.
- [ ] Confirm the correct branch, project location, dependencies and generated lockfile.

This is an AI-generated reference. It does not establish that the user watched
the video or independently wrote the syntax. Do not mark the assignment's
self-written-syntax checkbox based on this reference.

## Sources used for scope and adaptations

- Issue: https://github.com/CodelineAtyab/CodelineLegendsAIWorkflows/issues/257
- Video: https://www.youtube.com/watch?v=jGg_1h0qzaM
- Chapter list reproduced from the video description: https://podwise.ai/episodes/6519081
- Indexed transcript: https://sozai.app/transcript/langgraph-complete-course-beginners-python/
- Instructor repository: https://github.com/iamvaibhavmehra/LangGraph-Course-freeCodeCamp
- Instructor sources: `Exercises/Exercise_Graph5.ipynb`, `Agents/Agent_Bot.py`,
  `Agents/Memory_Agent.py`, `Agents/ReAct.py`, `Agents/Drafter.py`, `Agents/RAG_Agent.py`.
- Graph API: https://docs.langchain.com/oss/python/langgraph/use-graph-api
