import json
from typing import TypedDict

CONFIG_PATH = "test_plan.json"


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
    case_name: str
    instruction: str
    expected: str
    agent_answer: str
    tools_used: list[str]
    actual: str
    message: str
    passed: bool


if __name__ == "__main__":
    config = load_config(CONFIG_PATH)
    if config is not None:
        print(f"Configuration loaded successfully: {len(config['cases'])} cases")
        first_case = config["cases"][0]
        state = TestState(
            case_name=first_case["name"],
            instruction=first_case["instruction"],
            expected=first_case["expected"],
        )
        print(state)
    else:
        print("Failed to load configuration.")