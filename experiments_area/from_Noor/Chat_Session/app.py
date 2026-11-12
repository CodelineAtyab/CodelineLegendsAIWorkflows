import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, AuthenticationError, OpenAI

# reads the .env file and loads its values into environment variables
load_dotenv()
# retrieves the API key without hardcoding it


def create_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("No API key found. Add OPENAI_API_KEY to your .env file.")
        return None

    return OpenAI(api_key=api_key)


# This function accepts the conversation history and returns the assistant's reply
def chat_with_model(client, messages):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )

    return response.choices[0].message.content


# Folder and file paths
SESSIONS_DIR = Path(__file__).parent / "sessions"
INDEX_FILE = SESSIONS_DIR / "index.json"


def load_index():
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    if not INDEX_FILE.exists():
        return {}

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError, OSError:
        print("Could not read the session index. Starting with an empty index.")
        return {}


def save_index(index):
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=4)


def load_history(session_name):
    history_file = SESSIONS_DIR / f"{session_name}.json"

    if not history_file.exists():
        return []

    try:
        with open(history_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError, OSError:
        print("Could not read the conversation history.")
        return []


def save_history(session_name, messages):
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    history_file = SESSIONS_DIR / f"{session_name}.json"

    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4)


def choose_session(index):
    session_name = input(
        "Enter a session name to resume, or press Enter for a new chat: "
    ).strip()

    if not session_name:
        return None

    if session_name in index:
        print(f"Resuming session: {session_name}")
        return session_name

    print(f"No session called '{session_name}'. Starting a new one.")
    return None


def generate_session_name(client, question):
    messages = [
        {
            "role": "system",
            "content": (
                "Generate a short name for a chat based on the user's "
                "question. Reply with exactly two words and nothing else."
            ),
        },
        {"role": "user", "content": question},
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )

    name = response.choices[0].message.content.strip()
    words = name.lower().split()

    if len(words) < 2:
        return "new_session"

    return "_".join(words[:2])


# It creates IDs such as session-1, session-2, and so on.
def create_session_id(index):
    return f"session-{len(index) + 1}"


def main():
    client = create_client()

    if client is None:
        return

    index = load_index()
    session_name = choose_session(index)

    # Resume an existing session.
    if session_name:
        messages = load_history(session_name)

    # Create a new session.
    else:
        messages = []
        question = input("You: ").strip()

        if question.lower() in ("exit", "quit"):
            return

        if not question:
            print("Please enter a question.")
            return

        try:
            session_name = generate_session_name(client, question)
        except AuthenticationError:
            print("Authentication failed. Please check your API key.")
            return
        except (APIError, OSError, ValueError) as error:
            print(f"Sorry, something went wrong: {error}")
            return
        # Avoid overwriting an existing session.
        if session_name in index:
            session_name = f"{session_name}_{len(index) + 1}"

        index[session_name] = create_session_id(index)
        messages.append({"role": "user", "content": question})

        try:
            reply = chat_with_model(client, messages)
            print(f"Assistant: {reply}")
            messages.append({"role": "assistant", "content": reply})

            save_index(index)
            save_history(session_name, messages)

        except AuthenticationError:
            messages.pop()
            print("Invalid API key. Check your OPENAI_API_KEY in the .env file.")
            return
        except (APIError, OSError, ValueError) as error:
            messages.pop()
            print(f"Sorry, something went wrong: {error}")
            return
    # Continue the conversation.
    while True:
        question = input("You: ").strip()

        if question.lower() in ("exit", "quit"):
            print("Chat ended.")
            break

        if not question:
            continue

        messages.append({"role": "user", "content": question})

        try:
            reply = chat_with_model(client, messages)
            print(f"Assistant: {reply}")
            messages.append({"role": "assistant", "content": reply})
            save_history(session_name, messages)

        except AuthenticationError:
            messages.pop()
            print("Invalid API key. Check your OPENAI_API_KEY in the .env file.")
            return
        except (APIError, OSError, ValueError) as error:
            messages.pop()
            print(f"Sorry, something went wrong: {error}")
            return


if __name__ == "__main__":
    main()
