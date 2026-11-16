import asyncio
import json
import logging
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.exceptions import ModelError
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StdioConnection
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import create_react_agent

# MCP tool schemas carry keys Gemini ignores; hide the one warning per tool.
logging.getLogger("langchain_google_genai._function_utils").setLevel(logging.ERROR)

CONFIG_PATH = "test_plan.json"
DEFAULT_MODEL = "gemini-3.8-flash"
PLAYWRIGHT_MCP_SERVER: StdioConnection = {
    "transport": "stdio",
    "command": "cmd",
    "args": ["/c", "npx", "-y", "@playwright/mcp@0.0.85", "--isolated", "--output-dir", "outputs"],
}
VERDICT_PREFIX = "VERDICT:"
VALID_VERDICTS = ("valid", "invalid")
AGENT_STEP_LIMIT = 50  # each tool call costs two graph steps (model + tool)
# The Gemini client defaults to 6 retries with growing waits and no timeout,
# which makes a run look frozen once the free quota is used up.
MODEL_MAX_RETRIES = 2
MODEL_TIMEOUT_SECONDS = 60


def load_config(path):
    try:
        with open(path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file not found: {path}")
        return None
    except json.JSONDecodeError as error:
        print(f"Error decoding JSON from {path}: {error}")
        return None
    return config


class TestState(TypedDict):
    base_url: str
    case_name: str
    instruction: str
    expected: str
    agent_answer: str
    tools_used: list[str]
    actual: str
    message: str
    passed: bool


def prepare_prompt(state: TestState) -> dict:
    instruction = state["instruction"].format(
        DEMO_USER_PASSWORD=os.environ["DEMO_USER_PASSWORD"]
    )
    return {"instruction": f"Base URL: {state['base_url']}\n{instruction}"}


async def run_agent(state: TestState, config: RunnableConfig) -> dict:
    agent = config["configurable"]["agent"]
    result = await agent.ainvoke(
        {"messages": [("user", state["instruction"])]},
        config={"recursion_limit": AGENT_STEP_LIMIT},
    )
    tools_used = [
        tool_call["name"]
        for message in result["messages"]
        for tool_call in getattr(message, "tool_calls", [])
    ]
    return {"agent_answer": result["messages"][-1].text, "tools_used": tools_used}


def parse_verdict(state: TestState) -> dict:
    for line in state["agent_answer"].splitlines():
        line = line.strip()
        if not line.startswith(VERDICT_PREFIX):
            continue
        verdict, _, message = line.removeprefix(VERDICT_PREFIX).partition("|")
        verdict = verdict.strip().lower()
        if verdict not in VALID_VERDICTS:
            verdict = "unknown"
        return {"actual": verdict, "message": message.strip()}
    return {"actual": "unknown", "message": "no VERDICT line in agent answer"}


def check_result(state: TestState) -> str:
    if state["actual"] == state["expected"]:
        return "pass"
    return "fail"


def record_pass(state: TestState) -> dict:
    return {"passed": True}


def record_fail(state: TestState) -> dict:
    return {"passed": False}


def build_workflow():
    graph = StateGraph(TestState)
    graph.add_node("prepare_prompt", prepare_prompt)
    graph.add_node("run_agent", run_agent)
    graph.add_node("parse_verdict", parse_verdict)
    graph.add_node("record_pass", record_pass)
    graph.add_node("record_fail", record_fail)

    graph.add_edge(START, "prepare_prompt")
    graph.add_edge("prepare_prompt", "run_agent")
    graph.add_edge("run_agent", "parse_verdict")
    graph.add_conditional_edges(
        "parse_verdict",
        check_result,
        {"pass": "record_pass", "fail": "record_fail"},
    )
    graph.add_edge("record_pass", END)
    graph.add_edge("record_fail", END)
    return graph.compile()


def print_result(state: TestState) -> None:
    status = "PASS" if state["passed"] else "FAIL"
    print(
        f"{status} | {state['case_name']} | expected={state['expected']} "
        f"| actual={state['actual']} | {state['message']}"
    )
    print(f"    tools used: {', '.join(state['tools_used'])}")


async def main() -> None:
    load_dotenv()
    config = load_config(CONFIG_PATH)
    if config is None:
        return

    client = MultiServerMCPClient({"playwright": PLAYWRIGHT_MCP_SERVER})
    # One session = one Playwright server = one browser shared by every tool call.
    # client.get_tools() would start a new session (and browser) per tool call.
    async with client.session("playwright") as session:
        tools = await load_mcp_tools(session)
        print(f"Loaded {len(tools)} Playwright MCP tools: {[tool.name for tool in tools]}\n")
        await run_cases(config, tools)


async def run_cases(config: dict, tools: list) -> None:
    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", DEFAULT_MODEL),
        max_retries=MODEL_MAX_RETRIES,
        timeout=MODEL_TIMEOUT_SECONDS,
    )
    agent = create_react_agent(model, tools, prompt=config["system_prompt"])
    workflow = build_workflow()
    run_config = {"configurable": {"agent": agent}}

    passed_count = 0
    for case in config["cases"]:
        try:
            final_state = await workflow.ainvoke(
                {
                    "base_url": config["base_url"],
                    "case_name": case["name"],
                    "instruction": case["instruction"],
                    "expected": case["expected"],
                },
                config=run_config,
            )
        except (KeyError, GraphRecursionError, ModelError) as error:
            print(f"ERROR | {case.get('name', '<unnamed>')} | {type(error).__name__}: {error}")
            continue
        print_result(final_state)
        if final_state["passed"]:
            passed_count += 1

    print(f"\n{passed_count}/{len(config['cases'])} passed")


if __name__ == "__main__":
    asyncio.run(main())