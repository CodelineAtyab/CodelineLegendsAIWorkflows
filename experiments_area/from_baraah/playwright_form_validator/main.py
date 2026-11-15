import asyncio
import json
import re
from pathlib import Path
from typing import Any, TypedDict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")


class TestState(TypedDict, total=False):
    case_name: str
    instruction: str
    expected: str
    expected_message: str
    prompt: str
    training_password: str
    agent_answer: str
    tools_used: list[str]
    actual: str
    message: str
    passed: bool


def load_config() -> dict[str, Any] | None:
    try:
        return json.loads((BASE_DIR / "test_plan.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Config error: {error}")
        return None


def content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )
    return str(content)


def redact(text: str, secret: str) -> str:
    return text.replace(secret, "[redacted]") if secret else text


async def main() -> None:
    config = load_config()
    if config is None:
        return

    import os

    training_password = os.getenv("DEMO_USER_PASSWORD")
    if not training_password:
        print("ERROR | configuration | DEMO_USER_PASSWORD is not available")
        return

    client = MultiServerMCPClient(
        {
            "playwright": {
                "transport": "stdio",
                "command": "npx.cmd",
                "args": [
                    "-y",
                    "@playwright/mcp",
                    "--browser",
                    "chromium",
                    "--headless",
                    "--isolated",
                    "--timeout-navigation",
                    "30000",
                ],
            }
        }
    )
    model = ChatOpenAI(model="gpt-4.1-mini")
    active_agent: Any = None

    async def prepare_prompt(state: TestState) -> dict[str, str]:
        needs_credentials = state["case_name"] in {
            "valid_login",
            "valid_chat",
            "empty_chat",
            "long_chat",
        }
        credentials = ""
        if needs_credentials:
            credentials = (
                f"Use username demo_user and password {state['training_password']} "
                "through the login form. Never repeat the password in your answer."
            )
        prompt = (
            f"{config['base_url']}\n{state['instruction']}\n{credentials}\n"
            f"The expected visible result is exactly: {state.get('expected_message', '')}. "
            "Use the exact username specified by the test case. Start from a fresh page, "
            "inspect the result selector after submission, and do not infer success from "
            "navigation alone. End with exactly one line in this format: "
            "VERDICT: valid | exact observed message or VERDICT: invalid | exact observed "
            "message or VERDICT: error | short reason. Do not add explanation after that line."
        )
        return {"prompt": prompt}

    async def run_agent(state: TestState) -> dict[str, Any]:
        if active_agent is None:
            return {
                "agent_answer": "VERDICT: error | browser agent was not initialized",
                "tools_used": [],
            }
        try:
            result = await active_agent.ainvoke(
                {"messages": [{"role": "user", "content": state["prompt"]}]}
            )
            messages = result.get("messages", [])
            answer = content_text(messages[-1].content) if messages else ""
            tools_used = [
                call.get("name", "unknown")
                for message in messages
                for call in getattr(message, "tool_calls", [])
            ]
            return {
                "agent_answer": redact(answer, state.get("training_password", "")),
                "tools_used": tools_used,
            }
        except Exception:  # noqa: BLE001 - a browser failure must become VERDICT: error
            return {
                "agent_answer": "VERDICT: error | browser interaction failed",
                "tools_used": [],
            }

    async def parse_verdict(state: TestState) -> dict[str, str]:
        matches = re.findall(
            r"^\s*VERDICT:\s*(valid|invalid|error)\s*(?:\|\s*(.*))?$",
            state.get("agent_answer", ""),
            flags=re.IGNORECASE | re.MULTILINE,
        )
        if not matches:
            return {"actual": "error", "message": "Missing VERDICT line"}
        actual, message = matches[-1]
        return {"actual": actual.lower(), "message": message.strip()}

    def check_result(state: TestState) -> str:
        expected_message = state.get("expected_message", "")
        message_matches = state.get("message", "").strip() == expected_message
        return (
            "pass"
            if state.get("actual") == state.get("expected") and message_matches
            else "fail"
        )

    async def record_pass(state: TestState) -> dict[str, bool]:
        return {"passed": True}

    async def record_fail(state: TestState) -> dict[str, bool]:
        return {"passed": False}

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
    workflow = graph.compile()

    passed = 0
    for case in config["cases"]:
        result: dict[str, Any] = {}
        for attempt in range(2):
            try:
                async with client.session("playwright") as session:
                    tools = await load_mcp_tools(session)
                    active_agent = create_agent(
                        model,
                        tools,
                        system_prompt=config["system_prompt"],
                    )
                    result = await workflow.ainvoke(
                        {
                            **case,
                            "case_name": case["name"],
                            "training_password": training_password,
                        }
                    )
                if result.get("actual") != "error":
                    break
            except Exception:  # noqa: BLE001 - one failed case must not stop the suite
                result = {
                    "actual": "error",
                    "message": "browser session failed",
                    "passed": False,
                    "tools_used": [],
                    "expected": case["expected"],
                }
            if attempt == 0:
                await asyncio.sleep(2)

        status = "PASS" if result.get("passed") else "FAIL"
        passed += int(bool(result.get("passed")))
        print(
            f"{status} | {case['name']} | expected={result.get('expected')} | "
            f"actual={result.get('actual')} | {result.get('message', '')}"
        )
        print("    tools used: " + ", ".join(result.get("tools_used", [])))
        await asyncio.sleep(1)
    print(f"{passed}/{len(config['cases'])} passed")


if __name__ == "__main__":
    asyncio.run(main())
