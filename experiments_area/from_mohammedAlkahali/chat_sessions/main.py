import json
import os
from dotenv import load_dotenv 
from openai import OpenAI

load_dotenv()

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


def main():
    client = OpenAI()
    index = load_index("sessions_index.json")

    typed_name = input("Session name (press Enter for new): ")

    if typed_name in index:
        session_name = typed_name
        message = load_session(f"sessions/{session_name}.json")
    else:
        if typed_name != "":
            print(f"No session called {typed_name}. Starting a new session.")
        session_name = "new_session"
        message = []

        new_id = f"session-{len(index) + 1}"
        index[session_name] = new_id
        save_index("sessions_index.json", index)

    while True:
        user_input = input("You: ")

        if user_input in ["exit", "EXIT"]:
            break

        message.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=message,
        )
        reply = response.choices[0].message.content

        print("bot:", reply)
        message.append({"role": "assistant", "content": reply})
        save_session(f"sessions/{session_name}.json", message)
        

if __name__ == "__main__":
    main()