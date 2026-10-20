import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from openai.types.chat import ChatCompletionMessageParam

from utils.cli_args import clean_session_name, is_exit_word, parse_args

INDEX_FILE = "sessions_index.json"
SESSIONS_DIR = "sessions"
MODEL = "gpt-4.1-mini"


def load_index() -> dict[str, str]:
    """Load the session index, or return an empty index when it is missing."""
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_index(index: dict[str, str]) -> None:
    """Save the mapping of session names to session IDs."""
    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=4)


def load_session(name: str) -> list[ChatCompletionMessageParam]:
    """Load the messages saved for the named session."""
    path = os.path.join(SESSIONS_DIR, f"{name}.json")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_session(name: str, messages: list[ChatCompletionMessageParam]) -> None:
    """Save the session's complete message history as JSON."""
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    path = os.path.join(SESSIONS_DIR, f"{name}.json")

    with open(path, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)


def create_session(client: OpenAI, question: str, index: dict[str, str]) -> str:
    """Generate a session name from the first question and register its ID."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Create a session title based only on the user's question. "
                    "Reply with exactly two words and nothing else."
                ),
            },
            {"role": "user", "content": question},
        ],
    )

    base_name = clean_session_name(response.choices[0].message.content or "")
    name = base_name
    number = 2

    while name in index:
        name = f"{base_name}{number}"
        number += 1

    index[name] = f"session-{len(index) + 1}"
    return name


def get_reply(
    client: OpenAI,
    messages: list[ChatCompletionMessageParam],
    question: str,
) -> str:
    """Send a question with the full history and append the assistant's reply."""
    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
    except OpenAIError:
        messages.pop()
        raise

    reply = response.choices[0].message.content or ""
    messages.append({"role": "assistant", "content": reply})
    return reply


def run_interactive(client: OpenAI, index: dict[str, str]) -> None:
    """Prompt for a session and keep chatting until the user enters exit or quit."""
    requested_name = input("Enter a session name to resume (Enter for new): ").strip()

    session_name: str | None = None
    messages: list[ChatCompletionMessageParam] = []

    if requested_name and requested_name in index:
        session_name = requested_name
        messages = load_session(session_name)
        print(f"Resumed session: {session_name}")
    elif requested_name:
        print(f"No session called {requested_name}. Starting a new one.")

    while True:
        question = input("\nYou: ").strip()

        if is_exit_word(question):
            print("Chat ended.")
            break

        if not question:
            continue

        if session_name is None:
            session_name = create_session(client, question, index)
            print(f"New session: {session_name}")

        reply = get_reply(client, messages, question)
        save_session(session_name, messages)
        save_index(index)
        print(f"\nAssistant: {reply}")


def run_non_interactive(
    client: OpenAI,
    index: dict[str, str],
    session_name: str | None,
    question: str,
) -> None:
    """Answer one question, save the session, and print exactly two lines."""
    messages: list[ChatCompletionMessageParam] = []

    if session_name is None:
        session_name = create_session(client, question, index)
    else:
        messages = load_session(session_name)

    reply = get_reply(client, messages, question)
    save_session(session_name, messages)
    save_index(index)

    # Keep the original reply in JSON, but display it on one terminal line.
    reply_line = " ".join(reply.splitlines())
    print(f"Session: {session_name}")
    print(f"Assistant: {reply_line}")


def main() -> None:
    """Parse command-line arguments and run the requested chat mode."""
    session_name, question = parse_args(sys.argv)

    try:
        index = load_index()

        if (
            question is not None
            and session_name is not None
            and session_name not in index
        ):
            raise SystemExit(f"Error: no session called {session_name}.")

        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing from .env.")

        client = OpenAI(api_key=api_key)

        if session_name is None and question is None:
            run_interactive(client, index)
        elif question is not None:
            run_non_interactive(client, index, session_name, question)

    except OpenAIError as error:
        error_name = type(error).__name__
        status = getattr(error, "status_code", None)
        code = getattr(error, "code", None)

        raise SystemExit(
            f"Error: {error_name} | HTTP status: {status} | API code: {code}"
        ) from None

    except (OSError, ValueError, TypeError, KeyError, IndexError) as error:
        raise SystemExit(f"Error: {error}") from None


if __name__ == "__main__":
    main()
