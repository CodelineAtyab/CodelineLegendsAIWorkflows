import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, OpenAI

from utils.cli_args import (
    clean_session_name,
    is_exit_word,
    parse_args,
)

# reads the .env file and loads its values into environment variables
load_dotenv()
# retrieves the API key without hardcoding it
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")

# configures the API client
client = OpenAI(api_key=api_key)


# This function accepts the conversation history and returns the assistant's reply
def chat_with_model(messages):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )

    return response.choices[0].message.content


# Folder and file paths
SESSIONS_DIR = Path(__file__).parent / "sessions"
INDEX_FILE = SESSIONS_DIR / "index.json"


def load_index():
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    if not INDEX_FILE.exists():
        return {}

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError, OSError:
        print("Could not read the session index. Starting with an empty index.")
        return {}


def save_index(index):
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=4)


def load_history(session_name):
    history_file = SESSIONS_DIR / f"{session_name}.json"

    if not history_file.exists():
        return []

    try:
        with open(history_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError, OSError:
        print("Could not read the conversation history.")
        return []


def save_history(session_name, messages):
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    history_file = SESSIONS_DIR / f"{session_name}.json"

    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4)


def choose_session(index):
    while True:
        session_name = input(
            "Enter a session name to resume, or press Enter for a new chat: "
        ).strip()

        if not session_name:
            return None

        if session_name in index:
            print(f"Resuming session: {session_name}")
            return session_name

        print(f"No session called '{session_name}'. Please try again.")


def generate_session_name(question):
    messages = [
        {
            "role": "system",
            "content": (
                "Generate a short name for a chat based on the user's "
                "question. Reply with exactly two words and nothing else."
            ),
        },
        {"role": "user", "content": question},
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )

    name = response.choices[0].message.content.strip()
    words = name.lower().split()

    if len(words) < 2:
        return "new_session"

    return "_".join(words[:2])


# It creates IDs such as session-1, session-2, and so on.
def create_session_id(index):
    return f"session-{len(index) + 1}"


def run_non_interactive(session_name, question):
    """Answer one question, save the session, and exit."""
    index = load_index()

    if session_name is not None:
        if session_name not in index:
            raise SystemExit(f"Error: No session called '{session_name}'.")
        messages = load_history(session_name)
    else:
        messages = []

    try:
        if session_name is None:
            session_name = clean_session_name(generate_session_name(question))

            if session_name in index:
                session_name = f"{session_name}_{len(index) + 1}"

            index[session_name] = create_session_id(index)

        messages.append({"role": "user", "content": question})
        reply = chat_with_model(messages)
        messages.append({"role": "assistant", "content": reply})

        save_index(index)
        save_history(session_name, messages)

    except (APIError, OSError, ValueError) as error:
        if messages and messages[-1]["role"] == "user":
            messages.pop()

        raise SystemExit(f"Error: Could not process the question: {error}") from None

    print(f"Session: {session_name}")
    print(f"Assistant: {reply}")


def run_interactive():
    """Run the existing interactive chat session."""
    index = load_index()
    session_name = choose_session(index)

    if session_name:
        messages = load_history(session_name)

    else:
        messages = []
        question = input("You: ").strip()

        if is_exit_word(question):
            return

        if not question:
            print("Please enter a question.")
            return

        try:
            session_name = clean_session_name(generate_session_name(question))

            if session_name in index:
                session_name = f"{session_name}_{len(index) + 1}"

            index[session_name] = create_session_id(index)
            messages.append({"role": "user", "content": question})

            reply = chat_with_model(messages)
            print(f"Assistant: {reply}")
            messages.append({"role": "assistant", "content": reply})

            save_index(index)
            save_history(session_name, messages)

        except (APIError, OSError, ValueError) as error:
            if messages and messages[-1]["role"] == "user":
                messages.pop()

            print(f"Sorry, something went wrong: {error}")
            return

    while True:
        question = input("You: ").strip()

        if is_exit_word(question):
            print("Chat ended.")
            break

        if not question:
            continue

        messages.append({"role": "user", "content": question})

        try:
            reply = chat_with_model(messages)
            print(f"Assistant: {reply}")
            messages.append({"role": "assistant", "content": reply})
            save_history(session_name, messages)

        except (APIError, OSError, ValueError) as error:
            messages.pop()
            print(f"Sorry, something went wrong: {error}")


def main():
    """Select interactive or non-interactive mode."""
    session_name, question = parse_args(sys.argv)

    if session_name is None and question is None:
        run_interactive()
    else:
        run_non_interactive(session_name, question)


if __name__ == "__main__":
    main()
