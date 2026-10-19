import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from utils.cli_args import clean_session_name, is_exit_word, parse_args

MODEL = "gpt-4.1-mini"
INDEX_FILE = Path("sessions_index.json")
SESSIONS_FOLDER = Path("sessions")


def load_index() -> dict[str, str]:
    """Load the session-name index."""
    if not INDEX_FILE.exists():
        return {}

    return json.loads(INDEX_FILE.read_text(encoding="utf-8"))


def save_index(index: dict[str, str]) -> None:
    """Save the session-name index."""
    INDEX_FILE.write_text(
        json.dumps(index, indent=2),
        encoding="utf-8",
    )


def load_history(session_id: str) -> list[dict[str, str]]:
    """Load a session's message history."""
    path = SESSIONS_FOLDER / f"{session_id}.json"

    if not path.exists():
        return []

    return json.loads(path.read_text(encoding="utf-8"))


def save_history(session_id: str, history: list[dict[str, str]]) -> None:
    """Save a session's message history."""
    SESSIONS_FOLDER.mkdir(parents=True, exist_ok=True)
    path = SESSIONS_FOLDER / f"{session_id}.json"
    path.write_text(json.dumps(history, indent=2), encoding="utf-8")


def create_session(question: str, index: dict[str, str]) -> str:
    """Create a unique session name based on the question."""
    name = clean_session_name(question)

    if name == "new_session":
        name = "new_session"

    original_name = name
    number = 2

    while name in index:
        name = f"{original_name}_{number}"
        number += 1

    index[name] = name
    save_index(index)
    save_history(name, [])
    return name


def ask_question(
    client: OpenAI,
    history: list[dict[str, str]],
    question: str,
) -> str:
    """Send a question with the conversation history."""
    history.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=MODEL,
        messages=history,
    )

    answer = response.choices[0].message.content or ""
    history.append({"role": "assistant", "content": answer})
    return answer


def run_non_interactive(
    client: OpenAI,
    session_name: str | None,
    question: str,
) -> None:
    """Ask one question and save the conversation."""
    index = load_index()

    if session_name is None:
        session_name = create_session(question, index)
    elif session_name not in index:
        raise SystemExit(f"Error: Session '{session_name}' was not found.")

    session_id = index[session_name]
    history = load_history(session_id)

    answer = ask_question(client, history, question)
    save_history(session_id, history)

    print(answer)


def run_interactive(client: OpenAI) -> None:
    """Run the interactive chat loop."""
    index = load_index()
    session_name = input("Enter session name: ").strip()

    if not session_name:
        session_name = create_session("new session", index)
        index = load_index()
    elif session_name not in index:
        index[session_name] = session_name
        save_index(index)
        save_history(session_name, [])

    session_id = index[session_name]
    history = load_history(session_id)

    print("Chat started. Type 'exit' or 'quit' to stop.")

    while True:
        question = input("You: ").strip()

        if is_exit_word(question):
            save_history(session_id, history)
            print("Chat ended.")
            break

        if not question:
            print("Error: Question cannot be blank.")
            continue

        try:
            answer = ask_question(client, history, question)
            print(f"Assistant: {answer}")
            save_history(session_id, history)
        except (OSError, ValueError, TypeError, KeyError, IndexError) as error:
            print(f"Error: Could not get a response: {error}")


def main() -> None:
    """Start interactive or command-line chat mode."""
    load_dotenv()
    session_name, question = parse_args(sys.argv)

    client = OpenAI()

    if question is None:
        run_interactive(client)
    else:
        run_non_interactive(client, session_name, question)


if __name__ == "__main__":
    main()
