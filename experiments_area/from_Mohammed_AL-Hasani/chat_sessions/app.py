import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

MODEL = "gpt-4.1-mini"
SESSIONS_DIR = "sessions"
INDEX_FILE = "sessions_index.json"


def load_index():
    """Return the {name: id} dict. Empty dict if the file is missing or unreadable."""
    if not os.path.exists(INDEX_FILE):
        return {}
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        print("Could not read the session index, starting with an empty one.")
        return {}


def save_index(index):
    try:
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)
    except OSError:
        print("Warning: could not save the session index.")


def history_path(name):
    return os.path.join(SESSIONS_DIR, f"{name}.json")


def load_history(name):
    """Return the saved message list, or None if it cannot be read."""
    try:
        with open(history_path(name), "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        print(f"Could not read the saved chat for '{name}'.")
        return None


def save_history(name, history):
    try:
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        with open(history_path(name), "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except OSError:
        print("Warning: could not save the chat history.")


def ask_session_name(index):
    """Return an existing session name to resume, or None for a new session."""
    answer = input("Session name to resume (press Enter for a new chat): ").strip()
    if not answer:
        return None
    if answer in index:
        return answer
    print(f"No session called '{answer}' was found. Starting a new chat.")
    return None


def clean_name(reply):
    """Turn the model's reply into at most two lower-case words joined by _."""
    words = re.findall(r"[a-z0-9]+", reply.lower())[:2]
    return "_".join(words) if words else "new_session"


def generate_name(client, first_question):
    """Ask the model for a two-word name based on the first question."""
    messages = [
        {
            "role": "system",
            "content": (
                "Reply with ONLY two words that summarise the user's message. "
                "No punctuation, no explanation, nothing else."
            ),
        },
        {"role": "user", "content": first_question},
    ]
    reply = call_model(client, messages)
    return clean_name(reply) if reply else "new_session"


def register_session(index, name):
    """Make the name unique, give it an id, and store it in the index."""
    unique = name
    n = 2
    while unique in index:
        unique = f"{name}_{n}"
        n += 1
    index[unique] = f"session-{len(index) + 1}"
    save_index(index)
    return unique


def call_model(client, messages):
    """Send the messages list to the model. Return the reply text, or None on error."""
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages)
        return response.choices[0].message.content.strip()
    except (OpenAIError, OSError, ValueError, json.JSONDecodeError) as e:
        print(f"Sorry, the model call failed ({type(e).__name__}). Please try again.")
        return None


def chat_loop(client, index, name, history):
    """Run the chat. `name` is None for a new session until the first question."""
    print("Type 'exit' to quit.\n")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return
        if question.lower() == "exit":
            print("Bye!")
            return
        if not question:
            continue

        if name is None:
            name = register_session(index, generate_name(client, question))
            print(f"[session: {name}]")

        history.append({"role": "user", "content": question})
        reply = call_model(client, history)
        if reply is None:
            history.pop()
            continue

        print(f"\nAssistant: {reply}\n")
        history.append({"role": "assistant", "content": reply})
        save_history(name, history)


def main():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not found. Add it to a .env file next to app.py.")
        return
    client = OpenAI()

    index = load_index()
    name = ask_session_name(index)
    history = []

    if name is not None:
        history = load_history(name)
        if history is None:
            print("Starting a new chat instead.")
            name, history = None, []
        else:
            print(f"Resumed '{name}' ({len(history)} messages).")

    chat_loop(client, index, name, history)


if __name__ == "__main__":
    main()
