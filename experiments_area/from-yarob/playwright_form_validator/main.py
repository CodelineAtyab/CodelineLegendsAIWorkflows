import asyncio
import json
import os
import re
from string import Template
from typing import TypedDict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph
from openai import OpenAIError

CONFIG_PATH = "test_plan.json"
VERDICT_PATTERN = re.compile(r"VERDICT:\s*(valid|invalid)\s*\|\s*(.*)", re.IGNORECASE)
PASSWORD_VARIABLE_SUFFIX = "_PASSWORD"


class CaseState(TypedDict):
    case_name: str
    instruction: str
    expected: str
    base_url: str
    user_prompt: str
    agent_answer: str
    tools_used: list[str]
    actual: str
    message: str
    passed: bool


def load_config(path: str) -> dict | None:
    try:
        with open(path, encoding="utf-8") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Config file '{path}' was not found. Create it next to main.py.")
    except json.JSONDecodeError as error:
        print(f"Config file '{path}' is not valid JSON (line {error.lineno}, column {error.colno}): {error.msg}")
    return None


def test_passwords() -> dict[str, str]:
    return {name: value for name, value in os.environ.items() if name.endswith(PASSWORD_VARIABLE_SUFFIX)}


def prepare_prompt(state: CaseState) -> dict:
    instruction = Template(state["instruction"]).safe_substitute(test_passwords())
    user_prompt = f"The app under test runs at {state['base_url']}.\n{instruction}"
    return {"user_prompt": user_prompt}


def parse_verdict(state: CaseState) -> dict:
    verdicts = VERDICT_PATTERN.findall(state["agent_answer"])
    if not verdicts:
        return {"actual": "unknown", "message": "agent answer has no VERDICT line"}
    actual, message = verdicts[-1]
    return {"actual": actual.lower(), "message": message.strip()}


def check_result(state: CaseState) -> str:
    return "pass" if state["actual"] == state["expected"] else "fail"


def record_pass(state: CaseState) -> dict:
    return {"passed": True}


def record_fail(state: CaseState) -> dict:
    return {"passed": False}


def build_workflow(agent, agent_step_limit: int):
    async def run_agent(state: CaseState) -> dict:
        result = await agent.ainvoke(
            {"messages": [("user", state["user_prompt"])]},
            {"recursion_limit": agent_step_limit},
        )
        messages = result["messages"]
        tools_used = [tool_call["name"] for message in messages for tool_call in getattr(message, "tool_calls", [])]
        return {"agent_answer": messages[-1].text, "tools_used": tools_used}

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


def print_case_result(state: CaseState) -> None:
    status = "PASS" if state["passed"] else "FAIL"
    print(f"{status} | {state['case_name']} | expected={state['expected']} | actual={state['actual']} | {state['message']}")
    print(f"    tools used: {', '.join(state['tools_used'])}")


async def run_cases(config: dict) -> None:
    server = config["mcp_server"]
    client = MultiServerMCPClient({server["name"]: server["connection"]})
    async with client.session(server["name"]) as session:
        tools = await load_mcp_tools(session)
        print(f"Loaded {len(tools)} MCP tools: {[tool.name for tool in tools]}")

        model = ChatOpenAI(model=config["model"], temperature=0)
        agent = create_agent(model, tools, system_prompt=config["system_prompt"])
        workflow = build_workflow(agent, config["agent_step_limit"])
        print(workflow.get_graph().draw_ascii())

        cases = config["cases"]
        passed_count = 0
        for case in cases:
            case_name = case.get("name", "<unnamed case>")
            try:
                final_state = await workflow.ainvoke({
                    "case_name": case_name,
                    "instruction": case["instruction"],
                    "expected": case["expected"],
                    "base_url": config["base_url"],
                })
            except KeyError as error:
                print(f"ERROR | {case_name} | case is missing the key {error}")
                continue
            except GraphRecursionError:
                print(f"ERROR | {case_name} | agent did not finish within {config['agent_step_limit']} steps")
                continue
            except OpenAIError as error:
                print(f"ERROR | {case_name} | OpenAI request failed: {type(error).__name__}: {error}")
                continue
            print_case_result(final_state)
            passed_count += final_state["passed"]

        print(f"{passed_count}/{len(cases)} passed")


async def main() -> None:
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set. Add it to the .env file (see .env.example).")
        return
    config = load_config(CONFIG_PATH)
    if config is None:
        return
    await run_cases(config)


if __name__ == "__main__":
    asyncio.run(main())
