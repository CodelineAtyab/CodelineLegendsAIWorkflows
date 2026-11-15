import datetime
from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

FORM_URL = Path("booking_form.html").resolve().as_uri()
TODAY = datetime.datetime.now().astimezone().date()
TOMORROW = (TODAY + datetime.timedelta(days=1)).isoformat()
YESTERDAY = (TODAY - datetime.timedelta(days=1)).isoformat()


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

TEST_CASES = [
    {"case_name": "valid_booking", "name": "Sara", "email": "sara@mail.com", "date": TOMORROW, "expected": "valid"},
    {"case_name": "empty_name", "name": "", "email": "sara@mail.com", "date": TOMORROW, "expected": "invalid"},
    {"case_name": "one_character_name", "name": "S", "email": "sara@mail.com", "date": TOMORROW, "expected": "invalid"},
    {"case_name": "bad_email", "name": "Sara", "email": "sara.mail", "date": TOMORROW, "expected": "invalid"},
    {"case_name": "past_date", "name": "Sara", "email": "sara@mail.com", "date": YESTERDAY, "expected": "invalid"},
    {"case_name": "empty_date", "name": "Sara", "email": "sara@mail.com", "date": "", "expected": "invalid"},
    {"case_name": "deliberate_fail_demo", "name": "Sara", "email": "sara@mail.com", "date": TOMORROW, "expected": "invalid"},
]


def main() -> None:
    """Run every test case through the workflow and print one line per case."""
    passed_count = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        for case in TEST_CASES:
            try:
                result = workflow.invoke({
                    "page": page,
                    "url": FORM_URL,
                    "case_name": case["case_name"],
                    "name": case["name"],
                    "email": case["email"],
                    "date": case["date"],
                    "expected": case["expected"],
                    "actual": "",
                    "message": "",
                    "passed": False,
                })
            except PlaywrightError as error:
                print(f"ERROR | {case['case_name']} | {error.message.splitlines()[0]}")
                continue
            if result["passed"]:
                passed_count += 1
                status = "PASS"
            else:
                status = "FAIL"
            print(f"{status} | {result['case_name']} | expected={result['expected']} | actual={result['actual']} | {result['message']}")
        browser.close()
    print(f"{passed_count}/{len(TEST_CASES)} passed")


if __name__ == "__main__":
    main()
