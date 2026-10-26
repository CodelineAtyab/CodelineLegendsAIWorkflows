import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, OpenAI
from openai.types.chat import ChatCompletionMessageParam

from utils.cli_args import clean_session_name, is_exit_word, parse_args

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4.1-mini"
BASE_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = BASE_DIR / "sessions"
INDEX_FILE = SESSIONS_DIR / "index.json"


def to_api_message(message: dict[str, str]) -> ChatCompletionMessageParam:
    """Convert a saved message into the message format the OpenAI API expects."""
    if message["role"] == "assistant":
        return {"role": "assistant", "content": message["content"]}

    return {"role": "user", "content": message["content"]}


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
    except OSError, json.JSONDecodeError:
        print("Could not read session index.")
        return None


def save_json(path: Path, data: object) -> bool:
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
        name = f"{base_name}_{number}"
        number += 1

    return name


def resolve_session_id(session_name: str, index: dict[str, str]) -> str:
    """Return a saved session ID or exit with an error."""
    if not session_name:
        raise SystemExit("Error: the session name cannot be empty.")

    if session_name not in index:
        raise SystemExit(f"Error: no session named '{session_name}'.")

    return index[session_name]


def get_answer(client: OpenAI, messages: list[dict[str, str]]) -> str | None:
    """Request an AI reply using the conversation history."""
    api_messages: list[ChatCompletionMessageParam] = [
        to_api_message(message) for message in messages
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=api_messages,
        )
        return response.choices[0].message.content or ""
    except APIError:
        return None


def exchange(
    client: OpenAI,
    question: str,
    history: list[dict[str, str]],
) -> list[dict[str, str]] | None:
    """Return the history with a successful question and reply added."""
    pending_messages = history + [{"role": "user", "content": question}]
    answer = get_answer(client, pending_messages)

    if answer is None:
        return None

    return pending_messages + [{"role": "assistant", "content": answer}]


def load_history(name: str) -> list[dict[str, str]] | None:
    """Load a saved conversation."""
    path = SESSIONS_DIR / f"{name}.json"

    try:
        with open(path, "r", encoding="utf-8") as file:
            history = json.load(file)

        if not isinstance(history, list):
            print("Invalid session history.")
            return None

        return history
    except OSError, json.JSONDecodeError:
        print("Could not load session history.")
        return None


def chat(
    client: OpenAI,
    name: str,
    history: list[dict[str, str]],
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
    history: list[dict[str, str]] = []

    if session_name is None:
        name = unique_name(generate_name(client, question), index)
        session_id = f"session-{len(index) + 1}"
    else:
        session_id = resolve_session_id(session_name, index)
        name = session_name
        saved_history = load_history(name)

        if saved_history is None:
            raise SystemExit(f"Error: could not load session '{name}'.")

        history = saved_history

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
    session_name, question = parse_args(sys.argv)

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
