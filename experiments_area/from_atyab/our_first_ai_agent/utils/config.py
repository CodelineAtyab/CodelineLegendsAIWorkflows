# Central configuration: environment loading, tunable settings, and shared paths.

import os
from pathlib import Path

from dotenv import load_dotenv

# Load variables from the local .env file (e.g. OPENAI_API_KEY) into the environment.
load_dotenv()

# --- Model settings ---------------------------------------------------------
MODEL = "gpt-4.1-mini"
EXIT_WORDS = {"exit", "quit"}
MAX_HISTORY_MESSAGES = 5  # how many recent messages get sent back to the model
SYSTEM_PROMPT = {"role": "system", "content": "You are a helpful assistant."}

# --- Shared paths -----------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"


def require_api_key() -> None:
    """Fail fast with a clear message if the API key is missing."""
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Error: OPENAI_API_KEY is not set in your environment.")
