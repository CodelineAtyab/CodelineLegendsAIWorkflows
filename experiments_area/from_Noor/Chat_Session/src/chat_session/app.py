import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from pathlib import Path
#reads the .env file and loads its values into environment variables
load_dotenv()
#retrieves the API key without hardcoding it
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")

#configures the API client
client = OpenAI(api_key=api_key)
#This function accepts the conversation history and returns the assistant's reply
def chat_with_model(messages):
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
    except (json.JSONDecodeError, OSError):
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
    except (json.JSONDecodeError, OSError):
        print("Could not read the conversation history.")
        return []


def save_history(session_name, messages):
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    history_file = SESSIONS_DIR / f"{session_name}.json"

    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4)




def choose_session(index):
    while True:
        session_name = input(
            "Enter a session name to resume, or press Enter for a new chat: "
        ).strip()

        if not session_name:
            return None

        if session_name in index:
            print(f"Resuming session: {session_name}")
            return session_name

        print(f"No session called '{session_name}'. Please try again.")



def generate_session_name(question):
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

#It creates IDs such as session-1, session-2, and so on.
def create_session_id(index):
    return f"session-{len(index) + 1}"


def main():
    index = load_index()
    session_name = choose_session(index)

    if session_name:
        messages = load_history(session_name)
    else:
        messages = []
        question = input("You: ").strip()

        if question.lower() == "exit":
            return

        if not question:
            print("Please enter a question.")
            return

        session_name = generate_session_name(question)

        # Avoid overwriting an existing session with the same name.
        if session_name in index:
            session_name = f"{session_name}_{len(index) + 1}"

        session_id = create_session_id(index)
        index[session_name] = session_id

        messages.append({"role": "user", "content": question})

        try:
            reply = chat_with_model(messages)
            print(f"Assistant: {reply}")
            messages.append({"role": "assistant", "content": reply})

            save_index(index)
            save_history(session_name, messages)

        except Exception as error:
            print(f"Sorry, something went wrong: {error}")
            return

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit" or question.upper() == "EXIT":
            print("Chat ended.")
            break

        if not question:
            continue

        messages.append({"role": "user", "content": question})

        try:
            reply = chat_with_model(messages)
            print(f"Assistant: {reply}")
            messages.append({"role": "assistant", "content": reply})

            save_history(session_name, messages)

        except Exception as error:
            # Remove the unsent message so history stays consistent.
            messages.pop()
            print(f"Sorry, something went wrong: {error}")

if __name__ == "__main__":
    main()