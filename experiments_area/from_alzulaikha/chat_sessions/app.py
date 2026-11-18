import json
import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

SESSION_INDEX_FILE = "session_index.json"
SESSIONS_DIR = "sessions"
MODEL_NAME = "gpt-4.1-mini"


def load_session_index(path=SESSION_INDEX_FILE):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not read the session index: {error}")
        return {}
    if not isinstance(data, dict):
        print("Session index is not a dictionary. Starting with an empty index.")
        return {}
    return data


def save_session_index(index, path=SESSION_INDEX_FILE):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(index, file, indent=2)
    except (OSError, TypeError) as error:
        print(f"Could not save the session index: {error}")


def load_session_history(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not read session history: {error}")
        return []
        
    if not isinstance(data, list):
        print("Session history is not a list. Starting with an empty history.")
        return []
    return data


def save_session_history(history, path):
    try:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=2)
    except (OSError, TypeError) as error:
        print(f"Could not save session history: {error}")


def get_openai_client():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("No API key found. Add OPENAI_API_KEY to your .env file.")
        return None

    try:
        return OpenAI(api_key=api_key)
    except OpenAIError as error:
        print(f"Could not create the OpenAI client: {error}")
        return None


def unique_session_name(base_name, index):
    """Return a session name that is not already in the index.

    If base_name is taken, append _2, _3, and so on until the name is free.
    This prevents a new session from overwriting an existing conversation.
    """
    if base_name not in index:
        return base_name
    counter = 2
    while f"{base_name}_{counter}" in index:
        counter += 1
    return f"{base_name}_{counter}"


def generate_two_word_session_name(client, question):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "Return exactly two words and nothing else.",
                },
                {"role": "user", "content": question},
            ],
        )
    except OpenAIError as error:
        print(f"Could not generate a session name: {error}")
        return "new_session"

    content = response.choices[0].message.content or ""

    words = content.strip().lower().split()
    if len(words) < 2:
        return "new_session"
    return "_".join(words[:2])


def main():
    client = get_openai_client()
    if client is None:
        return

    index = load_session_index()

    session_name = input("Enter a session name (or press Enter to start a new session): ").strip()

    new_session = False
    history = []
    session_path = None

    if session_name == "":
        new_session = True
    elif session_name in index:
        session_path = os.path.join(SESSIONS_DIR, f"{session_name}.json")
        history = load_session_history(session_path)
    else:
        print(f"No session called {session_name}. Starting a new one.")
        new_session = True

    if new_session:
        first_question = input("You: ").strip()
        if first_question in ("exit", "EXIT"):
            print("Goodbye!")
            return

        generated_name = generate_two_word_session_name(client, first_question)
        session_name = unique_session_name(generated_name, index)
        session_path = os.path.join(SESSIONS_DIR, f"{session_name}.json")
        history = [{"role": "user", "content": first_question}]

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=history,
            )
            answer = response.choices[0].message.content or ""
        except OpenAIError as error:
            print(f"API error: {error}")
            return

        print("Assistant:", answer)
        history.append({"role": "assistant", "content": answer})
        save_session_history(history, session_path)
        index[session_name] = session_name
        save_session_index(index)

    while True:
        user_input = input("You: ").strip()
        if user_input in ("exit", "EXIT"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=history,
            )
            answer = response.choices[0].message.content or ""
        except OpenAIError as error:
            print(f"API error: {error}")
            history.pop()
            continue

        print("Assistant:", answer)
        history.append({"role": "assistant", "content": answer})
        save_session_history(history, session_path)
        save_session_index(index)


if __name__ == "__main__":
    main()
