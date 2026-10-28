
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "gpt-4.1-mini"
SESSIONS_DIR = "sessions"
INDEX_FILE = "session_index.json"


def load_index():
    """Load the session name-to-ID mapping."""
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except (OSError, json.JSONDecodeError):
        print("Could not read the session index.")
        raise


def save_index(index):
    """Save the session index."""
    try:
        with open(INDEX_FILE, "w", encoding="utf-8") as file:
            json.dump(index, file, indent=4)
    except OSError:
        print("Could not save the session index.")
        raise


def load_history(session_name):
    """Load a session's messages."""
    path = os.path.join(SESSIONS_DIR, f"{session_name}.json")

    try:
        with open(path, "r", encoding="utf-8") as file:
            history = json.load(file)

        if not isinstance(history, list):
            raise ValueError("Invalid conversation history.")

        return history
    except (OSError, json.JSONDecodeError, ValueError):
        print("Could not read this conversation.")
        raise


def save_history(session_name, history):
    """Save the conversation messages."""
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    path = os.path.join(SESSIONS_DIR, f"{session_name}.json")

    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4, ensure_ascii=False)
    except OSError:
        print("Could not save the conversation.")
        raise


def ask_for_session(index):
    """Resume a named session or start a new one."""
    session_name = input(
        "Enter a session name to resume, or press Enter for a new chat: "
    ).strip()

    if not session_name:
        return None

    if session_name in index:
        return session_name

    print(f"No session called {session_name}. Starting a new one.")
    return None


def generate_session_name(client, question, index):
    """Ask the model for a unique, two-word session name."""
    for attempt in range(5):
        instruction = (
            "Create a short name for this conversation based on the user's "
            "first question. Reply with exactly two meaningful words, "
            "and nothing else. Use only lowercase English letters and "
            "a space between the words. Do not use punctuation."
        )

        if attempt > 0:
            instruction += (
                " Choose a different name from these existing names: "
                + ", ".join(index.keys())
            )

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": question},
                ],
            )

            text = response.choices[0].message.content or ""

            # Split the text into words and join the first two with an underscore.
            words = text.lower().split()
            name = "_".join(words[:2])

            if len(words) >= 2 and name not in index:
                return name

        except Exception:
            print("Could not generate a session name.")
            raise

    # Use a fallback name if the model cannot create a unique name.
    name = "new_session"
    number = 2

    while name in index:
        name = f"new_session_{number}"
        number += 1

    return name


def get_answer(client, history):
    """Send the full conversation to the model."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=history,
    )

    return response.choices[0].message.content or ""


def create_session_id(index):
    """Create a simple ID for a new session."""
    return f"session-{len(index) + 1}"


def chat_loop(client, session_name, history, index, is_new=False):
    """Run the terminal conversation."""
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nChat ended.")
            break

        if question.lower() == "exit":
            print("Chat ended.")
            break

        if not question:
            continue

        try:
            if is_new:
                session_name = generate_session_name(
                    client, question, index
                )

                index[session_name] = create_session_id(index)
                save_index(index)

                is_new = False
                print(f"Session name: {session_name}")

            history.append(
                {"role": "user", "content": question}
            )

            answer = get_answer(client, history)

            print(f"Assistant: {answer}")

            history.append(
                {"role": "assistant", "content": answer}
            )

            save_history(session_name, history)

        except Exception:
            print(
                "Something went wrong. Please check your API key, "
                "internet connection, and session files."
            )
            break


def main():
    try:
        client = OpenAI()
        index = load_index()

        if not isinstance(index, dict):
            print("The session index must be a JSON object.")
            return

        session_name = ask_for_session(index)

        if session_name:
            history = load_history(session_name)
            chat_loop(client, session_name, history, index)
        else:
            os.makedirs(SESSIONS_DIR, exist_ok=True)
            chat_loop(
                client, "", [], index, is_new=True
            )

    except KeyboardInterrupt:
        print("\nProgram ended.")
    except Exception:
        print("Could not start the chat. Check your files and API key.")


if __name__ == "__main__":
    main()
