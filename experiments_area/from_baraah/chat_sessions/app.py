import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

BASE_DIR = Path(__file__).parent
SESSIONS_DIR = BASE_DIR / "sessions"
INDEX_FILE = SESSIONS_DIR / "index.json"
MODEL = "gpt-4.1-mini"


def load_json(path, default):
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default
    except (OSError, json.JSONDecodeError):
        print(f"Could not read {path.name}. Starting with empty data.")
        return default


def save_json(path, data):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        return True
    except OSError:
        print(f"Could not save {path.name}.")
        return False


def load_index():
    index = load_json(INDEX_FILE, {})
    if not isinstance(index, dict):
        print("The session index is not valid. Starting with an empty index.")
        return {}
    return index


def save_index(index):
    return save_json(INDEX_FILE, index)


def session_file(session_name):
    return SESSIONS_DIR / f"{session_name}.json"


def load_history(session_name):
    return load_json(session_file(session_name), [])


def save_history(session_name, history):
    return save_json(session_file(session_name), history)


def ask_for_session(index):
    requested_name = input(
        "Enter a session name to resume, or press Enter for a new session: "
    ).strip()

    if requested_name and requested_name in index:
        return requested_name, True

    if requested_name:
        print(f"No session called {requested_name}. Starting a new one.")

    return "", False


def clean_session_name(model_name):
    words = model_name.replace("_", " ").replace("-", " ").split()
    clean_words = []

    for word in words:
        clean_word = "".join(
            character for character in word.lower() if character.isalnum()
        )
        if clean_word:
            clean_words.append(clean_word)

    if not clean_words:
        return "new_session"

    return "_".join(clean_words[:2])


def unique_session_name(session_name, index):
    if session_name not in index:
        return session_name

    suffix = 2
    while f"{session_name}_{suffix}" in index:
        suffix += 1

    return f"{session_name}_{suffix}"


def call_model(client, messages):
    response = client.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content.strip()


def generate_session_name(client, first_question):
    naming_prompt = (
        "Choose a short name for this conversation based on the question below. "
        "Reply with only two words and nothing else.\n\n"
        f"Question: {first_question}"
    )
    naming_messages = [{"role": "user", "content": naming_prompt}]
    return clean_session_name(call_model(client, naming_messages))


def chat_loop(client, index, session_name, history, is_new_session):
    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            return

        if not question:
            continue

        if is_new_session:
            try:
                session_name = generate_session_name(client, question)
            except OpenAIError:
                print("Could not generate a session name. Using new_session.")
                session_name = "new_session"
            session_name = unique_session_name(session_name, index)

        history.append({"role": "user", "content": question})

        try:
            answer = call_model(client, history)
        except OpenAIError:
            history.pop()
            print("The assistant could not answer. Please try again.")
            continue

        print(f"Assistant: {answer}")
        history.append({"role": "assistant", "content": answer})

        if not save_history(session_name, history):
            return

        if is_new_session:
            index[session_name] = f"session-{len(index) + 1}"
            is_new_session = False

        if not save_index(index):
            print("The reply was saved, but the session index could not be updated.")


def main():
    load_dotenv()
    index = load_index()
    session_name, is_resumed = ask_for_session(index)
    history = load_history(session_name) if is_resumed else []

    if is_resumed and not isinstance(history, list):
        print("The session file is not a valid message list.")
        return

    try:
        client = OpenAI()
    except OpenAIError:
        print("Could not create the OpenAI client. Check your API key in .env.")
        return

    chat_loop(client, index, session_name, history, not is_resumed)


if __name__ == "__main__":
    main()
