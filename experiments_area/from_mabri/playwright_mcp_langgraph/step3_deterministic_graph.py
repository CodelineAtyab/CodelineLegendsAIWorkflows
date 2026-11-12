"""Step 3 - LangGraph workflow that calls Playwright MCP tools directly (no LLM).

The graph tests the registration form end to end:

    open_page -> read_snapshot -> (refs found?) -> fill_form -> submit -> verify
                                 \\-> fail                                   |
                                  (passed?) -> save_evidence(pass | fail) -> END

Every browser action goes through the MCP server, exactly the same tools an AI
agent would call. Here the *graph* decides the order; in Step 4 the LLM will.

Prerequisite: serve the form ->  uv run python -m http.server 8000 --directory demo_site
Run:                              uv run python step3_deterministic_graph.py
"""

import argparse
import asyncio
import re
from pathlib import Path
from typing import TypedDict

from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from mcp_client import playwright_tools, tool_text

FORM_URL = "http://localhost:8000/"
OUTPUT_DIR = Path("outputs")

# Matches snapshot lines such as:  - textbox "Full name" [ref=e5]
REF_PATTERN = re.compile(r'- (\w+) "([^"]+)"[^\n]*?\[ref=(e\d+)\]')
# Matches the result box, e.g.:   - status [ref=e15]: Registered Sara ...
STATUS_PATTERN = re.compile(r"- status(?: \[ref=e\d+\])?: (.+)")


class FormTestState(TypedDict, total=False):
    url: str
    applicant: dict[str, str]
    expected: str
    snapshot: str
    refs: dict[str, str]  # accessible name -> snapshot ref, e.g. "Email" -> "e7"
    result_text: str
    passed: bool
    error: str
    screenshot: str


REQUIRED_FIELDS = [
    "Full name",
    "Email",
    "Discipline",
    "Years of experience",
    "I accept the terms",
]


def parse_refs(snapshot: str) -> dict[str, str]:
    """Map each element's accessible name to its ref."""
    return {name: ref for _role, name, ref in REF_PATTERN.findall(snapshot)}


def build_graph(tools: dict[str, BaseTool]) -> CompiledStateGraph:
    """Build the graph. Nodes close over the MCP tools of one live session."""

    async def call(tool: str, args: dict) -> str:
        return tool_text(await tools[tool].ainvoke(args))

    async def open_page(state: FormTestState) -> FormTestState:
        await call("browser_navigate", {"url": state["url"]})
        return {}

    async def read_snapshot(state: FormTestState) -> FormTestState:
        snapshot = await call("browser_snapshot", {})
        refs = parse_refs(snapshot)
        missing = [f for f in REQUIRED_FIELDS + ["Register"] if f not in refs]
        error = f"Fields not found on page: {missing}" if missing else ""
        return {"snapshot": snapshot, "refs": refs, "error": error}

    async def fill_form(state: FormTestState) -> FormTestState:
        refs, a = state["refs"], state["applicant"]
        fields = [
            {
                "name": "Full name",
                "type": "textbox",
                "target": refs["Full name"],
                "value": a["name"],
            },
            {
                "name": "Email",
                "type": "textbox",
                "target": refs["Email"],
                "value": a["email"],
            },
            {
                "name": "Discipline",
                "type": "combobox",
                "target": refs["Discipline"],
                "value": a["discipline"],
            },
            {
                "name": "Years",
                "type": "textbox",
                "target": refs["Years of experience"],
                "value": a["years"],
            },
            {
                "name": "Terms",
                "type": "checkbox",
                "target": refs["I accept the terms"],
                "value": "true",
            },
        ]
        await call("browser_fill_form", {"fields": fields})
        return {}

    async def submit(state: FormTestState) -> FormTestState:
        await call(
            "browser_click",
            {"element": "Register button", "target": state["refs"]["Register"]},
        )
        return {}

    async def verify(state: FormTestState) -> FormTestState:
        snapshot = await call("browser_snapshot", {})
        match = STATUS_PATTERN.search(snapshot)
        result_text = match.group(1).strip() if match else ""
        return {"result_text": result_text, "passed": result_text == state["expected"]}

    async def save_evidence(state: FormTestState) -> FormTestState:
        label = "pass" if state.get("passed") else "fail"
        path = OUTPUT_DIR / f"step3_{label}.png"
        await call("browser_take_screenshot", {"filename": str(path)})
        return {"screenshot": str(path)}

    def route_after_snapshot(state: FormTestState) -> str:
        return "save_evidence" if state.get("error") else "fill_form"

    graph = StateGraph(FormTestState)
    for node in (open_page, read_snapshot, fill_form, submit, verify, save_evidence):
        graph.add_node(node.__name__, node)

    graph.add_edge(START, "open_page")
    graph.add_edge("open_page", "read_snapshot")
    graph.add_conditional_edges(
        "read_snapshot", route_after_snapshot, ["fill_form", "save_evidence"]
    )
    graph.add_edge("fill_form", "submit")
    graph.add_edge("submit", "verify")
    graph.add_edge("verify", "save_evidence")
    graph.add_edge("save_evidence", END)
    return graph.compile()


async def main(headless: bool) -> None:
    applicant = {
        "name": "Sara Al Balushi",
        "email": "sara@example.com",
        "discipline": "Civil",
        "years": "7",
    }
    initial: FormTestState = {
        "url": FORM_URL,
        "applicant": applicant,
        "expected": f"Registered {applicant['name']} as a civil engineer.",
    }

    async with playwright_tools(headless=headless) as tools:
        app = build_graph(tools)
        Path("step3_graph.mmd").write_text(
            app.get_graph().draw_mermaid(), encoding="utf-8"
        )
        final = await app.ainvoke(initial)

    print("Refs found :", final.get("refs"))
    if final.get("error"):
        print("ERROR      :", final["error"])
    print("Expected   :", final["expected"])
    print("Got        :", final.get("result_text"))
    print("RESULT     :", "PASS" if final.get("passed") else "FAIL")
    print("Screenshot :", final.get("screenshot"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--headless", action="store_true", help="hide the browser window"
    )
    asyncio.run(main(parser.parse_args().headless))
