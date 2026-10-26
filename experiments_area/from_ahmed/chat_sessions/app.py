import json
import os
import sys
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from utils.cli_args import clean_session_name, is_exit_word, parse_args

INDEX_FILE = "session_index.json"
SESSIONS_DIR = "sessions"
MODEL_NAME = "gpt-4.1-mini"


def load_session_index() -> dict[str, str]:
    """Read saved session mapping, returning an empty dict if not found."""
    if not os.path.exists(INDEX_FILE):
        return {}
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        print("Warning: Could not read index file, starting with empty session list.")
        return {}


def load_history(session_name: str) -> list[dict[str, Any]] | None:
    """Load session conversation history from disk."""
    file_path = os.path.join(SESSIONS_DIR, f"{session_name}.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Could not load session '{session_name}': {e}")
        return None


def save_session(index: dict[str, str], session_name: str, history: list[dict[str, Any]]) -> None:
    """Save history to session JSON file and update index."""
    try:
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        file_path = os.path.join(SESSIONS_DIR, f"{session_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"Could not save session data: {e}")


def ask_model(client: OpenAI, messages: list[Any]) -> str:
    """Call GPT-4.1 mini and return trimmed response text."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )
        content = response.choices[0].message.content or ""
        return content.strip()
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI API call failed: {e}") from e


def generate_two_word_name(client: OpenAI, first_question: str, existing_index: dict[str, str]) -> str:
    """Request a 2-word title from the model and ensure unique file name."""
    prompt = [
        {
            "role": "system",
            "content": "Generate a concise 2-word title for the following query. Return only two words separated by a space, nothing else."
        },
        {"role": "user", "content": first_question}
    ]
    try:
        raw_reply = ask_model(client, prompt)
        base_name = clean_session_name(raw_reply)
    except (OpenAIError, RuntimeError):
        base_name = "new_session"

    name = base_name
    counter = 2
    while name in existing_index:
        name = f"{base_name}_{counter}"
        counter += 1
    return name


def select_session(index: dict[str, str]) -> tuple[str | None, list[dict[str, Any]], bool]:
    """Prompt user interactively to pick or start a session."""
    try:
        name_input = input("Enter session name (press Enter for a new session): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        return None, [], True

    if not name_input:
        return None, [], False

    if name_input not in index:
        print(f"No session called {name_input}. Starting a new one.")
        return None, [], False

    history = load_history(name_input)
    if history is None:
        print("Falling back to a new session.")
        return None, [], False

    return name_input, history, False


def run_interactive(client: OpenAI, index: dict[str, str]) -> None:
    """Run interactive terminal chat loop."""
    session_name, history, should_exit = select_session(index)
    if should_exit:
        return

    is_new = session_name is None
    if not is_new and session_name is not None:
        print(f"Resumed session '{session_name}' with {len(history)} messages.")

    while True:
        try:
            prompt_label = "First question: " if is_new else "You: "
            user_input = input(prompt_label).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if is_exit_word(user_input):
            print("Session ended.")
            break

        if is_new or session_name is None:
            session_name = generate_two_word_name(client, user_input, index)
            session_id = f"session-{len(index) + 1}"
            index[session_name] = session_id
            print(f"Session name: {session_name}")
            is_new = False

        history.append({"role": "user", "content": user_input})

        try:
            assistant_reply = ask_model(client, history)
        except RuntimeError as e:
            print(f"Could not get response: {e}")
            history.pop()
            continue

        history.append({"role": "assistant", "content": assistant_reply})
        print(f"Assistant: {assistant_reply}\n")

        save_session(index, session_name, history)


def run_non_interactive(client: OpenAI, index: dict[str, str], session_arg: str | None, question: str) -> None:
    """Run one-shot question without interactive prompts."""
    history: list[dict[str, Any]] = []
    if session_arg is not None:
        if session_arg not in index:
            raise SystemExit(f"Error: session '{session_arg}' does not exist.")
        session_name = session_arg
        loaded = load_history(session_name)
        if loaded is None:
            raise SystemExit(f"Error: could not read history for session '{session_name}'.")
        history = loaded
    else:
        session_name = generate_two_word_name(client, question, index)
        session_id = f"session-{len(index) + 1}"
        index[session_name] = session_id

    history.append({"role": "user", "content": question})

    try:
        reply = ask_model(client, history)
    except RuntimeError as e:
        raise SystemExit(f"Error: {e}")

    history.append({"role": "assistant", "content": reply})

    print(f"Session: {session_name}")
    print(f"Assistant: {reply}")

    save_session(index, session_name, history)


def main() -> None:
    session_arg, question_arg = parse_args(sys.argv)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Error: OPENAI_API_KEY not found in environment or .env file.")

    try:
        client = OpenAI(api_key=api_key)
    except OpenAIError as e:
        raise SystemExit(f"Error: failed to initialize OpenAI client: {e}")

    index = load_session_index()

    if question_arg is None:
        run_interactive(client, index)
    else:
        run_non_interactive(client, index, session_arg, question_arg)


if __name__ == "__main__":
    main()
