import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from utils.cli_args import clean_session_name, is_exit_word, parse_args

MODEL = "gpt-4.1-mini"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.join(BASE_DIR, "sessions")
INDEX_PATH = os.path.join(BASE_DIR, "sessions_index.json")

NAMING_INSTRUCTION = (
    "Give a short title for a chat that starts with the user's message. "
    "Answer with exactly two words and nothing else: no punctuation, no quotes."
)


# ---------- File helpers ----------


def load_json(path, default):
    """Return the JSON stored at path, or default if the file is missing or unreadable."""
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except OSError, json.JSONDecodeError:
        print(f"Sorry, could not read {os.path.basename(path)}.")
        return default


def save_json(path, data):
    """Write data to path as JSON, creating the folder if needed. Return True on success."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except OSError:
        print(f"Sorry, could not save {os.path.basename(path)}.")
        return False


def load_index():
    return load_json(INDEX_PATH, {})


def save_index(index):
    save_json(INDEX_PATH, index)


def session_path(session_name):
    return os.path.join(SESSIONS_DIR, f"{session_name}.json")


def load_history(session_name):
    """Return the saved message list, or None if it cannot be loaded."""
    return load_json(session_path(session_name), None)


def save_history(session_name, history):
    save_json(session_path(session_name), history)


# ---------- Session naming ----------


def ask_session_name(index):
    """Return an existing session name to resume, or None to start a new session."""
    name = input("Session name to resume (press Enter for a new session): ").strip()
    if not name:
        return None
    if name in index:
        return name
    print(f"No session called {name}. Starting a new one.")
    return None


def make_unique(name, index):
    """Add a number to the last word if the name is taken, so old sessions are never reused."""
    unique_name = name
    number = 2
    while unique_name in index or os.path.exists(session_path(unique_name)):
        unique_name = f"{name}{number}"
        number += 1
    return unique_name


def generate_session_name(client, first_question, index):
    """Ask the model for a two-word name based only on the first question."""
    messages = [
        {"role": "system", "content": NAMING_INSTRUCTION},
        {"role": "user", "content": first_question},
    ]
    raw_name = ask_model(client, messages) or ""
    return make_unique(clean_session_name(raw_name), index)


def next_session_id(index):
    return f"session-{len(index) + 1}"


# ---------- Chat ----------


def ask_model(client, messages):
    """Send the messages to the model and return the reply text, or None on failure."""
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages)
        return response.choices[0].message.content.strip()
    except OpenAIError as error:
        print(
            f"Sorry, the model could not be reached ({type(error).__name__}). Please try again."
        )
        return None


def chat_loop(client, session_name, history, index):
    """Ask, answer and save until the user types exit. session_name is None for a new session."""
    while True:
        question = input("\nYou: ").strip()
        if is_exit_word(question):
            print("Goodbye!")
            return
        if not question:
            continue

        if session_name is None:
            session_name = generate_session_name(client, question, index)
            print(f"Session name: {session_name}")

        history.append({"role": "user", "content": question})
        answer = ask_model(client, history)
        if answer is None:
            history.pop()  # keep the saved history consistent: no question without an answer
            if session_name not in index:
                session_name = (
                    None  # nothing saved yet, so the next question names the session
                )
            continue

        print(f"\nAssistant: {answer}")
        history.append({"role": "assistant", "content": answer})

        if session_name not in index:
            index[session_name] = next_session_id(index)
            save_index(index)
        save_history(session_name, history)


def start_session(client):
    """Pick a new or resumed session, then run the chat loop."""
    index = load_index()
    session_name = ask_session_name(index)
    history = []

    if session_name is not None:
        loaded_history = load_history(session_name)
        if loaded_history is None:
            print(f"Could not load {session_name}. Starting a new session.")
            session_name = None
        else:
            history = loaded_history
            print(f"Resumed {session_name} ({len(history)} messages).")

    chat_loop(client, session_name, history, index)


def run_once(client, session_name: str | None, question: str) -> None:
    """Answer one question in a new or named session, save it, and print two lines."""
    index = load_index()

    if session_name is None:
        history = []
        session_name = generate_session_name(client, question, index)
    else:
        if session_name not in index:
            raise SystemExit(f"Error: no session called '{session_name}'.")
        history = load_history(session_name)
        if history is None:
            raise SystemExit(f"Error: could not load session '{session_name}'.")

    history.append({"role": "user", "content": question})
    answer = ask_model(client, history)
    if answer is None:
        raise SystemExit("Error: No answer from the model.")

    history.append({"role": "assistant", "content": answer})
    if session_name not in index:
        index[session_name] = next_session_id(index)
        save_index(index)
    save_history(session_name, history)

    print(f"Session: {session_name}")
    print(f"Assistant: {answer}")


def main():
    session_name, question = parse_args(sys.argv)
    load_dotenv()
    try:
        client = OpenAI()
    except OpenAIError:
        print("Sorry, no OpenAI API key found. Add OPENAI_API_KEY to your .env file.")
        return

    try:
        if question is None:
            start_session(client)
        else:
            run_once(client, session_name, question)
    except KeyboardInterrupt, EOFError:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
