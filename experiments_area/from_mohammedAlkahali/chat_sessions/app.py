import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from utils.cli_args import clean_session_name, is_exit_word, parse_args

load_dotenv()

INDEX_FILE = "sessions_index.json"


def save_session(file_name, messages):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4)


def load_session(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def load_index(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_index(file_name, index):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=4)


def make_unique_name(name, index):
    if name not in index:
        return name
    number = 2
    while f"{name}_{number}" in index:
        number += 1
    return f"{name}_{number}"


def generate_session_name(client, first_question):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Reply with exactly two words, lowercase, separated by a space, nothing else. Summarize the topic of the user's message in those two words.",
            },
            {"role": "user", "content": first_question},
        ],
    )
    raw = response.choices[0].message.content.strip().lower()
    cleaned = clean_session_name(raw)
    return cleaned


def main():
    client = OpenAI()
    index = load_index(INDEX_FILE)

    session_name, question = parse_args(sys.argv)

    if session_name is None and question is None:
        # Interactive mode
        typed_name = input("Session name (press Enter for new): ")

        if typed_name in index:
            session_name = typed_name
            message = load_session(f"sessions/{session_name}.json")
            is_new = False
        else:
            if typed_name != "":
                print(f"No session called {typed_name}. Starting a new session.")
            session_name = None
            message = []
            is_new = True

        while True:
            user_input = input("You: ")

            if is_exit_word(user_input):
                break

            if is_new and len(message) == 0:
                try:
                    session_name = generate_session_name(client, user_input)
                except OpenAIError as error:
                    print(f"Could not generate a session name, using 'new_session' instead: {error}")
                    session_name = "new_session"
                session_name = make_unique_name(session_name, index)

            message.append({"role": "user", "content": user_input})

            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=message,
                )
                reply = response.choices[0].message.content
            except OpenAIError as error:
                print(f"Sorry, something went wrong talking to the model: {error}")
                message.pop()
                continue

            print("bot:", reply)
            message.append({"role": "assistant", "content": reply})

            try:
                save_session(f"sessions/{session_name}.json", message)
                if is_new:
                    index[session_name] = f"session-{len(index) + 1}"
                    save_index(INDEX_FILE, index)
                    is_new = False
            except OSError as error:
                print(f"Could not save this session to disk: {error}")

    else:
        # Non-interactive mode
        if session_name is not None and session_name not in index:
            raise SystemExit(f"Error: Unknown session '{session_name}'")

        if session_name is None:
            # New session: ask the model for a two-word name
            try:
                session_name = generate_session_name(client, question)
            except OpenAIError:
                session_name = "new_session"
            session_name = make_unique_name(session_name, index)
            message = []
            is_new = True
        else:
            # Existing session
            message = load_session(f"sessions/{session_name}.json")
            is_new = False

        message.append({"role": "user", "content": question})

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=message,
            )
            reply = response.choices[0].message.content
        except OpenAIError as error:
            raise SystemExit(f"Error: OpenAI request failed: {error}")

        message.append({"role": "assistant", "content": reply})

        try:
            save_session(f"sessions/{session_name}.json", message)
            if is_new:
                index[session_name] = f"session-{len(index) + 1}"
                save_index(INDEX_FILE, index)
        except OSError as error:
            raise SystemExit(f"Error: Could not save session: {error}")

        print(f"Session: {session_name}")
        print(f"Assistant: {reply}")


if __name__ == "__main__":
    main()
