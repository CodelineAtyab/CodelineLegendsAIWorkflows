import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Define constants and load the API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4.1-mini"
BASE_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = BASE_DIR / "sessions"
INDEX_FILE = SESSIONS_DIR / "index.json"


# Create a function to read the index
def load_index():
    if not INDEX_FILE.exists():
        return {}
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            print("Invalid session index.")
            return None
        return data
    except OSError, json.JSONDecodeError:
        print("Could not read session index.")
        return None


# Create a function to save JSON
def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError:
        print("Could not save the file.")
        return False


# Generate a session name using AI
def generate_name(client, question):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Generate exactly two short English words "
                        "describing the user's question. "
                        "Return only the two words."
                    ),
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )
        text = response.choices[0].message.content or ""
        words = re.findall(r"[a-z]+", text.lower())
        if len(words) >= 2:
            return "_".join(words[:2])
        return "new_session"
    except Exception:
        print("Could not generate session name.")
        return "new_session"


# Create the function that asks AI a question
def get_answer(client, messages):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        return response.choices[0].message.content or ""
    except Exception:
        print("Could not get an AI response.")
        return None


# Load an old conversation
def load_history(name):
    path = SESSIONS_DIR / f"{name}.json"
    try:
        with open(path, "r", encoding="utf-8") as file:
            history = json.load(file)
        if not isinstance(history, list):
            print("Invalid session history.")
            return None
        return history
    except OSError, json.JSONDecodeError:
        print("Could not load session history.")
        return None


# Create the chat loop
def chat(client, name, history, index, new_session):
    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        if new_session:
            name = generate_name(client, question)

            # Keep session names unique and two words
            base_name = name
            number = 2
            while name in index:
                name = f"{base_name.split('_')[0]}_{number}"
                number += 1

            session_id = f"session-{len(index) + 1}"

        # Add the user's question to the conversation
        pending_messages = history + [
            {"role": "user", "content": question}
        ]

        # Get the AI response
        answer = get_answer(client, pending_messages)

        if answer is None:
            continue

        # Add the AI response to the conversation
        updated_history = pending_messages + [
            {"role": "assistant", "content": answer}
        ]

        # Save the conversation after the AI response
        if not save_json(SESSIONS_DIR / f"{name}.json", updated_history):
            return

        # Save the index only after the first successful response
        if new_session:
            index[name] = session_id

            if not save_json(INDEX_FILE, index):
                return

            print(f"Session created: {name}")
            new_session = False

        history = updated_history
        print(f"AI: {answer}")


# Create main()
def main():
    if not API_KEY:
        print("API key not found. Check your .env file.")
        return
    client = OpenAI(api_key=API_KEY)
    try:
        SESSIONS_DIR.mkdir(exist_ok=True)
    except OSError:
        print("Could not create sessions folder.")
        return
    index = load_index()
    if index is None:
        return
    name = input("Enter session name (Enter for new): ")
    if not name:
        chat(client, "", [], index, True)
    elif name in index:
        history = load_history(name)
        if history is not None:
            print(f"Session loaded: {name}")
            chat(client, name, history, index, False)
    else:
        print("Session not found. Starting a new session.")
        chat(client, "", [], index, True)


if __name__ == "__main__":
    main()
