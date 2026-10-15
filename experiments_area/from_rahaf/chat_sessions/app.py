import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


MODEL = "gpt-4.1-mini"
PROJECT_DIR = Path(__file__).resolve().parent
INDEX_PATH = PROJECT_DIR / "sessions_index.json"
SESSIONS_DIR = PROJECT_DIR / "sessions"
SESSION_NAME_PATTERN = re.compile(r"[a-z0-9]+(?:_[a-z0-9]+)*\Z")


def load_session_index():
    """Load the session-name-to-ID mapping, or return an empty mapping."""
    try:
        with INDEX_PATH.open("r", encoding="utf-8") as file:
            index = json.load(file)
    except FileNotFoundError:
        return {}

    if not isinstance(index, dict) or not all(
        isinstance(name, str) and isinstance(session_id, str)
        for name, session_id in index.items()
    ):
        raise ValueError("The session index must map session names to IDs.")

    return index


def save_session_index(index):
    """Write the current session-name-to-ID mapping to JSON."""
    with INDEX_PATH.open("w", encoding="utf-8") as file:
        json.dump(index, file, indent=2, ensure_ascii=False)


def get_session_path(session_name):
    """Return a safe history-file path for a session name."""
    if not SESSION_NAME_PATTERN.fullmatch(session_name):
        raise ValueError("The saved session name is not valid.")

    return SESSIONS_DIR / f"{session_name}.json"


def load_session_history(session_name):
    """Load and validate a session's list of chat messages."""
    with get_session_path(session_name).open("r", encoding="utf-8") as file:
        messages = json.load(file)

    if not isinstance(messages, list):
        raise ValueError("The session history must be a list of messages.")

    for message in messages:
        role = message.get("role") if isinstance(message, dict) else None
        if (
            not isinstance(message, dict)
            or not isinstance(role, str)
            or role not in {"user", "assistant"}
            or not isinstance(message.get("content"), str)
        ):
            raise ValueError("The session history contains an invalid message.")

    return messages


def save_session_history(session_name, messages):
    """Save a session's full conversation history as JSON."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    with get_session_path(session_name).open("w", encoding="utf-8") as file:
        json.dump(messages, file, indent=2, ensure_ascii=False)


def generate_session_name(client, first_question):
    """Ask the model for a two-word title based only on the first question."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Give this chat a short name based only on the user's question. "
                    "Reply with exactly two words and nothing else."
                ),
            },
            {"role": "user", "content": first_question},
        ],
        temperature=0,
    )

    if not response.choices:
        return "new_session"

    title = response.choices[0].message.content or ""
    words = re.findall(r"[a-z0-9]+", title.lower())

    if len(words) < 2:
        return "new_session"

    return "_".join(words[:2])


def make_unique_session_name(session_name, index):
    """Avoid overwriting a session if the model repeats an existing title."""
    existing_names = set(index)
    if SESSIONS_DIR.exists():
        existing_names.update(
            path.stem for path in SESSIONS_DIR.glob("*.json") if path.is_file()
        )

    if session_name not in existing_names:
        return session_name

    first_word, second_word = session_name.split("_", maxsplit=1)
    suffix = 2
    while f"{first_word}_{second_word}{suffix}" in existing_names:
        suffix += 1

    return f"{first_word}_{second_word}{suffix}"


def create_session_id(index):
    """Return an unused, simple session ID."""
    existing_ids = set(index.values())
    number = len(index) + 1
    while f"session-{number}" in existing_ids:
        number += 1
    return f"session-{number}"


def get_assistant_reply(client, messages):
    """Ask the model to answer using the complete conversation history."""
    response = client.chat.completions.create(model=MODEL, messages=messages)
    if not response.choices:
        return ""
    return response.choices[0].message.content or ""


def main():
    load_dotenv(PROJECT_DIR / ".env")

    try:
        index = load_session_index()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Could not read the session index: {error}")
        return

    try:
        requested_name = input(
            "Enter a session name to resume (press Enter for a new session): "
        ).strip()
    except EOFError:
        print("Chat ended.")
        return

    if requested_name.lower() == "exit":
        print("Chat ended.")
        return

    session_name = None
    messages = []
    is_new_session = True

    if requested_name:
        if requested_name in index:
            session_name = requested_name
            try:
                messages = load_session_history(session_name)
            except (OSError, json.JSONDecodeError, ValueError) as error:
                print(f"Could not load session '{session_name}': {error}")
                return
            is_new_session = False
            print(f"Resumed session: {session_name}")
        else:
            print(f"No session called {requested_name}. Starting a new one.")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is missing. Add it to the project's .env file.")
        return

    client = OpenAI(api_key=api_key)

    while True:
        try:
            question = input("\nYou (or type exit): ").strip()
        except EOFError:
            print("\nChat ended.")
            return

        if question.lower() == "exit":
            print("Chat ended.")
            return

        if not question:
            continue

        creating_this_session = is_new_session

        try:
            if creating_this_session:
                generated_name = generate_session_name(client, question)
                session_name = make_unique_session_name(generated_name, index)
                index[session_name] = create_session_id(index)

            messages.append({"role": "user", "content": question})
            reply = get_assistant_reply(client, messages)
        except OpenAIError:
            if messages and messages[-1].get("role") == "user":
                messages.pop()
            if creating_this_session and session_name is not None:
                index.pop(session_name, None)
                session_name = None
            print("Could not contact OpenAI. Check your API key and connection.")
            return

        messages.append({"role": "assistant", "content": reply})

        try:
            save_session_history(session_name, messages)
            save_session_index(index)
        except (OSError, ValueError) as error:
            print(f"Could not save the conversation: {error}")
            return

        if creating_this_session:
            print(f"New session: {session_name}")
            is_new_session = False

        print(f"\nAssistant: {reply}")


if __name__ == "__main__":
    main()
