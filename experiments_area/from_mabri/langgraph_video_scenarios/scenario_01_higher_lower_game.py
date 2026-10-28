"""
Scenario 01: Automatic Higher or Lower game (Exercise for Graph V, ~1:30:00)

START -> setup -> guess -> hint -> (continue: back to guess | end: END)

- setup: picks a random target between 1 and 20
- guess: picks a number inside [lower_bound, upper_bound], records it, counts the attempt
- hint: says "higher" or "lower" and narrows the bounds accordingly
- decider: "end" when the guess is correct or 7 attempts are used, otherwise "continue"
"""
import random
from pathlib import Path
from typing import NotRequired, TypedDict

from langgraph.graph import StateGraph, START, END


class GameState(TypedDict):
    player_name: str
    guesses: list[int]
    attempts: int
    lower_bound: int
    upper_bound: int
    target: NotRequired[int]  # set by the setup node, not passed in


def setup(state: GameState) -> GameState:
    state["target"] = random.randint(1, 20)
    return state


def guess(state: GameState) -> GameState:
    guess = random.randint(state["lower_bound"], state["upper_bound"])
    state["guesses"].append(guess)
    state["attempts"] += 1
    return state


def hint(state: GameState) -> GameState:
    if state["guesses"][-1] < state["target"]:
        state["lower_bound"] = state["guesses"][-1] + 1
    elif state["guesses"][-1] > state["target"]:
        state["upper_bound"] = state["guesses"][-1] - 1
    return state

def decider(state: GameState) -> str:
    if state["guesses"][-1] == state["target"]:
        return "end"
    elif state["attempts"] >= 7:
        return "end"
    else:
        return "continue"


graph = StateGraph(GameState)

graph.add_node("setup", setup)
graph.add_node("guess", guess)
graph.add_node("hint", hint)

graph.add_edge(START, "setup")
graph.add_edge("setup", "guess")
graph.add_edge("guess", "hint")
graph.add_conditional_edges("hint", decider, {"continue": "guess", "end": END})

workflow = graph.compile()

print(workflow.invoke({"player_name": "Student", "guesses": [], "attempts": 0, "lower_bound": 1, "upper_bound": 20}))
print(workflow.invoke({"player_name": "Mohammed", "guesses": [], "attempts": 0, "lower_bound": 1, "upper_bound": 20}))

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
print(f"Graph saved to {png_path}")
