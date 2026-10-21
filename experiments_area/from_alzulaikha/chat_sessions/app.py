"""Interactive and one shot chatbot backed by the OpenAI chat completions API."""

import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from openai.types.chat import ChatCompletionMessageParam

from utils.cli_args import clean_session_name, is_exit_word, parse_args

SESSION_INDEX_FILE = "session_index.json"
SESSIONS_DIR = "sessions"
MODEL_NAME = "gpt-4.1-mini"


def load_session_index(path: str = SESSION_INDEX_FILE) -> dict:
    """Read the session index, or return an empty index when it is missing."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not read the session index: {error}")
        return {}
    if not isinstance(data, dict):
        print("Session index is not a dictionary. Starting with an empty index.")
        return {}
    return data


def save_session_index(index: dict, path: str = SESSION_INDEX_FILE) -> None:
    """Write the session index to disk."""
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(index, file, indent=2)
    except (OSError, TypeError) as error:
        print(f"Could not save the session index: {error}")


def load_session_history(path: str) -> list[ChatCompletionMessageParam]:
    """Read the saved messages of one session."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not read session history: {error}")
        return []

    if not isinstance(data, list):
        print("Session history is not a list. Starting with an empty history.")
        return []
    return data


def save_session_history(history: list[ChatCompletionMessageParam], path: str) -> None:
    """Write the messages of one session to disk."""
    try:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=2)
    except (OSError, TypeError) as error:
        print(f"Could not save session history: {error}")


def get_openai_client() -> OpenAI | None:
    """Build an OpenAI client, or return None when no key is available."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("No API key found. Add OPENAI_API_KEY to your .env file.")
        return None

    try:
        return OpenAI(api_key=api_key)
    except OpenAIError as error:
        print(f"Could not create the OpenAI client: {error}")
        return None


def unique_session_name(base_name: str, index: dict) -> str:
    """Return a session name that is not already in the index.

    If base_name is taken, append _2, _3, and so on until the name is free.
    This prevents a new session from overwriting an existing conversation.
    """
    if base_name not in index:
        return base_name
    counter = 2
    while f"{base_name}_{counter}" in index:
        counter += 1
    return f"{base_name}_{counter}"


def generate_two_word_session_name(client: OpenAI, question: str) -> str:
    """Ask the model for a short two word session name."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "Return exactly two words and nothing else.",
                },
                {"role": "user", "content": question},
            ],
        )
    except OpenAIError as error:
        print(f"Could not generate a session name: {error}")
        return "new_session"

    return clean_session_name(response.choices[0].message.content or "")


def ask_model(client: OpenAI, history: list[ChatCompletionMessageParam], question: str) -> str | None:
    """Send the history plus one question and return the answer."""
    history.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=history,
        )
    except OpenAIError as error:
        print(f"API error: {error}")
        history.pop()
        return None

    answer = response.choices[0].message.content or ""
    history.append({"role": "assistant", "content": answer})
    return answer


def run_interactive(client: OpenAI, index: dict) -> None:
    """Ask for a session name and keep chatting until the user types exit or quit."""
    session_name = input(
        "Enter a session name (or press Enter to start a new session): "
    ).strip()

    history: list[ChatCompletionMessageParam] = []
    session_path = None

    if session_name in index:
        session_path = os.path.join(SESSIONS_DIR, f"{session_name}.json")
        history = load_session_history(session_path)
    elif session_name:
        print(f"No session called {session_name}. Starting a new one.")

    if session_path is None:
        first_question = input("You: ").strip()

        if is_exit_word(first_question):
            print("Goodbye!")
            return

        session_name = unique_session_name(
            generate_two_word_session_name(client, first_question), index
        )
        session_path = os.path.join(SESSIONS_DIR, f"{session_name}.json")
        history = []

        answer = ask_model(client, history, first_question)
        if answer is None:
            return

        print("Assistant:", answer)
        save_session_history(history, session_path)
        index[session_name] = session_name
        save_session_index(index)

    while True:
        user_input = input("You: ").strip()

        if is_exit_word(user_input):
            print("Goodbye!")
            break
        if not user_input:
            continue

        answer = ask_model(client, history, user_input)
        if answer is None:
            continue

        print("Assistant:", answer)
        save_session_history(history, session_path)
        save_session_index(index)


def run_non_interactive(
    client: OpenAI,
    index: dict,
    session_name: str | None,
    question: str,
) -> None:
    """Answer one question, save the session and print the result."""
    history: list[ChatCompletionMessageParam] = []

    if session_name is None:
        session_name = unique_session_name(
            generate_two_word_session_name(client, question), index
        )
    else:
        session_path = os.path.join(SESSIONS_DIR, f"{session_name}.json")
        history = load_session_history(session_path)

    answer = ask_model(client, history, question)
    if answer is None:
        return

    session_path = os.path.join(SESSIONS_DIR, f"{session_name}.json")
    save_session_history(history, session_path)
    index[session_name] = session_name
    save_session_index(index)

    print(f"Session: {session_name}")
    print(f"Assistant: {' '.join(answer.splitlines())}")


def main() -> None:
    """Run the interactive chat or the one question command line mode."""
    session_name, question = parse_args(sys.argv)

    index = load_session_index()

    if question is not None and session_name is not None and session_name not in index:
        raise SystemExit(f"Error: no session called {session_name}.")

    client = get_openai_client()
    if client is None:
        return

    if question is None:
        run_interactive(client, index)
    else:
        run_non_interactive(client, index, session_name, question)


if __name__ == "__main__":
    main()
