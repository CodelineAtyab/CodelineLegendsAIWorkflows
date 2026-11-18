import asyncio
import json
import os
from typing import Any, TypedDict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.exceptions import ModelError
from langchain_core.messages import AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

CONFIG_FILE = "test_plan.json"
PLAYWRIGHT_MCP_ARGS = ["@playwright/mcp@latest", "--headless", "--isolated", "--browser", "msedge"]


class CaseState(TypedDict):
    agent: Any
    base_url: str
    case_name: str
    instruction: str
    expected: str
    prompt: str
    agent_answer: str
    tools_used: list[str]
    actual: str
    message: str
    passed: bool


def prepare_prompt(state: CaseState) -> CaseState:
    """Build the user message for the agent from the base URL and the case instruction."""
    instruction = state["instruction"].replace("{demo_password}", os.environ["DEMO_PASSWORD"])
    state["prompt"] = f"The app runs at {state['base_url']}. {instruction}"
    return state


async def run_agent(state: CaseState) -> CaseState:
    """Let the agent test the app, then keep its final answer and the tools it called."""
    result = await state["agent"].ainvoke({"messages": [("user", state["prompt"])]})
    tools_used: list[str] = []
    for message in result["messages"]:
        if isinstance(message, AIMessage):
            for tool_call in message.tool_calls:
                tools_used.append(tool_call["name"])
    state["agent_answer"] = result["messages"][-1].content
    state["tools_used"] = tools_used
    return state


def parse_verdict(state: CaseState) -> CaseState:
    """Read the VERDICT line of the agent's answer into actual and message."""
    state["actual"] = "unknown"
    state["message"] = "the agent gave no VERDICT line"
    for line in state["agent_answer"].splitlines():
        if line.strip().startswith("VERDICT:"):
            verdict, _, message = line.strip().removeprefix("VERDICT:").partition("|")
            if verdict.strip() in ("valid", "invalid"):
                state["actual"] = verdict.strip()
            state["message"] = message.strip()
    return state


def check_result(state: CaseState) -> str:
    """Return "pass" when the actual result matches the expected one, else "fail"."""
    if state["actual"] == state["expected"]:
        return "pass"
    else:
        return "fail"


def record_pass(state: CaseState) -> CaseState:
    """Mark the case as passed."""
    state["passed"] = True
    return state


def record_fail(state: CaseState) -> CaseState:
    """Mark the case as failed."""
    state["passed"] = False
    return state


def build_workflow() -> CompiledStateGraph:
    """Connect the nodes into a graph and compile it."""
    graph = StateGraph(CaseState)
    graph.add_node("prepare_prompt", prepare_prompt)
    graph.add_node("run_agent", run_agent)
    graph.add_node("parse_verdict", parse_verdict)
    graph.add_node("record_pass", record_pass)
    graph.add_node("record_fail", record_fail)
    graph.add_edge(START, "prepare_prompt")
    graph.add_edge("prepare_prompt", "run_agent")
    graph.add_edge("run_agent", "parse_verdict")
    graph.add_conditional_edges("parse_verdict", check_result, {"pass": "record_pass", "fail": "record_fail"})
    graph.add_edge("record_pass", END)
    graph.add_edge("record_fail", END)
    return graph.compile()


def load_config(path: str) -> dict | None:
    """Read the test plan from a JSON file, or print why it could not be read."""
    try:
        with open(path, encoding="utf-8") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Config file not found: {path}")
    except json.JSONDecodeError as error:
        print(f"Config file {path} is not valid JSON: {error}")
    return None


async def main() -> None:
    """Load the config, give the Playwright MCP tools to the agent and run every case."""
    load_dotenv()
    config = load_config(CONFIG_FILE)
    if config is None:
        return
    if "OPENAI_API_KEY" not in os.environ or "DEMO_PASSWORD" not in os.environ:
        print("Please set the OPENAI_API_KEY and DEMO_PASSWORD environment variables first.")
        return
    client = MultiServerMCPClient({
        "playwright": {"transport": "stdio", "command": "npx", "args": PLAYWRIGHT_MCP_ARGS},
    })
    async with client.session("playwright") as session:
        tools = await load_mcp_tools(session)
        print(f"Tools: {[tool.name for tool in tools]}")
        model = ChatOpenAI(model="gpt-4.1-mini")
        agent = create_agent(model, tools, system_prompt=config["system_prompt"])
        workflow = build_workflow()
        passed_count = 0
        for case in config["cases"]:
            try:
                result = await workflow.ainvoke({
                    "agent": agent,
                    "base_url": config["base_url"],
                    "case_name": case["name"],
                    "instruction": case["instruction"],
                    "expected": case["expected"],
                })
            except (KeyError, ModelError) as error:
                print(f"ERROR | {case.get('name')} | {type(error).__name__}: {error}")
                continue
            status = "PASS" if result["passed"] else "FAIL"
            print(
                f"{status} | {result['case_name']} | expected={result['expected']} "
                f"| actual={result['actual']} | {result['message']}"
            )
            print(f"    tools used: {', '.join(result['tools_used'])}")
            if result["passed"]:
                passed_count += 1
        print(f"{passed_count}/{len(config['cases'])} passed")


if __name__ == "__main__":
    asyncio.run(main())
