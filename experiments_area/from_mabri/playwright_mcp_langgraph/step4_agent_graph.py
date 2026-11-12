"""Step 4 - Agentic LangGraph: Gemini decides which Playwright MCP tools to call.

    START -> agent <-> tools   (ReAct loop: think, call a browser tool, observe)
               |
               v  (no more tool calls)
             report -> END     (structured JSON report saved to outputs/)

Setup:  copy .env.example to .env and put your free Google AI Studio key in it.
Run:    uv run python step4_agent_graph.py --preset form-test
        uv run python step4_agent_graph.py --preset hotels --city Muscat
        uv run python step4_agent_graph.py --task "any browser task in English"
"""

import argparse
import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field

from mcp_client import playwright_tools

# MCP tool schemas carry "$schema"/"additionalProperties" keys that Gemini
# does not support; the adapter drops them safely but logs one warning per tool.
logging.getLogger("langchain_google_genai._function_utils").setLevel(logging.ERROR)

OUTPUT_DIR = Path("outputs")
MAX_TOOL_CHARS = 25_000  # ~6k tokens per tool result sent back to the LLM
# Comma-separated fallback chain; override with GEMINI_MODEL in .env.
DEFAULT_MODEL = "gemini-3.8-flash,gemini-3.1-flash-lite"

# Only hand the LLM the tools it needs. Leaving out browser_evaluate and
# browser_run_code_unsafe means the model can never run arbitrary JavaScript.
ALLOWED_TOOLS = {
    "browser_navigate",
    "browser_navigate_back",
    "browser_snapshot",
    "browser_find",
    "browser_click",
    "browser_type",
    "browser_fill_form",
    "browser_select_option",
    "browser_press_key",
    "browser_wait_for",
    "browser_handle_dialog",
    "browser_take_screenshot",
}

SYSTEM_PROMPT = """You control a real web browser through Playwright tools.
Rules:
- Before clicking or typing, call browser_snapshot (or browser_find for a
  specific text) and use the exact [ref=eN] values from it as `target`.
- To save tokens, prefer browser_find when you only need some text (e.g. prices).
- Cookie/consent banners: choose the most privacy-preserving option
  ("Decline", "Reject all", "Only necessary"), then continue.
- If you see a CAPTCHA, a robot check or a login wall: STOP, do not try to
  bypass it, and report that you were blocked.
- Never enter real personal data, passwords or payment details.
- Evidence only: report a result or a bug ONLY if you saw it in a snapshot
  taken AFTER the action, and quote the exact page text as evidence. Test
  one change at a time so you know which input caused which message.
- When finished, take a screenshot named outputs/step4_final.png and reply
  with a short plain-text summary of what you did and what you found."""


def hotels_task(city: str) -> str:
    checkin = datetime.now().astimezone().date() + timedelta(days=30)
    checkout = checkin + timedelta(days=2)
    url = (
        "https://www.booking.com/searchresults.html"
        f"?ss={city}&checkin={checkin}&checkout={checkout}"
        "&group_adults=2&no_rooms=1&group_children=0&selected_currency=USD"
    )
    return (
        f"Open {url} . Find hotel prices for {city} from {checkin} to "
        f"{checkout} (2 adults, 1 room). Report the first 5 hotels you see "
        "with their name and the total price shown."
    )


PRESETS = {
    "form-test": (
        "You are a QA tester. Open http://localhost:8000/ . "
        "1) Submit the form empty and note every validation error. "
        "2) Register a software engineer named Omar Al Harthy, email "
        "omar@example.com, 4 years of experience, accept the terms, submit, "
        "and confirm the success message. "
        "3) Try to find one input the form accepts but should reject, and report it."
    ),
}


class Finding(BaseModel):
    name: str = Field(description="Hotel/flight/item name, or test-case name")
    value: str = Field(description="Price with currency, or the observed result")


class Report(BaseModel):
    task_succeeded: bool
    summary: str = Field(description="2-4 sentence summary of what happened")
    findings: list[Finding] = Field(default_factory=list)
    blocked_reason: str | None = Field(
        default=None,
        description="Set if a CAPTCHA, login wall or error stopped the task",
    )


class AgentState(MessagesState):
    report: dict


