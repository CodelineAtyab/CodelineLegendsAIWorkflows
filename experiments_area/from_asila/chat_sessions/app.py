# app.py
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load OPENAI_API_KEY from .env. The key stays out of your code.
load_dotenv()

# One shared client used for both naming and chat replies.
client = OpenAI()

# Required model for both calls.
MODEL = "gpt-4.1-mini"

# Index: session name -> string session id
INDEX_FILE = Path("sessions.json")

# Conversation files: sessions/<name>.json
SESSIONS_DIR = Path("sessions")


def load_index():
    """Read the mapping of session names to string IDs."""
    try:
        if not INDEX_FILE.exists():
            return {}
        with INDEX_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            print("Session index was not valid. Starting fresh.")
            return {}
        return data
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not read the session index: {error}")
        return {}


def save_index(index):
    """Save the name -> id mapping."""
    try:
        with INDEX_FILE.open("w", encoding="utf-8") as file:
            json.dump(index, file, indent=2)
    except OSError as error:
        print(f"Could not save the session index: {error}")


def make_session_id(index):
    """Simple string ID based on how many sessions already exist."""
    return f"session-{len(index) + 1}"


def load_history(session_name):
    """Load one conversation's message list from sessions/<name>.json."""
    path = SESSIONS_DIR / f"{session_name}.json"
    try:
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            print(f"History for {session_name} was not a list. Starting fresh.")
            return []
        return data
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not read session {session_name}: {error}")
        return []


def save_history(session_name, history):
    """Save one conversation after every assistant reply."""
    try:
        # Create the sessions folder if it does not exist yet.
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        path = SESSIONS_DIR / f"{session_name}.json"
        with path.open("w", encoding="utf-8") as file:            json.dump(history, file, indent=2)
    except OSError as error:
        print(f"Could not save session {session_name}: {error}")


def ask_session_name(index):
    """Empty = new. Known name = resume. Unknown = friendly message + new."""
    typed = input("Session name (press Enter for a new session): ").strip()

    if typed == "":
        return None

    if typed in index:
        return typed

    print(f"No session called '{typed}'. Starting a new one.")
    return None


def generate_session_name(first_question, index):
    """Separate model call: two lowercase words joined with underscore."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Reply with exactly two lowercase words separated by a space. "
                        "No punctuation and no extra text."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Give a short two-word name for this question: {first_question}",
                },
            ],
        )
        reply = response.choices[0].message.content.strip().lower()
        words = [word.strip(".,!?") for word in reply.split() if word.strip(".,!?")]

        if len(words) >= 2:
            name = f"{words[0]}_{words[1]}"
        elif len(words) == 1:
            name = f"{words[0]}_session"
        else:
            name = "new_session"
    except Exception as error:  # noqa: BLE001
        print(f"Could not generate a session name: {error}")
        name = "new_session"
    # Avoid overwriting an existing session when names repeat.
    original_name = name
    counter = 2
    while name in index:
        name = f"{original_name}_{counter}"
        counter += 1

    return name


def chat_with_history(history):
    """Send the full conversation and return the assistant reply."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=history,
        )
        return response.choices[0].message.content
    except Exception as error:  # noqa: BLE001
        print(f"Sorry, the API call failed: {error}")
        return None

def main():
    index = load_index()
    chosen_name = ask_session_name(index)

    if chosen_name is None:
        session_name = None
        history = []
        is_new_session = True
        print("Starting a new session.")
    else:
        session_name = chosen_name
        history = load_history(session_name)
        is_new_session = False
        print(f"Resumed session '{session_name}' with {len(history)} saved messages.")

    while True:
        try:
            user_message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_message == "":
            continue

        if user_message.lower() == "exit":
            print("Goodbye!")
            break

        # First question of a new session gets a model-generated name first.
        if is_new_session and session_name is None:
            session_name = generate_session_name(user_message, index)
            session_id = make_session_id(index)
            index[session_name] = session_id
            save_index(index)
            print(f"Session name: {session_name}")
            is_new_session = False

        history.append({"role": "user", "content": user_message})

        reply = chat_with_history(history)
        if reply is None:
            # Do not keep a question that was never answered.
            history.pop()
            continue

        print(f"Assistant: {reply}")
        history.append({"role": "assistant", "content": reply})
        save_history(session_name, history)


if __name__ == "__main__":
    main()
