import json
import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

MODEL = "gpt-4.1-mini"
INDEX_FILE = "sessions_index.json"
SESSIONS_FOLDER = "sessions"


def load_session_index():
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_session_index(index):
    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=2)


def load_session_history(session_name):
    file_name = os.path.join(SESSIONS_FOLDER, session_name + ".json")
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def save_session_history(session_name, messages):
    os.makedirs(SESSIONS_FOLDER, exist_ok=True)
    file_name = os.path.join(SESSIONS_FOLDER, session_name + ".json")
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=2, ensure_ascii=False)


def generate_session_name(client, first_question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Name this chat in two words. Reply with only the name.",
            },
            {"role": "user", "content": first_question},
        ],
    )

    title = response.choices[0].message.content or ""
    title = title.lower()

    for mark in ".,!?:;'\"":
        title = title.replace(mark, "")

    words = title.split()
    if len(words) < 2:
        return "new_session"

    return words[0] + "_" + words[1]


def get_assistant_reply(client, messages):
    response = client.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content or ""


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please add OPENAI_API_KEY to your .env file first.")
        return

    try:
        index = load_session_index()
    except (OSError, json.JSONDecodeError) as error:
        print("Could not read the session index:", error)
        return

    requested_name = input(
        "Enter a session name to resume (press Enter for a new session): "
    ).strip()

    if requested_name.lower() == "exit":
        print("Chat ended.")
        return

    messages = []
    session_name = ""
    is_new_session = True

    if requested_name in index:
        session_name = requested_name
        try:
            messages = load_session_history(session_name)
        except (OSError, json.JSONDecodeError) as error:
            print("Could not load that session:", error)
            return

        is_new_session = False
        print("Resumed session:", session_name)
    elif requested_name:
        print("No session called", requested_name + ". Starting a new one.")

    client = OpenAI(api_key=api_key)

    while True:
        question = input("\nYou (or type exit): ").strip()

        if question.lower() == "exit":
            print("Chat ended.")
            break

        if not question:
            continue

        try:
            if is_new_session:
                session_name = generate_session_name(client, question)

                original_name = session_name
                number = 2
                while session_name in index:
                    session_name = original_name + "_" + str(number)
                    number += 1

                index[session_name] = "session-" + str(len(index) + 1)

            messages.append({"role": "user", "content": question})
            reply = get_assistant_reply(client, messages)
        except OpenAIError as error:
            print("Could not contact OpenAI:", error)
            return

        messages.append({"role": "assistant", "content": reply})

        try:
            save_session_history(session_name, messages)
            save_session_index(index)
        except (OSError, TypeError) as error:
            print("Could not save the conversation:", error)
            return

        if is_new_session:
            print("New session:", session_name)
            is_new_session = False

        print("\nAssistant:", reply)


if __name__ == "__main__":
    main()
