import asyncio
import json
import os
import re
import shutil
import sys
from pathlib import Path
from string import Template
from typing import Any, TypedDict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.tools import ToolException
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph
from openai import OpenAIError

CONFIG_PATH = Path(__file__).with_name("test_plan.json")
VERDICT_PATTERN = re.compile(r"^VERDICT:\s*(valid|invalid)\s*\|\s*(.*)$", re.MULTILINE)
MISSING_VERDICT_MESSAGE = "No VERDICT line in the agent answer"

CASE_ERRORS = (KeyError, GraphRecursionError, OpenAIError, ToolException)


class FormTestState(TypedDict):
    case_name: str
    instruction: str
    expected: str
    base_url: str
    user_message: str
    agent_answer: str
    tools_used: list[str]
    actual: str
    message: str
    passed: bool


def load_config(path: Path) -> dict[str, Any]:
    try:
        with open(path, encoding="utf-8") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        sys.exit(f"Config file not found: {path}")
    except json.JSONDecodeError as error:
        sys.exit(f"Config file {path.name} is not valid JSON: {error}")


def new_case_state(case: dict[str, str], base_url: str) -> FormTestState:
    return {
        "case_name": case["name"],
        "instruction": case["instruction"],
        "expected": case["expected"],
        "base_url": base_url,
        "user_message": "",
        "agent_answer": "",
        "tools_used": [],
        "actual": "",
        "message": "",
        "passed": False,
    }


def prepare_prompt(state: FormTestState) -> dict[str, str]:
    instruction = Template(state["instruction"]).substitute(os.environ)
    return {"user_message": f"{instruction}\n\nThe app is running at {state['base_url']}."}


def collect_tools_used(messages: list[Any]) -> list[str]:
    return [
        tool_call["name"]
        for message in messages
        if isinstance(message, AIMessage)
        for tool_call in message.tool_calls
    ]


def make_run_agent(agent: Any, recursion_limit: int):
    async def run_agent(state: FormTestState) -> dict[str, Any]:
        result = await agent.ainvoke(
            {"messages": [("user", state["user_message"])]},
            config={"recursion_limit": recursion_limit},
        )
        return {
            "agent_answer": str(result["messages"][-1].content),
            "tools_used": collect_tools_used(result["messages"]),
        }

    return run_agent


def parse_verdict(state: FormTestState) -> dict[str, str]:
    matches = VERDICT_PATTERN.findall(state["agent_answer"])
    if not matches:
        return {"actual": "unknown", "message": MISSING_VERDICT_MESSAGE}
    verdict, message = matches[-1]
    return {"actual": verdict, "message": message.strip()}


def check_result(state: FormTestState) -> str:
    return "pass" if state["actual"] == state["expected"] else "fail"


def record_pass(state: FormTestState) -> dict[str, bool]:
    return {"passed": True}


def record_fail(state: FormTestState) -> dict[str, bool]:
    return {"passed": False}


def build_workflow(agent: Any, recursion_limit: int):
    graph = StateGraph(FormTestState)

    graph.add_node("prepare_prompt", prepare_prompt)
    graph.add_node("run_agent", make_run_agent(agent, recursion_limit))
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


def print_result(final_state: FormTestState) -> None:
    status = "PASS" if final_state["passed"] else "FAIL"
    print(
        f"{status} | {final_state['case_name']} | expected={final_state['expected']} "
        f"| actual={final_state['actual']} | {final_state['message']}"
    )
    print(f"    tools used: {', '.join(final_state['tools_used'])}")


async def run_cases(config: dict[str, Any]) -> None:
    mcp_server: Any = dict(config["mcp_server"])
    mcp_server["command"] = shutil.which(mcp_server["command"]) or mcp_server["command"]
    mcp_client = MultiServerMCPClient({"playwright": mcp_server})

    async with mcp_client.session("playwright") as session:
        tools = await load_mcp_tools(session)
        print(f"Agent tools: {[tool.name for tool in tools]}")

        model = ChatOpenAI(model=config["model"], temperature=0)
        agent = create_agent(model, tools, system_prompt=config["system_prompt"])
        workflow = build_workflow(agent, config["recursion_limit"])

        passed_count = 0
        for case in config["cases"]:
            try:
                state = new_case_state(case, config["base_url"])
                final_state = await workflow.ainvoke(state)
            except CASE_ERRORS as error:
                print(f"ERROR | {case['name']} | {type(error).__name__}: {error}")
                continue
            print_result(final_state)
            passed_count += final_state["passed"]

        print(f"{passed_count}/{len(config['cases'])} passed")


def main() -> None:
    load_dotenv()
    config = load_config(CONFIG_PATH)
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("Set OPENAI_API_KEY in your environment or in a .env file first.")
    asyncio.run(run_cases(config))


if __name__ == "__main__":
    main()
