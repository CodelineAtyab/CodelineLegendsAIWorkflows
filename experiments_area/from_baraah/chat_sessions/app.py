
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from utils.cli_args import clean_session_name, is_exit_word, parse_args

BASE_DIR = Path(__file__).parent
SESSIONS_DIR = BASE_DIR / "sessions"
INDEX_FILE = SESSIONS_DIR / "index.json"
MODEL = "gpt-4.1-mini"


def load_json(path, default):
    """Read data from a JSON file."""
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default
    except (OSError, json.JSONDecodeError):
        print(f"Could not read {path.name}. Starting with empty data.")
        return default


def save_json(path, data):
    """Save data to a JSON file."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        return True
    except OSError:
        print(f"Could not save {path.name}.")
        return False


def load_index():
    """Load the saved session names."""
    index = load_json(INDEX_FILE, {})

    if not isinstance(index, dict):
        print("The session index is not valid. Starting with an empty index.")
        return {}

    return index


def save_index(index):
    """Save the session index."""
    return save_json(INDEX_FILE, index)


def session_file(session_name):
    """Get the file path for a session."""
    return SESSIONS_DIR / f"{session_name}.json"


def load_history(session_name):
    """Load previous messages."""
    return load_json(session_file(session_name), [])


def save_history(session_name, history):
    """Save all chat messages."""
    return save_json(session_file(session_name), history)


def ask_for_session(index):
    """Ask whether to resume an existing session."""
    requested_name = input(
        "Enter a session name to resume, or press Enter for a new session: "
    ).strip()

    if requested_name and requested_name in index:
        return requested_name, True

    if requested_name:
        print(f"No session called {requested_name}. Starting a new one.")

    return "", False


def unique_session_name(session_name, index):
    """Avoid creating duplicate session names."""
    if session_name not in index:
        return session_name

    suffix = 2

    while f"{session_name}_{suffix}" in index:
        suffix += 1

    return f"{session_name}_{suffix}"


def call_model(client, messages):
    """Send messages to GPT-4.1 mini."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    return response.choices[0].message.content.strip()


def generate_session_name(client, first_question):
    """Generate a short session name using the model."""
    naming_prompt = (
        "Choose a short name for this conversation based on the question below. "
        "Reply with only two words and nothing else.\n\n"
        f"Question: {first_question}"
    )

    naming_messages = [
        {"role": "user", "content": naming_prompt}
    ]

    return clean_session_name(call_model(client, naming_messages))


def chat_loop(client, index, session_name, history, is_new_session):
    """Run the interactive chatbot."""
    while True:
        question = input("You: ").strip()

        if is_exit_word(question):
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


def run_non_interactive(client, index, session_name, question):
    """Answer one question without asking for input."""
    is_new_session = session_name is None

    if is_new_session:
        history = []
        session_name = generate_session_name(client, question)
        session_name = unique_session_name(session_name, index)
    else:
        history = load_history(session_name)

    if not isinstance(history, list):
        raise SystemExit(f"Error: session {session_name} has invalid history.")

    history.append({"role": "user", "content": question})

    try:
        answer = call_model(client, history)
    except OpenAIError:
        history.pop()
        raise

    history.append({"role": "assistant", "content": answer})

    if not save_history(session_name, history):
        raise SystemExit("Error: could not save session history.")

    if is_new_session:
        index[session_name] = f"session-{len(index) + 1}"

    if not save_index(index):
        raise SystemExit("Error: could not save the session index.")

    answer_line = " ".join(answer.splitlines())

    print(f"Session: {session_name}")
    print(f"Assistant: {answer_line}")


def main():
    """Choose interactive or non-interactive mode."""
    session_name, question = parse_args(sys.argv)

    load_dotenv()

    index = load_index()

    # If a question is provided, use non-interactive mode.
    if question is not None:

        # Only check existing sessions when a name is provided.
        if session_name is not None and session_name not in index:
            raise SystemExit(f"Error: no session called {session_name}.")

        try:
            client = OpenAI()
            run_non_interactive(client, index, session_name, question)
        except OpenAIError as error:
            raise SystemExit(f"Error: {error}") from None
        except ValueError:
            raise SystemExit("Error: Check your OpenAI API key.") from None

        return

    # No question means interactive mode.
    session_name, is_resumed = ask_for_session(index)

    history = load_history(session_name) if is_resumed else []

    if is_resumed and not isinstance(history, list):
        print("The session file is not a valid message list.")
        return

    try:
        client = OpenAI()
    except (OpenAIError, ValueError):
        print("Could not create the OpenAI client. Check your API key in .env.")
        return

    chat_loop(client, index, session_name, history, not is_resumed)


if __name__ == "__main__":
    main()
