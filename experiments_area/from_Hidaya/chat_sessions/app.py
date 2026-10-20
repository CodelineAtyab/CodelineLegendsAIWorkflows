import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import APIError, OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4.1-mini"
BASE_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = BASE_DIR / "sessions"
INDEX_FILE = SESSIONS_DIR / "index.json"

History = list[dict[str, str]]


def parse_args(args: list[str]) -> tuple[str | None, str | None]:
    """Parse and validate command-line arguments."""
    if len(args) > 2:
        raise SystemExit(
            "Error: pass a question, or a session name and a question."
        )

    if not args:
        return None, None

    question = args[-1].strip()
    if not question:
        raise SystemExit("Error: the question cannot be empty.")

    if len(args) == 1:
        return None, question

    session_name = args[0].strip()
    if not session_name:
        raise SystemExit("Error: the session name cannot be empty.")

    return session_name, question


def clean_session_name(name: str) -> str:
    """Convert an AI suggestion into a two-word session name."""
    words = re.findall(r"[a-z]+", name.lower())
    if len(words) < 2:
        return "new_session"
    return "_".join(words[:2])


def is_exit_word(text: str) -> bool:
    """Check whether the user wants to end the chat."""
    return text.strip().lower() in ("exit", "quit")


def load_index() -> dict[str, str] | None:
    """Load the saved session index."""
    if not INDEX_FILE.exists():
        return {}

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print("Invalid session index.")
            return None

        return data
    except (OSError, json.JSONDecodeError):
        print("Could not read session index.")
        return None


def save_json(path: Path, data: Any) -> bool:
    """Save data to a JSON file."""
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError:
        return False


def generate_name(client: OpenAI, question: str) -> str:
    """Generate a session name from the first question."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Generate exactly two short English words "
                        "describing the user's question. "
                        "Return only the two words."
                    ),
                },
                {"role": "user", "content": question},
            ],
        )
        text = response.choices[0].message.content or ""
        return clean_session_name(text)
    except APIError:
        return "new_session"


def unique_name(base_name: str, index: dict[str, str]) -> str:
    """Choose a session name that is not already in the index."""
    name = base_name
    number = 2

    while name in index:
        name = f"{base_name.split('_')[0]}_{number}"
        number += 1

    return name


def resolve_session_id(session_name: str, index: dict[str, str]) -> str:
    """Return a saved session ID or exit with an error."""
    if not session_name:
        raise SystemExit("Error: the session name cannot be empty.")

    if session_name not in index:
        raise SystemExit(f"Error: no session named '{session_name}'.")

    return index[session_name]


def get_answer(client: OpenAI, messages: History) -> str | None:
    """Request an AI reply using the conversation history."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        return response.choices[0].message.content or ""
    except APIError:
        return None


def exchange(
    client: OpenAI,
    question: str,
    history: History,
) -> History | None:
    """Return the history with a successful question and reply added."""
    pending_messages = history + [{"role": "user", "content": question}]
    answer = get_answer(client, pending_messages)

    if answer is None:
        return None

    return pending_messages + [{"role": "assistant", "content": answer}]


def load_history(name: str) -> History | None:
    """Load a saved conversation."""
    path = SESSIONS_DIR / f"{name}.json"

    try:
        with open(path, "r", encoding="utf-8") as file:
            history = json.load(file)

        if not isinstance(history, list):
            print("Invalid session history.")
            return None

        return history
    except (OSError, json.JSONDecodeError):
        print("Could not load session history.")
        return None


def chat(
    client: OpenAI,
    name: str,
    history: History,
    index: dict[str, str],
    new_session: bool,
) -> None:
    """Run the interactive chat until the user exits."""
    while True:
        question = input("You: ").strip()

        if is_exit_word(question):
            print("Goodbye!")
            break

        if not question:
            continue

        if new_session:
            name = unique_name(generate_name(client, question), index)
            session_id = f"session-{len(index) + 1}"

        updated_history = exchange(client, question, history)

        if updated_history is None:
            print("Could not get an AI response.")
            continue

        if not save_json(SESSIONS_DIR / f"{name}.json", updated_history):
            print("Could not save the file.")
            return

        if new_session:
            index[name] = session_id

            if not save_json(INDEX_FILE, index):
                print("Could not save the file.")
                return

            print(f"Session created: {name}")
            new_session = False

        history = updated_history
        print(f"AI: {updated_history[-1]['content']}")


def run_once(
    client: OpenAI,
    question: str,
    index: dict[str, str],
    session_name: str | None = None,
) -> None:
    """Answer one question, save the history, and exit."""
    if session_name is None:
        name = unique_name(generate_name(client, question), index)
        session_id = f"session-{len(index) + 1}"
        history = []
    else:
        session_id = resolve_session_id(session_name, index)
        name = session_name
        history = load_history(name)

        if history is None:
            raise SystemExit(f"Error: could not load session '{name}'.")

    updated_history = exchange(client, question, history)

    if updated_history is None:
        raise SystemExit("Error: could not get an AI response.")

    if not save_json(SESSIONS_DIR / f"{name}.json", updated_history):
        raise SystemExit("Error: could not save the session history.")

    if session_name is None:
        index[name] = session_id

        if not save_json(INDEX_FILE, index):
            raise SystemExit("Error: could not save the session index.")

    answer = updated_history[-1]["content"]
    print(f"Session: {name}")
    print(f"Assistant: {' '.join(answer.split())}")


def main() -> None:
    """Start interactive chat or answer a command-line question."""
    session_name, question = parse_args(sys.argv[1:])

    if not API_KEY:
        raise SystemExit("Error: API key not found. Check your .env file.")

    try:
        SESSIONS_DIR.mkdir(exist_ok=True)
    except OSError:
        raise SystemExit("Error: could not create sessions folder.") from None

    index = load_index()
    if index is None:
        raise SystemExit("Error: could not read the session index.")

    if session_name is not None:
        resolve_session_id(session_name, index)

    client = OpenAI(api_key=API_KEY)

    if question is not None:
        run_once(client, question, index, session_name)
        return

    name = input("Enter session name (Enter for new): ").strip()

    if not name:
        chat(client, "", [], index, True)
    elif name in index:
        history = load_history(name)
        if history is not None:
            print(f"Session loaded: {name}")
            chat(client, name, history, index, False)
    else:
        print("Session not found. Starting a new session.")
        chat(client, "", [], index, True)


if __name__ == "__main__":
    main()