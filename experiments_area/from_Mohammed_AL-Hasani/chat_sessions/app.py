import json
import os

import openai
from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-4.1-mini"
INDEX_FILE = "sessions_index.json"
SESSIONS_FOLDER = "sessions"


def load_index():
    # name -> id. If the file does not exist yet, start with an empty dict.
    if not os.path.exists(INDEX_FILE):
        return {}
    try:
        with open(INDEX_FILE, "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        print("Could not read the index file, starting with an empty one.")
        return {}


def save_index(index):
    try:
        with open(INDEX_FILE, "w") as f:
            json.dump(index, f)
    except (OSError, TypeError, ValueError):
        print("Could not save the index file.")


def load_history(name):
    # returns the list of messages, or None if the file cannot be read
    try:
        with open(SESSIONS_FOLDER + "/" + name + ".json", "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        print("Could not read the saved chat.")
        return None


def save_history(name, history):
    try:
        if not os.path.exists(SESSIONS_FOLDER):
            os.makedirs(SESSIONS_FOLDER)
        with open(SESSIONS_FOLDER + "/" + name + ".json", "w") as f:
            json.dump(history, f)
    except (OSError, TypeError, ValueError):
        print("Could not save the chat.")


def ask_session_name(index):
    # returns a name to resume, or None for a new session
    answer = input("Session name (press Enter for a new chat): ").strip()
    if answer == "":
        return None
    if answer in index:
        return answer
    print("No session with that name. Starting a new chat.")
    return None


def call_model(client, messages):
    # returns the reply text, or None if something went wrong
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages)
        return response.choices[0].message.content
    except (openai.APIError, IndexError, AttributeError):
        print("Something went wrong with the model call. Please try again.")
        return None


def make_name(client, first_question):
    messages = [
        {"role": "system", "content": "Answer with only two words, nothing else."},
        {"role": "user", "content": first_question},
    ]
    reply = call_model(client, messages)
    if reply is None:
        return "new_session"

    words = reply.lower().split()
    words = [w.strip(".,!?:;\"'") for w in words]
    words = [w for w in words if w]
    words = words[:2]

    if len(words) < 2:
        return "new_session"

    return "_".join(words)


def create_session(client, index, first_question):
    name = make_name(client, first_question)
    if name in index:
        # do not overwrite an old chat
        name = name + "_" + str(len(index) + 1)
    index[name] = "session-" + str(len(index) + 1)
    save_index(index)
    return name


def chat_loop(client, index, name, history):
    print("Type exit to stop.")
    while True:
        question = input("You: ").strip()
        if question.lower() == "exit":
            print("Bye!")
            break
        if question == "":
            continue

        # first question of a new chat: get the name first
        if name is None:
            name = create_session(client, index, question)
            print("Session name:", name)

        history.append({"role": "user", "content": question})
        reply = call_model(client, history)
        if reply is None:
            history.pop()
            continue

        print("Assistant:", reply)
        history.append({"role": "assistant", "content": reply})
        save_history(name, history)


def main():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("No OPENAI_API_KEY found. Put it in a .env file.")
        return
    client = OpenAI()

    index = load_index()
    name = ask_session_name(index)
    history = []

    if name is not None:
        history = load_history(name)
        if history is None:
            print("Starting a new chat instead.")
            name = None
            history = []
        else:
            print("Resumed", name)

    chat_loop(client, index, name, history)


if __name__ == "__main__":
    main()
