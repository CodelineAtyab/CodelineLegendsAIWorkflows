import asyncio
import json
import os
from pathlib import Path
from typing import Any, TypedDict

import openai
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.tools import ToolException
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StdioConnection
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

TEST_PLAN_PATH = Path(__file__).with_name("test_plan.json")
DEFAULT_MODEL = "gpt-4.1-mini"
AGENT_STEP_LIMIT = 30
REQUIRED_ENV_VARS = ["OPENAI_API_KEY", "DEMO_PASSWORD"]
PLAYWRIGHT_SERVER: StdioConnection = {
    "transport": "stdio",
    "command": "npx",
    "args": ["@playwright/mcp@latest", "--isolated"],
}


class TestCaseState(TypedDict):
    case_name: str
    base_url: str
    instruction: str
    expected: str
    user_message: str
    agent_answer: str
    tools_used: list[str]
    actual: str
    message: str
    passed: bool


def prepare_prompt(state: TestCaseState) -> TestCaseState:
    instruction = state["instruction"].replace("{demo_password}", os.environ["DEMO_PASSWORD"])
    state["user_message"] = f"The web app is running at {state['base_url']}.\n{instruction}"
    return state


def make_run_agent_node(agent: Any) -> Any:
    async def run_agent(state: TestCaseState) -> TestCaseState:
        result = await agent.ainvoke(
            {"messages": [("user", state["user_message"])]},
            {"recursion_limit": AGENT_STEP_LIMIT},
        )
        messages = result["messages"]
        tools_used = []
        for message in messages:
            if isinstance(message, AIMessage):
                for tool_call in message.tool_calls:
                    tools_used.append(tool_call["name"])
        state["agent_answer"] = messages[-1].text
        state["tools_used"] = tools_used
        return state

    return run_agent


def parse_verdict(state: TestCaseState) -> TestCaseState:
    verdict_line = ""
    for line in state["agent_answer"].splitlines():
        if line.strip().startswith("VERDICT:"):
            verdict_line = line.strip()

    if not verdict_line:
        state["actual"] = "unknown"
        state["message"] = "the agent did not finish with a VERDICT line"
        return state

    verdict, _, message = verdict_line.removeprefix("VERDICT:").partition("|")
    verdict = verdict.strip().lower()
    state["actual"] = verdict if verdict in ("valid", "invalid") else "unknown"
    state["message"] = message.strip()
    return state


def check_result(state: TestCaseState) -> str:
    if state["actual"] == state["expected"]:
        return "pass"
    return "fail"


def record_pass(state: TestCaseState) -> TestCaseState:
    state["passed"] = True
    return state


def record_fail(state: TestCaseState) -> TestCaseState:
    state["passed"] = False
    return state


def build_workflow(agent: Any) -> CompiledStateGraph:
    graph = StateGraph(TestCaseState)

    graph.add_node("prepare_prompt", prepare_prompt)
    graph.add_node("run_agent", make_run_agent_node(agent))
    graph.add_node("parse_verdict", parse_verdict)
    graph.add_node("record_pass", record_pass)
    graph.add_node("record_fail", record_fail)

    graph.add_edge(START, "prepare_prompt")
    graph.add_edge("prepare_prompt", "run_agent")
    graph.add_edge("run_agent", "parse_verdict")
    graph.add_conditional_edges(
        "parse_verdict", check_result, {"pass": "record_pass", "fail": "record_fail"}
    )
    graph.add_edge("record_pass", END)
    graph.add_edge("record_fail", END)

    return graph.compile()


def load_test_plan(path: Path) -> dict | None:
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Could not find the test plan at {path}")
    except json.JSONDecodeError as error:
        print(f"The test plan is not valid JSON (line {error.lineno}): {error.msg}")
    return None


def print_result(state: dict[str, Any]) -> None:
    status = "PASS" if state["passed"] else "FAIL"
    print(
        f"{status} | {state['case_name']} | expected={state['expected']} "
        f"| actual={state['actual']} | {state['message']}"
    )
    print(f"    tools used: {', '.join(state['tools_used'])}")


async def main() -> None:
    missing = [name for name in REQUIRED_ENV_VARS if not os.environ.get(name)]
    if missing:
        print(f"Please set these environment variables first: {', '.join(missing)}")
        return

    test_plan = load_test_plan(TEST_PLAN_PATH)
    if test_plan is None:
        return

    model = ChatOpenAI(
        model=os.environ.get("MODEL_NAME", DEFAULT_MODEL),
        base_url=os.environ.get("OPENAI_BASE_URL"),
    )
    client = MultiServerMCPClient({"playwright": PLAYWRIGHT_SERVER})

    async with client.session("playwright") as session:
        tools = await load_mcp_tools(session)
        print(f"Loaded {len(tools)} tools: {[tool.name for tool in tools]}\n")

        agent = create_agent(model, tools, system_prompt=test_plan["system_prompt"])
        workflow = build_workflow(agent)
        print(workflow.get_graph().draw_ascii())

        passed_count = 0
        cases = test_plan["cases"]
        for case in cases:
            case_name = case.get("name", "unnamed_case")
            try:
                final_state = await workflow.ainvoke(
                    {
                        "case_name": case_name,
                        "base_url": test_plan["base_url"],
                        "instruction": case["instruction"],
                        "expected": case["expected"],
                    }
                )
            except (KeyError, openai.APIError, ToolException, GraphRecursionError) as error:
                print(f"ERROR | {case_name} | {type(error).__name__}: {error}")
                continue

            print_result(final_state)
            if final_state["passed"]:
                passed_count += 1

        print(f"\n{passed_count}/{len(cases)} passed")


if __name__ == "__main__":
    asyncio.run(main())
