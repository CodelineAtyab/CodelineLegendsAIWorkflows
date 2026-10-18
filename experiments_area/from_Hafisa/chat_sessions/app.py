import json
import os

from dotenv import load_dotenv
from openai import APIError, OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INDEX_FILE = "sessions_index.json"
SESSIONS_FOLDER = "sessions"


def load_index():
    try:
        with open(INDEX_FILE, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError as error:
        print("Could not read session index:", error)
        return {}

    except OSError as error:
        print("Could not open session index:", error)
        return {}


def save_index(index):
    try:
        with open(INDEX_FILE, "w") as file:
            json.dump(index, file, indent=4)

    except OSError as error:
        print("Could not save session index:", error)


def load_session(session_name):
    path = f"{SESSIONS_FOLDER}/{session_name}.json"

    try:
        with open(path, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError as error:
        print("Could not read session:", error)
        return []

    except OSError as error:
        print("Could not open session:", error)
        return []


def save_session(session_name, messages):
    os.makedirs(SESSIONS_FOLDER, exist_ok=True)

    path = f"{SESSIONS_FOLDER}/{session_name}.json"

    try:
        with open(path, "w") as file:
            json.dump(messages, file, indent=4)

    except OSError as error:
        print("Could not save session:", error)


def generate_session_name(first_question):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Create exactly two simple words for a chat session name. "
                        "Reply with only two words."
                    ),
                },
                {
                    "role": "user",
                    "content": first_question,
                },
            ],
        )

        name = response.choices[0].message.content

        if name is None:
            return "new_session"

        words = name.lower().split()

        if len(words) == 0:
            return "new_session"

        if len(words) == 1:
            words.append("session")

        return "_".join(words[:2])

    except APIError as error:
        print("Could not create session name:", error)
        return "new_session"


def chat_with_model(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
        )

        return response.choices[0].message.content

    except APIError as error:
        print("Could not get AI reply:", error)
        return None


def main():
    index = load_index()

    session_name = input(
        "Enter a session name to continue, or press Enter for a new session: "
    ).strip()

    messages = []

    if session_name:
        if session_name in index:
            messages = load_session(session_name)
            print(f"Continuing session: {session_name}")

        else:
            print(f"No session called {session_name}. Starting a new one.")
            session_name = ""

    while True:
        user_message = input("You: ")

        if user_message.lower() == "exit":
            print("Chat ended.")
            break

        if session_name == "":
            session_name = generate_session_name(user_message)

            session_id = f"session-{len(index) + 1}"

            index[session_name] = session_id
            save_index(index)

            print(f"New session: {session_name}")

        messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        assistant_reply = chat_with_model(messages)

        if assistant_reply is None:
            continue

        messages.append(
            {
                "role": "assistant",
                "content": assistant_reply,
            }
        )

        save_session(session_name, messages)

        print("Assistant:", assistant_reply)


if __name__ == "__main__":
    main()
