import json
import os

from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-4.1-mini"
INDEX_FILE = "sessions_index.txt"
SESSIONS_DIR = "sessions"


def load_index():
    if not os.path.exists(INDEX_FILE):
        return {}
    with open(INDEX_FILE, "r") as f:
        return json.load(f)


def save_index(index):
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)


def session_path(name):
    return os.path.join(SESSIONS_DIR, f"{name}.json")


def load_history(name):
    with open(session_path(name), "r") as f:
        return json.load(f)


def save_history(name, history):
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    with open(session_path(name), "w") as f:
        json.dump(history, f, indent=2)


def ask_session_name(index):
    """Returns (name, history). name is None for a new session."""
    name = input("Session name (press Enter for a new session): ").strip()
    if name == "":
        return None, []
    if name in index:
        print(f"Resuming session '{name}'.")
        return name, load_history(name)
    print(f"No session called {name}. Starting a new one.")
    return None, []


def generate_name(client, first_question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Give a name for this chat. Reply with ONLY two words, nothing else.",
            },
            {"role": "user", "content": first_question},
        ],
    )
    reply = response.choices[0].message.content
    words = []
    for w in reply.lower().split():
        w = "".join(c for c in w if c.isalnum())
        if w:
            words.append(w)
    if not words:
        return "new_session"
    return "_".join(words[:2])


def get_reply(client, history):
    response = client.chat.completions.create(model=MODEL, messages=history)
    return response.choices[0].message.content


def main():
    load_dotenv()
    client = OpenAI()

    try:
        index = load_index()
        name, history = ask_session_name(index)
    except Exception as e:
        print("Could not read the session files:", str(e))
        return

    while True:
        question = input("You: ").strip()
        if question.lower() == "exit":
            print("Goodbye!")
            break
        if question == "":
            continue

        try:
            # New session: get the two-word name BEFORE showing the answer
            if name is None:
                name = generate_name(client, question)
                if name in index:  # avoid overwriting an older session
                    name = f"{name}_{len(index) + 1}"
                index[name] = f"session-{len(index) + 1}"
                save_index(index)

            history.append({"role": "user", "content": question})
            reply = get_reply(client, history)
            print("Bot:", reply)
            history.append({"role": "assistant", "content": reply})
            save_history(name, history)
        except Exception as e:
            print("Something went wrong:", str(e))
            if history and history[-1]["role"] == "user":
                history.pop()  # drop the unanswered question


if __name__ == "__main__":
    main()