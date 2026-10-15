import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, APIError, AuthenticationError, OpenAI, RateLimitError


INDEX_PATH = Path("session_index.json")
SESSIONS_DIR = Path("sessions")
MODEL = "gpt-4.1-mini"
PLACEHOLDER_KEYS = {"your-key", "your_api_key_here", "your-api-key", "replace-me", "changeme"}


def validate_index(data):
    if not isinstance(data, dict):
        return False

    session_ids = []
    for name, session_id in data.items():
        if not isinstance(name, str) or not name:
            return False
        if not isinstance(session_id, str) or not session_id:
            return False
        if session_id in session_ids:
            return False
        session_ids.append(session_id)
    return True


def load_index():
    if not INDEX_PATH.exists():
        return {}
    try:
        with INDEX_PATH.open("r", encoding="utf-8") as index_file:
            data = json.load(index_file)
    except json.JSONDecodeError:
        raise ValueError("The session index contains malformed JSON.")
    except OSError as error:
        raise OSError(f"Could not read the session index: {error}")
    if not validate_index(data):
        raise ValueError("The session index has invalid data.")
    return data


def validate_history(history):
    if not isinstance(history, list):
        return False

    for message in history:
        if not isinstance(message, dict):
            return False
        if "role" not in message or "content" not in message:
            return False
        if len(message) != 2:
            return False
        if not isinstance(message["role"], str):
            return False
        if not isinstance(message["content"], str):
            return False
    return True


def load_history(session_name):
    path = SESSIONS_DIR / f"{session_name}.json"
    try:
        with path.open("r", encoding="utf-8") as history_file:
            history = json.load(history_file)
    except json.JSONDecodeError:
        raise ValueError(f"The history for {session_name} contains malformed JSON.")
    except OSError as error:
        raise OSError(f"Could not read the history for {session_name}: {error}")
    if not validate_history(history):
        raise ValueError(f"The history for {session_name} has invalid data.")
    return history


def save_session(index, session_name, history):
    try:
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        with (SESSIONS_DIR / f"{session_name}.json").open("w", encoding="utf-8") as history_file:
            json.dump(history, history_file, indent=2, ensure_ascii=False)
            history_file.write("\n")
        with INDEX_PATH.open("w", encoding="utf-8") as index_file:
            json.dump(index, index_file, indent=2, ensure_ascii=False)
            index_file.write("\n")
    except OSError as error:
        raise OSError(f"Saving did not complete: {error}")


def clean_generated_name(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    words = words[:2]
    if len(words) == 2:
        return "_".join(words)
    if len(words) == 1:
        return f"{words[0]}_session"
    return "new_session"


def request_model(client, messages, purpose):
    try:
        return client.chat.completions.create(model=MODEL, messages=messages)
    except AuthenticationError:
        raise RuntimeError("OpenAI authentication failed. Check OPENAI_API_KEY in .env.")
    except RateLimitError:
        raise RuntimeError("OpenAI rate limit or billing limit reached. Check your account.")
    except APIConnectionError:
        raise RuntimeError("Could not connect to OpenAI. Check your internet connection.")
    except APIError:
        raise RuntimeError(f"The OpenAI {purpose} request failed. Please try again.")
    except Exception:
        raise RuntimeError(f"The OpenAI {purpose} request could not be completed.")


def response_text(response, purpose):
    try:
        content = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError):
        raise RuntimeError(f"The OpenAI {purpose} response was malformed.")
    if not isinstance(content, str):
        raise RuntimeError(f"The OpenAI {purpose} response was malformed.")
    if not content.strip():
        raise RuntimeError(f"The OpenAI {purpose} response was empty.")
    return content.strip()


def name_session(client, first_question, index):
    response = request_model(
        client,
        [
            {"role": "system", "content": "Return only two words that describe the user's question."},
            {"role": "user", "content": first_question},
        ],
        "naming",
    )
    raw_name = response_text(response, "naming")

    base_name = clean_generated_name(raw_name)
    candidate = base_name
    suffix = 2
    while candidate in index or (SESSIONS_DIR / f"{candidate}.json").exists():
        first, second = base_name.split("_", 1)
        candidate = f"{first}_{second}{suffix}"
        suffix += 1
    return candidate


def get_session(index):
    try:
        requested_name = input("Session name (Enter for a new session): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
        return None, None, True

    if not requested_name:
        return None, [], False
    if requested_name not in index:
        print(f"No session called {requested_name}. Starting a new one.")
        return None, [], False
    try:
        return requested_name, load_history(requested_name), False
    except (OSError, ValueError) as error:
        print(f"Could not load session: {error}")
        return None, None, True


def request_reply(client, history):
    response = request_model(client, history, "chat")
    return response_text(response, "chat")


def main():
    load_dotenv(dotenv_path=Path(__file__).with_name(".env"))
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("OPENAI_API_KEY is missing. Create a local .env with your real API key.")
        return
    if api_key.lower() in PLACEHOLDER_KEYS:
        print("OPENAI_API_KEY is still a placeholder. Put your real API key in .env.")
        return

    # Load the saved index before asking for a session.
    try:
        index = load_index()
    except (OSError, ValueError) as error:
        print(f"Could not load sessions: {error}")
        return

    session_name, history, stopped = get_session(index)
    if stopped:
        return
    # Create the client only after the local key has been checked.
    try:
        client = OpenAI(api_key=api_key)
    except Exception:
        print("Could not start the OpenAI client. Please check your local configuration.")
        return
    is_new = session_name is None

    # Continue asking questions until the user exits.
    while True:
        prompt = "First question: " if is_new else "You: "
        try:
            message = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return
        if message.lower() == "exit":
            return
        if not message:
            continue

        if is_new:
            try:
                session_name = name_session(client, message, index)
            except RuntimeError as error:
                print(error)
                return
            session_number = len(index) + 1
            session_id = f"session-{session_number}"
            while session_id in index.values():
                session_number += 1
                session_id = f"session-{session_number}"
            index[session_name] = session_id
            is_new = False

        history.append({"role": "user", "content": message})
        try:
            reply = request_reply(client, history)
        except RuntimeError as error:
            history.pop()
            print(error)
            continue

        history.append({"role": "assistant", "content": reply})
        print(f"Assistant: {reply}")
        try:
            save_session(index, session_name, history)
        except OSError as error:
            print(error)
            return


if __name__ == "__main__":
    main()
