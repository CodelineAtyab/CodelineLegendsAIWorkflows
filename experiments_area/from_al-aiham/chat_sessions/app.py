
import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

INDEX_FILE = "sessions_index.json"
SESSIONS_DIR = "sessions"
MODEL = "gpt-4.1-mini"


def load_index():
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_index(index):
    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=4)


def load_session(name):
    path = os.path.join(SESSIONS_DIR, f"{name}.json")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_session(name, messages):
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    path = os.path.join(SESSIONS_DIR, f"{name}.json")

    with open(path, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)


def generate_session_name(client, question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Create a short session title based only on the user's "
                    "question. Reply with exactly two words and nothing else."
                ),
            },
            {"role": "user", "content": question},
        ],
    )

    title = response.choices[0].message.content or ""
    words = re.findall(r"\w+", title.lower(), flags=re.UNICODE)

    if len(words) < 2:
        return "new_session"

    return "_".join(words[:2])


def get_reply(client, messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    return response.choices[0].message.content or ""


def main():
    try:
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing from .env")

        client = OpenAI(api_key=api_key)
        index = load_index()

        session_name = input(
            "Enter a session name to resume (Enter for new): "
        ).strip()

        if session_name and session_name in index:
            messages = load_session(session_name)
            print(f"Resumed session: {session_name}")

        else:
            if session_name:
                print(
                    f"No session called {session_name}. "
                    "Starting a new one."
                )

            session_name = None
            messages = []

        while True:
            question = input("\nYou: ").strip()

            if question.lower() == "exit":
                print("Chat ended.")
                break

            if not question:
                continue

            if session_name is None:
                session_name = generate_session_name(client, question)

                if session_name in index:
                    base_name = session_name
                    number = 2

                    while session_name in index:
                        session_name = f"{base_name}_{number}"
                        number += 1

                session_id = f"session-{len(index) + 1}"

                index[session_name] = session_id
                save_index(index)

                print(f"New session: {session_name}")

            messages.append({"role": "user", "content": question})

            try:
                reply = get_reply(client, messages)
            except OpenAIError:
                messages.pop()
                raise

            print(f"\nAssistant: {reply}")

            messages.append({"role": "assistant", "content": reply})

            save_session(session_name, messages)
            save_index(index)

    except (OpenAIError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()