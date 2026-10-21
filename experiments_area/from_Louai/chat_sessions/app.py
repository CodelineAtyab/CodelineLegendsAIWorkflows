import json
import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

MODEL = "gpt-4.1-mini"
INDEX_FILE = "sessions_index.json"
SESSIONS_DIR = "sessions"


def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError:
        print("Could not save the file.")


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except OSError, json.JSONDecodeError:
        print("Could not read the file.")
        return default


def get_session_path(name):
    return os.path.join(SESSIONS_DIR, name + ".json")


def ask_model(client, messages):
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages)
        return response.choices[0].message.content
    except OpenAIError:
        print(
            "Could not get a reply from the model. Check your key, credits or internet."
        )
        return None


def clean_name(text):
    cleaned = ""
    for ch in text.lower():
        if ch.isalnum():
            cleaned += ch
        else:
            cleaned += " "
    words = cleaned.split()[:2]
    if not words:
        return "new_session"
    return "_".join(words)


def generate_session_name(client, first_question):
    naming_messages = [
        {
            "role": "user",
            "content": "Reply with only two words, nothing else, "
            "that name this question: " + first_question,
        }
    ]
    reply = ask_model(client, naming_messages)
    if reply is None:
        return "new_session"
    return clean_name(reply)


def make_unique_name(name, index):
    unique = name
    counter = 2
    while unique in index:
        unique = f"{name}_{counter}"
        counter += 1
    return unique


def create_session(client, first_question, index):
    name = make_unique_name(generate_session_name(client, first_question), index)
    index[name] = "session-" + str(len(index) + 1)
    save_json(INDEX_FILE, index)
    return name


def ask_session_name(index):
    name = input("Session name (press Enter for a new session): ").strip()

    if name == "":
        return None

    if name in index:
        return name

    print(f"No session called {name}. Starting a new one.")
    return None


def chat_loop(client, index, session_name, chat_messages):
    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            break

        if question == "":
            continue

        if session_name is None:
            session_name = create_session(client, question, index)
            print(f"Session name: {session_name}")

        chat_messages.append({"role": "user", "content": question})
        reply = ask_model(client, chat_messages)

        if reply is None:
            chat_messages.pop()
            continue

        print("Assistant:", reply)
        chat_messages.append({"role": "assistant", "content": reply})
        save_json(get_session_path(session_name), chat_messages)


def main():
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except OpenAIError:
        print("No API key found. Add OPENAI_API_KEY to your .env file.")
        return

    os.makedirs(SESSIONS_DIR, exist_ok=True)
    index = load_json(INDEX_FILE, {})

    session_name = ask_session_name(index)
    chat_messages = []

    if session_name is not None:
        chat_messages = load_json(get_session_path(session_name), [])
        print(f"Resumed '{session_name}' with {len(chat_messages)} messages.")

    try:
        chat_loop(client, index, session_name, chat_messages)
    except KeyboardInterrupt, EOFError:
        print("\nBye.")


if __name__ == "__main__":
    main()
