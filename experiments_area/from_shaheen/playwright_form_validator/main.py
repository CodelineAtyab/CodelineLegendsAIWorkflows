from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph


class BookingState(TypedDict):
    page: Any
    url: str
    case_name: str
    name: str
    email: str
    date: str
    expected: str
    actual: str
    message: str
    passed: bool


def open_form(state: BookingState) -> BookingState:
    """Go to the booking form URL."""
    state["page"].goto(state["url"])
    return state


def fill_form(state: BookingState) -> BookingState:
    """Fill the name, email and date fields from the state."""
    state["page"].fill("#name", state["name"])
    state["page"].fill("#email", state["email"])
    state["page"].fill("#date", state["date"])
    return state


def submit_form(state: BookingState) -> BookingState:
    """Click the submit button."""
    state["page"].click("#submit")
    return state


def read_outcome(state: BookingState) -> BookingState:
    """Read the result message and decide if the booking was valid."""
    message = state["page"].inner_text("#result")
    if message.startswith("Booking confirmed"):
        state["actual"] = "valid"
    else:
        state["actual"] = "invalid"
    state["message"] = message
    return state


def check_result(state: BookingState) -> str:
    """Return "pass" when the actual outcome matches the expected one."""
    if state["actual"] == state["expected"]:
        return "pass"
    else:
        return "fail"


def record_pass(state: BookingState) -> BookingState:
    """Mark the test case as passed."""
    state["passed"] = True
    return state


def record_fail(state: BookingState) -> BookingState:
    """Mark the test case as failed and save a screenshot."""
    state["passed"] = False
    state["page"].screenshot(path=f"screenshots/{state['case_name']}.png")
    return state


graph = StateGraph(BookingState)
graph.add_node("open_form", open_form)
graph.add_node("fill_form", fill_form)
graph.add_node("submit_form", submit_form)
graph.add_node("read_outcome", read_outcome)
graph.add_node("record_pass", record_pass)
graph.add_node("record_fail", record_fail)
graph.add_edge(START, "open_form")
graph.add_edge("open_form", "fill_form")
graph.add_edge("fill_form", "submit_form")
graph.add_edge("submit_form", "read_outcome")
graph.add_conditional_edges("read_outcome", check_result, {"pass": "record_pass", "fail": "record_fail"})
graph.add_edge("record_pass", END)
graph.add_edge("record_fail", END)
workflow = graph.compile()
