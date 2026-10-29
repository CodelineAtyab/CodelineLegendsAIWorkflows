# Scenarios — Issue #257

| # | Timestamp | Scenario name | File | State keys | Nodes | Edges (plain / conditional) | Result matches video? |
|---|---|---|---|---|---|---|---|
| 1 | 1:29:19, continuing after 1:30:00 | Guessing game | `scenario_01_guessing_game.py` | `player_name`, `target_number`, `guesses`, `attempts`, `hint`, `lower_bound`, `upper_bound` | 3 | Plain and conditional | Same higher/lower guessing logic and seven-attempt limit. The random numbers can differ. |
| 2 | 1:31:01 | Simple chat | `scenario_02_simple_chat.py` | `question`, `reply` | 1 | Plain | Same single-node flow, but a simple Python reply replaces the LLM response. |
| 3 | 1:42:54 | Chat memory | `scenario_03_chat_memory.py` | `messages` | 1 | Plain | Previous messages are carried into the next call. The reply uses Python instead of an LLM. |
| 4 | 2:03:20 | Arithmetic tool loop | `scenario_04_tool_loop.py` | `number1`, `number2`, `operation`, `next_operation`, `next_number`, `result`, `reply` | 2 | Plain and conditional | The workflow calculates and returns to the decision node. Operations come from state instead of being selected by an LLM. |
| 5 | 2:28:46 | Document drafter | `scenario_05_document_drafter.py` | `drafts`, `draft_index`, `document`, `saved` | 3 | Plain and conditional | 	Drafts are updated in state. Saving is represented by saved = True instead of writing a text file. |
| 6 | 2:52:09 | Retrieval | `scenario_06_retrieval.py` | `question`, `documents`, `context`, `searched`, `answer` | 2 | Plain and conditional | The workflow searches supplied text and returns a match or a no-match message. Text matching replaces PDF and vector retrieval. |