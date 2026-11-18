import asyncio
import json
import os
import re
from pathlib import Path
from string import Template
from typing import Literal, TypedDict

from langchain.agents import create_agent
from langchain_core.tools import ToolException
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph
from mcp import McpError
from openai import OpenAIError


class TestState(TypedDict):
    case_name: str
    instruction: str
    expected: Literal["valid", "invalid"]
    base_url: str
    prompt: str
    agent_answer: str
    tools_used: list[str]
    actual: Literal["valid", "invalid", "unknown"]
    message: str
    passed: bool


def prepare_prompt(state: TestState) -> dict:
    instruction = Template(state["instruction"]).substitute(os.environ)
    return {"prompt": f"Base URL: {state['base_url']}\nTest goal: {instruction}"}


def parse_verdict(state: TestState) -> dict:
    verdict = re.search(
        r"^VERDICT: (valid|invalid|unknown) \| ([^\r\n]+)$",
        state["agent_answer"].strip(),
        re.MULTILINE,
    )
    if verdict is None:
        return {"actual": "unknown", "message": "Missing or malformed VERDICT line"}
    return {"actual": verdict.group(1), "message": verdict.group(2).strip()}


def check_result(state: TestState) -> Literal["pass", "fail"]:
    return "pass" if state["actual"] == state["expected"] else "fail"


def record_pass(state: TestState) -> dict:
    return {"passed": True}


def record_fail(state: TestState) -> dict:
    return {"passed": False}


def build_workflow(agent, recursion_limit: int):
    async def run_agent(state: TestState) -> dict:
        result = await agent.ainvoke(
            {"messages": [("user", state["prompt"])]},
            config={"recursion_limit": recursion_limit},
        )
        messages = result["messages"]
        return {
            "agent_answer": messages[-1].text,
            "tools_used": [
                call["name"]
                for message in messages
                for call in getattr(message, "tool_calls", [])
            ],
        }

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
        "parse_verdict", check_result, {"pass": "record_pass", "fail": "record_fail"}
    )
    graph.add_edge("record_pass", END)
    graph.add_edge("record_fail", END)
    return graph.compile()


async def run_cases(workflow, plan: dict) -> None:
    passed = 0
    for case in plan["cases"]:
        try:
            result = await workflow.ainvoke({
                "case_name": case["name"],
                "instruction": case["instruction"],
                "expected": case["expected"],
                "base_url": plan["base_url"],
            })
        except (OpenAIError, GraphRecursionError, McpError, ToolException,
                TimeoutError, ConnectionError, OSError, KeyError, ValueError) as error:
            reason = " ".join(str(error).split())
            print(f"ERROR | {case['name']} | {type(error).__name__}: {reason}")
            continue
        passed += result["passed"]
        status = "PASS" if result["passed"] else "FAIL"
        print(
            f"{status} | {result['case_name']} | expected={result['expected']} | "
            f"actual={result['actual']} | {result['message']}"
        )
        print(f"    tools used: {', '.join(result['tools_used'])}")
    print(f"{passed}/{len(plan['cases'])} passed")


def load_test_plan() -> dict:
    with open(Path(__file__).with_name("test_plan.json"), encoding="utf-8") as file:
        return json.load(file)


async def main() -> None:
    try:
        plan = await asyncio.to_thread(load_test_plan)
    except FileNotFoundError:
        print("Config not found: put test_plan.json beside main.py.")
        return
    except json.JSONDecodeError as error:
        print(f"Invalid JSON in test_plan.json at line {error.lineno}: {error.msg}")
        return

    if not os.environ.get("OPENAI_API_KEY"):
        print("Set OPENAI_API_KEY in your environment before running the agent.")
        return

    client = MultiServerMCPClient({"playwright": plan["mcp_server"]})
    async with client.session("playwright") as session:
        tools = await load_mcp_tools(session)
        model = ChatOpenAI(
            model=plan["model"], temperature=0, max_retries=0,
            model_kwargs={"parallel_tool_calls": False},
        )
        agent = create_agent(model, tools, system_prompt=plan["system_prompt"])
        workflow = build_workflow(agent, plan["recursion_limit"])
        await run_cases(workflow, plan)


if __name__ == "__main__":
    asyncio.run(main())
