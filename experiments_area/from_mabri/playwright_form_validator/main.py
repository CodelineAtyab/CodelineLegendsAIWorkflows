import json
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph

CONFIG_PATH = "test_plan.json"
VERDICT_PREFIX = "VERDICT:"
VALID_VERDICTS = ("valid", "invalid")


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
    result = await agent.ainvoke({"messages": [("user", state["instruction"])]})
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


if __name__ == "__main__":
    load_dotenv()
    config = load_config(CONFIG_PATH)
    if config is not None:
        print(f"Configuration loaded successfully: {len(config['cases'])} cases")
        first_case = config["cases"][0]
        state = TestState(
            base_url=config["base_url"],
            case_name=first_case["name"],
            instruction=first_case["instruction"],
            expected=first_case["expected"],
        )
        print(state)
    else:
        print("Failed to load configuration.")