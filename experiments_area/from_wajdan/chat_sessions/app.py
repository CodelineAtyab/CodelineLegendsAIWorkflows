import json
import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


INDEX_FILE = "session_index.json"
SESSIONS_FOLDER = "sessions"
MODEL = "gpt-4.1-mini"


def load_index():
    """Read and validate the dictionary of session names and IDs."""
    if not os.path.exists(INDEX_FILE):
        return {}

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            index = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("The session index contains malformed JSON.")
    except OSError:
        raise OSError("The session index could not be read.")

    if not isinstance(index, dict):
        raise ValueError("The session index must be a JSON dictionary.")

    session_ids = []
    for name, session_id in index.items():
        if not isinstance(name, str) or not name:
            raise ValueError("The session index contains an invalid name.")
        if name != os.path.basename(name) or "/" in name or "\\" in name:
            raise ValueError("The session index contains an unsafe name.")
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("The session index contains an invalid ID.")
        if session_id in session_ids:
            raise ValueError("The session index contains duplicate IDs.")
        session_ids.append(session_id)

    return index


def load_history(session_name):
    """Read and validate one saved conversation."""
    file_name = os.path.join(SESSIONS_FOLDER, session_name + ".json")
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            history = json.load(file)
    except json.JSONDecodeError:
        raise ValueError(f"The history for {session_name} contains malformed JSON.")
    except OSError:
        raise OSError(f"The history for {session_name} could not be read.")

    if not isinstance(history, list):
        raise ValueError(f"The history for {session_name} must be a list.")

    for message in history:
        if not isinstance(message, dict):
            raise ValueError(f"The history for {session_name} contains invalid data.")
        if len(message) != 2 or "role" not in message or "content" not in message:
            raise ValueError(f"The history for {session_name} contains invalid data.")
        if message["role"] not in ("user", "assistant"):
            raise ValueError(f"The history for {session_name} contains an invalid role.")
        if not isinstance(message["content"], str):
            raise ValueError(f"The history for {session_name} contains invalid content.")

    return history


def save_data(index, session_name, history):
    """Save the conversation and the session index after an answer."""
    try:
        os.makedirs(SESSIONS_FOLDER, exist_ok=True)
        history_file_name = os.path.join(SESSIONS_FOLDER, session_name + ".json")
        with open(history_file_name, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=2, ensure_ascii=False)
            file.write("\n")

        with open(INDEX_FILE, "w", encoding="utf-8") as file:
            json.dump(index, file, indent=2, ensure_ascii=False)
            file.write("\n")
    except OSError:
        raise OSError("Saving did not complete. The program will stop safely.")


def choose_session(index):
    """Ask for a session name and return its name and history."""
    try:
        name = input("Session name (Enter for a new session): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
        return None, None, True

    if name == "":
        return None, [], False

    if name not in index:
        print(f"No session called {name}. Starting a new one.")
        return None, [], False

    try:
        history = load_history(name)
    except (OSError, ValueError) as error:
        print(f"Could not load session: {error}")
        return None, None, True
    return name, history, False


def make_session_name(client, first_question, index):
    """Ask the model for two words and make a safe, unique file name."""
    messages = [
        {"role": "system", "content": "Return only two words that describe the user's question."},
        {"role": "user", "content": first_question},
    ]
    answer = ask_openai(client, messages, "naming")

    # Keep letters and numbers, and use spaces as word separators.
    words = []
    current_word = ""
    for character in answer.lower():
        if ("a" <= character <= "z") or ("0" <= character <= "9"):
            current_word += character
        elif current_word:
            words.append(current_word)
            current_word = ""
    if current_word:
        words.append(current_word)

    if len(words) >= 2:
        base_name = words[0] + "_" + words[1]
    elif len(words) == 1:
        base_name = words[0] + "_session"
    else:
        base_name = "new_session"

    # Add a number instead of overwriting an old session.
    name = base_name
    number = 2
    while name in index or os.path.exists(os.path.join(SESSIONS_FOLDER, name + ".json")):
        first_word, second_word = base_name.split("_", 1)
        name = first_word + "_" + second_word + str(number)
        number += 1
    return name


def ask_openai(client, messages, purpose):
    """Send messages and return the model's text response."""
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages)
    except OpenAIError as error:
        if type(error).__name__ == "RateLimitError":
            error_code = getattr(error, "code", None) or "unknown"
            raise RuntimeError(f"RateLimitError code: {error_code}. Check your usage limits.")
        raise RuntimeError(f"The OpenAI {purpose} request failed. Check your key, billing, or connection.")

    try:
        text = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError):
        raise RuntimeError(f"The OpenAI {purpose} response was malformed.")
    if not isinstance(text, str) or text.strip() == "":
        raise RuntimeError(f"The OpenAI {purpose} response was empty.")
    return text.strip()


def main():
    # Load the key before creating the OpenAI client.
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    placeholder_keys = ("your-key", "your_api_key_here", "your-api-key", "replace-me", "changeme")
    if not api_key:
        print("OPENAI_API_KEY is missing. Add your real key to .env.")
        return
    if api_key.lower() in placeholder_keys:
        print("OPENAI_API_KEY is still a placeholder. Add your real key to .env.")
        return

    try:
        index = load_index()
    except (OSError, ValueError) as error:
        print(f"Could not load sessions: {error}")
        return

    session_name, history, stopped = choose_session(index)
    if stopped:
        return

    try:
        client = OpenAI(api_key=api_key)
    except OpenAIError:
        print("The OpenAI client could not start. Check your API key.")
        return

    new_session = session_name is None
    while True:
        prompt = "First question: " if new_session else "You: "
        try:
            user_message = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return

        if user_message.lower() == "exit":
            return
        if user_message == "":
            continue

        if new_session:
            try:
                session_name = make_session_name(client, user_message, index)
            except RuntimeError as error:
                print(error)
                return
            print(f"Session name: {session_name}")

            session_number = len(index) + 1
            session_id = "session-" + str(session_number)
            while session_id in index.values():
                session_number += 1
                session_id = "session-" + str(session_number)
            index[session_name] = session_id
            new_session = False

        history.append({"role": "user", "content": user_message})
        try:
            assistant_message = ask_openai(client, history, "chat")
        except RuntimeError as error:
            history.pop()
            print(error)
            continue

        history.append({"role": "assistant", "content": assistant_message})
        print(f"Assistant: {assistant_message}")
        try:
            save_data(index, session_name, history)
        except OSError as error:
            print(error)
            return


if __name__ == "__main__":
    main()