def compact_history(
    messages: list[AnyMessage], keep_last: int = 3, head: int = 300, tail: int = 900
) -> list[AnyMessage]:
    """Shorten old tool outputs so page snapshots don't blow the token budget.

    The newest observations stay complete. Older ones keep their head (which
    page/URL) AND their tail: in a snapshot the outcome of an action (status
    text, error messages) is usually near the end. Keeping only the head once
    erased the evidence and made the agent invent a bug it had not observed.
    """
    tool_indexes = [i for i, m in enumerate(messages) if isinstance(m, ToolMessage)]
    old = set(tool_indexes[:-keep_last])
    compacted: list[AnyMessage] = []
    for i, message in enumerate(messages):
        if isinstance(message, ToolMessage):
            text = str(message.content)
            if i in old and len(text) > head + tail:
                text = f"{text[:head]}\n...[older output truncated]...\n{text[-tail:]}"
            elif len(text) > MAX_TOOL_CHARS:
                # Even the newest snapshot of a big site (hotel lists!) can be
                # 100k+ tokens - more than the free tier allows per minute.
                text = text[:MAX_TOOL_CHARS] + (
                    "\n...[page too large, truncated. Use browser_find to "
                    "search the page for specific text, e.g. a price or name]"
                )
            message = message.model_copy(update={"content": text})
        compacted.append(message)
    return compacted


def build_graph(tools: list[BaseTool], models: list[str]) -> CompiledStateGraph:
    # Fail fast (no silent retry loops) and fall back to the next model when
    # the free tier answers 503 "high demand" / 504 "deadline exceeded".
    llms = [
        ChatGoogleGenerativeAI(model=m, temperature=0, timeout=60, max_retries=1)
        for m in models
    ]
    llm_with_tools = (
        llms[0]
        .bind_tools(tools)
        .with_fallbacks([llm.bind_tools(tools) for llm in llms[1:]])
    )
    reporter = (
        llms[0]
        .with_structured_output(Report)
        .with_fallbacks([llm.with_structured_output(Report) for llm in llms[1:]])
    )

    async def agent(state: AgentState) -> dict:
        history = compact_history(state["messages"])
        response = await llm_with_tools.ainvoke(
            [SystemMessage(SYSTEM_PROMPT), *history]
        )
        for call in response.tool_calls:  # type: ignore[attr-defined]
            print(f"  -> {call['name']}({json.dumps(call['args'])[:120]})")
        return {"messages": [response]}

    async def report(state: AgentState) -> dict:
        final_answer = state["messages"][-1].text
        result = await reporter.ainvoke(
            [
                SystemMessage(
                    "Turn the browser agent's final answer into the report schema."
                ),
                HumanMessage(final_answer),
            ]
        )
        return {"report": result.model_dump()}  # type: ignore[union-attr]

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent)
    # handle_tool_errors: a failed click becomes a message the LLM can react
    # to (e.g. take a new snapshot) instead of crashing the whole graph.
    graph.add_node("tools", ToolNode(tools, handle_tool_errors=True))
    graph.add_node("report", report)

    graph.add_edge(START, "agent")
    # tools_condition returns "tools" if the last AI message has tool calls,
    # otherwise END - which we redirect to the report node.
    graph.add_conditional_edges(
        "agent", tools_condition, {"tools": "tools", END: "report"}
    )
    graph.add_edge("tools", "agent")
    graph.add_edge("report", END)
    return graph.compile()


async def main(task: str, headless: bool, max_steps: int) -> None:
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise SystemExit(
            "GOOGLE_API_KEY is missing: copy .env.example to .env and add your key."
        )
    models = [m.strip() for m in os.getenv("GEMINI_MODEL", DEFAULT_MODEL).split(",")]
    OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"Models (fallback order): {', '.join(models)}\nTask : {task}\n")
    async with playwright_tools(headless=headless) as all_tools:
        tools = [t for name, t in all_tools.items() if name in ALLOWED_TOOLS]
        app = build_graph(tools, models)
        Path("step4_graph.mmd").write_text(
            app.get_graph().draw_mermaid(), encoding="utf-8"
        )
        final = await app.ainvoke(
            {"messages": [HumanMessage(task)]},
            # Each loop is 2 steps (agent + tools); this caps runaway agents.
            config={"recursion_limit": 2 * max_steps + 3},
        )

    report_path = OUTPUT_DIR / "step4_report.json"
    report_path.write_text(json.dumps(final["report"], indent=2), encoding="utf-8")
    print("\n" + json.dumps(final["report"], indent=2))
    print(f"\nReport saved to {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preset", choices=["form-test", "hotels"])
    group.add_argument("--task", help="free-text browser task")
    parser.add_argument("--city", default="Muscat", help="city for the hotels preset")
    parser.add_argument(
        "--headless", action="store_true", help="hide the browser window"
    )
    parser.add_argument(
        "--max-steps", type=int, default=25, help="max tool-call rounds"
    )
    args = parser.parse_args()

    if args.task:
        chosen_task = args.task
    elif args.preset == "hotels":
        chosen_task = hotels_task(args.city)
    else:
        chosen_task = PRESETS[args.preset]
    asyncio.run(main(chosen_task, args.headless, args.max_steps))
