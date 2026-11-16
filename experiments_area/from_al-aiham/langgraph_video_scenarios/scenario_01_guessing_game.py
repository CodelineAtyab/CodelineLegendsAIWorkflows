import random
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class GameState(TypedDict):
    player_name: str
    target_number: int
    guesses: list[int]
    attempts: int
    hint: str
    lower_bound: int
    upper_bound: int


def setup_game(state: GameState) -> GameState:
    state["target_number"] = random.randint(state["lower_bound"], state["upper_bound"])
    return state


def make_guess(state: GameState) -> GameState:
    guess = random.randint(state["lower_bound"], state["upper_bound"])
    state["guesses"].append(guess)
    state["attempts"] += 1
    return state


def give_hint(state: GameState) -> GameState:
    guess = state["guesses"][-1]

    if guess < state["target_number"]:
        state["hint"] = "Too low"
        state["lower_bound"] = guess + 1
    elif guess > state["target_number"]:
        state["hint"] = "Too high"
        state["upper_bound"] = guess - 1
    else:
        state["hint"] = "Correct"

    return state


def choose_next(state: GameState) -> str:
    if state["guesses"][-1] == state["target_number"]:
        return "finish"
    if state["attempts"] >= 7:
        return "finish"
    return "repeat"


graph = StateGraph(GameState)
graph.add_node("setup_game", setup_game)
graph.add_node("make_guess", make_guess)
graph.add_node("give_hint", give_hint)

graph.add_edge(START, "setup_game")
graph.add_edge("setup_game", "make_guess")
graph.add_edge("make_guess", "give_hint")
graph.add_conditional_edges(
    "give_hint", choose_next, {"repeat": "make_guess", "finish": END}
)

workflow = graph.compile()

for player_name in ["Aiham", "Sara"]:
    print(
        workflow.invoke(
            {
                "player_name": player_name,
                "target_number": 0,
                "guesses": [],
                "attempts": 0,
                "hint": "",
                "lower_bound": 1,
                "upper_bound": 20,
            }
        )
    )

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
