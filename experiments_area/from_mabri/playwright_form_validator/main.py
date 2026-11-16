import json
import os
from typing import TypedDict

from dotenv import load_dotenv

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