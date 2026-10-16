import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

INDEX_FILE = "session_index.json"
SESSIONS_DIR = "sessions"
MODEL_NAME = "gpt-4.1-mini"


def load_session_index():
    if not os.path.exists(INDEX_FILE):
        return {}
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("Warning: Could not read index file, starting with empty session list.")
        return {}


def load_history(session_name):
    file_path = os.path.join(SESSIONS_DIR, f"{session_name}.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Could not load session '{session_name}': {e}")
        return None


def save_session(index, session_name, history):
    try:
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        file_path = os.path.join(SESSIONS_DIR, f"{session_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Could not save session data: {e}")


def ask_model(client, messages):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI API call failed: {e}")


def generate_two_word_name(client, first_question, existing_index):
    prompt = [
        {
            "role": "system",
            "content": "Generate a concise 2-word title for the following query. Return only two words separated by a space, nothing else."
        },
        {"role": "user", "content": first_question}
    ]
    try:
        reply = ask_model(client, prompt)
        words = re.findall(r"[a-zA-Z0-9]+", reply.lower())
        if len(words) >= 2:
            base_name = f"{words[0]}_{words[1]}"
        elif len(words) == 1:
            base_name = f"{words[0]}_chat"
        else:
            base_name = "new_session"
    except Exception:
        base_name = "new_session"

    name = base_name
    counter = 2
    while name in existing_index:
        name = f"{base_name}_{counter}"
        counter += 1
    return name


def select_session(index):
    try:
        name_input = input("Enter session name (press Enter for a new session): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        return None, None, True

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


def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment or .env file.")
        return

    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        print(f"Failed to initialize OpenAI client: {e}")
        return

    index = load_session_index()
    session_name, history, should_exit = select_session(index)
    if should_exit:
        return

    is_new = session_name is None
    if not is_new:
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

        if user_input.lower() == "exit":
            print("Session ended.")
            break

        if is_new:
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


if __name__ == "__main__":
    main()
