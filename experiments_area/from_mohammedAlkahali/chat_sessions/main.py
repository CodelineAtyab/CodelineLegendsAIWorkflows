import json
import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

INDEX_FILE = "sessions_index.json"



def save_session(file_name, messages):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4)



def load_session(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []



def load_index(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}



def save_index(file_name, index):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=4)



def generate_session_name(client, first_question):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Reply with exactly two words, lowercase, separated by a space, nothing else. Summarize the topic of the user's message in those two words.",
            },
            {"role": "user", "content": first_question},
        ],
    )
    raw = response.choices[0].message.content.strip().lower()
    words = [w.strip(".,!?;:\"'") for w in raw.split()]
    words = [w for w in words if w]

    if len(words) >= 2:
        return f"{words[0]}_{words[1]}"
    elif len(words) == 1:
        return words[0]
    else:
        return "new_session"



def main():
    client = OpenAI()
    index = load_index(INDEX_FILE)

    typed_name = input("Session name (press Enter for new): ")

    if typed_name in index:
        session_name = typed_name
        message = load_session(f"sessions/{session_name}.json")
        is_new = False
    else:
        if typed_name != "":
            print(f"No session called {typed_name}. Starting a new session.")
        session_name = None
        message = []
        is_new = True

    while True:
        user_input = input("You: ")

        if user_input in ["exit", "EXIT"]:
            break

        if is_new and len(message) == 0:
            try:
                session_name = generate_session_name(client, user_input)
            except OpenAIError as error:
                print(f"Could not generate a session name, using 'new_session' instead: {error}")
                session_name = "new_session"

            new_id = f"session-{len(index) + 1}"
            index[session_name] = new_id
            try:
                save_index(INDEX_FILE, index)
            except OSError as error:
                print(f"Could not save the session index: {error}")
            is_new = False

        message.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=message,
            )
            reply = response.choices[0].message.content
        except OpenAIError as error:
            print(f"Sorry, something went wrong talking to the model: {error}")
            message.pop()
            continue

        print("bot:", reply)
        message.append({"role": "assistant", "content": reply})

        try:
            save_session(f"sessions/{session_name}.json", message)
        except OSError as error:
            print(f"Could not save this session to disk: {error}")



if __name__ == "__main__":
    main()