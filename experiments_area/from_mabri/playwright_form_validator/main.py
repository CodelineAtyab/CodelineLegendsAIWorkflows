import json

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


if __name__ == "__main__":
    config = load_config(CONFIG_PATH)
    if config is not None:
        print(f"Configuration loaded successfully: {len(config['cases'])} cases")
    else:
        print("Failed to load configuration.")
