import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from utils.cli_args import clean_session_name, is_exit_word, parse_args

INDEX_FILE = "session_index.json"
SESSIONS_FOLDER = "sessions"
MODEL = "gpt-4.1-mini"


def load_index():
    """Read the saved session index."""
    if not os.path.exists(INDEX_FILE):
        return {}
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError("The session index contains malformed JSON.") from error
    except OSError as error:
        raise OSError("The session index could not be read.") from error


def load_history(session_name):
    """Read one saved conversation."""
    file_name = os.path.join(SESSIONS_FOLDER, session_name + ".json")
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"The history for {session_name} contains malformed JSON."
        ) from error
    except OSError as error:
        raise OSError(f"The history for {session_name} could not be read.") from error


def save_data(index, session_name, history):
    """Save the conversation and the session index after an answer."""
    try:
        os.makedirs(SESSIONS_FOLDER, exist_ok=True)
        with open(
            os.path.join(SESSIONS_FOLDER, session_name + ".json"),
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(history, file, indent=2, ensure_ascii=False)
            file.write("\n")
        with open(INDEX_FILE, "w", encoding="utf-8") as file:
            json.dump(index, file, indent=2, ensure_ascii=False)
            file.write("\n")
    except OSError as error:
        raise OSError(
            "Saving did not complete. The program will stop safely."
        ) from error


def choose_session(index):
    """Ask for a session name and return its name and history."""
    try:
        name = input("Session name (Enter for a new session): ").strip()
    except EOFError, KeyboardInterrupt:
        print("\nGoodbye.")
        return None, None, True
    if name == "":
        return None, [], False
    name = clean_session_name(name)
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
        {
            "role": "system",
            "content": "Return only two words that describe the user's question.",
        },
        {"role": "user", "content": first_question},
    ]
    answer = ask_openai(client, messages, "naming")
    base_name = clean_session_name(answer)
    name = base_name
    number = 2
    while name in index or os.path.exists(
        os.path.join(SESSIONS_FOLDER, name + ".json")
    ):
        name = f"{base_name}{number}"
        number += 1
    return name


def ask_openai(client, messages, purpose):
    """Send messages and return the model's text response."""
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages)
    except OpenAIError as error:
        if type(error).__name__ == "RateLimitError":
            error_code = getattr(error, "code", None) or "unknown"
            raise RuntimeError(
                f"RateLimitError code: {error_code}. Check your usage limits."
            ) from error
        raise RuntimeError(
            f"The OpenAI {purpose} request failed. Check your key, billing, or connection."
        ) from error
    try:
        text = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError) as error:
        raise RuntimeError(f"The OpenAI {purpose} response was malformed.") from error
    if not isinstance(text, str) or text.strip() == "":
        raise RuntimeError(f"The OpenAI {purpose} response was empty.")
    return text.strip()


def create_session_id(index):
    """Return the next available session identifier."""
    session_number = len(index) + 1
    session_id = f"session-{session_number}"
    while session_id in index.values():
        session_number += 1
        session_id = f"session-{session_number}"
    return session_id


def get_client():
    """Load credentials and create the OpenAI client."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    placeholder_keys = {
        "your-key",
        "your_api_key_here",
        "your-api-key",
        "replace-me",
        "changeme",
    }
    if not api_key:
        raise SystemExit("Error: OPENAI_API_KEY is missing.")
    if api_key.lower() in placeholder_keys:
        raise SystemExit("Error: OPENAI_API_KEY is still a placeholder.")
    try:
        return OpenAI(api_key=api_key)
    except OpenAIError as error:
        raise SystemExit("Error: the OpenAI client could not start.") from error


def answer_once(client, index, session_name, history, question):
    """Answer one question, save the session, and return its name and reply."""
    if session_name is None:
        session_name = make_session_name(client, question, index)
        index[session_name] = create_session_id(index)
    history.append({"role": "user", "content": question})
    try:
        reply = ask_openai(client, history, "chat")
    except RuntimeError:
        history.pop()
        raise
    history.append({"role": "assistant", "content": reply})
    save_data(index, session_name, history)
    return session_name, reply


def run_non_interactive(session_name, question, index):
    """Run one non-interactive question and print exactly two result lines."""
    if session_name is not None:
        session_name = clean_session_name(session_name)
        if session_name not in index:
            raise SystemExit(f"Error: unknown session '{session_name}'.")
        history = load_history(session_name)
    else:
        history = []
    client = get_client()
    try:
        session_name, reply = answer_once(
            client, index, session_name, history, question
        )
    except (OSError, RuntimeError, ValueError) as error:
        raise SystemExit(f"Error: {error}") from error
    print(f"Session: {session_name}")
    print(f"Assistant: {reply.replace(chr(13), ' ').replace(chr(10), ' ')}")


def main():
    """Run interactive or one-question chat mode."""
    session_name, question = parse_args(sys.argv)
    try:
        index = load_index()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Error: {error}") from error
    if question is not None:
        run_non_interactive(session_name, question, index)
        return

    session_name, history, stopped = choose_session(index)
    if stopped:
        return
    try:
        client = get_client()
    except SystemExit as error:
        print(error)
        return
    new_session = session_name is None
    while True:
        prompt = "First question: " if new_session else "You: "
        try:
            user_message = input(prompt).strip()
        except EOFError, KeyboardInterrupt:
            print("\nGoodbye.")
            return
        if is_exit_word(user_message):
            return
        if user_message == "":
            continue
        try:
            session_name, reply = answer_once(
                client, index, session_name, history, user_message
            )
        except RuntimeError as error:
            print(error)
            continue
        if new_session:
            print(f"Session name: {session_name}")
            new_session = False
        print(f"Assistant: {reply}")


if __name__ == "__main__":
    main()
