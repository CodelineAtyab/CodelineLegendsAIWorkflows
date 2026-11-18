import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

MODEL = "gpt-4.1-mini"
BASE_DIR = Path(__file__).parent
INDEX_FILE = BASE_DIR / "session_index.json"
SESSIONS_DIR = BASE_DIR / "sessions"


def load_index():
    try:
        with open(INDEX_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_index(index):
    with open(INDEX_FILE, "w") as file:
        json.dump(index, file, indent=2)


def load_history(session_name):
    with open(SESSIONS_DIR / f"{session_name}.json", "r") as file:
        return json.load(file)


def save_history(session_name, history):
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    with open(SESSIONS_DIR / f"{session_name}.json", "w") as file:
        json.dump(history, file, indent=2)


def make_session_name(client, first_question, index):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Reply with only two words that describe the user's question.",
            },
            {"role": "user", "content": first_question},
        ],
    )
    reply = response.choices[0].message.content or ""

    words = []
    for word in reply.lower().split():
        clean_word = ""
        for letter in word:
            if letter.isalnum():
                clean_word += letter
        if clean_word:
            words.append(clean_word)

    if words:
        name = "_".join(words[:2])
    else:
        name = "new_session"

    session_name = name
    number = 2
    while session_name in index:
        session_name = f"{name}_{number}"
        number += 1
    return session_name


def get_reply(client, history):
    response = client.chat.completions.create(model=MODEL, messages=history)
    return response.choices[0].message.content


def main():
    load_dotenv()
    try:
        client = OpenAI()
        index = load_index()
        requested_name = input("Session name (press Enter for a new chat): ").strip().lower()
        session_name = ""
        history = []

        if requested_name in index:
            session_name = requested_name
            history = load_history(session_name)
            print(f"Resumed session {session_name}.")
        elif requested_name:
            print(f"No session called {requested_name}. Starting a new one.")

        print("Type exit to finish.")
        while True:
            question = input("You: ").strip()
            if question in ["exit", "EXIT"]:
                print("Goodbye!")
                break
            if not question:
                continue

            history.append({"role": "user", "content": question})
            try:
                if not session_name:
                    session_name = make_session_name(client, question, index)
                    index[session_name] = f"session-{len(index) + 1}"
                    print(f"Session name: {session_name}")
                reply = get_reply(client, history)
            except OpenAIError:
                history.pop()
                print("Could not reach OpenAI. Check your API key and internet connection.")
                continue

            history.append({"role": "assistant", "content": reply})
            save_history(session_name, history)
            save_index(index)
            print(f"Assistant: {reply}")

    except OpenAIError:
        print("Could not start OpenAI. Check OPENAI_API_KEY in your .env file.")
    except (OSError, ValueError):
        print("Could not read or save the session files. Check the sessions folder and JSON files.")


if __name__ == "__main__":
    main()
