import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


INDEX_PATH = Path("session_index.json")
SESSIONS_DIR = Path("sessions")
MODEL = "gpt-4.1-mini"


def validate_index(data):
    """Return whether the session index has the expected shape and unique IDs."""
    if not isinstance(data, dict):
        return False
    values = []
    for name, session_id in data.items():
        if not isinstance(name, str) or not name:
            return False
        if not isinstance(session_id, str) or not session_id:
            return False
        values.append(session_id)
    return len(values) == len(set(values))


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
    return all(
        isinstance(message, dict)
        and set(message) == {"role", "content"}
        and isinstance(message["role"], str)
        and isinstance(message["content"], str)
        for message in history
    )


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
    """Save readable UTF-8 JSON after a successful assistant response."""
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


def name_session(client, first_question, index):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Return only two words that describe the user's question."},
                {"role": "user", "content": first_question},
            ],
        )
        raw_name = response.choices[0].message.content or ""
    except Exception as error:
        raise RuntimeError(f"Could not generate a session name: {error}")

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
    try:
        response = client.chat.completions.create(model=MODEL, messages=history)
        reply = response.choices[0].message.content
        if not reply:
            raise ValueError("The model returned an empty response.")
        return reply
    except Exception as error:
        raise RuntimeError(f"The request failed: {error}")


def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is missing. Create a local .env with OPENAI_API_KEY=your-key.")
        return

    try:
        index = load_index()
    except (OSError, ValueError) as error:
        print(f"Could not load sessions: {error}")
        return

    session_name, history, stopped = get_session(index)
    if stopped:
        return
    client = OpenAI(api_key=api_key)
    is_new = session_name is None

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
            session_id = f"session-{len(index) + 1}"
            while session_id in index.values():
                session_id = f"session-{int(session_id.split('-')[1]) + 1}"
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
