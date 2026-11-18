from pathlib import Path
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class GuessingGameState(TypedDict):
    player_name: str
    secret_number: int
    guesses: list[int]
    attempts: int
    lower_bound: int
    upper_bound: int
    current_guess: int
    max_attempts: int
    greeting: str
    hint: Literal["", "higher", "lower", "correct"]
    status: Literal["playing", "won", "out_of_guesses"]


def greet_player(state: GuessingGameState) -> GuessingGameState:
    state["greeting"] = f"Hi there, {state['player_name']}! Let's play higher or lower."
    return state


def make_guess(state: GuessingGameState) -> GuessingGameState:
    guess = (state["lower_bound"] + state["upper_bound"]) // 2
    state["current_guess"] = guess
    state["guesses"].append(guess)
    state["attempts"] += 1
    return state


def evaluate_guess(state: GuessingGameState) -> GuessingGameState:
    guess = state["current_guess"]

    if guess == state["secret_number"]:
        state["hint"] = "correct"
        state["status"] = "won"
    elif guess < state["secret_number"]:
        state["hint"] = "higher"
        state["lower_bound"] = guess + 1
    else:
        state["hint"] = "lower"
        state["upper_bound"] = guess - 1

    if state["status"] != "won" and state["attempts"] >= state["max_attempts"]:
        state["status"] = "out_of_guesses"

    return state


def route_after_guess(state: GuessingGameState) -> str:
    if state["status"] == "playing":
        return "guess_again"
    return "finish"


graph = StateGraph(GuessingGameState)
graph.add_node("greet_player", greet_player)
graph.add_node("make_guess", make_guess)
graph.add_node("evaluate_guess", evaluate_guess)
graph.add_edge(START, "greet_player")
graph.add_edge("greet_player", "make_guess")
graph.add_edge("make_guess", "evaluate_guess")
graph.add_conditional_edges(
    "evaluate_guess",
    route_after_guess,
    {"guess_again": "make_guess", "finish": END},
)

workflow = graph.compile()


def initial_state(secret_number: int, max_attempts: int = 7) -> GuessingGameState:
    return {
        "player_name": "Student",
        "secret_number": secret_number,
        "guesses": [],
        "attempts": 0,
        "lower_bound": 1,
        "upper_bound": 20,
        "current_guess": 0,
        "max_attempts": max_attempts,
        "greeting": "",
        "hint": "",
        "status": "playing",
    }


for game_state in (
    initial_state(secret_number=1),
    initial_state(secret_number=20),
    initial_state(secret_number=1, max_attempts=2),
):
    print(workflow.invoke(game_state))

png_path = Path(__file__).with_suffix(".png")
png_path.write_bytes(
    workflow.get_graph().draw_mermaid_png(max_retries=5, retry_delay=2.0)
)
print(f"Graph saved to {png_path}")
